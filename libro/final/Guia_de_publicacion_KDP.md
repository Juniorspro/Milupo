# Estudiar con IA sin hacer trampa: guía de publicación

Este documento reúne las etapas 5, 6 y 7: el diseño editorial, la preparación para Amazon KDP y el control de calidad. **El libro todavía no está listo para publicar:** antes hay que completar los datos marcados entre corchetes y hacer una lectura humana completa (ver la lista de comprobación del punto 3.9).

---

## 1. Archivos finales

| Archivo | Para qué sirve |
|---|---|
| `Interior_EstudiarConIA_6x9_ByN.pdf` | Interior para la **tapa blanda en blanco y negro** (122 páginas, 6 × 9 pulgadas). Es el que se sube a KDP. |
| `Interior_EstudiarConIA_6x9.pdf` | Mismo interior a color: para lectura, para un PDF de regalo o para una edición con interior a color. |
| `Portada_TapaBlanda_KDP.pdf` | Portada completa de la tapa blanda: contratapa, lomo y tapa, con sangrado (12,525 × 9,25 pulgadas). |
| `EstudiarConIA_ebook.epub` | Libro electrónico para Kindle (EPUB 3, con índice navegable y portada). |
| `Portada_Ebook_1600x2560.jpg` | Portada del ebook (1600 × 2560 píxeles). |

Para regenerar todo después de cambiar el texto (desde `libro/herramientas`):

```
AUTOR="Nombre Apellido" BYN=1 python3 construir_libro.py ../final/Interior_EstudiarConIA_6x9_ByN.pdf
AUTOR="Nombre Apellido" python3 construir_libro.py ../final/Interior_EstudiarConIA_6x9.pdf
AUTOR="Nombre Apellido" python3 portada.py <número de páginas del interior> blanco
AUTOR="Nombre Apellido" python3 ebook.py
```

**Importante:** si cambia la cantidad de páginas del interior, hay que regenerar la portada con el número nuevo, porque el ancho del lomo depende de él.

---

## 2. Diseño editorial (etapa 5)

### 2.1 Portada
- **Concepto:** un semáforo encendido (verde, amarillo y rojo) junto al título. Resume la idea central del libro, el Semáforo del uso honesto, y se reconoce incluso en miniatura en la tienda.
- **Colores:** fondo azul noche con degradé, título en blanco y "sin hacer trampa" en amarillo.
- **Tipografías:** Nunito Sans ExtraBold para el título; Source Serif 4 itálica para el subtítulo.
- **Elemento de gancho:** un globo de chat con la frase *«Explícamelo, pero no me des la respuesta»*, que resume el método.
- **Reglas de KDP que respeta:** el título y el subtítulo de la tapa coinciden exactamente con los de la ficha, y todo el texto queda dentro de la zona segura.
- **Hecha sin imágenes de stock ni generadas por IA:** se dibujó con código, así que no hay derechos de terceros que revisar.

### 2.2 Contratapa (texto incluido en la portada)
> **¿Usas la IA para tus tareas y aun así llegas al examen sin saber nada?**
> No es culpa tuya: casi nadie te enseñó a usarla para aprender.
> Este libro te muestra cómo convertir cualquier asistente de inteligencia artificial en un profesor particular que te explica, te pone a prueba y te corrige, **sin hacer la tarea por ti**.
> Vas a aprender a: pedir explicaciones a tu nivel hasta entender de verdad · practicar para tus exámenes con preguntas que te hace la IA · resolver dudas de matemática y ciencias sin que te resuelva el ejercicio · detectar cuándo la IA inventa datos y fuentes · hacer trabajos y exposiciones que sean tuyos de verdad.
> Incluye el **Semáforo del uso honesto**, ejercicios en cada capítulo, un banco de pedidos listos para usar y un capítulo para madres, padres y docentes.
> *Para estudiantes que quieren aprender más, no copiar mejor.*

La esquina inferior derecha de la contratapa queda libre para el código de barras que agrega KDP.

### 2.3 Páginas iniciales (incluidas en el interior)
- **Página de título:** título, subtítulo y autor.
- **Página de derechos y créditos:** copyright, permiso para fotocopiar los anexos B, C y D, aviso de que los personajes son ficticios, aviso de marcas y vigencia de la información. **Falta completar:** nombre del autor, fecha de la primera edición e ISBN.
- **Índice:** de una sola página, con los números de página reales.

