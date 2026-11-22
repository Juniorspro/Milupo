// Rodaje: graba las tomas del tráiler cuadro por cuadro con el reloj virtual.
// Uso: node rodar.js <sesion1> <sesion2> ...   (ver TOMAS más abajo)
const { abrir } = require('./arnes');
const CAM = require('./camara'), PIL = require('./piloto');
const fs = require('fs'), path = require('path');
const FPS = 30;
const PREVIA = process.env.PREVIA === '1';

const AYUDAS = `
window.__haciaBarco = function (dist, alt, tipo) {
  const g = __juego(); const lista = g.debug.foes.near(g.S.p, 6000).filter(b => b.state === 'ok' && (!tipo || b.kind === tipo)).sort((a, c) => a.p.distanceTo(g.S.p) - c.p.distanceTo(g.S.p));
  const b = lista[0]; if (!b) return null; const ang = Math.atan2(g.S.p.x - b.p.x, g.S.p.z - b.p.z);
  const x = b.p.x + Math.sin(ang) * dist, z = b.p.z + Math.cos(ang) * dist;
  g.debug.fly(x, z, alt, Math.atan2(-(b.p.x - x), -(b.p.z - z))); g.A.yaw = g.S.head; g.A.pitch = 0;
  window.__barco = b; __piloto.activo = true; __piloto.objetivo = { x: b.p.x, y: b.p.y + 3, z: b.p.z }; __piloto.altura = alt; __piloto.picada = false;
  return b.kind;
};
window.__haciaAnillo = function (dist, alt) {
  const g = __juego(); const a = g.world.nearestRing(g.S.p, 3000); if (!a) return null;
  const c = a.p || a.c || a; const dir = a.dir || null;
  return JSON.stringify(Object.keys(a));
};
window.__limpiar = function () { const g = __juego(); g.H.brief = null; g.SAVE.tut = 1; };
`;

