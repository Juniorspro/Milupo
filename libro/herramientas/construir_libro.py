#!/usr/bin/env python3
"""Arma el interior completo del libro (PDF 6 × 9 pulgadas) con páginas iniciales, índice paginado
y capítulos que empiezan en página impar.
Uso: python3 construir_libro.py <salida.pdf>"""
import subprocess, sys, os, re, html, glob, unicodedata
from pypdf import PdfReader
AQUI = os.path.dirname(os.path.abspath(__file__))
MANUSCRITO = os.path.join(AQUI, '..', 'manuscrito')
salida = os.path.abspath(sys.argv[1])
TITULO = 'Estudiar con IA sin hacer trampa'
SUBTITULO = 'Guía práctica para aprender de verdad, preparar tus exámenes y hacer mejores trabajos con la inteligencia artificial'
AUTOR = os.environ.get('AUTOR', '[Nombre del autor]')

archivos = sorted(glob.glob(os.path.join(MANUSCRITO, '*.md')))
md = '\n\n'.join(open(a, encoding='utf-8').read() for a in archivos)
cuerpo = subprocess.run(['pandoc', '-f', 'markdown+fenced_divs+pipe_tables+smart+task_lists', '-t', 'html5'],
                        input=md.encode(), capture_output=True, check=True).stdout.decode()

# Lista de títulos de nivel 1 (partes, capítulos, introducción, conclusión, anexos)
titulos = []
for m in re.finditer(r'<h1([^>]*)>(.*?)</h1>', cuerpo, re.S):
    attrs, texto = m.group(1), re.sub('<[^>]+>', '', m.group(2)).strip()
    clase = re.search(r'class="([^"]*)"', attrs); clase = clase.group(1) if clase else ''
    tipo = 'parte' if 'parte' in clase else ('otro' if 'unnumbered' in clase else 'cap')
    titulos.append({'texto': html.unescape(texto), 'tipo': tipo})
n = 0
for t in titulos:
    if t['tipo'] == 'cap': n += 1; t['num'] = n

def normal(s):
    s = unicodedata.normalize('NFKC', s).replace('­', '')
    return re.sub(r'[^a-záéíóúüñ0-9]', '', s.lower())

def portada():
    return f'''<section class="portadilla">
  <div class="semaforo"><i style="background:#1d8a4e"></i><i style="background:#d9a200"></i><i style="background:#c8323c"></i></div>
  <div class="t1">Estudiar con IA<br>sin hacer trampa</div>
  <div class="t2">{SUBTITULO}</div>
  <div class="autor">{html.escape(AUTOR)}</div>
</section>
<section class="derechos">
  <p><strong>{TITULO}</strong><br>{SUBTITULO}</p>
  <p>© 2026 {html.escape(AUTOR)}. Todos los derechos reservados.</p>
  <p>Ninguna parte de esta publicación puede reproducirse, almacenarse ni transmitirse por ningún medio sin permiso previo y por escrito del autor, salvo citas breves en reseñas. Los anexos B, C y D pueden fotocopiarse para uso personal, familiar o en el aula.</p>
  <p>Primera edición: [mes y año].<br>ISBN de la edición en tapa blanda: [completar].</p>
  <p>Los personajes y las situaciones de este libro son ficticios. Los nombres de productos y servicios que pudieran mencionarse pertenecen a sus respectivos dueños; este libro no está afiliado a ninguna empresa de inteligencia artificial.</p>
  <p>La información sobre herramientas de IA refleja el momento en que se escribió este libro. Las herramientas, sus funciones y sus condiciones de uso cambian con frecuencia: consulta siempre las condiciones de cada servicio.</p>
  <p>[Opcional: nota sobre el uso de inteligencia artificial en la elaboración de este libro.]</p>
</section>'''

def indice(paginas):
    filas = []
    for i, t in enumerate(titulos):
        p = paginas.get(i, '')
        if t['tipo'] == 'parte':
            if t['texto'] == 'Anexos': continue
            filas.append(f'<li class="parte-i"><span class="t">{html.escape(t["texto"])}</span></li>')
        elif t['tipo'] == 'cap':
            filas.append(f'<li class="cap"><span class="num">{t["num"]}</span><span class="t">{html.escape(t["texto"])}</span><span class="p"></span><span class="n">{p}</span></li>')
        else:
            filas.append(f'<li><span class="t">{html.escape(t["texto"])}</span><span class="p"></span><span class="n">{p}</span></li>')
    return f'<section class="indice"><h1 class="unnumbered">Índice</h1><ol>{"".join(filas)}</ol></section>'

