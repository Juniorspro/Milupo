// Arnés de rodaje: abre la copia local del juego con reloj virtual.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const RAIZ = path.join(__dirname, 'juego_rodaje');
const TIPOS = { '.html': 'text/html', '.js': 'application/javascript', '.png': 'image/png', '.mp3': 'audio/mpeg', '.ttf': 'font/ttf', '.json': 'application/json', '.bin': 'application/octet-stream', '.glb': 'model/gltf-binary', '.jpg': 'image/jpeg', '.webp': 'image/webp' };
async function abrir({ idioma = 'en-US', ancho = 540, alto = 960, dpr = 2, consulta = 'test=1' } = {}) {
  const navegador = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', `--lang=${idioma}`] });
  const contexto = await navegador.newContext({ viewport: { width: ancho, height: alto }, deviceScaleFactor: dpr, locale: idioma, hasTouch: true, isMobile: true });
  const pagina = await contexto.newPage();
  const faltantes = new Set();
  await pagina.route('**/*', async ruta => {
    const u = new URL(ruta.request().url());
    if (u.hostname !== 'juego.local') return ruta.abort();            // sin analíticas ni internet
    const archivo = path.join(RAIZ, decodeURIComponent(u.pathname));
    if (!archivo.startsWith(RAIZ) || !fs.existsSync(archivo)) { faltantes.add(u.pathname); return ruta.fulfill({ status: 404, body: '' }); }
    ruta.fulfill({ status: 200, body: fs.readFileSync(archivo), headers: { 'content-type': TIPOS[path.extname(archivo)] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
  });
  await pagina.clock.install({ time: new Date('2026-11-21T18:00:00') });
  await pagina.goto('http://juego.local/index.html?' + consulta);
  return { navegador, pagina, faltantes };
}
module.exports = { abrir };
