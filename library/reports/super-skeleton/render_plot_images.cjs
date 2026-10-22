// 将本地 SVG 图表输出为 PNG，并用浏览器字体度量检查裁切。
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');
const dir = path.join(__dirname, 'reading', 'plot', 'images');
const manifest = JSON.parse(fs.readFileSync(path.join(dir, 'manifest.json'), 'utf8'));
(async () => {
  const browser = await chromium.launch({ headless: true, ...(process.env.PLOT_BROWSER_CHANNEL ? { channel: process.env.PLOT_BROWSER_CHANNEL } : {}) });
  try {
    const page = await browser.newPage({ deviceScaleFactor: 1 });
    let textCount = 0;
    for (const im of manifest.images) {
      if (process.argv[2] && !im.file.includes(process.argv[2])) continue;
      await page.setViewportSize({ width: im.width, height: Math.min(im.height, 1200) });
      await page.goto(pathToFileURL(path.join(dir, im.file + '.svg')).href);
      await page.evaluate(() => document.fonts.ready);
      const check = await page.evaluate(() => {
        const root = document.documentElement;
        const width = Number(root.getAttribute('width'));
        const height = Number(root.getAttribute('height'));
        const texts = [...document.querySelectorAll('text')];
        const bad = texts.flatMap(el => {
          const b = el.getBBox();
          const right = Math.min(width - 20, Number(el.dataset.right));
          return b.x < Number(el.dataset.left)-2 || b.x+b.width > right+2 || b.y+b.height > Math.min(height-20, Number(el.dataset.bottom))+2
            ? [{ text: el.textContent, x:b.x, y:b.y, w:b.width, h:b.height, right }] : [];
        });
        return { count: texts.length, bad };
      });
      if (check.bad.length) throw new Error(im.file + ': text overflow ' + JSON.stringify(check.bad));
      await page.locator('svg').screenshot({ path: path.join(dir, im.file + '.png'), animations: 'disabled', timeout: 30000 });
      textCount += check.count;
      console.log(JSON.stringify({file:im.file, width:im.width, height:im.height, texts:check.count}));
    }
    console.log(JSON.stringify({textCount, overflow:0}));
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