### 2.4 Diagramación interior
- **Formato:** tapa blanda de 6 × 9 pulgadas, con márgenes en espejo (0,72 pulgadas en el lomo, 0,55 por fuera). Son más amplios que el mínimo de KDP para este número de páginas.
- **Texto:** Source Serif 4 a 10,3 puntos con interlineado de 1,43. Títulos en Nunito Sans y pedidos de ejemplo en Source Code Pro. Las tres fuentes tienen licencia SIL Open Font, que permite el uso comercial, y van incrustadas en el PDF.
- **Recuadros:** cada uno tiene su estilo, para reconocerlos de un vistazo: **Pídeselo así**, **Ojo con esto**, **Tu turno** y **En pocas palabras**. En la versión en blanco y negro se diferencian por el tipo de borde.
- **Capítulos:** cada capítulo, parte y anexo empieza en página impar, como en los libros impresos profesionales. Por eso hay páginas en blanco intencionales.
- **Números de página:** abajo y al centro; no aparecen en la portadilla, en la página de derechos ni en las páginas de parte o en blanco.
- **Plantillas para completar a mano:** el acuerdo de uso, el plan de siete días y la lista de verificación ocupan cada uno una página completa, con renglones para escribir.

### 2.5 Ilustraciones
El género no las necesita: la información se apoya en tablas, diálogos y recuadros. El único elemento gráfico es el semáforo, presente en la portada, en la portadilla y en el anexo B. Si más adelante se quiere sumar algo, la mejor inversión serían íconos simples para cada tipo de recuadro.

---

## 3. Preparación para Amazon KDP (etapa 6)

### 3.1 Datos básicos
- **Idioma:** español.
- **Título:** Estudiar con IA sin hacer trampa
- **Subtítulo:** Guía práctica para aprender de verdad, preparar tus exámenes y hacer mejores trabajos con la inteligencia artificial
- **Autor:** [completar]
- **Edad de lectura sugerida:** de 13 a 18 años. El capítulo 13 está dirigido a adultos, pero el lector principal es adolescente.

### 3.2 Descripción comercial
KDP acepta algunas etiquetas HTML en la descripción. Esta versión ya está lista para pegar:

```html
<b>¿Usas la inteligencia artificial para tus tareas y aun así llegas al examen sin saber nada?</b><br>
No es culpa tuya: casi nadie te enseñó a usarla para aprender.<br><br>
<i>Estudiar con IA sin hacer trampa</i> es una guía práctica para estudiantes de secundaria y bachillerato que quieren sacarle provecho a la IA de forma honesta. Con situaciones reales de clase, vas a aprender a convertir cualquier asistente de IA en un profesor particular que te explica, te pone a prueba y te corrige, sin hacer la tarea por ti.<br><br>
<b>Con este libro vas a aprender a:</b>
<ul>
<li>Pedir explicaciones a tu nivel hasta entender de verdad cualquier tema.</li>
<li>Practicar para tus exámenes con preguntas que te hace la IA y aprender de tus errores.</li>
<li>Resolver dudas de matemática y ciencias sin que te resuelva el ejercicio.</li>
<li>Leer mejor textos difíciles y practicar idiomas conversando.</li>
<li>Detectar cuándo la IA inventa datos, citas y fuentes, y verificar la información.</li>
<li>Hacer trabajos escritos y exposiciones que sean tuyos de verdad.</li>
<li>Llegar al examen preparado con un plan de siete días.</li>
</ul>
<b>Incluye</b> el Semáforo del uso honesto, para saber qué está permitido, qué conviene consultar y qué cruza la línea; ejercicios en cada capítulo; un banco de pedidos listos para usar; plantillas imprimibles, y un capítulo para madres, padres y docentes.<br><br>
Sirve con cualquier asistente de IA, porque no depende de botones ni menús: depende de cómo piensas y de qué pides.<br><br>
<b>Para estudiantes que quieren aprender más, no copiar mejor.</b>
```

### 3.3 Siete palabras clave
Son frases que un comprador escribiría en el buscador y que no repiten el título. Evité marcas de terceros, como nombres de asistentes de IA, porque pueden traer problemas con las pautas de KDP.

1. técnicas de estudio para adolescentes
2. cómo usar la inteligencia artificial para estudiar
3. inteligencia artificial en la educación
4. preparar exámenes secundaria y bachillerato
5. hábitos de estudio y organización escolar
6. guía para padres y docentes sobre IA
7. evitar el plagio en trabajos escolares

