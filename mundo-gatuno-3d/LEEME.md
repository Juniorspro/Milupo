# Mundo Gatuno 3D · El valle secreto 🐱

Un juego en 3D: tu gatito camina, corre y salta por un valle enorme lleno de árboles, flores y
mariposas, y busca **8 lugares secretos**. En cada uno vive un gatito amigo.

## Cómo abrirlo

1. Descarga `mundo-gatuno-3d.html`.
2. Haz doble clic. Se abre en el navegador (Chrome, Edge, Firefox o Safari).

Necesita **internet**, porque la librería 3D (three.js) se descarga al abrirlo.

## Controles

| Acción | Computadora | Celular |
|---|---|---|
| Caminar | WASD o flechas | Palanca (abajo a la izquierda) |
| Correr | Shift | Botón 🏃 |
| Saltar | Espacio | Botón ⤒ |
| Maullar | M | Botón 🐾 |
| Mirar alrededor | Arrastrar el mouse (rueda = acercar) | Deslizar el dedo |
| Cuaderno / Pista | C / P | Botones de arriba |

## Dónde cambiar cosas

Todo está en `mundo-gatuno-3d.html`, en secciones numeradas:

- **1 · CONFIG**: velocidad, fuerza del salto, gravedad y rebote de los hongos.
- **2 · LUGARES**: nombre, posición, pista y amigo de cada lugar secreto.
- **3 · PELAJES**: los colores de los gatitos que se pueden elegir.
- **8 · Plantas**: cuántos árboles, flores y piedras hay (por ejemplo, `arboles.length < 280`).
- **9 · crearGato**: cómo se arma un gatito con esferas y conos.
- **10 · CONSTRUCTORES**: cómo se construye cada lugar secreto.
