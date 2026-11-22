# FLUXO — paquete listo para publicar

Este paquete contiene la versión web de FLUXO con `index.html` en la raíz. No requiere compilación.

## Publicación
Sube el **contenido** de este ZIP (no el ZIP como un único archivo) a un repositorio o alojamiento web estático con HTTPS. Deben permanecer juntos `index.html`, `styles.css`, `sw.js`, `manifest.webmanifest`, `icon.svg` y los PNG de iconos.

En GitHub Pages: crea un repositorio `fluxo`, sube estos archivos a la raíz, abre Settings → Pages, elige Deploy from a branch, rama `main`, carpeta `/(root)` y guarda.

## Instalar en iPad
Abre la URL publicada en Safari → Compartir → Añadir a pantalla de inicio. Activa “Abrir como app web” si aparece. Después abre FLUXO desde el icono de la pantalla de inicio.

## Importante
FLUXO es una PWA, no una app nativa de App Store. Los datos se guardan localmente en el navegador/app instalada; no hay sincronización automática entre dispositivos. Exporta copias desde Ajustes.
