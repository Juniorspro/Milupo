# Portada para TikTok (1080x1920) a partir de un cuadro del tráiler, con el título grande.
import sys, os
sys.argv = ['montar.py', sys.argv[1], 'nada']
import importlib.util
spec = importlib.util.spec_from_file_location('montar', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'montar.py'))
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
from PIL import Image
base = M.gradar(M.zoom(M.cuadro_toma('s10_heroe', 60), 1.08), 0).convert('RGBA')
logo = M.texto_con_borde('DRAGON RIDER', M.F('dr-logo', 170), (255, 255, 255), borde=(70, 15, 0), grosor=7, sombra=30, degradado=M.ORO)
if logo.width > M.W - 60: logo = logo.resize((M.W - 60, int(logo.height * (M.W - 60) / logo.width)), Image.LANCZOS)
M.poner(base, logo, M.W / 2, 420)
lema = M.texto_con_borde(M.TEXTOS['lema'], M.F('dr-title', 74), (255, 240, 215), grosor=4, sombra=14)
M.poner(base, lema, M.W / 2, 580)
base.convert('RGB').save(f'/home/user/Milupo/trailers/DragonRider_Portada_{M.IDIOMA.upper()}.jpg', quality=93)
print('portada lista')
