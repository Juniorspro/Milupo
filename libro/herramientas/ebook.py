#!/usr/bin/env python3
"""Arma el ebook (EPUB 3) a partir del manuscrito. Uso: python3 ebook.py"""
import glob, os, subprocess, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))
FINAL = os.path.join(AQUI, '..', 'final')
AUTOR = os.environ.get('AUTOR', '[Nombre del autor]')
partes, cap = [], 0
for a in sorted(glob.glob(os.path.join(AQUI, '..', 'manuscrito', '*.md'))):
    lineas = open(a, encoding='utf-8').read().split('\n')
    sec, dentro = 0, False
    for i, l in enumerate(lineas):
        if l.startswith('```'): dentro = not dentro
        if dentro: continue
        if l.startswith('# ') and '.parte' not in l and '.unnumbered' not in l:
            cap += 1; sec = 0
            lineas[i] = f'# [Capítulo {cap}]{{.num}} ' + l[2:]
        elif l.startswith('# '):
            sec = -1
        elif l.startswith('## ') and '.subtitulo' not in l and sec >= 0 and cap > 0:
            sec += 1
            lineas[i] = f'## {cap}.{sec} ' + l[3:]
    partes.append('\n'.join(lineas))
creditos = f'''# Créditos {{.unnumbered .unlisted}}

**Estudiar con IA sin hacer trampa**\
Guía práctica para aprender de verdad, preparar tus exámenes y hacer mejores trabajos con la inteligencia artificial

© 2026 {AUTOR}. Todos los derechos reservados.

Ninguna parte de esta publicación puede reproducirse, almacenarse ni transmitirse por ningún medio sin permiso previo y por escrito del autor, salvo citas breves en reseñas.

Los personajes y las situaciones de este libro son ficticios. Los nombres de productos y servicios que pudieran mencionarse pertenecen a sus respectivos dueños; este libro no está afiliado a ninguna empresa de inteligencia artificial.

La información sobre herramientas de IA refleja el momento en que se escribió este libro. Las herramientas, sus funciones y sus condiciones de uso cambian con frecuencia: consulta siempre las condiciones de cada servicio.

'''
partes.insert(0, creditos)
md = '\n\n'.join(partes).replace(
    '# Anexo B. El Semáforo del uso honesto y el acuerdo de uso {.unnumbered .anexo}',
    '# Anexo B. El Semáforo del uso honesto y el acuerdo de uso {.unnumbered .anexo}\n\n*En la versión digital, puedes copiar estas plantillas en un cuaderno o en un documento.*')
meta = f'''---
title:
- type: main
  text: Estudiar con IA sin hacer trampa
- type: subtitle
  text: Guía práctica para aprender de verdad, preparar tus exámenes y hacer mejores trabajos con la inteligencia artificial
creator:
- role: author
  text: "{AUTOR}"
lang: es
rights: © 2026 {AUTOR}. Todos los derechos reservados.
---
'''
with tempfile.TemporaryDirectory() as t:
    open(os.path.join(t, 'meta.yaml'), 'w', encoding='utf-8').write(meta)
    open(os.path.join(t, 'libro.md'), 'w', encoding='utf-8').write(md)
    subprocess.run(['pandoc', os.path.join(t, 'meta.yaml'), os.path.join(t, 'libro.md'),
                    '-f', 'markdown+fenced_divs+pipe_tables+smart+task_lists+bracketed_spans', '-t', 'epub3',
                    '--toc', '--toc-depth=1', '--split-level=1', '--css', os.path.join(AQUI, 'ebook.css'),
                    '--epub-cover-image', os.path.join(FINAL, 'Portada_Ebook_1600x2560.jpg'),
                    '-o', os.path.join(FINAL, 'EstudiarConIA_ebook.epub')], check=True)
print('epub listo:', os.path.getsize(os.path.join(FINAL, 'EstudiarConIA_ebook.epub')) // 1024, 'KB')
