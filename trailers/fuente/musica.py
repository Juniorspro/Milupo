# Música original del tráiler (35 s, re menor, 120 BPM), hecha con síntesis.
import numpy as np, wave
SR = 48000; DUR = 35.0; N = int(SR * DUR)
rng = np.random.default_rng(7)
t_total = np.arange(N) / SR

def vacio(): return np.zeros((N, 2))
def onda_sierra(f, t, desafinar=0.0):
    x = np.zeros_like(t)
    for d in ([0] if not desafinar else [-desafinar, 0, desafinar]):
        ph = (f * (1 + d) * t) % 1.0
        x += 2 * ph - 1
    return x / (3 if desafinar else 1)
def filtro_fft(x, bajo=None, alto=None):
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR); m = np.ones_like(fr)
    if alto: m *= 1 / np.sqrt(1 + (fr / alto) ** 4)
    if bajo: m *= 1 / np.sqrt(1 + (bajo / np.maximum(fr, 1e-3)) ** 4)
    return np.fft.irfft(X * m, len(x))
def poner(destino, sonido, inicio, vol=1.0, pan=0.0):
    i = int(inicio * SR); s = sonido[: max(0, N - i)]
    if s.ndim == 1: s = np.stack([s * np.sqrt((1 - pan) / 2), s * np.sqrt((1 + pan) / 2)], 1) * np.sqrt(2)
    destino[i:i + len(s)] += s * vol
def env(n, a, r, sostener=None):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4))
    return e * np.exp(-t / r) if sostener is None else e * np.clip((sostener - t) / max(r, 1e-4) + 1, 0, 1)
def reverb(x, segundos=2.2, mezcla=0.3):
    n = int(SR * segundos); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 6.9 / segundos)
    ir = filtro_fft(ir, alto=5000); ir /= np.sqrt((ir ** 2).sum())
    salida = np.zeros_like(x)
    for c in range(2):
        L = len(x) + n; F = 1 << (L - 1).bit_length()
        y = np.fft.irfft(np.fft.rfft(x[:, c], F) * np.fft.rfft(np.roll(ir, c * 37), F), F)[:len(x)]
        salida[:, c] = x[:, c] * (1 - mezcla) + y * mezcla * 3
    return salida

NOTA = {'D1': 36.71, 'A1': 55.0, 'Bb1': 58.27, 'C2': 65.41, 'D2': 73.42, 'F2': 87.31, 'A2': 110.0, 'Bb2': 116.54, 'C3': 130.81,
        'D3': 146.83, 'E3': 164.81, 'F3': 174.61, 'G3': 196.0, 'A3': 220.0, 'Bb3': 233.08, 'C4': 261.63, 'C#4': 277.18, 'D4': 293.66,
        'E4': 329.63, 'F4': 349.23, 'G4': 392.0, 'A4': 440.0, 'Bb4': 466.16, 'C5': 523.25, 'D5': 587.33, 'A5': 880.0}
ACORDES = {'Dm': ['D2', 'D3', 'F3', 'A3', 'D4'], 'Bb': ['Bb1', 'Bb2', 'D3', 'F3', 'Bb3'], 'F': ['F2', 'C3', 'F3', 'A3', 'C4'],
           'C': ['C2', 'C3', 'E3', 'G3', 'C4'], 'A': ['A1', 'A2', 'C#4', 'E4', 'A3']}

# --- 1. Drone y brillo de la apertura (0 – 6.5 s) ---
drone = vacio(); n = int(6.9 * SR); t = np.arange(n) / SR
d = (onda_sierra(NOTA['D1'], t, .003) + .7 * onda_sierra(NOTA['D2'], t, .004) + .4 * onda_sierra(NOTA['A2'], t, .003))
d = filtro_fft(d, alto=420) * np.minimum(1, t / 3.0) * (0.85 + 0.15 * np.sin(t * 2.1))
brillo = (np.sin(2 * np.pi * NOTA['D5'] * t) + .6 * np.sin(2 * np.pi * NOTA['A5'] * t)) * (0.5 + 0.5 * np.sin(t * 9)) * np.minimum(1, t / 4) * 0.12
poner(drone, d * 0.5, 0); poner(drone, brillo, 0, pan=0.3)
for s in [1.0, 2.0, 3.0, 4.0, 5.0, 5.5, 6.0]:   # latido grave
    k = np.arange(int(.5 * SR)) / SR; poner(drone, np.sin(2 * np.pi * (55 * np.exp(-k * 3)) * k) * np.exp(-k * 9) * 0.7, s)