### 3.4 Categorías recomendadas
KDP permite elegir hasta tres categorías desde su buscador, y los nombres cambian un poco según la tienda (Amazon.com, Amazon.es, Amazon.com.mx). Conviene buscar estas tres ramas y elegir la más específica que aparezca:

1. **Juvenil > No ficción > Estudio, escuela o técnicas de aprendizaje.** Es la más cercana al lector principal.
2. **Educación > Tecnología educativa**, o Educación > Métodos de estudio.
3. **Informática > Inteligencia artificial**, preferiblemente una subcategoría de introducción o uso cotidiano.

### 3.5 Precio inicial propuesto
No tengo datos de ventas de libros comparables, así que esta es una propuesta de partida, no un cálculo de rentabilidad. Antes de fijarla, conviene mirar el precio de los 5 a 10 libros más parecidos en las tiendas donde vayas a vender.

| Formato | Precio de partida | Por qué |
|---|---|---|
| Ebook | US$ 4,99 o su equivalente local | Entra en la franja de regalías del 70 % de KDP (entre US$ 2,99 y 9,99) y es accesible para estudiantes y familias. Opcional: US$ 2,99 durante las dos primeras semanas como precio de lanzamiento. |
| Tapa blanda | US$ 12,99 o su equivalente local | Precio razonable para una guía práctica de 122 páginas. Verifica en la calculadora de KDP el costo de impresión y la regalía que queda; KDP los muestra al cargar el interior. |

### 3.6 Formatos
- **Tapa blanda:** interior en blanco y negro, papel blanco, 6 × 9 pulgadas, acabado mate o brillante (la portada oscura luce bien en ambos). Usa `Interior_..._ByN.pdf`.
- **Ebook Kindle:** subir el EPUB. Antes, abrirlo en **Kindle Previewer** (gratis, de Amazon) para revisar cómo se ve en teléfono, tableta y Kindle.
- **Opcional:** KDP Select (Kindle Unlimited) para el ebook. Exige exclusividad digital con Amazon por 90 días renovables.

### 3.7 ISBN
- **Tapa blanda:** KDP ofrece un ISBN gratuito (figura como "Independently published"). Si prefieres que figure una editorial propia, puedes tramitar un ISBN en la agencia de tu país.
- **Ebook:** no necesita ISBN en KDP.
- **Página de derechos:** después de obtener el ISBN, agrégalo ahí y regenera el interior.

### 3.8 Declaración de contenido generado con IA
Al publicar, KDP pregunta si el libro tiene contenido generado con inteligencia artificial (texto, imágenes o traducciones). KDP distingue el contenido **generado** por IA, que se declara, del contenido creado por una persona y solo **asistido** por IA, que no hace falta declarar. Como este texto fue redactado con IA, lo honesto es **declarar el texto como generado por IA**, aunque lo revises y lo edites. La portada se diseñó con código, sin imágenes generadas: decláralo según cómo lo interpretes, y ante la duda, declara.

Para un libro que enseña a usar la IA con honestidad, una nota breve en la página de derechos sobre cómo se hizo el libro es coherente y puede ser un punto a favor. El lugar ya está reservado en el interior.

### 3.9 Lista de comprobación antes de publicar
- [ ] Leí el manuscrito completo y cambié lo que no suena a mí.
- [ ] Una persona más leyó el libro (ideal: un docente y un estudiante de 14 a 18 años) y tuve en cuenta sus comentarios.
- [ ] Completé el nombre del autor, la fecha de la primera edición y el ISBN, y regeneré los archivos.
- [ ] El título y el subtítulo de la ficha coinciden exactamente con los de la portada.
- [ ] Revisé el PDF del interior página por página en el previsualizador de KDP, sin advertencias de márgenes ni de fuentes.
- [ ] Regeneré la portada con el número final de páginas y KDP la aceptó sin advertencias.
- [ ] Revisé el EPUB en Kindle Previewer en tres dispositivos.
- [ ] Pegué la descripción y comprobé cómo se ve en la vista previa.
- [ ] Cargué las siete palabras clave y elegí tres categorías.
- [ ] Respondí la pregunta sobre contenido generado con IA.
- [ ] Fijé los precios y revisé la regalía en cada tienda.
- [ ] Pedí una copia de prueba impresa y la revisé en papel antes de habilitar la venta.

