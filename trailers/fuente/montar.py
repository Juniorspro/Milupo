# Editor del tráiler: arma los 1050 cuadros (35 s a 30 fps) y los manda a ffmpeg.
# Uso: python montar.py en|es [prueba t1 t2 ...]
import sys, os, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

IDIOMA = sys.argv[1]
W, H, FPS, DUR = 1080, 1920, 30, 35.0
NF = int(DUR * FPS)
RAIZ = os.path.dirname(os.path.abspath(__file__))
F = lambda nombre, tam: ImageFont.truetype(os.path.join(RAIZ, 'juego/fonts', nombre + '.ttf'), tam)

# ---------- 1. Montaje: qué toma va en cada momento ----------
EDICION = [  # (inicio, fin, toma, primer cuadro, zoom inicial, zoom final)
    (0.0, 3.0, 's1_apertura', 1, 1.00, 1.05),
    (3.0, 4.65, 's2_bajo', 1, 1.02, 1.08),
    (4.65, 6.5, 's3_frente', 1, 1.00, 1.04),
    (6.5, 8.5, 's2_bajo', 1, 1.10, 1.18),          # fondo del título (desenfocado)
    (8.5, 12.0, f's5_hud_{IDIOMA}', 3 if IDIOMA == 'en' else 4, 1.0, 1.0),   # el «nivel superado» cae en 11,33 s en los dos idiomas
    (12.0, 14.4, 's6_fuego_lento', 1, 1.00, 1.04),        # fuego en cámara lenta real (×4)
    (14.4, 15.5, 's6_fuego', 16, 1.04, 1.06),             # sigue a velocidad normal
    (15.5, 17.45, 's7_picada_lento', 1, 1.00, 1.05),      # picada y choque en cámara lenta real (×4)
    (17.45, 18.0, 's7_picada', 22, 1.05, 1.06),           # sale del agua a velocidad normal
    (18.0, 21.0, 's8_taladro', 4, 1.00, 1.05),
    (21.0, 21.85, 's9a_acantilados', 4, 1.02, 1.07),
    (21.85, 22.7, 's9b_aurora', 4, 1.02, 1.07),
    (22.7, 23.55, 's9c_hielo', 4, 1.02, 1.07),
    (23.55, 24.5, 's9d_final', 3, 1.02, 1.07),
    (24.5, 29.5, 's10_heroe', [(24.5, 29.5, 1, 110)], 1.00, 1.08),   # órbita en cámara lenta suave
    (29.5, 35.0, 's11_fondo', -1, 1.06, 1.16),     # placa final sobre el último cuadro
]
TRANSICIONES = {3.0: 'barrido', 4.65: 'barrido', 6.5: 'destello', 8.5: 'destello', 12.0: 'barrido', 15.5: 'barrido', 18.0: 'barrido',
                21.0: 'destello', 21.85: 'corte', 22.7: 'corte', 23.55: 'corte', 24.5: 'destello', 29.5: 'destello'}
TEMBLORES = [(6.5, 0.5, 14), (8.5, 0.3, 8), (16.2, 0.8, 16), (24.5, 0.5, 12), (29.5, 0.5, 10)]   # (momento, duración, píxeles)
BANDAS = [(0.0, 8.5), (24.5, 29.5)]   # franjas de cine

TEXTOS = {
  'en': {'titulo_sub': 'A SKY WITHOUT LIMITS', 'cartas': [(8.6, 11.25, 'SWIPE TO SOAR'), (12.1, 15.4, 'BREATHE FIRE'), (15.6, 17.9, 'DIVE STRIKE'),
          (18.1, 20.9, 'DRILL SHIELD'), (24.6, 27.4, '20 LEVELS')], 'lema': 'Ride the dragon. Rule the sky.', 'boton': 'PLAY NOW', 'donde': 'Free to play on Rezona'},
  'es': {'titulo_sub': 'UN CIELO SIN LÍMITES', 'cartas': [(8.6, 11.25, 'DESLIZA PARA VOLAR'), (12.1, 15.4, 'ESCUPE FUEGO'), (15.6, 17.9, 'ATAQUE EN PICADA'),
          (18.1, 20.9, 'ESCUDO TALADRO'), (24.6, 27.4, '20 NIVELES')], 'lema': 'Monta el dragón. Domina el cielo.', 'boton': 'JUEGA YA', 'donde': 'Gratis en Rezona'},
}[IDIOMA]
LINEAS = json.load(open(os.path.join(RAIZ, 'vo/lineas.json'), encoding='utf-8'))[IDIOMA]
COLOR_VOZ = {'narrador': (255, 255, 255), 'dragon': (255, 206, 110), 'jinete': (150, 230, 255)}

