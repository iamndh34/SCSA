"""
StyleID (Chung et al., CVPR 2024) và StyleID + SCSA (Shen et al., CVPR 2025) trên Stable Diffusion v1.4.

Viết lại trên diffusers, bám theo code gốc của tác giả (bản ldm):
  - StyleID:        github.com/jiwoogit/StyleID  (run_styleid.py, ldm/modules/attention.py; MIT)
                    và bản diffusers chính thức của họ (diffusers_implementation/, MIT)
  - StyleID + SCSA: github.com/scn-00/SCSA  (StyleID+SCSA/StyleID+SCSA/SCSA.py, function.py,
                    ldm/modules/attention.py)
Trọng số U-Net của CompVis/stable-diffusion-v1-4 (diffusers) là bản EMA của sd-v1-4.ckpt mà hai repo dùng.
Lớp decoder ldm output_blocks[i] ↔ diffusers up_blocks[i // 3].attentions[i % 3].

Chạy trên MPS / CUDA / CPU. Mặc định giống code gốc: 50 bước DDIM, lớp 6–11, không tiêm ở bước đầu
(start_step = 49).

StyleID (mỗi lớp được tiêm):
    Q = γ·Q_ảnh + (1−γ)·Q_hiện tại,  K, V = của tranh,  softmax(T · QKᵀ/√d) V      γ = 0.75, T = 1.5
    latent đầu = AdaIN(z_T ảnh, z_T tranh)

StyleID + SCSA (thay self-attention trên bằng hai nhánh; tham số theo SCSA.py):
    x̂_c = local AdaIN(x_c, x_s) theo từng vùng nhãn       (x: đầu vào khối transformer, lưu khi inversion)
    SCA: Q = a1·Q_map ảnh + (1−a1)·to_q(norm(x̂_c)),  K = a1·K_map tranh + (1−a1)·to_k(norm(x_s)),  V = V_tranh
         softmax(T · QKᵀ/√d + mặt nạ cùng nhãn) V
    SSA: Q = a2·to_q(norm(x̂_c)) + (1−a2)·to_q(mvn(x)),  K, V = của tranh
         chỉ giữ điểm giống nhất (top-1) trong vùng cùng nhãn
    ra = t1·SCA + t2·SSA       t1 = 0.8, t2 = 0.2, a1 = 0.3, a2 = 0.5, T = 1.2
    latent đầu = local AdaIN(z_T ảnh, z_T tranh) theo vùng
    (Q_map, K_map: lấy từ DDIM inversion chính hai bản đồ nhãn, như get_pre_features.py)
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

import numpy as np
import torch
from PIL import Image

from gatys_nst import BenchmarkResult, get_optimal_device, sync_device, get_memory_mb

MODEL_KEY = "CompVis/stable-diffusion-v1-4"
_LOCAL = Path(__file__).resolve().parent / "weights" / "sd-v1-4"
if (_LOCAL / "unet" / "diffusion_pytorch_model.fp16.safetensors").exists():
    MODEL_KEY = str(_LOCAL)  # bản fp16 tải sẵn; nếu không có, diffusers tự tải từ Hugging Face

_SD = None


def _load_sd(device, dtype):
    global _SD
    if _SD is not None and _SD[0] == (str(device), dtype):
        return _SD[1]
    from diffusers import AutoencoderKL, UNet2DConditionModel, DDIMScheduler
    from transformers import CLIPTextModel, CLIPTokenizer
    unet = UNet2DConditionModel.from_pretrained(MODEL_KEY, subfolder="unet", torch_dtype=dtype, variant="fp16").to(device)
    text_encoder = CLIPTextModel.from_pretrained(MODEL_KEY, subfolder="text_encoder", torch_dtype=dtype, variant="fp16").to(device)
    vae = AutoencoderKL.from_pretrained(MODEL_KEY, subfolder="vae", torch_dtype=torch.float32, variant="fp16").to(device)
    tokenizer = CLIPTokenizer.from_pretrained(MODEL_KEY, subfolder="tokenizer")
    scheduler = DDIMScheduler.from_pretrained(MODEL_KEY, subfolder="scheduler")
    _SD = ((str(device), dtype), (unet, text_encoder, vae, tokenizer, scheduler))
    return _SD[1]


def _load(path, size, device):
    im = Image.open(path).convert("RGB").resize((size, size), Image.BICUBIC)
    x = torch.from_numpy(np.asarray(im).astype(np.float32) / 127.5 - 1).permute(2, 0, 1)[None]
    return x.to(device)


# ── nhãn vùng (theo sem.py của SCSA: màu → nhãn, resize nearest) ──────────────
def _label_maps(c_sem, s_sem, sizes=(32, 64)):
    """Trả về {size: (nhãn ảnh (size, size), nhãn tranh (size, size))}, cùng bảng nhãn cho hai bên."""
    ca = np.asarray(Image.open(c_sem).convert("RGB").resize((512, 512), Image.NEAREST)).reshape(-1, 3)
    sa = np.asarray(Image.open(s_sem).convert("RGB").resize((512, 512), Image.NEAREST)).reshape(-1, 3)
    pal = np.unique(np.concatenate([ca, sa]), axis=0)
    out = {}
    for n in sizes:
        def lab(path):
            a = np.asarray(Image.open(path).convert("RGB").resize((512, 512), Image.NEAREST).resize((n, n), Image.NEAREST)).reshape(-1, 3)
            return np.argmin(((a[:, None, :].astype(int) - pal[None].astype(int)) ** 2).sum(-1), 1).reshape(n, n)
        out[n] = (lab(c_sem), lab(s_sem))
    return out, len(pal)


def _local_adain(c, s, lc, ls, n_lab):
    """function.py/local_adain: AdaIN riêng từng vùng; c, s: (b, ch, h, w); lc, ls: nhãn (h, w)."""
    out = torch.zeros_like(c)
    for i in range(n_lab):
        mc = torch.as_tensor(lc == i, device=c.device, dtype=c.dtype)
        ms = torch.as_tensor(ls == i, device=c.device, dtype=c.dtype)
        if mc.sum() == 0 or ms.sum() == 0:
            continue

        def mean_std(x, m):
            x = x * m
            k = m.sum()
            mu = (x.sum((-1, -2)) / k)[..., None, None]
            sd = ((((x - mu) ** 2) * m).sum((-1, -2)) / k + 1e-5).sqrt()[..., None, None]
            return mu, sd
        s_mu, s_sd = mean_std(s, ms)
        c_mu, c_sd = mean_std(c, mc)
        out = out + ((c * mc - c_mu) / c_sd * s_sd + s_mu) * mc
    return out


def _tokens_adain(xc, xs, lc, ls, n_lab):
    """get_local_adain_q: x (b, n, ch) → (b, ch, h, w) → local AdaIN → (b, n, ch)."""
    b, n, ch = xc.shape
    w = int(n ** 0.5)
    c = xc.transpose(1, 2).reshape(b, ch, w, w)
    s = xs.transpose(1, 2).reshape(b, ch, w, w)
    return _local_adain(c, s, lc, ls, n_lab).reshape(b, ch, n).transpose(1, 2)


def _mvn(x, eps=1e-5):  # ldm.util.mean_variance_norm: chuẩn hoá từng kênh trên các điểm
    return (x - x.mean(1, keepdim=True)) / (x.var(1, keepdim=True) + eps).sqrt()


class _Injector:
    """Gắn vào khối transformer đầu của các lớp decoder: lưu đặc trưng khi inversion, thay self-attention khi sinh."""

    def __init__(self, unet, layers):
        self.cur_t, self.capture, self.inject = None, False, False
        self.saved, self.feats, self.blocks = {}, {}, {}
        self.mode, self.cfg = None, {}
        for i in layers:
            blk = unet.up_blocks[i // 3].attentions[i % 3].transformer_blocks[0]
            self.blocks[i] = blk
            self.saved[i] = {}
            blk.register_forward_pre_hook(self._pre(i), with_kwargs=True)
            blk.attn1.register_forward_hook(self._post(i))
        self._x = {}

    def _pre(self, i):
        def hook(module, args, kwargs):
            x = args[0] if args else kwargs["hidden_states"]
            self._x[i] = x
        return hook

    def _post(self, i):
        def hook(attn, inputs, output):
            hn = inputs[0]  # norm1(x)
            if self.capture:
                H = attn.head_to_batch_dim
                self.saved[i][self.cur_t] = dict(q=H(attn.to_q(hn)), k=H(attn.to_k(hn)), v=H(attn.to_v(hn)), x=self._x[i])
            if self.inject and self.cur_t in self.feats.get(i, {}):
                f = self.feats[i][self.cur_t]
                if self.mode == "styleid":
                    return self._styleid(attn, hn, f)
                return self._scsa(attn, i, f)
        return hook

    @staticmethod
    def _attend(attn, q, k, v, T, mask=None, top1=False):
        sim = torch.bmm(q.float(), k.float().transpose(1, 2)) * attn.scale * T
        if mask is not None:
            sim = sim.masked_fill(mask[None] < 0.5, -torch.finfo(sim.dtype).max)
        if top1:
            idx = sim.argmax(-1, keepdim=True)
            sim = torch.full_like(sim, -torch.finfo(sim.dtype).max).scatter(-1, idx, sim.gather(-1, idx))
        out = torch.bmm(sim.softmax(-1).to(v.dtype), v)
        out = attn.batch_to_head_dim(out)
        return attn.to_out[1](attn.to_out[0](out))

    def _styleid(self, attn, hn, f):
        g, T = self.cfg["gamma"], self.cfg["T"]
        q = f["q_c"] * g + attn.head_to_batch_dim(attn.to_q(hn)) * (1 - g)
        return self._attend(attn, q, f["k_s"], f["v_s"], T)

    def _scsa(self, attn, i, f):
        c = self.cfg
        H, norm = attn.head_to_batch_dim, self.blocks[i].norm1
        n = f["x_c"].shape[1]
        side = int(n ** 0.5)
        lc, ls = c["labels"][side]
        mask = c["maps"][side]
        xc_hat = _tokens_adain(f["x_c"], f["x_s"], lc, ls, c["n_lab"])
        q_hat = H(attn.to_q(norm(xc_hat)))
        # SCA: hỏi bằng bản đồ nhãn, nhìn cả vùng cùng nhãn
        q1 = c["a1"] * f["q_csem"] + (1 - c["a1"]) * q_hat
        k1 = c["a1"] * f["k_ssem"] + (1 - c["a1"]) * H(attn.to_k(norm(f["x_s"])))
        sca = self._attend(attn, q1, k1, f["v_s"], c["T"], mask)
        # SSA: chỉ lấy một điểm giống nhất trong vùng cùng nhãn
        q2 = c["a2"] * q_hat + (1 - c["a2"]) * H(attn.to_q(_mvn(self._x[i])))
        ssa = self._attend(attn, q2, f["k_s"], f["v_s"], c["T"], mask, top1=True)
        return c["t1"] * sca + c["t2"] * ssa


def _run(content_path, style_path, mode, img_size, ddim_steps, layers, start_step, device, cfg,
         content_sem=None, style_sem=None):
    device = device or get_optimal_device()
    dtype = torch.float16 if device.type in ("mps", "cuda") else torch.float32
    unet, text_encoder, vae, tokenizer, scheduler = _load_sd(device, dtype)
    scheduler.set_timesteps(ddim_steps)
    for blk in unet.up_blocks:  # gỡ hook của lần chạy trước (nếu có)
        for a in getattr(blk, "attentions", []):
            a.transformer_blocks[0]._forward_pre_hooks.clear()
            a.transformer_blocks[0].attn1._forward_hooks.clear()
    inj = _Injector(unet, layers)
    inj.mode, inj.cfg = mode, dict(cfg)
    steps = [int(t) for t in scheduler.timesteps]
    inject_ts = set(steps[ddim_steps - start_step:])  # code gốc: bỏ qua bước i < 50 − start_step

    with torch.no_grad():
        ids = tokenizer([""], padding="max_length", max_length=tokenizer.model_max_length, return_tensors="pt").input_ids
        cond = text_encoder(ids.to(device))[0].to(dtype)

        def eps(z, t):
            inj.cur_t = int(t)
            return unet(z, t.to(device), encoder_hidden_states=cond).sample

        def invert(path, keep):
            z = (0.18215 * vae.encode(_load(path, img_size, device)).latent_dist.mode()).to(dtype)
            inj.capture = True
            for t in reversed(scheduler.timesteps):
                e = eps(z, t)
                a_t = scheduler.alphas_cumprod[max(0, int(t) - 1000 // ddim_steps)].to(device)
                a_n = scheduler.alphas_cumprod[int(t)].to(device)
                z = (z - (1 - a_t).sqrt() * e) * (a_n.sqrt() / a_t.sqrt()) + (1 - a_n).sqrt() * e
                for i in layers:  # chỉ giữ thứ cần dùng, ở các bước có tiêm
                    d = inj.saved[i].pop(int(t))
                    if int(t) in inject_ts:
                        inj.feats.setdefault(i, {}).setdefault(int(t), {}).update({nk: d[k] for k, nk in keep.items()})
            inj.capture = False
            return z

        sync_device(device)
        ram0 = get_memory_mb(device)
        t0 = time.perf_counter()

        if mode == "styleid":
            z_s = invert(style_path, {"k": "k_s", "v": "v_s"})
            z_c = invert(content_path, {"q": "q_c"})
            z = (z_c - z_c.mean((2, 3), keepdim=True)) / (z_c.std((2, 3), keepdim=True) + 1e-4) \
                * z_s.std((2, 3), keepdim=True) + z_s.mean((2, 3), keepdim=True)
        else:
            labels, n_lab = _label_maps(content_sem, style_sem, sizes=(32, 64))
            inj.cfg["labels"], inj.cfg["n_lab"] = labels, n_lab
            inj.cfg["maps"] = {n: torch.as_tensor(labels[n][0].reshape(-1)[:, None] == labels[n][1].reshape(-1)[None, :],
                                                  device=device, dtype=torch.float32) for n in (32, 64)}
            z_s = invert(style_path, {"k": "k_s", "v": "v_s", "x": "x_s"})
            z_c = invert(content_path, {"x": "x_c"})
            invert(content_sem, {"q": "q_csem"})
            invert(style_sem, {"k": "k_ssem"})
            lc, ls = labels[64]
            z = _local_adain(z_c.float(), z_s.float(), lc, ls, n_lab).to(dtype)

        inj.inject = True
        for t in scheduler.timesteps:
            z = scheduler.step(eps(z, t), t, z).prev_sample
        inj.inject = False
        img = vae.decode(z.float() / 0.18215).sample
        sync_device(device)
        elapsed = time.perf_counter() - t0
        peak = get_memory_mb(device) - ram0
        inj.feats.clear()

    out = ((img[0].clamp(-1, 1) + 1) * 127.5).round().byte().permute(1, 2, 0).cpu().numpy()
    name = "StyleID" if mode == "styleid" else "StyleID + SCSA"
    n_inv = 2 if mode == "styleid" else 4
    print(f"[{name} | {device.type.upper()}]  SD v1.4, {ddim_steps} bước DDIM + {n_inv} × {ddim_steps} bước inversion"
          f"  | {elapsed:.1f} s | Peak RAM: {peak:.0f} MB")
    return BenchmarkResult(
        method_name=f"{name} (SD v1.4)",
        output_image=Image.fromarray(out),
        inference_time_sec=elapsed,
        time_per_step_ms=elapsed * 1e3 / ((n_inv + 1) * ddim_steps),
        peak_memory_mb=peak,
        total_steps=(n_inv + 1) * ddim_steps,
        loss_history=[],
        device_name=f"({device.type.upper()})",
    )


def run_styleid(content_path, style_path, img_size=512, ddim_steps=50, gamma=0.75, T=1.5,
                layers=(6, 7, 8, 9, 10, 11), start_step=49, device: Optional[torch.device] = None) -> BenchmarkResult:
    return _run(content_path, style_path, "styleid", img_size, ddim_steps, layers, start_step, device,
                dict(gamma=gamma, T=T))


def run_styleid_scsa(content_path, style_path, content_sem, style_sem, img_size=512, ddim_steps=50,
                     T=1.2, t1=0.8, t2=0.2, a1=0.3, a2=0.5,
                     layers=(6, 7, 8, 9, 10, 11), start_step=49, device: Optional[torch.device] = None) -> BenchmarkResult:
    return _run(content_path, style_path, "scsa", img_size, ddim_steps, layers, start_step, device,
                dict(T=T, t1=t1, t2=t2, a1=a1, a2=a2), content_sem, style_sem)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--cnt", default="img/yosemite.jpg")
    ap.add_argument("--sty", default="img/yosemite_paint.jpg")
    ap.add_argument("--cnt_sem", default="img/yosemite_sem.png")
    ap.add_argument("--sty_sem", default="img/yosemite_paint_sem.png")
    ap.add_argument("--mode", choices=["styleid", "scsa", "both"], default="both")
    ap.add_argument("--steps", type=int, default=50)
    a = ap.parse_args()
    if a.mode in ("styleid", "both"):
        r = run_styleid(a.cnt, a.sty, ddim_steps=a.steps)
        r.output_image.save("img/yosemite_out_styleid.jpg", quality=95)
    if a.mode in ("scsa", "both"):
        r = run_styleid_scsa(a.cnt, a.sty, a.cnt_sem, a.sty_sem, ddim_steps=a.steps)
        r.output_image.save("img/yosemite_out_styleid_scsa.jpg", quality=95)
