# Mundo Gatuno 🐱

Un juego con 10 niveles para acompañar a Mishi, el gatito protagonista.

## Cómo abrirlo

1. Descarga el archivo `mundo-gatuno.html`.
2. Haz doble clic sobre él. Se abre en tu navegador (Chrome, Edge, Firefox o Safari).

No hace falta instalar nada. Funciona sin internet; con internet solo se ve una letra más linda.

## Dónde cambiar cosas

Todo está en `mundo-gatuno.html`, dividido en secciones numeradas:

- **Estilos (`<style>`)**: colores, tamaños y animaciones. Los colores principales están al principio, en `:root`.
- **Sección 1 · NIVELES**: el nombre, el fondo, el emoji y las instrucciones de cada nivel.
- **Sección 4 · dibujoGato**: cómo se dibuja Mishi. Prueba a cambiar `#ffb26b` por otro color.
- **Sección 5 · Mensajes**: las frases divertidas.
- **Sección 9 · Los desafíos**: cada nivel tiene su función, por ejemplo `nivelJardin`. Los mapas
  (`MAPA_JARDIN`, `MAPA_CIUDAD`, `MAPA_ESPACIO`) se dibujan con letras: cambia las letras y cambia el nivel.
  Las preguntas del castillo están en `PREGUNTAS`.

Para empezar de cero (borrar estrellas), abre la consola del navegador (F12) y escribe:
`localStorage.removeItem('mundoGatuno')`, y después recarga la página.
