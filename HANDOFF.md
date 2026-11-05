# PremiacionesBA — Contexto para continuar en Claude Code

Catálogo web estático de trofeos, copas y medallas (Buenos Aires, desde 1999). Cada producto lleva un botón de consulta por WhatsApp con mensaje pre-cargado.

## Hosting y deploy

- Sitio: https://premiacionesba.pages.dev (Cloudflare Pages, dominio gratuito `*.pages.dev`)
- Repo GitHub: `premiacionesba/premiacionesba`, rama `main`
- Cada push a `main` redeploya solo. No hay build: son archivos estáticos.
- Para ver el proyecto en Cloudflare: dash.cloudflare.com → Workers & Pages → premiacionesba

## Estructura del repo

```
/
├── index.html        # Sitio completo (rediseño nov-2026): grilla + vitrina en la misma página
├── index2.html       # Solo redirige a index.html?vista=vitrina (links viejos)
├── productos.js      # ÚNICO lugar donde se editan productos, categorías y número de WhatsApp
├── icono.png / wordmark.png
├── herramientas/miniaturas.py   # genera fotos/mini/*.webp (python herramientas/miniaturas.py)
└── fotos/
    ├── art1.jpg ... artN.jpg    # fotos grandes 2000x2000
    └── mini/art1.webp ...       # miniaturas 720px para la grilla (~25 KB c/u)
```

CSS y JS inline en index.html; datos en productos.js. Sin framework, solo Google Fonts.
Si se sube una foto nueva sin miniatura, la web usa la foto grande automáticamente.

## Datos de contacto y marca

- WhatsApp: `5491131502179` (constante `WA` en el JS)
- Mensaje pre-cargado: "Hola PremiacionesBA! 👋 Quisiera consultar el precio del *{nombre}* ({ID}) — {dim}. Gracias!"
- Fuentes: Cormorant Garamond (títulos, estilo grabado) + Outfit (cuerpo)
- Paleta (variables CSS en `:root`):
  - `--gold: #b07d2a`
  - `--gold-l: #d4a843`
  - `--gold-pale: #fdf3dc`
  - `--ink: #1a1714`
  - `--bg: #f8f7f4`
  - `--wa: #25d366`
- Copyright del footer: © 2026

## Datos de productos

Array `P` en `productos.js`, 176 artículos (los ids 32–35 y 53–58 se reemplazaron por variantes 33a–d, 34a–b, 35a–b; por eso no son 178). Formato:

```js
{id:"art36", cat:"trofeos", n:"Nombre", d:"Descripción", dim:"17/21/24 cm", b:"Badge opcional", img:"fotos/art36.jpg"}
```

- Categorías (`cat`): `trofeos`, `copas`, `futbol`, `mega`. Se mapean a nombres visibles en el objeto `CATS`.
- Si `img` falta o la foto no existe, se muestra el placeholder "Próximamente".
- Orden por tamaño: `parseDim()` toma el primer número del string `dim`.

## Funcionalidades de index.html

- Hero con icono + wordmark apilados (flex columna)
- Búsqueda por nombre, ID o descripción
- Filtros por categoría (scroll horizontal en mobile)
- Ordenar por: defecto, nombre A–Z / Z–A, tamaño menor / mayor
- Toggle grilla / lista (oculto en mobile ≤500px)
- Contador de resultados ("178 artículos" o "12 de 178")
- Modal de producto con layout vertical u horizontal según proporción de la foto (`layout-v` / `layout-h`)
- Flechas prev/next dentro del modal y navegación con teclado ← → (se agregó en el modal del index; la idea original era solo para el slideshow, decidir si se deja)
- Menú hamburguesa en mobile (≤860px) con Catálogo, Slideshow, Nosotros, Contacto y WhatsApp
- Sección Nosotros, Contacto, footer con logo invertido a blanco
- Botón flotante de WhatsApp

## Funcionalidades de index2.html (slideshow)

- Un producto por vez: imagen a la izquierda, info a la derecha
- Filtros y búsqueda
- Flechas: en desktop, 2 externas a los costados del slideshow. En mobile (≤768px), las externas se ocultan y se usan 2 superpuestas sobre la imagen (`.img-nav`). Esto evita el bug de las 4 flechas.
- Dots, contador "Artículo X de Y", navegación con teclado ← →
- Menú hamburguesa en mobile con "Catálogo grilla" (vuelve a `index.html`) y "Slideshow"
- Los dos modos se enlazan entre sí desde el nav

## Flujo de trabajo con las fotos

1. Fotos originales: PNG sin fondo (o con fondo negro sólido, revisar caso por caso)
2. Se editan una por una en PhotoRoom: fondo de mármol, reflejo espejado, resolución 2000x2000. No tiene plan pago ni batch.
3. Se suben a `fotos/` en GitHub por la web (no hay git local instalado, usa solo la interfaz web)
4. El nombre del archivo debe coincidir con el `id`: `art36` → `fotos/art36.jpg`

Estado: ~95% subidas. Del art162 en adelante faltan, la hermana de Juan las está consiguiendo. Mientras tanto muestran "Próximamente".

Se probó automatizar con Python (Pillow) pero el resultado no igualó a PhotoRoom y se descartó.

## Pendientes y problemas conocidos

- [ ] **Verificar el conteo de productos en index2.html.** Al copiar el array desde `index.html` un `grep` dio 175 líneas en vez de 178, y el slideshow muestra "X / 175". Comparar ambos arrays, probablemente faltan 3 artículos.
- [ ] **Datos duplicados.** El array `P` está copiado en `index.html` e `index2.html`. Conviene extraerlo a `productos.js` compartido para no tener que editar dos veces.
- [ ] Borrar del repo `catalogo-d-slideshow.html` (reemplazado por `index2.html`) y los PNG subidos por error en `fotos/` (unos 10, ej. `art36.png`, `art38.png`). La web de GitHub no permite borrado múltiple.
- [ ] Wordmark del header se ve chico: subir de `32px` a ~`44px` en el `<img src="wordmark.png">` del header.
- [ ] Revisar `logo.png` y borrarlo si no se usa.
- [ ] Artículo 174: `n` y `d` estaban invertidos y se corrigieron. Revisar si hay más casos similares.
- [ ] Probar en mobile real: modal del index, hamburguesa en ambas páginas, flechas del slideshow, categoría que se cortaba bajo la imagen (ya corregido con más padding).

## Ideas de mejora (propuestas, no implementadas)

- Precio o rango "desde $X" (hoy solo se consulta por WhatsApp)
- Favicon (usar `icono.png`), meta tags SEO y Open Graph con imagen de la copa
- Lazy loading con `loading="lazy"` ya está en las imágenes. Evaluar convertir fotos a WebP.
- Dirección o zona de envío en Contacto para dar confianza

## Alternativas de diseño descartadas

Se generaron 4 variantes de catálogo. Se eligió la **D (slideshow)** y ahora es `index2.html`. Las otras no están en el repo:

- A: lookbook / masonry con overlay en hover
- B: tabla con fichas técnicas
- C: masonry dark luxury (negro + dorado)

## Convenciones al editar

- Idioma de la interfaz y comentarios: español rioplatense
- Mantener todo en un solo archivo por página (CSS y JS inline), salvo que se decida extraer `productos.js`
- Los PNG de logo los maneja Juan. Claude solo ajusta tamaños y posición en el código.
- Responder breve y paso a paso
