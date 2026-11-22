// Cámara de cine: se coloca alrededor del dragón según la "toma" actual.
// Las posiciones se dan en el sistema del dragón: f = adelante, u = arriba, r = derecha.
module.exports = `
window.__toma = null; window.__k = 0;
window.__camHook = function (U) {
  const t = window.__toma;
  if (!t) return null;
  const g = window.__drDebug.debug.game(), S = g.S, T = window.__dr.THREE;
  const p = new T.Vector3(S.p.x, S.p.y, S.p.z);
  const f = new T.Vector3(S.v.x, 0, S.v.z); if (f.lengthSq() < 1e-6) f.set(0, 0, -1); f.normalize();
  const up = new T.Vector3(0, 1, 0), r = new T.Vector3().crossVectors(f, up).normalize();
  const k = window.__k, e = k * k * (3 - 2 * k);
  const mix = (a, b) => ({ f: a.f + (b.f - a.f) * e, u: a.u + (b.u - a.u) * e, r: a.r + (b.r - a.r) * e });
  let pos = t.desde ? mix(t.desde, t.hasta || t.desde) : null; const mira = mix(t.mira, t.mira2 || t.mira);
  if (t.orbita) { const o = t.orbita, a = o.a0 + (o.a1 - o.a0) * e, R = o.r0 + ((o.r1 == null ? o.r0 : o.r1) - o.r0) * e;
    pos = { f: Math.cos(a) * R, u: o.u0 + ((o.u1 == null ? o.u0 : o.u1) - o.u0) * e, r: Math.sin(a) * R }; }
  const guardado = { p: U.position.clone(), q: U.quaternion.clone(), fov: U.fov };
  U.position.copy(p).addScaledVector(f, pos.f).addScaledVector(up, pos.u).addScaledVector(r, pos.r);
  if (t.fijo) { if (!t._fija) t._fija = U.position.clone(); U.position.copy(t._fija); }   // cámara quieta: el dragón se aleja
  else {
    // Que la roca no tape al dragón: recorremos la línea dragón → cámara y acercamos la cámara si hay piedra.
    const dir = U.position.clone().sub(p), largo = dir.length(); dir.normalize();
    let libre = largo;
    for (let s = 2.5; s <= largo; s += 1.0) { const q = p.clone().addScaledVector(dir, s); if (g.world.sdf(q) < 3.0) { libre = Math.max(5, s - 2.5); break; } }
    if (t._libre == null || libre < t._libre) t._libre = libre; else t._libre += (libre - t._libre) * 0.08;
    U.position.copy(p).addScaledVector(dir, Math.min(largo, t._libre));
  }
  if (U.position.y < 3) U.position.y = 3;    // nunca bajo el agua
  if (t.temblor) { U.position.x += Math.sin(k * 97) * t.temblor; U.position.y += Math.sin(k * 131) * t.temblor; }
  U.lookAt(p.clone().addScaledVector(f, mira.f).addScaledVector(up, mira.u).addScaledVector(r, mira.r));
  if (t.giro) U.rotateZ(t.giro * (1 - 2 * e) * 0.5);
  U.fov = t.fov || 55; U.updateProjectionMatrix(); U.updateMatrixWorld();
  return function () { U.position.copy(guardado.p); U.quaternion.copy(guardado.q); U.fov = guardado.fov; U.updateProjectionMatrix(); U.updateMatrixWorld(); };
};
window.__hud = function (si) { try { window.__dr.ui.uniforms.uUi.value = si ? 1 : 0; } catch (e) {} };
`;
