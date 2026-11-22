# Mezcla de audio: música + voces + efectos del juego, con la música que baja cuando hablan.
import sys, os, json, subprocess
import numpy as np
IDIOMA = sys.argv[1]
SR, DUR = 48000, 35.0; N = int(SR * DUR)
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0], IDIOMA, 'nada']
import importlib.util
spec = importlib.util.spec_from_file_location('montar', os.path.join(RAIZ, 'montar.py')); M = importlib.util.module_from_spec(spec)
sys.argv = ['montar.py', IDIOMA]; spec.loader.exec_module(M)

def leer(ruta):
    crudo = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', ruta, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'])
    return np.frombuffer(crudo, dtype=np.float32).reshape(-1, 2).copy()
def db(x): return 10 ** (x / 20)
def poner(pista, sonido, t, vol_db=0.0, fundido=0.0):
    i = int(t * SR); s = sonido[: max(0, N - i)] * db(vol_db)
    if fundido: k = min(len(s), int(fundido * SR)); s[-k:] *= np.linspace(1, 0, k)[:, None]
    pista[i:i + len(s)] += s
SFX = {n: leer(os.path.join(RAIZ, 'juego_rodaje/audio', n + '.mp3')) for n in
       ['roar0', 'roar1', 'roar2', 'growl1', 'flap0', 'flap1', 'flap2', 'fire', 'boom', 'splash', 'hit', 'drill', 'skim', 'wind_lo', 'wind_hi', 'gull', 'sparkle']}

# ¿En qué momento del tráiler pasa cada evento grabado?
def eventos(toma):
    ruta = os.path.join(RAIZ, 'cuadros', toma, 'eventos.json')
    return json.load(open(ruta)) if os.path.exists(ruta) else []
def momento(toma, cuadro):   # cuadro grabado (desde 1) → primer segundo del tráiler donde aparece
    for i in range(int(35 * 30)):
        tm, n = M.cuadro_fuente(i / 30)
        if tm == toma and n >= cuadro: return i / 30
    return None
def primer(toma, cond):
    for i, e in enumerate(eventos(toma)):
        if cond(e): return momento(toma, i + 1)
    return None

efectos = np.zeros((N, 2), np.float32)
viento = SFX['wind_lo']; reps = int(np.ceil(N / len(viento))) + 1
poner(efectos, np.tile(viento, (reps, 1))[:N], 0, -20)
poner(efectos, SFX['gull'], 0.4, -16)
poner(efectos, SFX['flap0'], 2.75, -6); poner(efectos, SFX['flap1'], 3.2, -6); poner(efectos, SFX['roar0'], 2.9, -3)
poner(efectos, SFX['growl1'], 3.3, -12)
poner(efectos, SFX['roar1'], 6.5, -1)
t_fuego = 12.0 + 6 / 30
poner(efectos, SFX['fire'], t_fuego, 0); poner(efectos, SFX['roar2'], t_fuego - 0.15, -5)
t_quema = 12.0 + 11 / 30
poner(efectos, SFX['boom'], t_quema, -3)
poner(efectos, SFX['wind_hi'], 15.5, -8, fundido=0.6)
t_choque = 15.5 + 21 / 30
poner(efectos, SFX['boom'], t_choque, 0); poner(efectos, SFX['splash'], t_choque + 0.05, -2); poner(efectos, SFX['skim'], t_choque + 0.3, -8)
t_escudo = primer('s8_taladro', lambda e: e['escudo']) or 19.0
poner(efectos, SFX['drill'], t_escudo, -2)
for k in range(3): poner(efectos, SFX['hit'], t_escudo + 0.6 + k * 0.55, -6)
poner(efectos, SFX['flap2'], 21.1, -6); poner(efectos, SFX['roar2'], 21.9, -8); poner(efectos, SFX['fire'], 23.85, -4)
poner(efectos, SFX['roar0'], 24.55, -2); poner(efectos, SFX['flap1'], 25.6, -7); poner(efectos, SFX['flap0'], 27.4, -7)
poner(efectos, SFX['roar1'], 29.5, -2); poner(efectos, SFX['sparkle'], 30.7, -8)

voces = np.zeros((N, 2), np.float32)
for li in json.load(open(os.path.join(RAIZ, 'vo/lineas.json'), encoding='utf-8'))[IDIOMA]:
    poner(voces, leer(os.path.join(RAIZ, li['archivo'])), li['inicio'], 0)
musica = leer(os.path.join(RAIZ, 'musica.wav'))[:N]
musica = np.pad(musica, ((0, N - len(musica)), (0, 0)))

# La música (y el viento) bajan cuando hay voz: hasta −9 dB, con subida y bajada suaves.
def promedio(x, n):   # promedio móvil rápido (con sumas acumuladas)
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n // 2)])); return (c[n:] - c[:-n])[:len(x)] / n
energia = np.sqrt(promedio((voces ** 2).mean(1), 2400))
habla = promedio((energia > 0.01).astype(np.float32), int(0.25 * SR)).clip(0, 1)
musica *= (1 - (1 - db(-9)) * habla)[:, None]; efectos *= (1 - (1 - db(-4)) * habla)[:, None]

total = musica * db(-2) + efectos * db(-3) + voces * db(2)
total = np.tanh(total * 0.9) / 0.9      # limitador suave
crudo = os.path.join(RAIZ, f'mezcla_{IDIOMA}_cruda.wav'); final = os.path.join(RAIZ, f'mezcla_{IDIOMA}.wav')
import wave
with wave.open(crudo, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(total, -1, 1) * 32767).astype(np.int16).tobytes())
# Volumen final: −14 LUFS y picos por debajo de −1 dB (dos pasadas de loudnorm)
med = subprocess.run(['ffmpeg', '-hide_banner', '-i', crudo, '-af', 'loudnorm=I=-14:TP=-1:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
j = json.loads(med[med.rindex('{'):med.rindex('}') + 1])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', crudo, '-af',
    f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000",
    '-ar', '48000', final], check=True)
print(f'{IDIOMA}: fuego {t_fuego:.2f}s · quema {t_quema:.2f}s · choque {t_choque:.2f}s · escudo {t_escudo:.2f}s →', final)