# ---------- 2. Imagen: escalado, color de cine, viñeta y grano ----------
x = np.linspace(0, 1, 256)
curva = np.clip(x - 0.075 * np.sin(2 * np.pi * x), 0, 1)                                  # curva en S (más contraste)
LUT = np.stack([np.clip(curva * 1.03 + 0.01, 0, 1), curva, np.clip(curva * 0.97 + 0.03 * (1 - x), 0, 1)], 1)   # cálido en luces, frío en sombras
LUT = (LUT * 255).astype(np.uint8)
yy, xx = np.mgrid[0:H, 0:W]
VINETA = (1 - 0.32 * np.clip(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2, 0, 1.4))[..., None].astype(np.float32)
rng = np.random.default_rng(3)
GRANOS = [rng.normal(0, 4.5, (H, W, 1)).astype(np.float32) for _ in range(6)]
cache = {}
CARPETA = os.environ.get('CUADROS', 'cuadros')
def numeros(toma):
    ruta = os.path.join(RAIZ, CARPETA, toma)
    return sorted(int(f[:4]) for f in os.listdir(ruta) if f.endswith('.jpg')) if os.path.isdir(ruta) else []
def un_cuadro(toma, n):
    nums = numeros(toma)
    if not nums: return Image.new('RGB', (W, H), (40, 40, 48))
    n = nums[-1] if n < 1 else max([k for k in nums if k <= n] or [nums[0]])
    clave = (toma, n)
    if clave not in cache:
        if len(cache) > 40: cache.clear()
        im = Image.open(os.path.join(RAIZ, CARPETA, toma, f'{n:04d}.jpg')).convert('RGB')
        if im.size != (W, H): im = im.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
        cache[clave] = im
    return cache[clave]
def cuadro_toma(toma, n):
    if n < 1 or abs(n - round(n)) < 0.05: return un_cuadro(toma, round(n) if n >= 1 else -1)
    a = int(n); return Image.blend(un_cuadro(toma, a), un_cuadro(toma, a + 1), n - a)
def zoom(im, z, dx=0, dy=0):
    if abs(z - 1) < 1e-3 and dx == 0 and dy == 0: return im
    w, h = W / z, H / z; x0, y0 = (W - w) / 2 + dx, (H - h) / 2 + dy
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC)
def gradar(im, i):
    a = np.asarray(im)
    a = np.stack([LUT[a[..., c], c] for c in range(3)], -1).astype(np.float32)
    gris = a.mean(-1, keepdims=True); a = gris + (a - gris) * 1.08              # un poco más de color
    a = a * VINETA + GRANOS[i % 6]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def toma_en(t):
    for k, (a, b, toma, desde, z0, z1) in enumerate(EDICION):
        if a <= t < b: return k, a, b, toma, desde, z0, z1
    return len(EDICION) - 1, *EDICION[-1][:2], *EDICION[-1][2:]
def cuadro_fuente(t):   # qué cuadro grabado corresponde al segundo t del tráiler (con rampas de velocidad)
    k, a, b, toma, desde, z0, z1 = toma_en(t)
    if isinstance(desde, list):
        for t0, t1, f0, f1 in desde:
            if t0 <= t < t1: return toma, f0 + (f1 - f0) * (t - t0) / (t1 - t0)
        return toma, desde[-1][3]
    if desde < 0: return toma, -1
    return toma, desde + int(round((t - a) * FPS))
def imagen_en(t):
    k, a, b, toma, desde, z0, z1 = toma_en(t)
    p = (t - a) / (b - a); _, n = cuadro_fuente(t)
    im = zoom(cuadro_toma(toma, n), z0 + (z1 - z0) * (p * p * (3 - 2 * p)))
    if a == 6.5: im = im.filter(ImageFilter.GaussianBlur(9)); im = Image.eval(im, lambda v: int(v * 0.55))
    if a == 29.5:
        r = min(1, (t - 29.5) / 0.8); im = im.filter(ImageFilter.GaussianBlur(2 + 8 * r)); im = Image.eval(im, lambda v, r=r: int(v * (1 - 0.45 * r)))
    return im

