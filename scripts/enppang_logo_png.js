// 엔빵 로고 SVG를 PNG로 내보낸다. Playwright(Chromium)가 필요하다.
// 사용법: node scripts/enppang_logo_png.js library/brand/enppang
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const jobs = [
  // [svg, png, 폭, 투명 배경]
  ['symbol.svg', 'channel-icon-800.png', 800, false],
  ['symbol-alt-receipt.svg', 'channel-icon-alt-receipt-800.png', 800, false],
  ['symbol-alt-letters.svg', 'channel-icon-alt-letters-800.png', 800, false],
  ['symbol-coin-only.svg', 'symbol-coin-only-800.png', 800, true],
  ['wordmark.svg', 'wordmark-2400.png', 2400, true],
  ['wordmark-on-dark.svg', 'wordmark-on-dark-2400.png', 2400, true],
  ['wordmark-on-gold.svg', 'wordmark-on-gold-2400.png', 2400, true],
  ['lockup.svg', 'lockup-2400.png', 2400, true],
  ['lockup-on-dark.svg', 'lockup-on-dark-2400.png', 2400, true],
];

(async () => {
  const root = path.resolve(process.argv[2] || 'library/brand/enppang');
  const browser = await chromium.launch();
  for (const [svg, png, width, transparent] of jobs) {
    const src = path.join(root, 'svg', svg);
    if (!fs.existsSync(src)) { console.log('없음, 건너뜀:', svg); continue; }
    const text = fs.readFileSync(src, 'utf8');
    const m = text.match(/viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"/);
    const height = Math.round(width * (+m[4]) / (+m[3]));
    const page = await browser.newPage({ viewport: { width, height } });
    // file:// 이미지는 빈 페이지에서 막히므로 SVG를 그대로 페이지에 넣는다
    const sized = text.replace(/<svg([^>]*?) width="[^"]*" height="[^"]*"/, `<svg$1 width="${width}" height="${height}" style="display:block"`);
    await page.setContent(`<body style="margin:0;background:transparent">${sized}</body>`);
    await page.waitForTimeout(100);
    await page.screenshot({ path: path.join(root, 'png', png), omitBackground: transparent });
    await page.close();
    console.log(png, width + '×' + height);
  }
  await browser.close();
})();
