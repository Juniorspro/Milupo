const { chromium } = require('playwright');
const [,, entrada, salida] = process.argv;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + require('path').resolve(entrada), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: salida, width: '6in', height: '9in', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;text-align:center;font-family:Georgia,serif;font-size:8.5pt;color:#555;padding-bottom:0.25in"><span class="pageNumber"></span></div>' });
  await b.close();
})();