def desenfoque_movimiento(im, fuerza):
    a = np.asarray(im).astype(np.float32); r = max(1, int(fuerza))
    c = np.cumsum(np.pad(a, ((0, 0), (r, r), (0, 0)), mode='edge'), axis=1)
    b = (c[:, 2 * r:] - c[:, :-2 * r]) / (2 * r)
    return Image.fromarray(np.clip(b[:, :W], 0, 255).astype(np.uint8))

# ---------- 3. Textos ----------
def texto_con_borde(txt, fuente, relleno, borde=(0, 0, 0), grosor=5, sombra=18, degradado=None, espaciado=0):
    caja = fuente.getbbox(txt); w, h = caja[2] - caja[0] + 40 + espaciado * len(txt), caja[3] - caja[1] + 40
    capa = Image.new('RGBA', (w + sombra * 2, h + sombra * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
    pos = (sombra + 20 - caja[0], sombra + 20 - caja[1])
    def escribir(dib, color, **kw):
        if espaciado:
            xx = pos[0]
            for ch in txt: dib.text((xx, pos[1]), ch, font=fuente, fill=color, **kw); xx += fuente.getlength(ch) + espaciado
        else: dib.text(pos, txt, font=fuente, fill=color, **kw)
    if sombra:
        s = Image.new('RGBA', capa.size, (0, 0, 0, 0)); escribir(ImageDraw.Draw(s), (0, 0, 0, 170), stroke_width=grosor + 4, stroke_fill=(0, 0, 0, 170))
        capa = Image.alpha_composite(capa, s.filter(ImageFilter.GaussianBlur(sombra / 2)))
    if degradado:
        mascara = Image.new('L', capa.size, 0); escribir(ImageDraw.Draw(mascara), 255)
        borde_capa = Image.new('RGBA', capa.size, (0, 0, 0, 0)); escribir(ImageDraw.Draw(borde_capa), borde + (255,), stroke_width=grosor, stroke_fill=borde + (255,))
        capa = Image.alpha_composite(capa, borde_capa)
        g = Image.new('RGBA', capa.size); arriba, abajo = degradado
        col = np.linspace(0, 1, capa.size[1])[:, None, None]
        arr = (np.array(arriba)[None, None] * (1 - col) + np.array(abajo)[None, None] * col)
        g = Image.fromarray(np.concatenate([np.broadcast_to(arr, (capa.size[1], capa.size[0], 3)), np.full((capa.size[1], capa.size[0], 1), 255)], -1).astype(np.uint8), 'RGBA')
        capa.paste(g, (0, 0), mascara)
    else:
        escribir(ImageDraw.Draw(capa), relleno + (255,), stroke_width=grosor, stroke_fill=borde + (255,))
    return capa
def poner(base, capa, cx, cy, escala=1.0, alfa=1.0, angulo=0):
    if escala != 1.0: capa = capa.resize((max(1, int(capa.width * escala)), max(1, int(capa.height * escala))), Image.BICUBIC)
    if angulo: capa = capa.rotate(angulo, Image.BICUBIC, expand=True)
    if alfa < 1: capa = capa.copy(); capa.putalpha(capa.getchannel('A').point(lambda v: int(v * alfa)))
    base.alpha_composite(capa, (int(cx - capa.width / 2), int(cy - capa.height / 2)))
def partir(txt, fuente, ancho):
    lineas, actual = [], ''
    for palabra in txt.split():
        prueba = (actual + ' ' + palabra).strip()
        if fuente.getlength(prueba) > ancho and actual: lineas.append(actual); actual = palabra
        else: actual = prueba
    return lineas + [actual]

ORO = ((255, 236, 170), (255, 150, 40))
CAPAS = {}
def capa(clave, fn):
    if clave not in CAPAS: CAPAS[clave] = fn()
    return CAPAS[clave]
fuente_sub = F('dr-body-bold', 66)
def subtitulos(base, t):
    if t >= 29.5: return     # en la placa final el texto ya está en pantalla
    for li in LINEAS:
        a, b = li['inicio'] - 0.05, li['inicio'] + max(li['dur'] + 0.35, 1.1)
        if not (a <= t < b): continue
        alfa = min(1, (t - a) / 0.12, (b - t) / 0.15)
        filas = partir(li['texto'], fuente_sub, 820)
        for j, fila in enumerate(filas):
            c = capa(('sub', fila, li['quien']), lambda fila=fila, q=li['quien']: texto_con_borde(fila, fuente_sub, COLOR_VOZ[q], grosor=5, sombra=16))
            poner(base, c, 500, 1330 + (j - (len(filas) - 1) / 2) * 82, alfa=alfa)
fuente_carta = F('dr-title', 128)
def cartas(base, t):
    for a, b, txt in TEXTOS['cartas']:
        if not (a <= t < b): continue
        p = t - a; escala = 1.0 + 0.35 * math.exp(-p * 9) + 0.02 * p; alfa = min(1, p / 0.12, (b - t) / 0.2)
        c = capa(('carta', txt), lambda txt=txt: texto_con_borde(txt, fuente_carta, (255, 255, 255), borde=(60, 20, 0), grosor=5, sombra=20, degradado=ORO))
        if c.width > W - 110: c = capa(('carta_ajustada', txt), lambda c=c: c.resize((W - 110, int(c.height * (W - 110) / c.width)), Image.LANCZOS))
        y = 560 if 'hud' in toma_en(t)[3] else 330
        poner(base, c, W / 2, y, escala=escala, alfa=alfa)
fuente_logo = F('dr-logo', 170); fuente_lema = F('dr-title', 72); fuente_boton = F('dr-body-bold', 70); fuente_donde = F('dr-body-bold', 54)
def titulo(base, t):
    if 6.5 <= t < 8.5:
        p = t - 6.5; alfa = min(1, p / 0.08, (8.5 - t) / 0.25)
        logo = capa('logo', lambda: texto_con_borde('DRAGON RIDER', fuente_logo, (255, 255, 255), borde=(70, 15, 0), grosor=6, sombra=26, degradado=ORO))
        if logo.width > W - 40: logo = capa('logo_aj', lambda: logo.resize((W - 40, int(logo.height * (W - 40) / logo.width)), Image.LANCZOS))
        poner(base, logo, W / 2, 900, escala=1.0 + 0.4 * math.exp(-p * 10) + 0.03 * p, alfa=alfa)
        sub = capa('tsub', lambda: texto_con_borde(TEXTOS['titulo_sub'], F('dr-body-bold', 46), (255, 244, 225), borde=(40, 10, 0), grosor=4, sombra=14, espaciado=8))
        poner(base, sub, W / 2, 1050, alfa=max(0, min(1, (p - 0.35) / 0.3)) * alfa)
def placa_final(base, t):
    if t < 29.5: return
    p = t - 29.5
    logo = capa('logo2', lambda: texto_con_borde('DRAGON RIDER', fuente_logo, (255, 255, 255), borde=(70, 15, 0), grosor=6, sombra=26, degradado=ORO))
    if logo.width > W - 60: logo = capa('logo2_aj', lambda: logo.resize((W - 60, int(logo.height * (W - 60) / logo.width)), Image.LANCZOS))
    poner(base, logo, W / 2, 700, escala=1.0 + 0.3 * math.exp(-p * 8), alfa=min(1, p / 0.15))
    lema = capa('lema', lambda: texto_con_borde(TEXTOS['lema'], fuente_lema, (255, 240, 215), grosor=3, sombra=12))
    poner(base, lema, W / 2, 860, alfa=max(0, min(1, (p - 0.6) / 0.4)))
    if p > 1.2:   # botón que late
        q = p - 1.2; pulso = 1 + 0.035 * math.sin(q * 6)
        boton = capa('boton', lambda: boton_jugar(TEXTOS['boton']))
        poner(base, boton, W / 2, 1120, escala=pulso * (1 + 0.25 * math.exp(-q * 9)), alfa=min(1, q / 0.2))
        donde = capa('donde', lambda: texto_con_borde(TEXTOS['donde'], fuente_donde, (255, 255, 255), grosor=3, sombra=10))
        poner(base, donde, W / 2, 1265, alfa=min(1, max(0, (q - 0.3) / 0.3)))
def boton_jugar(txt):
    tw = int(fuente_boton.getlength(txt)); w, h = tw + 230, 150
    c = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    s = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(s).rounded_rectangle((30, 40, 30 + w, 40 + h), 75, fill=(0, 0, 0, 140))
    c = Image.alpha_composite(c, s.filter(ImageFilter.GaussianBlur(12))); d = ImageDraw.Draw(c)
    d.rounded_rectangle((30, 30, 30 + w, 30 + h), 75, fill=(255, 122, 26, 255))
    d.rounded_rectangle((30, 30, 30 + w, 30 + h * 0.5), 75, fill=(255, 150, 60, 255))
    d.rounded_rectangle((30, 30 + h * 0.35, 30 + w, 30 + h), 75, fill=(255, 122, 26, 255))
    cx = 30 + 90; cy = 30 + h / 2; d.polygon([(cx - 22, cy - 30), (cx - 22, cy + 30), (cx + 30, cy)], fill='white')
    d.text((30 + 150, 30 + h / 2), txt, font=fuente_boton, fill='white', anchor='lm')
    return c

# ---------- 4. Chispas que flotan (título y placa final) ----------
CHISPAS = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(40, 140), rng.uniform(2, 6), rng.uniform(0, 6.28)) for _ in range(70)]
def chispas(base, t, alfa):
    d = ImageDraw.Draw(base)
    for x0, y0, vel, tam, fase in CHISPAS:
        y = (y0 - vel * t) % H; x = x0 + 30 * math.sin(t * 1.3 + fase)
        brillo = int(255 * alfa * (0.5 + 0.5 * math.sin(t * 4 + fase)))
        d.ellipse((x - tam, y - tam, x + tam, y + tam), fill=(255, 170 + int(60 * math.sin(fase)), 60, brillo))