### 3.10 Ideas de lanzamiento (marketing editorial)
- **Contenido gratuito como anzuelo:** el Semáforo del uso honesto y el acuerdo de uso en PDF, para docentes y familias, con un enlace al libro.
- **Videos cortos (TikTok, Reels, Shorts):** cada técnica del libro es un video. Por ejemplo, "la frase que hace que la IA no te haga la tarea", "3 preguntas trampa para tu IA" o "cómo la IA inventó un libro que no existe". Es contenido que ya sabemos producir.
- **Docentes:** ofrecer ejemplares para revisión a profesores y escuelas. El capítulo 13 y los anexos están pensados para usarse en clase.
- **Reseñas:** pedir opiniones honestas a lectores reales. Amazon prohíbe ofrecer pagos, regalos o descuentos a cambio de reseñas.
- **Ficha en Amazon:** crear el perfil de autor en Author Central y, más adelante, contenido A+ con el semáforo y un ejemplo de pedido.
- **Anuncios:** si se usan anuncios de Amazon, empezar con un presupuesto chico y las palabras clave del punto 3.3, y ajustar según resultados reales.

---

## 4. Control de calidad (etapa 7)

### 4.1 Qué se revisó y qué se corrigió

| Aspecto | Revisión | Resultado |
|---|---|---|
| **Coherencia** | Todas las referencias entre capítulos y anexos (21 en total); hilo de los personajes de principio a fin; índice frente a títulos reales. | Las 21 referencias apuntan al lugar correcto. Los arcos de Martina, Tomás y Sofía se cierran en la conclusión. |
| **Ortografía** | Diccionario Hunspell de español sobre las aproximadamente 25.000 palabras. | Un error real: "Propónme" pasó a "Proponme". El resto eran nombres propios, formas verbales con pronombre y palabras en inglés de un ejemplo. |
| **Español neutro** | Búsqueda de regionalismos que cambian de sentido según el país. | Se reemplazaron unos 20 usos: *prolijo* (en España significa "largo y pesado"), *consigna*, *heladera*, *computadora*, *acá*, *liviano*, *de a una*, *saltear*, *darla vuelta*, *se trabó*, entre otros. |
| **Repeticiones** | Conteo de muletillas e intensificadores. | Se quitaron 6 de "justamente" y "exactamente"; no aparecen frases hechas típicas de textos automáticos. |
| **Datos** | Sin estadísticas, citas ni fuentes inventadas. Cada dato concreto se comprobó. | Toma de la Bastilla (14 de julio de 1789); Estados Generales sin reunirse desde hacía más de siglo y medio; el oxígeno de la fotosíntesis proviene del agua; vellosidades del intestino delgado; amos de Lázaro y episodio de las uvas; las cuentas de matemática y física, recalculadas una por una. |
| **Afirmaciones generales** | Formuladas sin cifras y en términos verificables. | Edades mínimas de los servicios, falta de confiabilidad de los detectores de IA, beneficios de practicar recordando y de repasar con días de por medio, y el papel del sueño en la memoria. |
| **Utilidad** | Cada capítulo tiene escena, técnica, pedidos de ejemplo, errores comunes, ejercicio y resumen. | 13 de 13 capítulos completos; 3 ejercicios incluyen soluciones. |
| **Presentación** | Revisión visual de las 122 páginas en color y en blanco y negro. | Se corrigieron el índice que pasaba a una segunda página, formularios que se cortaban, títulos con palabras sueltas y recuadros partidos. |

### 4.2 Pendientes y limitaciones (honestamente)
- **Lectura humana:** el texto no fue leído todavía por un docente ni por un estudiante de la edad del lector. Es la revisión más valiosa que falta.
- **Validación del EPUB:** se comprobó que el XML es válido, pero no pude correr EPUBCheck, el validador oficial, porque el entorno no permitió ejecutarlo. Kindle Previewer lo reemplaza.
- **Vigencia:** las referencias a herramientas de IA son generales a propósito, pero conviene releer los capítulos 1 y 2 antes de cada edición nueva.
- **Datos por completar:** nombre del autor, fecha e ISBN.
- **Extensión:** 122 páginas, 15 de ellas en blanco por diseño. Si hace falta acortar, se puede permitir que los capítulos empiecen en página par y quedarían unas 108.