# --- 2. Golpes: BRAAM del título, impactos y subidas ---
def braam(dur, acorde, vol):
    k = np.arange(int(dur * SR)) / SR; x = sum(onda_sierra(NOTA[n], k, .006) for n in acorde)
    x = np.tanh(filtro_fft(x, alto=700) * 2.5) * np.minimum(1, k / 0.04) * np.exp(-k / (dur * 0.55))
    return x * vol
def impacto(vol=1.0):
    k = np.arange(int(2.5 * SR)) / SR
    boom = np.sin(2 * np.pi * (48 + 60 * np.exp(-k * 18)) * k) * np.exp(-k * 2.2)
    crack = filtro_fft(rng.standard_normal(len(k)), bajo=800, alto=9000) * np.exp(-k * 14) * 0.5
    return (boom + crack) * vol
def subida(dur, vol=0.5):
    k = np.arange(int(dur * SR)) / SR; ruido = rng.standard_normal(len(k))
    x = filtro_fft(ruido, bajo=600, alto=8000) * (k / dur) ** 2.5
    tono = np.sin(2 * np.pi * np.cumsum(200 + 1800 * (k / dur) ** 2) / SR) * (k / dur) ** 3 * 0.25
    return (x + tono) * vol
def zumbido(vol=0.6):   # whoosh para los cortes
    k = np.arange(int(0.7 * SR)) / SR; e = np.minimum(k / 0.25, 1) * np.exp(-np.maximum(k - 0.25, 0) * 9)
    return filtro_fft(rng.standard_normal(len(k)), bajo=300, alto=3500) * e * vol
golpes = vacio()
poner(golpes, subida(2.2, .45), 4.3); poner(golpes, braam(2.4, ['D1', 'D2', 'A2', 'D3', 'F3'], .55), 6.5); poner(golpes, impacto(1.0), 6.5)
poner(golpes, subida(1.0, .35), 7.5)
for s in [8.5, 12.0, 15.5, 18.0, 21.0]: poner(golpes, impacto(.55), s)
for s in [11.75, 15.25, 17.75, 20.75, 21.85, 22.7, 23.55, 24.25, 27.25]: poner(golpes, zumbido(.55), s, pan=rng.uniform(-.6, .6))
poner(golpes, subida(3.5, .5), 21.0); poner(golpes, braam(2.5, ['D1', 'D2', 'A2', 'D3'], .5), 24.5); poner(golpes, impacto(1.1), 24.5)
poner(golpes, subida(2.0, .5), 27.5); poner(golpes, braam(4.5, ['D1', 'D2', 'A2', 'D3', 'F3', 'A3'], .6), 29.5); poner(golpes, impacto(1.3), 29.5)

# --- 3. Taikos (8.5 – 29.5 s) ---
def taiko(vol=1.0, grave=True):
    k = np.arange(int(.8 * SR)) / SR; f0 = 62 if grave else 140
    cuerpo = np.sin(2 * np.pi * np.cumsum(f0 + f0 * 1.5 * np.exp(-k * 30)) / SR) * np.exp(-k * (5 if grave else 9))
    golpe = filtro_fft(rng.standard_normal(len(k)), alto=2500) * np.exp(-k * 40) * .5
    return (cuerpo + golpe) * vol
tambores = vacio()
PATRON = [(0, 1.0, True), (0.75, .55, False), (1.0, .8, True), (1.5, .55, False), (1.75, .5, False)]   # un compás de 2 s
s = 8.5
while s < 24.5:
    for off, v, g in PATRON: poner(tambores, taiko(v, g), s + off, pan=0 if g else -0.3)
    s += 2.0
