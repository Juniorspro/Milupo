const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + __dirname + '/eolica.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  // detectar desbordes dentro de cada página
  const over = await p.evaluate(() => [...document.querySelectorAll('.page')].map((pg,i) => {
    const foot = pg.querySelector('.foot'); const fb = foot ? foot.getBoundingClientRect().top : pg.getBoundingClientRect().bottom;
    let max = 0; pg.querySelectorAll('p,figure,table,.stats,.chart,.diagram,.callout,.tl,.gallery,.sources,.cols,.cols-3-2,.quote,.toc').forEach(e => { if (!e.closest('.cover')) max = Math.max(max, e.getBoundingClientRect().bottom); });
    return `p${i+1}: contenido termina ${(max - pg.getBoundingClientRect().top).toFixed(0)}px, pie en ${(fb - pg.getBoundingClientRect().top).toFixed(0)}px`;
  }));
  console.log(over.join('\n'));
  await p.pdf({ path: 'La_energia_eolica.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
