#!/usr/bin/env python3
"""Arma el libro (o un bloque) en HTML y PDF de 6 × 9 pulgadas.
Uso: python3 construir.py <salida.pdf> <título del bloque> archivo1.md archivo2.md ..."""
import subprocess, sys, os, html
AQUI = os.path.dirname(os.path.abspath(__file__))
salida, bloque, archivos = sys.argv[1], sys.argv[2], sys.argv[3:]
md = '\n\n'.join(open(a, encoding='utf-8').read() for a in archivos)
cuerpo = subprocess.run(['pandoc', '-f', 'markdown+fenced_divs+pipe_tables+smart', '-t', 'html5'], input=md.encode(), capture_output=True, check=True).stdout.decode()
portadilla = f'''<section class="portadilla">
  <div class="semaforo"><i style="background:#1d8a4e"></i><i style="background:#d9a200"></i><i style="background:#c8323c"></i></div>
  <div class="t1">Estudiar con IA<br>sin hacer trampa</div>
  <div class="t2">Guía práctica para aprender de verdad, preparar tus exámenes y hacer mejores trabajos con la inteligencia artificial</div>
  <div class="t3">{html.escape(bloque)}</div>
</section>'''
pagina = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Estudiar con IA sin hacer trampa</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:opsz,wght@6..12,400;6..12,700;6..12,800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,700;1,8..60,400&family=Source+Code+Pro:wght@400;600&display=swap" rel="stylesheet">
<style>{open(os.path.join(AQUI, 'libro.css'), encoding='utf-8').read()}</style></head>
<body>{portadilla}{cuerpo}</body></html>'''
html_salida = salida.replace('.pdf', '.html')
open(html_salida, 'w', encoding='utf-8').write(pagina)
subprocess.run(['node', os.path.join(AQUI, 'pdf.js'), html_salida, salida], check=True)
print('listo', salida)
