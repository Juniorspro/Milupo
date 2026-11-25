#!/usr/bin/env python3
"""Portada para KDP: tapa blanda completa (contratapa + lomo + tapa, con sangrado) y portada de ebook.
Uso: python3 portada.py <páginas del interior> [blanco|crema]"""
import sys, os, subprocess
AQUI = os.path.dirname(os.path.abspath(__file__))
FINAL = os.path.join(AQUI, '..', 'final')
paginas = int(sys.argv[1]); papel = sys.argv[2] if len(sys.argv) > 2 else 'blanco'
AUTOR = os.environ.get('AUTOR', '[Nombre del autor]')
grosor = paginas * (0.002252 if papel == 'blanco' else 0.0025)      # fórmula de KDP para interior en blanco y negro
SANGRADO, ANCHO, ALTO = 0.125, 6.0, 9.0
total_w = SANGRADO * 2 + ANCHO * 2 + grosor
total_h = ALTO + SANGRADO * 2
d = os.path.join(AQUI, 'fuentes')
fuentes = ''.join(f"@font-face {{ font-family: '{f}'; font-weight: {w}; font-style: {st}; src: url('file://{d}/{a}-latin-{w}-{st}.woff2'); }}\n"
                  for f, a, w, st in [('Source Serif 4', 'source-serif-4', 400, 'normal'), ('Source Serif 4', 'source-serif-4', 400, 'italic'),
                                      ('Source Serif 4', 'source-serif-4', 700, 'normal'), ('Nunito Sans', 'nunito-sans', 700, 'normal'),
                                      ('Nunito Sans', 'nunito-sans', 800, 'normal'), ('Source Code Pro', 'source-code-pro', 400, 'normal')])

FRENTE = f'''
<div class="frente">
  <div class="etiqueta">Para estudiantes de secundaria</div>
  <div class="bloque">
    <div class="titulo">Estudiar<br>con IA<br><span>sin hacer<br>trampa</span></div>
    <div class="semaforo"><i class="v"></i><i class="a"></i><i class="r"></i></div>
  </div>
  <div class="sub">Guía práctica para aprender de verdad, preparar tus exámenes y hacer mejores trabajos con la inteligencia artificial</div>
  <div class="globo">Explícamelo, pero<br>no me des la respuesta.</div>
  <div class="autor">{AUTOR}</div>
</div>'''

CSS = f'''{fuentes}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{ --fondo: #1c2040; --fondo2: #2c2f6e; --amarillo: #ffc531; --verde: #2fc46f; --rojo: #f0505a; --celeste: #9cc0ff; }}
html, body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.frente {{ position: relative; overflow: hidden; color: #fff;
  background: radial-gradient(circle at 85% 18%, rgba(255,197,49,.16), transparent 38%), radial-gradient(circle at 10% 95%, rgba(47,196,111,.14), transparent 40%),
              linear-gradient(160deg, var(--fondo2), var(--fondo) 62%); }}
.frente::before {{ content: ''; position: absolute; inset: 0; opacity: .13;
  background-image: radial-gradient(#fff 1px, transparent 1.2px); background-size: 0.22in 0.22in; }}
.etiqueta {{ position: absolute; left: 0.6in; top: 0.75in; font: 800 9.5pt 'Nunito Sans'; letter-spacing: 3px; text-transform: uppercase; color: var(--celeste); }}
.bloque {{ position: absolute; left: 0.6in; right: 0.55in; top: 1.25in; display: flex; justify-content: space-between; align-items: flex-start; }}
.titulo {{ font: 800 58pt/0.98 'Nunito Sans'; letter-spacing: -1.5px; }}
.titulo span {{ color: var(--amarillo); }}
.semaforo {{ width: 0.95in; padding: 0.14in 0; background: #0f1230; border-radius: 0.5in; display: flex; flex-direction: column; align-items: center; gap: 0.13in;
  box-shadow: 0 0 0 3px rgba(255,255,255,.12); margin-top: 0.12in; }}
.semaforo i {{ display: block; width: 0.62in; height: 0.62in; border-radius: 50%; }}
.semaforo .v {{ background: var(--verde); box-shadow: 0 0 22px rgba(47,196,111,.9); }}
.semaforo .a {{ background: var(--amarillo); box-shadow: 0 0 22px rgba(255,197,49,.85); }}
.semaforo .r {{ background: var(--rojo); box-shadow: 0 0 22px rgba(240,80,90,.85); }}
.sub {{ position: absolute; left: 0.6in; right: 0.7in; top: 5.45in; font: italic 13.5pt/1.35 'Source Serif 4'; color: rgba(255,255,255,.86); }}
.globo {{ position: absolute; left: 0.6in; top: 6.75in; background: #fff; color: var(--fondo); border-radius: 0.16in; padding: 0.14in 0.22in;
  font: 400 11.5pt/1.4 'Source Code Pro'; box-shadow: 0 6px 18px rgba(0,0,0,.3); }}
.globo::after {{ content: ''; position: absolute; left: 0.3in; bottom: -0.13in; border: 0.08in solid transparent; border-top: 0.13in solid #fff; border-bottom: 0; }}
.autor {{ position: absolute; left: 0.6in; bottom: 0.65in; font: 700 13pt 'Nunito Sans'; letter-spacing: 1px; }}
'''

def pagina(cuerpo, css, ancho, alto):
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>@page {{ size: {ancho}in {alto}in; margin: 0; }} {css}</style></head><body>{cuerpo}</body></html>'

