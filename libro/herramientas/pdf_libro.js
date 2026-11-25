const { chromium } = require('playwright');
const [,, entrada, salida] = process.argv;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + require('path').resolve(entrada), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: salida, preferCSSPageSize: true, printBackground: true });
  await b.close();
})();