// Cada sesión abre un navegador (idioma y resolución propios) y graba una o varias tomas.
const SESIONES = {
  // Apertura, héroe y final: Acantilados del amanecer (cielo rosado)
  amanecer: { idioma: 'en-US', dpr: 4 / 3, nivel: 3, preparar: `__piloto.activo = true; __piloto.altura = 48;`, preroll: 45, tomas: [
    { nombre: 's1_apertura', cuadros: 100, camara: { desde: { f: 30, u: 14, r: 12 }, hasta: { f: 19, u: 6, r: 7 }, mira: { f: 0, u: 0, r: 0 }, fov: 40 } },
    { nombre: 's9a_acantilados', cuadros: 32, camara: { desde: { f: -12, u: 2.5, r: 1.5 }, hasta: { f: -10, u: 2, r: 1 }, mira: { f: 6, u: 1, r: 0 }, fov: 55 } },
    { nombre: 's10_heroe', cuadros: 110, camara: { orbita: { a0: -0.9, a1: 0.9, r0: 15, r1: 13, u0: 2, u1: 3.5 }, mira: { f: 0, u: 1.2, r: 0 }, fov: 40 } },
    { nombre: 's11_fondo', cuadros: 60, camara: { desde: { f: -9, u: 3.5, r: 1.5 }, fijo: true, mira: { f: 0, u: 0.5, r: 0 }, fov: 42 } },
  ] },
  // Cañón rojo: pasada desde abajo y primer plano
  canon: { idioma: 'en-US', dpr: 4 / 3, nivel: 6, preparar: `__piloto.activo = true; __piloto.altura = 44;`, preroll: 45, tomas: [
    { nombre: 's2_bajo', cuadros: 70, alInicio: `__juego().G.btn('flap', true)`, enCuadro: `if (i === 12) __juego().G.btn('flap', false)`,
      camara: { desde: { f: 14, u: -6, r: -4 }, hasta: { f: -6, u: -5, r: -3 }, mira: { f: 0, u: 1, r: 0 }, fov: 55 } },
    { nombre: 's3_frente', cuadros: 55, camara: { desde: { f: 13, u: 2.5, r: 3.5 }, hasta: { f: 10, u: 1.8, r: 2.5 }, mira: { f: 0, u: 1.2, r: 0 }, fov: 36 } },
  ] },
  hud_en: { idioma: 'en-US', dpr: 1.6, nivel: 1, preparar: `__piloto.activo = true; __piloto.altura = __juego().S.p.y;`, preroll: 40, tomas: [
    { nombre: 's5_hud_en', cuadros: 110, hud: true },
  ] },
  hud_es: { idioma: 'es-AR', dpr: 1.6, nivel: 1, preparar: `__piloto.activo = true; __piloto.altura = __juego().S.p.y;`, preroll: 40, tomas: [
    { nombre: 's5_hud_es', cuadros: 110, hud: true },
  ] },
  fuego: { idioma: 'en-US', dpr: 4 / 3, nivel: 5, preparar: `__haciaBarco(105, 20)`, preroll: 4, tomas: [
    { nombre: 's6_fuego', cuadros: 105,
      enCuadro: `{ const g = __juego(), b = __barco; const dx = b.p.x - g.S.p.x, dz = b.p.z - g.S.p.z, d = Math.hypot(dx, dz);
        const v = Math.hypot(g.S.v.x, g.S.v.z) || 1, delante = (dx * g.S.v.x + dz * g.S.v.z) / (d * v);
        window.__d = Math.round(d) + '/' + delante.toFixed(2);
        if (b.state === 'ok' && g.S.fireCd <= 0 && d < 45 && delante > 0.85) g.G.fire();
        if (d > 30 && b.state === 'ok') { __piloto.objetivo = { x: b.p.x, y: 20, z: b.p.z }; } else __piloto.objetivo = null; }`,
      camara: { desde: { f: -19, u: 8, r: 6 }, hasta: { f: -15, u: 6, r: 5 }, mira: { f: 10, u: -3, r: 0 }, fov: 50 } },
  ] },
  fuego_lento: { idioma: 'en-US', dpr: 4 / 3, nivel: 5, preparar: `__haciaBarco(105, 20)`, preroll: 4, tomas: [
    { nombre: 's6_fuego_lento', cuadros: 108, lento: 64,
      enCuadro: `{ const g = __juego(), b = __barco; const dx = b.p.x - g.S.p.x, dz = b.p.z - g.S.p.z, d = Math.hypot(dx, dz);
        const v = Math.hypot(g.S.v.x, g.S.v.z) || 1, delante = (dx * g.S.v.x + dz * g.S.v.z) / (d * v);
        window.__d = Math.round(d) + '/' + delante.toFixed(2);
        if (b.state === 'ok' && g.S.fireCd <= 0 && d < 45 && delante > 0.85) g.G.fire();
        if (d > 30 && b.state === 'ok') { __piloto.objetivo = { x: b.p.x, y: 20, z: b.p.z }; } else __piloto.objetivo = null; }`,
      camara: { desde: { f: -19, u: 8, r: 6 }, hasta: { f: -15, u: 6, r: 5 }, mira: { f: 10, u: -3, r: 0 }, fov: 50 } },
  ] },
  picada_lento: { idioma: 'en-US', dpr: 4 / 3, nivel: 2, preparar: `__haciaBarco(135, 78); __piloto.picada = true;`, preroll: 1, tomas: [
    { nombre: 's7_picada_lento', cuadros: 84, lento: 56, enCuadro: `window.__d = ''`,
      camara: { desde: { f: -16, u: 9, r: 5 }, hasta: { f: -12, u: 5, r: 4 }, mira: { f: 14, u: -6, r: 0 }, fov: 55 } },
  ] },
  picada: { idioma: 'en-US', dpr: 4 / 3, nivel: 2, preparar: `__haciaBarco(135, 78); __piloto.picada = true;`, preroll: 4, tomas: [
    { nombre: 's7_picada', cuadros: 80, camara: { desde: { f: -16, u: 9, r: 5 }, hasta: { f: -12, u: 5, r: 4 }, mira: { f: 14, u: -6, r: 0 }, fov: 55 } },
  ] },
  taladro: { idioma: 'en-US', dpr: 4 / 3, nivel: 4, preparar: `__haciaBarco(150, 26, 'ballista')`, preroll: 8, tomas: [
    { nombre: 's8_taladro', cuadros: 95,
      enCuadro: `{ const g = __juego(), b = __barco; const d = Math.hypot(b.p.x - g.S.p.x, b.p.z - g.S.p.z); g.G.btn('drill', d < 95 && d > 25); if (d < 60) __piloto.objetivo = null; }`,
      camara: { desde: { f: 12, u: 3, r: 6 }, hasta: { f: 10, u: 2.5, r: 5 }, mira: { f: 0, u: 1, r: 0 }, fov: 44 } },
  ] },
  m_aurora: { idioma: 'en-US', dpr: 4 / 3, nivel: 12, preparar: `__piloto.activo = true; __piloto.altura = 50;`, preroll: 45, tomas: [
    { nombre: 's9b_aurora', cuadros: 32, camara: { desde: { f: 18, u: 5, r: -10 }, hasta: { f: 14, u: 4, r: -10 }, mira: { f: 0, u: 1, r: 0 }, fov: 40 } },
  ] },
  m_hielo: { idioma: 'en-US', dpr: 4 / 3, nivel: 13, preparar: `__piloto.activo = true; __piloto.altura = 30;`, preroll: 45, tomas: [
    { nombre: 's9c_hielo', cuadros: 32, camara: { desde: { f: 9, u: -2, r: 6 }, hasta: { f: 7, u: -1.5, r: 5 }, mira: { f: 0, u: 1, r: 0 }, fov: 48 } },
  ] },
  m_final: { idioma: 'en-US', dpr: 4 / 3, nivel: 20, preparar: `__haciaBarco(170, 30)`, preroll: 20, tomas: [
    { nombre: 's9d_final', cuadros: 32, enCuadro: `if (i === 8) __juego().G.fire()`, camara: { desde: { f: 14, u: 3, r: -5 }, hasta: { f: 11, u: 2.5, r: -4 }, mira: { f: 0, u: 1, r: 0 }, fov: 44 } },
  ] },
};

