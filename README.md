# Kairo Pagos — Terminales de pago para negocios

Sitio web estático de un distribuidor de soluciones de cobro con tarjeta (terminales, cobro con el móvil, pagos online, pago en mesa y reservas). Misma estructura y estilo que el sitio de Retuerto y Asociados, con paleta, tipografía, logotipo e ilustraciones propios.

- `*.html` — páginas generadas: inicio, terminales, soluciones, sectores, tarifas, cómo funciona, preguntas frecuentes, contacto, legales, mapa web y 404.
- `assets/` — `styles.css`, `site.js` (menú, «volver arriba», calculadora de liquidación y formulario por correo) y `favicon.svg`.
- `tools/build.py` — genera todas las páginas. **Los datos del distribuidor (teléfono, WhatsApp, correo, dirección, razón social, CIF) están en el bloque `CONFIG` y son provisionales**: cámbialos y ejecuta `python3 tools/build.py`.
- `tools/base.css` — hoja de estilo de partida; el script le aplica la paleta propia.

El sitio no nombra al proveedor del servicio de pago: el pie y el aviso legal indican que el servicio lo presta la entidad de pago autorizada que figure en el contrato de cada cliente.

Para publicarlo con GitHub Pages: Settings → Pages → Deploy from a branch.