# ---- Tapa blanda completa ----
contra = '''
<div class="contra">
  <p class="gancho">¿Usas la IA para tus tareas y aun así llegas al examen sin saber nada?</p>
  <p>No es culpa tuya: casi nadie te enseñó a usarla para aprender.</p>
  <p>Este libro te muestra cómo convertir cualquier asistente de inteligencia artificial en un profesor particular que te explica, te pone a prueba y te corrige, <b>sin hacer la tarea por ti</b>.</p>
  <p class="aprender">Vas a aprender a:</p>
  <ul>
    <li>Pedir explicaciones a tu nivel hasta entender de verdad.</li>
    <li>Practicar para tus exámenes con preguntas que te hace la IA.</li>
    <li>Resolver dudas de matemática y ciencias sin que te resuelva el ejercicio.</li>
    <li>Detectar cuándo la IA inventa datos y fuentes.</li>
    <li>Hacer trabajos y exposiciones que sean tuyos de verdad.</li>
  </ul>
  <p>Incluye el <b>Semáforo del uso honesto</b>, ejercicios en cada capítulo, un banco de pedidos listos para usar y un capítulo para madres, padres y docentes.</p>
  <p class="cierre">Para estudiantes que quieren aprender más,<br>no copiar mejor.</p>
</div>'''
css_tapa = CSS + f'''
body {{ width: {total_w}in; height: {total_h}in; display: flex; background: var(--fondo); }}
.contra {{ width: {SANGRADO + ANCHO}in; height: {total_h}in; position: relative; color: #fff; padding: {SANGRADO + 0.6}in 0.6in 0 {SANGRADO + 0.6}in;
  background: linear-gradient(200deg, var(--fondo2), var(--fondo) 55%); font: 12.6pt/1.5 'Source Serif 4'; }}
.contra p {{ margin-bottom: 0.13in; }}
.contra .gancho {{ font: 800 20pt/1.2 'Nunito Sans'; color: var(--amarillo); margin-bottom: 0.2in; }}
.contra .aprender {{ font: 800 10pt 'Nunito Sans'; letter-spacing: 2px; text-transform: uppercase; color: var(--celeste); margin-top: 0.2in; }}
.contra ul {{ list-style: none; margin: 0 0 0.18in; }}
.contra li {{ padding-left: 0.24in; position: relative; margin-bottom: 0.06in; }}
.contra li::before {{ content: ''; position: absolute; left: 0; top: 0.07in; width: 0.1in; height: 0.1in; border-radius: 50%; background: var(--verde); }}
.contra .cierre {{ font: italic 15pt/1.35 'Source Serif 4'; color: var(--amarillo); margin-top: 0.22in; }}
.lomo {{ width: {grosor}in; height: {total_h}in; background: #12152f; display: flex; align-items: center; justify-content: center; }}
.lomo div {{ transform: rotate(90deg); white-space: nowrap; font: 800 {min(9, grosor * 72 * 0.55):.1f}pt 'Nunito Sans'; letter-spacing: 1.5px; color: #fff; }}
.lomo span {{ color: var(--amarillo); }}
.frente {{ width: {SANGRADO + ANCHO}in; height: {total_h}in; padding-top: {SANGRADO}in; }}
.frente > * {{ margin-top: {SANGRADO}in; }}
'''
lomo = f'<div class="lomo"><div>ESTUDIAR CON IA <span>SIN HACER TRAMPA</span> · {AUTOR.upper()}</div></div>'
html_tapa = os.path.join(FINAL, 'portada_tapa.html')
open(html_tapa, 'w', encoding='utf-8').write(pagina(contra + lomo + FRENTE, css_tapa, total_w, total_h))

# ---- Ebook: 1600 × 2560 píxeles ----
css_ebook = CSS + '''
body { width: 6in; height: 9.6in; }
.frente { width: 6in; height: 9.6in; }
.frente .sub { top: 5.75in; } .frente .globo { top: 7.05in; } .frente .autor { bottom: 0.7in; }
'''
html_ebook = os.path.join(FINAL, 'portada_ebook.html')
open(html_ebook, 'w', encoding='utf-8').write(pagina(FRENTE, css_ebook, 6, 9.6))

js = f'''
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  let p = await b.newPage();
  await p.goto('file://{html_tapa}'); await p.evaluate(() => document.fonts.ready);
  await p.pdf({{ path: '{FINAL}/Portada_TapaBlanda_KDP.pdf', preferCSSPageSize: true, printBackground: true }});
  await p.close();
  p = await b.newPage({{ viewport: {{ width: 600, height: 960 }}, deviceScaleFactor: 2560 / 960 }});
  await p.goto('file://{html_ebook}'); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({{ path: '{FINAL}/Portada_Ebook_1600x2560.png' }});
  await b.close();
}})();'''
open(os.path.join(AQUI, '_portada.js'), 'w').write(js)
subprocess.run(['node', os.path.join(AQUI, '_portada.js')], check=True)
os.remove(os.path.join(AQUI, '_portada.js'))
subprocess.run(['python3', '-c', f"from PIL import Image; im=Image.open('{FINAL}/Portada_Ebook_1600x2560.png').convert('RGB'); print('ebook', im.size); im.save('{FINAL}/Portada_Ebook_1600x2560.jpg', quality=92)"], check=True)
os.remove(os.path.join(FINAL, 'Portada_Ebook_1600x2560.png'))
for h in (html_tapa, html_ebook): os.remove(h)
print(f'tapa: {total_w:.4f} × {total_h:.4f} in · lomo {grosor:.4f} in ({paginas} páginas, papel {papel})')