# ---------- 5. Cuadro final ----------
def cuadro(i):
    t = i / FPS
    dx = dy = 0
    for m, dur, px in TEMBLORES:
        if m <= t < m + dur: f = px * (1 - (t - m) / dur); dx += f * math.sin(t * 91); dy += f * math.cos(t * 77)
    im = imagen_en(t)
    corte = min(TRANSICIONES, key=lambda c: abs(c - t))
    tipo = TRANSICIONES[corte]; d = t - corte
    if tipo == 'barrido' and -0.1 <= d < 0.1:
        im = desenfoque_movimiento(im, 70 * (1 - abs(d) / 0.1))
    if tipo == 'fundido' and -0.2 <= d < 0.2:
        im = Image.blend(imagen_en(corte - 0.21), imagen_en(corte + 0.2), (d + 0.2) / 0.4)
    if dx or dy: im = zoom(im, 1.03, dx, dy)
    im = gradar(im, i).convert('RGBA')
    # franjas de cine
    for a, b in BANDAS:
        if a - 0.01 <= t < b + 0.4:
            k = 1 if t < b else 1 - (t - b) / 0.4
            if t < a + 0.4 and a > 0: k = (t - a) / 0.4
            alto = int(190 * max(0, min(1, k)))
            if alto: d0 = ImageDraw.Draw(im); d0.rectangle((0, 0, W, alto), fill='black'); d0.rectangle((0, H - alto, W, H), fill='black')
    if 6.5 <= t < 8.5 or t >= 29.5: chispas(im, t, 1.0 if t >= 29.5 else 0.8)
    titulo(im, t); cartas(im, t); placa_final(im, t); subtitulos(im, t)
    # destellos y fundidos a negro
    blanco = 0
    if tipo in ('destello', 'corte') and -0.03 <= d < 0.25: blanco = (0.85 if tipo == 'destello' else 0.35) * (1 - max(d, 0) / 0.25)
    if blanco: im = Image.blend(im, Image.new('RGBA', (W, H), (255, 250, 240, 255)), min(1, blanco))
    negro = 0
    if t < 0.8: negro = 1 - t / 0.8
    if t > 34.2: negro = (t - 34.2) / 0.8
    if negro > 0: im = Image.blend(im, Image.new('RGBA', (W, H), (0, 0, 0, 255)), min(1, negro))
    return im.convert('RGB')

if __name__ == '__main__' and not (len(sys.argv) > 2 and sys.argv[2] == 'nada'):
    if len(sys.argv) > 2 and sys.argv[2] == 'prueba':
        for t in map(float, sys.argv[3:]): cuadro(int(t * FPS)).save(f'prueba_{IDIOMA}_{t:05.2f}.jpg', quality=90)
        sys.exit()
    salida = os.path.join(RAIZ, f'video_{IDIOMA}.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', salida], stdin=subprocess.PIPE)
    for i in range(NF):
        ff.stdin.write(cuadro(i).tobytes())
        if i % 150 == 0: print(f'{IDIOMA}: cuadro {i}/{NF}', flush=True)
    ff.stdin.close(); ff.wait(); print('listo', salida)