async function rodarSesion(nombre) {
  const s = SESIONES[nombre];
  const { navegador, pagina } = await abrir({ idioma: s.idioma, ancho: 540, alto: 960, dpr: PREVIA ? 0.5 : s.dpr });
  const paso = async (codigo, i, ms) => {
    await pagina.evaluate(([c, i]) => { window.__pilotar && __pilotar(); if (c) (new Function('i', c))(i); }, [codigo || '', i]);
    if (ms) await pagina.evaluate(ms => window.__drDebug.debug.step(1, ms), ms);   // el juego avanza solo "ms" milisegundos
    else await pagina.clock.runFor(1000 / FPS);
  };
  await pagina.clock.runFor(1500);
  await pagina.evaluate(CAM); await pagina.evaluate(PIL); await pagina.evaluate(AYUDAS);
  await pagina.evaluate(n => { const g = __juego(); g.SAVE.tut = 1; g.SAVE.lvMax = 20; try { g.G.tutSkip(); } catch (e) {} g.debug.level(n); }, s.nivel);
  for (let i = 0; i < 30; i++) await paso('', i);                  // que cargue el nivel
  await pagina.evaluate(c => { __limpiar(); return (new Function(c))(); }, s.preparar);
  for (let i = 0; i < s.preroll; i++) await paso('', i);
  for (const toma of s.tomas) {
    const dir = path.join(__dirname, PREVIA ? 'previa' : 'cuadros', toma.nombre);
    const eventos = [];
    fs.mkdirSync(dir, { recursive: true });
    await pagina.evaluate(([t, hud]) => { window.__toma = t; window.__k = 0; __hud(hud); __limpiar(); }, [toma.camara || null, !!toma.hud]);
    if (toma.alInicio) await pagina.evaluate(c => (new Function(c))(), toma.alInicio);
    const t0 = Date.now();
    for (let i = 0; i < toma.cuadros; i++) {
      await pagina.evaluate(k => { window.__k = k; }, toma.cuadros > 1 ? i / (toma.cuadros - 1) : 0);
      if (toma.lento) {   // cámara lenta real: el juego avanza de a poquito y leemos la imagen directo del lienzo
        await pagina.evaluate(([c, i]) => { window.__pilotar && __pilotar(); if (c) (new Function('i', c))(i); }, [toma.enCuadro || '', i]);
        const ms = i < toma.lento ? 1000 / FPS / 4 : 1000 / FPS;
        const datos = await pagina.evaluate(ms => { window.__drDebug.debug.step(1, ms); return document.querySelector('canvas').toDataURL('image/jpeg', 0.93); }, ms);
        fs.writeFileSync(path.join(dir, String(i + 1).padStart(4, '0') + '.jpg'), Buffer.from(datos.split(',')[1], 'base64'));
      } else await paso(toma.enCuadro, i);
      const ev = await pagina.evaluate(() => { const g = __juego(), b = window.__barco; return { fuego: g.S.fire > 0 ? 1 : 0, escudo: g.H.shield && g.H.shield.on ? 1 : 0, barco: b ? b.state : '', spd: g.H.spd, y: Math.round(g.S.p.y), d: window.__d || '' }; });
      eventos.push(ev);
      if (!toma.lento && (!PREVIA || i % 3 === 0)) {
        const opciones = { path: path.join(dir, String(i + 1).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: PREVIA ? 80 : 93, timeout: 120000 };
        try { await pagina.screenshot(opciones); } catch (e) { await pagina.clock.runFor(1); await pagina.screenshot(opciones); }   // reintento
      }
    }
    fs.writeFileSync(path.join(dir, 'eventos.json'), JSON.stringify(eventos));
    const info = await pagina.evaluate(() => { const g = __juego(); return { hp: Math.round(g.S.hp), barco: window.__barco ? window.__barco.state + '/' + window.__barco.how : '-' }; });
    console.log(`${toma.nombre}: ${toma.cuadros} cuadros en ${Math.round((Date.now() - t0) / 1000)} s`, JSON.stringify(info));
  }
  await navegador.close();
}

(async () => {
  for (const nombre of process.argv.slice(2)) await rodarSesion(nombre);
})();
