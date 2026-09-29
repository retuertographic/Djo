# Kairo Pagos — Terminales de pago para negocios

Sitio web estático de un distribuidor de datáfonos y soluciones de cobro: Kairo Go (datáfono rápido con 4G), Kairo Pocket (pedido y cobro en mesa), Kairo Duo (TPV + datáfono preparado para VeriFactu), reservas y colas virtuales, enlaces de pago, integración con TPV y app de gestión. Misma estructura y estilo que el sitio de Retuerto y Asociados, con paleta, tipografía, logotipo e ilustraciones propios.

- `*.html` — páginas generadas: inicio, datáfonos, soluciones, sectores, tarifas, cómo funciona, preguntas frecuentes, contacto, legales, mapa web y 404.
- `assets/` — `styles.css`, `site.js` (menú, «volver arriba», calculadora de liquidación y formulario por correo) y `favicon.svg`.
- `tools/build.py` — genera todas las páginas. **Los datos del distribuidor (teléfono, WhatsApp, correo, dirección, razón social, CIF) están en el bloque `CONFIG` y son provisionales**: cámbialos y ejecuta `python3 tools/build.py`.
- `tools/base.css` — hoja de estilo de partida; el script le aplica la paleta propia.

El sitio no nombra al proveedor del servicio de pago: el pie y el aviso legal indican que el servicio lo presta la entidad de pago autorizada que figure en el contrato de cada cliente.

Para publicarlo con GitHub Pages: Settings → Pages → Deploy from a branch.

Las condiciones comerciales que aparecen en tarifas y preguntas frecuentes (mínimo mensual, contrato de 12 meses, reembolso de penalización, abono al día hábil siguiente, entrega en 24-48 h) son las publicadas por el proveedor del servicio de pago en septiembre de 2026. Revísalas si cambian.