s = 21.0
while s < 24.5:   # montaje: semicorcheas que crecen
    v = 0.25 + 0.5 * (s - 21) / 3.5; poner(tambores, taiko(v, False), s, pan=0.4); s += 0.125
s = 24.5
while s < 29.5:
    for off in [0, 0.5, 0.75, 1.0, 1.5]: poner(tambores, taiko(1.0 if off in (0, 1.0) else .6, off in (0, 1.0)), s + off)
    s += 2.0

# --- 4. Cuerdas rítmicas y bajo (8.5 – 29.5 s) ---
cuerdas = vacio(); bajo = vacio()
progresion = ['Dm', 'Bb', 'F', 'C'] * 2 + ['Dm', 'Bb', 'F', 'A']
for c, nombre in enumerate(progresion):
    inicio = 8.5 + c * 2.0
    if inicio >= 29.5: break
    notas = ACORDES[nombre]; arpegio = [notas[1], notas[3], notas[2], notas[4], notas[2], notas[3], notas[1], notas[3]]
    for j in range(16):
        k = np.arange(int(.14 * SR)) / SR; f = NOTA[arpegio[j % 8]] * (2 if c >= 8 else 1)
        x = filtro_fft(onda_sierra(f, k, .002), alto=2800) * np.minimum(1, k / .005) * np.exp(-k * 18)
        poner(cuerdas, x * (.18 + .08 * (j % 4 == 0)), inicio + j * .125, pan=(-0.4 if j % 2 else 0.4))
    k = np.arange(int(2.0 * SR)) / SR
    b = filtro_fft(onda_sierra(NOTA[notas[0]], k, .003), alto=300) * np.minimum(1, k / .02) * np.exp(-k * 0.6)
    poner(bajo, b * .55, inicio)

# --- 5. Melodía heroica de metales y coro (24.5 – 35 s) ---
metales = vacio()
MELODIA = [('D4', 0.0, 1.0), ('A4', 1.0, 1.0), ('F4', 2.0, 0.5), ('G4', 2.5, 0.5), ('A4', 3.0, 1.5), ('C5', 4.5, .5), ('D5', 5.0, 4.5)]
for nota, off, dur in MELODIA:
    k = np.arange(int((dur + .4) * SR)) / SR; f = NOTA[nota] * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * k) * np.minimum(1, k / .4))
    x = filtro_fft(onda_sierra(f, k, .004) + .5 * onda_sierra(f / 2, k, .003), alto=1800)
    e = np.minimum(1, k / .08) * np.clip((dur + .2 - k) / .3, 0, 1)
    poner(metales, np.tanh(x * 1.6) * e * .22, 24.5 + off)
coro = vacio()
for c, (nombre, ini, dur) in enumerate([('Dm', 24.5, 2), ('Bb', 26.5, 1), ('A', 27.5, 2), ('Dm', 29.5, 5.5)]):
    k = np.arange(int(dur * SR)) / SR; notas = ACORDES[nombre][2:]
    x = sum(filtro_fft(onda_sierra(NOTA[n] * 2, k, .008), bajo=500, alto=1600) for n in notas)
    poner(coro, x * np.minimum(1, k / .3) * np.clip((dur - k) / .8, 0, 1) * (.09 if dur < 5 else .1) * (np.exp(-k / 3) if dur > 5 else 1), ini)

mezcla = (reverb(drone, 3.0, .35) * .9 + reverb(golpes, 2.5, .25) + reverb(tambores, 1.6, .18) * .9 +
          reverb(cuerdas, 1.8, .3) * 1.4 + bajo * .8 + reverb(metales, 2.6, .35) * 1.3 + reverb(coro, 3.0, .45))
mezcla[-int(1.5 * SR):] *= np.linspace(1, 0, int(1.5 * SR))[:, None] ** 2
mezcla /= np.abs(mezcla).max() * 1.12
with wave.open('musica.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mezcla, -1, 1) * 32767).astype(np.int16).tobytes())
print('musica.wav lista', DUR, 's')