# Versión para imprimir en blanco y negro: grises calibrados en lugar de colores
BYN_CSS = """
:root { --azul:#3a3a3a; --azul-claro:#efefef; --naranja:#3a3a3a; --naranja-claro:#f4f4f4; --verde:#3a3a3a; --verde-claro:#efefef;
        --gris:#3a3a3a; --gris-claro:#f1f1f1; --rojo:#2a2a2a; --amarillo:#8a8a8a; }
.pidelo { border-left-style: solid; } .ojo { border-left-style: dashed; } .turno { border-left-style: double; border-left-width: 5pt; }
.luz.amarillo { background: #f4f4f4; } .luz.rojo { background: #e9e9e9; } .luz.verde { background: #fafafa; }
.portadilla .semaforo i:nth-child(1) { background: #3a3a3a !important; } .portadilla .semaforo i:nth-child(2) { background: #9a9a9a !important; }
.portadilla .semaforo i:nth-child(3) { background: #1a1a1a !important; }
.pidelo blockquote { border-color: #cfcfcf; }
"""

def fuentes():
    """Fuentes locales (licencia SIL OFL) para que el resultado sea siempre igual y quede incrustado en el PDF."""
    d = os.path.join(AQUI, 'fuentes')
    caras = [('Source Serif 4', 'source-serif-4', 400, 'normal'), ('Source Serif 4', 'source-serif-4', 400, 'italic'),
             ('Source Serif 4', 'source-serif-4', 700, 'normal'), ('Nunito Sans', 'nunito-sans', 400, 'normal'),
             ('Nunito Sans', 'nunito-sans', 700, 'normal'), ('Nunito Sans', 'nunito-sans', 800, 'normal'),
             ('Source Code Pro', 'source-code-pro', 400, 'normal')]
    return ''.join(f"@font-face {{ font-family: '{f}'; font-weight: {w}; font-style: {st}; src: url('file://{d}/{a}-latin-{w}-{st}.woff2') format('woff2'); }}\n"
                   for f, a, w, st in caras)

def armar(paginas, blancas):
    # Inserta páginas en blanco antes de los títulos indicados (por posición)
    contador = [-1]
    def reemplazo(m):
        contador[0] += 1
        return ('<div class="blanca"></div>' if contador[0] in blancas else '') + m.group(0)
    c = re.sub(r'<h1[^>]*>', reemplazo, cuerpo)
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{TITULO}</title>
<style>{fuentes()}{open(os.path.join(AQUI, 'libro.css'), encoding='utf-8').read()}{BYN_CSS if os.environ.get('BYN') == '1' else ''}</style></head>
<body>{portada()}{indice(paginas)}{c}</body></html>'''

def render(paginas, blancas):
    h = salida.replace('.pdf', '.html')
    open(h, 'w', encoding='utf-8').write(armar(paginas, blancas))
    subprocess.run(['node', os.path.join(AQUI, 'pdf_libro.js'), h, salida], check=True)
    textos = [normal(pg.extract_text() or '') for pg in PdfReader(salida).pages]
    # La página de cada título: la primera página, después del índice, donde aparece el comienzo del título
    inicio = next(i for i, t in enumerate(textos) if 'índice' in t or 'indice' in t) + 1
    pags, desde = {}, inicio
    for i, t in enumerate(titulos):
        clave = normal(t['texto'])[:22]
        for k in range(desde, len(textos)):
            if clave in textos[k]:
                pags[i] = k + 1; desde = k + 1; break
    return pags, len(textos)

pags, total = render({}, set())
# Capítulos, partes, introducción, conclusión y anexos empiezan en página impar
blancas, corrimiento = set(), 0
for i, t in enumerate(titulos):
    if i not in pags: continue
    p = pags[i] + corrimiento
    if p % 2 == 0:
        blancas.add(i); corrimiento += 1
for intento in range(3):
    nuevas, total = render(pags, blancas)
    if nuevas == pags: break
    pags = nuevas
faltan = [t['texto'] for i, t in enumerate(titulos) if i not in pags]
print('páginas:', total, '| títulos sin ubicar:', faltan)
for i, t in enumerate(titulos): print(f"  {pags.get(i, '?'):>4}  {t['texto']}")
os.remove(salida.replace('.pdf', '.html'))
