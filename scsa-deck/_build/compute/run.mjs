import { createRequire } from "module"; import fs from "fs";
const require = createRequire("/Users/bibeo/.npm/_npx/702923228c2ce1e6/node_modules/hyperframes/package.json");
const puppeteer = require("puppeteer-core");
const exe = "/Users/bibeo/.cache/hyperframes/chrome/chrome-headless-shell/mac_arm-152.0.7977.30/chrome-headless-shell-mac-arm64/chrome-headless-shell";
const [html, dir, outDir] = process.argv.slice(2);
const b = await puppeteer.launch({ executablePath: exe, headless: true, args: ["--allow-file-access-from-files"] });
const p = await b.newPage(); await p.goto(`file://${html}?dir=file://${dir}`);
await p.waitForFunction(() => document.title !== "", { timeout: 60000 });
const t = await p.title(); if (t !== "done") { console.log(t); process.exit(1); }
const o = await p.evaluate(() => window.__out);
for (const k of ["pngAdain","pngSadain"]) { fs.writeFileSync(`${outDir}/${k === "pngAdain" ? "29_adain.png" : "29_sadain.png"}`, Buffer.from(o[k].split(",")[1], "base64")); delete o[k]; }
fs.writeFileSync(`${outDir}/scsa-data.json`, JSON.stringify(o));
console.log(JSON.stringify({ regCount: o.regCount, regMean: o.regMean, uaWrongMean: o.uaWrongMean, uaWrongCells: o.uaWrongCells, maxRepeat: o.maxRepeat, uniqueSSA: o.uniqueSSA }));
await b.close();
