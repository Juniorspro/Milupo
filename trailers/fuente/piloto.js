// Piloto automático (se inyecta en la página). Esquiva rocas con el campo de distancias del juego.
module.exports = `
window.__piloto = { activo: false, rumbo: null, altura: 40, objetivo: null, picada: false };
window.__juego = () => window.__drDebug.debug.game();
window.__pilotar = function () {
  const P = window.__piloto; if (!P.activo) return;
  const g = __juego(), S = g.S, W = g.world;
  if (S.hp < 60) S.hp = 100;                      // que no se canse durante el rodaje
  if (S.energy < 60) S.energy = 100;
  let deseado = P.rumbo == null ? S.head : P.rumbo;
  if (P.objetivo) { const o = P.objetivo; deseado = Math.atan2(-(o.x - S.p.x), -(o.z - S.p.z)); }
  let mejor = deseado, mejorPuntaje = -1e9;
  for (const d of [0, .12, -.12, .25, -.25, .4, -.4, .6, -.6, .85, -.85, 1.1, -1.1]) {
    const y = deseado + d; let libre = 1e9;
    for (const dist of [12, 24, 36, 50, 65]) {
      const q = { x: S.p.x - Math.sin(y) * dist, y: S.p.y, z: S.p.z - Math.cos(y) * dist };
      libre = Math.min(libre, W.sdf(q) - dist * 0.08);
    }
    const puntaje = Math.min(libre, 18) - Math.abs(d) * 6;
    if (puntaje > mejorPuntaje) { mejorPuntaje = puntaje; mejor = y; }
  }
  let dif = mejor - g.A.yaw; dif = Math.atan2(Math.sin(dif), Math.cos(dif));
  g.A.yaw += dif * 0.25;
  const altura = P.picada && P.objetivo ? P.objetivo.y : P.altura;
  const dy = altura - S.p.y;
  g.A.pitch = Math.max(P.picada ? -1.0 : -0.45, Math.min(0.45, dy * (P.picada ? 0.05 : 0.025)));
};
`;
