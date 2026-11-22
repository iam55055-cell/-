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
  // svg/n0/ 폴더의 변형 심볼도 800px로 내보낸다
  const n0 = path.join(root, 'svg', 'n0');
  if (fs.existsSync(n0)) {
    fs.mkdirSync(path.join(root, 'png', 'n0'), { recursive: true });
    for (const f of fs.readdirSync(n0).filter((x) => x.endsWith('.svg')).sort()) {
      // 워드마크는 배경을 투명하게, 심볼은 바탕색 그대로
      const isWordmark = f.startsWith('wordmark');
      jobs.push([path.join('n0', f), path.join('n0', f.replace('.svg', isWordmark ? '-1600.png' : '-800.png')), isWordmark ? 1600 : 800, isWordmark]);
    }
  }
  // svg/nppang/ 바로 아래의 'N빵' 대표안은 폭 2400px, 투명 배경으로 내보낸다 (candidates/ 는 내보내지 않는다)
  const np = path.join(root, 'svg', 'nppang');
  if (fs.existsSync(np)) {
    fs.mkdirSync(path.join(root, 'png', 'nppang'), { recursive: true });
    for (const f of fs.readdirSync(np).filter((x) => x.endsWith('.svg')).sort()) {
      jobs.push([path.join('nppang', f), path.join('nppang', f.replace('.svg', '-2400.png')), 2400, true]);
    }
  }
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
