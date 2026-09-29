#!/usr/bin/env python3
"""Genera el sitio estático de Kairo Pagos.

Uso:  python3 tools/build.py

Todas las páginas comparten cabecera, pie e iconos definidos aquí. Para
cambiar el nombre comercial, los datos de contacto o el texto legal basta con
editar el bloque CONFIG y volver a ejecutar el script.
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Datos del distribuidor (sustituir por los reales antes de publicar)
# ---------------------------------------------------------------------------
CONFIG = {
    "marca": "Kairo Pagos",
    "marca_corta": "Kairo",
    "lema": "Cobra fácil. Cobra hoy.",
    "telefono": "900 000 000",
    "telefono_intl": "+34900000000",
    "whatsapp": "34600000000",
    "whatsapp_txt": "600 000 000",
    "email": "hola@kairopagos.es",
    "direccion": "Calle Ejemplo, 1 · 38001 Santa Cruz de Tenerife",
    "horario": "L-V 9-18 h",
    "razon_social": "[Razón social del distribuidor]",
    "cif": "[CIF]",
    "url": "https://retuertographic.github.io/Djo/",
    "anio": "2026",
}
C = CONFIG

# ---------------------------------------------------------------------------
# Iconos (trazo de 24 px, mismo estilo que el sitio de referencia)
# ---------------------------------------------------------------------------
P = {
    "tel": '<path d="M6.5 3.5h3l1.5 4-2 1.5a12 12 0 0 0 6 6l1.5-2 4 1.5v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.5 5.7 2 2 0 0 1 6.5 3.5Z"/>',
    "mail": '<path d="M3.5 6h17v12h-17z"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "pin": '<path d="M12 21s6.5-6 6.5-11a6.5 6.5 0 1 0-13 0C5.5 15 12 21 12 21Z"/><circle cx="12" cy="10" r="2.4"/>',
    "reloj": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "abajo": '<path d="m6.5 9.5 5.5 5 5.5-5"/>',
    "arriba": '<path d="M12 19V6"/><path d="m5.5 12.5 6.5-6.5 6.5 6.5"/>',
    "flecha": '<path d="M5 12h13"/><path d="m12.5 5.5 6.5 6.5-6.5 6.5"/>',
    "check": '<path d="m4.5 12.5 4.5 4.5 10.5-10.5"/>',
    "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5M12 7.8v.6"/>',
    "terminal": '<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><rect x="8.5" y="5" width="7" height="5" rx="1"/><path d="M9 13.5h.01M12 13.5h.01M15 13.5h.01M9 16.5h.01M12 16.5h.01M15 16.5h.01"/>',
    "movil": '<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>',
    "nfc": '<path d="M8.5 8.5a5 5 0 0 1 0 7"/><path d="M11.5 6a8.5 8.5 0 0 1 0 12"/><path d="M14.5 3.5a12 12 0 0 1 0 17"/>',
    "tarjeta": '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M3 10h18M7 15h3"/>',
    "rayo": '<path d="M13 2.5 4.5 13.5H12l-1 8 8.5-11H12z"/>',
    "banco": '<path d="M3.5 9.5 12 4l8.5 5.5"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3.5 20.5h17"/>',
    "grafica": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 20v-6M13 20V8M18 20v-9"/>',
    "enlace": '<path d="M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1 1"/><path d="M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1-1"/>',
    "web": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.6 3.5 5.4 3.5 8.5s-1 5.9-3.5 8.5c-2.5-2.6-3.5-5.4-3.5-8.5s1-5.9 3.5-8.5Z"/>',
    "mesa": '<path d="M4 9h16M6 9v10M18 9v10M8 5h8"/>',
    "calendario": '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/>',
    "cubiertos": '<path d="M7 3v8a2 2 0 0 0 2 2v8M5 3v5M9 3v5"/><path d="M17 21V3c-2 1.5-3 4-3 7v3h3"/>',
    "copa": '<path d="M7 3h10l-1 6a4 4 0 0 1-8 0z"/><path d="M12 13v7M8.5 20.5h7"/>',
    "bolsa": '<path d="M3.5 9h17l-1 11.5h-15z"/><path d="M8 9V6a4 4 0 0 1 8 0v3"/>',
    "tijeras": '<circle cx="6.5" cy="17" r="2.5"/><circle cx="17.5" cy="17" r="2.5"/><path d="M8.5 15.5 18 4M15.5 15.5 6 4"/>',
    "maletin": '<rect x="3.5" y="7" width="17" height="12.5" rx="2"/><path d="M9 7V5h6v2M3.5 12.5h17"/>',
    "cama": '<path d="M3 19V6M3 15h18v4M21 15v-3a3 3 0 0 0-3-3h-7v6"/><circle cx="7" cy="11" r="1.8"/>',
    "escudo": '<path d="M12 3.2 19 6v6c0 4.4-3 7.6-7 8.8-4-1.2-7-4.4-7-8.8V6Z"/><path d="m9 12 2 2 4-4"/>',
    "soporte": '<path d="M4.5 13v-1a7.5 7.5 0 0 1 15 0v1"/><rect x="3.5" y="13" width="4" height="6" rx="1.5"/><rect x="16.5" y="13" width="4" height="6" rx="1.5"/><path d="M18.5 19a3 3 0 0 1-3 2.5H13"/>',
    "caja": '<path d="M3.5 7.5 12 3l8.5 4.5v9L12 21l-8.5-4.5z"/><path d="M3.5 7.5 12 12l8.5-4.5M12 12v9"/>',
    "euro": '<path d="M17.5 6.5a6.5 6.5 0 1 0 0 11"/><path d="M4.5 10.5h9M4.5 13.5h9"/>',
    "estrella": '<path d="m12 3.5 2.6 5.5 6 .8-4.4 4.2 1.1 6-5.3-2.9-5.3 2.9 1.1-6L3.4 9.8l6-.8z"/>',
    "wifi": '<path d="M2.5 9a14 14 0 0 1 19 0M5.5 12.5a9.5 9.5 0 0 1 13 0M8.5 16a5 5 0 0 1 7 0"/><path d="M12 19.5h.01"/>',
    "bateria": '<rect x="2.5" y="7" width="17" height="10" rx="2"/><path d="M21.5 10.5v3M6 10.5v3M9.5 10.5v3"/>',
    "impresora": '<path d="M6.5 9V3.5h11V9"/><rect x="3.5" y="9" width="17" height="8" rx="2"/><path d="M6.5 14.5h11v6h-11z"/>',
    "dividir": '<path d="M12 3v18M5 8l-3 4 3 4M19 8l3 4-3 4"/>',
    "propina": '<circle cx="12" cy="12" r="8.5"/><path d="M14.5 9a2.5 2 0 0 0-2.5-1.5c-1.4 0-2.5.8-2.5 2 0 2.8 5 1.5 5 4.3 0 1.2-1.1 2-2.5 2A2.6 2 0 0 1 9.5 15M12 6v1.5M12 16.5V18"/>',
    "usuarios": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 5a3 3 0 0 1 0 6M18 14.5a5.5 5.5 0 0 1 3 5.5"/>',
}
WA_SVG = '<svg viewBox="0 0 448 512" fill="currentColor" aria-hidden="true"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 110.9L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>'


def ico(nombre):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + P[nombre] + '</svg>')


def logo(claro=False):
    """Logotipo en SVG: isotipo (onda de pago sin contacto) + nombre."""
    texto = "#FFFFFF" if claro else "#17152A"
    return (
        '<svg class="logo" viewBox="0 0 190 40" role="img" aria-label="' + C["marca"] + '">'
        '<rect x="0" y="2" width="36" height="36" rx="10" fill="#5B45C7"/>'
        '<path d="M12 12v16M12 20l8-8M12 20l8 8" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M24.5 15a7 7 0 0 1 0 10" stroke="#FF8A5B" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
        '<text x="46" y="27.5" font-family="Space Grotesk, Arial, sans-serif" font-size="22" font-weight="700" fill="' + texto + '">'
        + C["marca_corta"] + '<tspan fill="' + ("#FFB38A" if claro else "#5B45C7") + '" font-weight="500"> pagos</tspan></text>'
        '</svg>'
    )


# ---------------------------------------------------------------------------
# Plantilla común
# ---------------------------------------------------------------------------
NAV = [
    ("index.html", "Inicio"),
    ("terminales.html", "Terminales"),
    ("soluciones.html", "Soluciones"),
    ("sectores.html", "Sectores"),
    ("tarifas.html", "Tarifas"),
    ("como-funciona.html", "Cómo funciona"),
    ("preguntas-frecuentes.html", "Preguntas"),
    ("contacto.html", "Contacto"),
]


def cabecera(activo):
    items = "".join(
        '<li><a href="%s"%s>%s</a></li>' % (h, ' class="active"' if h == activo else "", t)
        for h, t in NAV
    )
    return f'''<div class="topbar"><div class="wrap">
  <div class="tb-items">
    <span>{ico("tel")}<a href="tel:{C["telefono_intl"]}">{C["telefono"]}</a></span>
    <span>{ico("mail")}<a href="mailto:{C["email"]}">{C["email"]}</a></span>
  </div>
  <div class="tb-items">
    <span>{ico("reloj")}{C["horario"]}</span>
    <span>{ico("rayo")}Alta en 24-48 h</span>
  </div>
</div></div>

<header class="site-header"><div class="wrap">
  <a class="brand" href="index.html">{logo()}</a>
  <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="mainNav" aria-label="Abrir menú">{ico("menu")}</button>
  <nav class="main-nav" id="mainNav" aria-label="Navegación principal">
    <ul>
      {items}
      <li class="nav-mas" hidden>
        <button type="button" aria-expanded="false" aria-haspopup="true">Más {ico("abajo")}</button>
        <ul class="nav-drop"></ul>
      </li>
      <li class="cta"><a class="btn btn-primary" href="contacto.html">{ico("terminal")}Pide tu terminal</a></li>
    </ul>
  </nav>
</div></header>
'''


def pie():
    enlaces = lambda lista: "".join(
        f'<li><a href="{h}">{ico(i)}<span>{t}</span></a></li>' for h, i, t in lista
    )
    producto = [
        ("terminales.html", "terminal", "Terminales de pago"),
        ("terminales.html#app", "movil", "Cobro con el móvil"),
        ("soluciones.html#online", "web", "Pagos online y enlaces"),
        ("soluciones.html#mesa", "mesa", "Pago en mesa"),
        ("soluciones.html#reservas", "calendario", "Reservas y lista de espera"),
        ("soluciones.html#informes", "grafica", "App de gestión e informes"),
        ("tarifas.html", "euro", "Tarifas"),
    ]
    info = [
        ("sectores.html", "bolsa", "Sectores"),
        ("como-funciona.html", "rayo", "Cómo funciona"),
        ("preguntas-frecuentes.html", "info", "Preguntas frecuentes"),
        ("contacto.html", "mail", "Contacto"),
        ("aviso-legal.html", "info", "Aviso legal"),
        ("politica-de-privacidad.html", "info", "Política de privacidad"),
        ("cookies.html", "info", "Cookies"),
        ("mapa-web.html", "flecha", "Mapa web"),
    ]
    return f'''<footer class="site"><div class="wrap">
  <div class="foot-grid">
    <div>
      <a class="foot-brand" href="index.html">{logo(claro=True)}</a>
      <p>Distribuidor autorizado de soluciones de cobro con tarjeta para comercios, hostelería y autónomos. Te asesoramos, tramitamos el alta y te acompañamos después.</p>
      <ul class="foot-links">
        <li><a href="contacto.html">{ico("pin")}<span>{C["direccion"]}</span></a></li>
        <li><a href="tel:{C["telefono_intl"]}">{ico("tel")}<span>{C["telefono"]}</span></a></li>
        <li><a href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener">{WA_SVG}<span>WhatsApp {C["whatsapp_txt"]}</span></a></li>
        <li><a href="mailto:{C["email"]}">{ico("mail")}<span>{C["email"]}</span></a></li>
        <li><a href="contacto.html">{ico("reloj")}<span>{C["horario"]}</span></a></li>
      </ul>
    </div>
    <div><h4>Producto</h4><ul class="foot-links">{enlaces(producto)}</ul></div>
    <div><h4>Información</h4><ul class="foot-links">{enlaces(info)}</ul></div>
  </div>
  <div class="foot-bottom">
    <p class="foot-legal-text">Copyright © {C["anio"]} {C["marca"]} · {C["razon_social"]} · {C["cif"]}. {C["marca"]} actúa como distribuidor comercial independiente. Los servicios de pago los presta la entidad de pago autorizada que se indica en el contrato de cada cliente. Las marcas de tarjetas y de monederos móviles pertenecen a sus respectivos titulares.</p>
    <p class="foot-credit">Desarrollado por Retuerto Graphic Design. Ricardo Retuerto Barrera | Spain-Germany | <a href="tel:0034922971723">0034 922 971 723</a> · <a href="tel:00493031878629">0049 30 31878629</a></p>
  </div>
</div></footer>
<button class="arriba" type="button" id="irArriba" hidden aria-label="Volver arriba" title="Volver arriba">{ico("arriba")}</button>
<a class="wa" href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{WA_SVG}</a>
'''


def pagina(archivo, titulo, descripcion, cuerpo, activo=None):
    t = C["marca"] if archivo == "index.html" else f"{titulo} | {C['marca']}"
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{descripcion}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{descripcion}">
<meta property="og:type" content="website">
<link rel="canonical" href="{C["url"]}{"" if archivo == "index.html" else archivo}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=Caveat:wght@600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#3B2A8C">
</head>
<body>
{cabecera(activo or archivo)}
<main>
{cuerpo}
</main>
{pie()}
<script src="assets/site.js"></script>
</body>
</html>
'''
    (RAIZ / archivo).write_text(html, encoding="utf-8")


def cabeza_pagina(miga, titulo, texto):
    return f'''<div class="page-head"><div class="wrap">
  <div class="crumbs"><a href="index.html">Inicio</a><span>/</span>{miga}</div>
  <h1>{titulo}</h1>
  <p>{texto}</p>
</div></div>'''


def tarjeta(icono, titulo, texto, href=None, mas="Saber más"):
    dentro = f'<span class="ico">{ico(icono)}</span><h3>{titulo}</h3><p>{texto}</p>'
    if href:
        return f'<a class="card prod" href="{href}">{dentro}<span class="more">{mas} {ico("flecha")}</span></a>'
    return f'<div class="card">{dentro}</div>'


def checks(items):
    return '<ul class="checks">' + "".join(
        f'<li>{ico("check")}<span><b>{b}</b>{t}</span></li>' for b, t in items
    ) + "</ul>"


def faq(items):
    return '<div class="faq">' + "".join(
        f'<details class="faq-item"><summary>{p}{ico("abajo")}</summary><div class="faq-r"><p>{r}</p></div></details>'
        for p, r in items
    ) + "</div>"


def panel_cta(titulo="¿Empezamos?", texto="Cuéntanos cómo es tu negocio y te preparamos una propuesta con el terminal y la tarifa que mejor encajan. Sin compromiso."):
    return f'''<section class="tight"><div class="wrap"><div class="panel">
  <h2>{titulo}</h2>
  <p>{texto}</p>
  <div class="actions">
    <a class="btn btn-primary" href="contacto.html">{ico("mail")}Solicitar propuesta</a>
    <a class="btn btn-line" href="tel:{C["telefono_intl"]}">{ico("tel")}{C["telefono"]}</a>
    <a class="btn btn-line" href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a>
  </div>
</div></div></section>'''


# Ilustraciones de los terminales (SVG propio, sin imágenes de terceros)
def dibujo_terminal(variante="portatil", importe="24,50"):
    if variante == "movil":
        return f'''<svg class="device" viewBox="0 0 200 320" aria-hidden="true">
  <rect x="30" y="10" width="140" height="300" rx="24" fill="#17152A"/>
  <rect x="40" y="26" width="120" height="268" rx="14" fill="#F6F5FA"/>
  <rect x="80" y="16" width="40" height="5" rx="2.5" fill="#2F2D40"/>
  <text x="100" y="80" text-anchor="middle" font-family="Plus Jakarta Sans, Arial" font-size="12" fill="#62607A">Cobrar</text>
  <text x="100" y="116" text-anchor="middle" font-family="Space Grotesk, Arial" font-size="30" font-weight="700" fill="#17152A">{importe} €</text>
  <circle cx="100" cy="182" r="34" fill="#EEEBFB"/>
  <path d="M92 168a16 16 0 0 1 0 28M100 162a24 24 0 0 1 0 40M108 156a32 32 0 0 1 0 52" stroke="#5B45C7" stroke-width="4" fill="none" stroke-linecap="round"/>
  <text x="100" y="244" text-anchor="middle" font-family="Plus Jakarta Sans, Arial" font-size="11" fill="#62607A">Acerca la tarjeta</text>
  <rect x="58" y="258" width="84" height="22" rx="11" fill="#5B45C7"/>
</svg>'''
    alto = 360 if variante == "mostrador" else 330
    impresora = ('<rect x="46" y="4" width="108" height="26" rx="6" fill="#2F2D40"/>'
                 '<rect x="58" y="-14" width="84" height="24" fill="#fff" stroke="#E4E2EE"/>') if variante == "mostrador" else ""
    return f'''<svg class="device" viewBox="0 -20 200 {alto}" aria-hidden="true">
  {impresora}
  <rect x="30" y="10" width="140" height="{alto - 40}" rx="26" fill="#17152A"/>
  <rect x="42" y="26" width="116" height="150" rx="12" fill="#F6F5FA"/>
  <text x="100" y="58" text-anchor="middle" font-family="Plus Jakarta Sans, Arial" font-size="11" fill="#62607A">Total</text>
  <text x="100" y="92" text-anchor="middle" font-family="Space Grotesk, Arial" font-size="28" font-weight="700" fill="#17152A">{importe} €</text>
  <path d="M92 118a12 12 0 0 1 0 22M100 112a20 20 0 0 1 0 34M108 106a28 28 0 0 1 0 46" stroke="#5B45C7" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <rect x="58" y="158" width="84" height="10" rx="5" fill="#E4E2EE"/>
  <g fill="#2F2D40">
    <rect x="46" y="190" width="32" height="22" rx="6"/><rect x="84" y="190" width="32" height="22" rx="6"/><rect x="122" y="190" width="32" height="22" rx="6"/>
    <rect x="46" y="218" width="32" height="22" rx="6"/><rect x="84" y="218" width="32" height="22" rx="6"/><rect x="122" y="218" width="32" height="22" rx="6"/>
    <rect x="46" y="246" width="32" height="22" rx="6"/><rect x="84" y="246" width="32" height="22" rx="6"/><rect x="122" y="246" width="32" height="22" rx="6" fill="#FF8A5B"/>
  </g>
  <rect x="80" y="{alto - 52}" width="40" height="5" rx="2.5" fill="#5B45C7"/>
</svg>'''


# ---------------------------------------------------------------------------
# Páginas
# ---------------------------------------------------------------------------
def inicio():
    cuerpo = f'''
<div class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">Terminales de pago · TPV para negocios</span>
    <h1>Cobra con tarjeta en segundos y ten tu dinero al día siguiente</h1>
    <p class="lead">Terminales rápidos, conectados por 4G y wifi, con una app para ver tus ventas al momento. Te ayudamos a elegir el equipo, tramitamos el alta y te lo dejamos funcionando.</p>
    <div class="actions">
      <a class="btn btn-primary" href="contacto.html">{ico("terminal")}Pide tu terminal</a>
      <a class="btn btn-line" href="tarifas.html">{ico("euro")}Ver tarifas</a>
    </div>
    <span class="respaldo">{C["lema"]}</span>
  </div>
  <div class="hero-device">{dibujo_terminal()}<span class="burbuja">{ico("check")}Pago aceptado</span></div>
</div>
<div class="wrap"><div class="hero-stats">
    <div><b>Siguiente día hábil</b><span>liquidación de tus ventas en los planes con abono rápido</span></div>
    <div><b>4G + wifi</b><span>el terminal sigue cobrando aunque falle la conexión del local</span></div>
    <div><b>Todas las tarjetas</b><span>débito, crédito, sin contacto y monederos del móvil</span></div>
    <div><b>Soporte en español</b><span>te atiende una persona, no un contestador</span></div>
</div></div></div>

<section><div class="wrap">
  <div class="section-head">
    <h2>Todo lo que necesitas para cobrar</h2>
    <p>En el mostrador, en la mesa, a domicilio o por internet: una sola plataforma y un único panel para ver todos tus cobros.</p>
  </div>
  <div class="grid g4">
    {tarjeta("terminal", "Terminales de pago", "Portátil, de mostrador con impresora o compacto de bolsillo. Pantalla táctil y batería para toda la jornada.", "terminales.html", "Ver terminales")}
    {tarjeta("movil", "Cobro con el móvil", "Convierte tu smartphone en un datáfono: el cliente acerca la tarjeta y listo. Ideal para empezar o para cobrar fuera.", "terminales.html#app", "Cómo funciona")}
    {tarjeta("web", "Pagos online", "Enlaces de pago por WhatsApp o correo, cobro de señales y pasarela para tu tienda web.", "soluciones.html#online", "Ver pagos online")}
    {tarjeta("mesa", "Pago en mesa y reservas", "Divide la cuenta, añade propina y gestiona reservas y lista de espera desde la misma app.", "soluciones.html#mesa", "Ver soluciones")}
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="grid g2" style="align-items:center;gap:44px">
    <div>
      <span class="eyebrow-dark">Tu dinero, cuando lo necesitas</span>
      <h2>Liquidación rápida para que la caja no se quede esperando</h2>
      <p style="color:var(--muted)">Con los planes de abono rápido, lo que cobras hoy llega a tu cuenta el siguiente día hábil. Sin esperar a fin de semana ni a cierres mensuales.</p>
      <div class="calc" id="calcLiq">
        <div class="row2">
          <div class="field"><label for="imp">Ventas con tarjeta del día (€)</label><input id="imp" name="importe" inputmode="decimal" value="850"></div>
          <div class="field"><label for="dia">Día de la venta</label>
            <select id="dia" name="dia"><option value="1">Lunes</option><option value="2">Martes</option><option value="3">Miércoles</option><option value="4">Jueves</option><option value="5" selected>Viernes</option><option value="6">Sábado</option><option value="0">Domingo</option></select>
          </div>
        </div>
        <p class="calc-out" data-salida aria-live="polite"></p>
        <p class="note-inline">Cálculo orientativo. Los plazos exactos dependen del plan y del banco receptor, y se detallan en tu contrato.</p>
      </div>
    </div>
    {checks([
        ("Sin sorpresas en la factura", "Te explicamos la tarifa por escrito antes de firmar: comisión por operación y cuota, si la hay."),
        ("Conexión que no se cae", "El terminal usa 4G y wifi y cambia de una a otra solo, para que no pierdas ninguna venta."),
        ("Ventas al momento", "Consulta en la app lo que has cobrado, por terminal, por empleado y por franja horaria."),
        ("Todo desde un solo panel", "Terminales, cobros online y reservas en el mismo sitio, con un único informe."),
    ])}
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head">
    <h2>Pensado para tu tipo de negocio</h2>
    <p>Configuramos el terminal y la app según cómo trabajas: no cobra igual una terraza que una peluquería.</p>
  </div>
  <div class="grid g3 g3-fijo">
    {tarjeta("cubiertos", "Restaurantes y cafeterías", "Pago en mesa, cuenta dividida, propinas y reservas. Menos colas en la barra y mesas que rotan antes.", "sectores.html#restauracion", "Ver solución")}
    {tarjeta("copa", "Bares y ocio nocturno", "Cobros rápidos en barra, varios terminales conectados y control de caja por turno.", "sectores.html#bares", "Ver solución")}
    {tarjeta("bolsa", "Comercio y tiendas", "Terminal de mostrador con impresora, devoluciones sencillas y ventas online con enlace de pago.", "sectores.html#comercio", "Ver solución")}
    {tarjeta("tijeras", "Peluquerías y estética", "Señales para reservar cita, cobro en el sillón y control de propinas por profesional.", "sectores.html#belleza", "Ver solución")}
    {tarjeta("maletin", "Autónomos y servicios", "Cobra a domicilio con un terminal de bolsillo o con tu móvil, y envía la factura al momento.", "sectores.html#servicios", "Ver solución")}
    {tarjeta("cama", "Alojamientos", "Preautorizaciones, cobros a distancia y terminal en recepción conectado a tu sistema.", "sectores.html#alojamiento", "Ver solución")}
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="section-head">
    <h2>Del primer contacto al primer cobro</h2>
    <p>Nosotros nos ocupamos del papeleo. Tú solo tienes que enchufar el terminal.</p>
  </div>
  <ol class="pasos">
    <li><span class="paso-n">1</span><h3>Nos cuentas tu negocio</h3><p>Volumen de ventas, tipo de local y cómo cobras hoy. Con eso te recomendamos terminal y tarifa.</p></li>
    <li><span class="paso-n">2</span><h3>Te enviamos la propuesta</h3><p>Por escrito y sin letra pequeña. Si te encaja, preparamos el alta con tu documentación.</p></li>
    <li><span class="paso-n">3</span><h3>Recibes el terminal</h3><p>Llega configurado. Te ayudamos a activarlo por teléfono o en persona.</p></li>
    <li><span class="paso-n">4</span><h3>Empiezas a cobrar</h3><p>Y seguimos a tu lado para cambios de tarifa, más terminales o cualquier incidencia.</p></li>
  </ol>
  <div style="margin-top:26px"><a class="btn btn-ghost" href="como-funciona.html">Ver el proceso completo {ico("flecha")}</a></div>
</div></section>

<section><div class="wrap">
  <div class="section-head">
    <span class="eyebrow-dark">Ideas equivocadas</span>
    <h2>Lo que se suele creer sobre el datáfono y lo que de verdad ocurre</h2>
  </div>
  <div class="grid g3">
    <div class="mito"><p class="mito-falso">«El datáfono del banco me sale gratis.»</p><p class="mito-real">Suele ir ligado a comisiones, cuotas o productos vinculados. Compara el coste total por operación, no solo el alquiler.</p></div>
    <div class="mito"><p class="mito-falso">«Cobrar con tarjeta es más lento que en efectivo.»</p><p class="mito-real">Un pago sin contacto tarda un par de segundos y no hay que dar cambio ni cuadrar monedas al cierre.</p></div>
    <div class="mito"><p class="mito-falso">«Cambiar de terminal es un lío.»</p><p class="mito-real">Tramitamos el alta con tu documentación y te dejamos el equipo funcionando. Tu cuenta bancaria no cambia.</p></div>
  </div>
</div></section>

{panel_cta()}
'''
    pagina("index.html", "Inicio", "Terminales de pago con tarjeta, cobro con el móvil y pagos online para comercios, hostelería y autónomos. Liquidación rápida y soporte en español.", cuerpo)


TERMINALES = [
    ("portatil", "Kairo Portátil", "El terminal para llevar a la mesa o a la terraza.",
     [("Pantalla táctil grande", "Fácil de leer para el cliente, también a pleno sol."),
      ("4G y wifi", "Cambia de red sola si una falla."),
      ("Batería para toda la jornada", "Con base de carga incluida."),
      ("Propinas y cuenta dividida", "El cliente elige la propina en la pantalla.")]),
    ("mostrador", "Kairo Mostrador", "Con impresora de tiques integrada, para la caja fija.",
     [("Impresora integrada", "Tique para el cliente y copia para el comercio."),
      ("Conexión por cable, wifi o 4G", "Para cajas con mucho movimiento."),
      ("Integrable con tu TPV", "Envía el importe desde el programa de caja y evita errores al teclear."),
      ("Devoluciones en un paso", "Desde el propio terminal o desde la app.")]),
    ("movil", "Kairo Tap (app)", "Tu móvil Android o iPhone compatible, convertido en datáfono.",
     [("Sin equipo adicional", "Descarga la app y empieza a cobrar."),
      ("Pagos sin contacto", "Tarjetas y monederos del móvil."),
      ("Recibo digital", "Por correo o SMS al cliente."),
      ("Perfecto para empezar", "O como segundo terminal para cobrar fuera.")]),
]


def terminales():
    fichas = ""
    for i, (var, nombre, lema, feats) in enumerate(TERMINALES):
        ancla = "app" if var == "movil" else var
        fichas += f'''
<section class="{"alt" if i % 2 else ""}" id="{ancla}"><div class="wrap">
  <div class="ficha{" invertida" if i % 2 else ""}">
    <div class="ficha-img">{dibujo_terminal(var, ["18,90", "62,35", "9,50"][i])}</div>
    <div>
      <span class="eyebrow-dark">{"App" if var == "movil" else "Terminal"}</span>
      <h2>{nombre}</h2>
      <p class="entradilla">{lema}</p>
      {checks(feats)}
      <div class="btn-par" style="margin-top:22px"><a class="btn btn-primary" href="contacto.html?interes={nombre}">{ico("mail")}Lo quiero</a><a class="btn btn-ghost" href="tarifas.html">Ver tarifas</a></div>
    </div>
  </div>
</div></section>'''
    cuerpo = cabeza_pagina("Terminales", "Terminales de pago", "Elige el equipo según dónde cobras. Todos aceptan tarjetas de débito y crédito, pagos sin contacto y monederos del móvil, y se gestionan desde la misma app.") + fichas + f'''
<section><div class="wrap">
  <div class="section-head"><h2>Comparativa rápida</h2><p>¿Dudas entre dos modelos? Aquí tienes las diferencias principales.</p></div>
  <div class="tabla-wrap"><table class="comparativa">
    <thead><tr><th></th><th>Portátil</th><th>Mostrador</th><th>Tap (app)</th></tr></thead>
    <tbody>
      <tr><td>Lo mejor para</td><td>Mesa y terraza</td><td>Caja fija</td><td>Empezar o cobrar fuera</td></tr>
      <tr><td>Conexión</td><td>4G + wifi</td><td>Cable, wifi, 4G</td><td>La del móvil</td></tr>
      <tr><td>Impresora</td><td>Tique digital</td><td>{ico("check")} Integrada</td><td>Tique digital</td></tr>
      <tr><td>Tarjeta con chip y PIN</td><td>{ico("check")}</td><td>{ico("check")}</td><td>Sin contacto</td></tr>
      <tr><td>Propinas y cuenta dividida</td><td>{ico("check")}</td><td>{ico("check")}</td><td>{ico("check")}</td></tr>
      <tr><td>Integración con TPV</td><td>{ico("check")}</td><td>{ico("check")}</td><td>—</td></tr>
    </tbody>
  </table></div>
</div></section>
''' + panel_cta("¿No sabes cuál elegir?", "Te lo recomendamos nosotros según tu volumen de ventas y tu forma de trabajar. Muchos negocios combinan un terminal de mostrador con uno portátil.")
    pagina("terminales.html", "Terminales de pago", "Terminal portátil, de mostrador con impresora y app para cobrar con el móvil. Tarjetas, pagos sin contacto y monederos móviles.", cuerpo)


def soluciones():
    bloques = [
        ("online", "web", "Pagos online y enlaces de pago", "Cobra sin que el cliente esté delante.",
         [("Enlaces de pago", "Crea un enlace con el importe y envíalo por WhatsApp, SMS o correo."),
          ("Señales y depósitos", "Asegura reservas y encargos cobrando una parte por adelantado."),
          ("Pasarela para tu web", "Integra el cobro en tu tienda online."),
          ("Pagos por teléfono", "Introduce los datos de la tarjeta de forma segura desde el panel.")]),
        ("mesa", "mesa", "Pago en mesa", "El cliente paga sin levantarse y sin esperar a que le traigan la cuenta.",
         [("Cuenta dividida", "A partes iguales o por productos, en el propio terminal."),
          ("Propinas en pantalla", "Porcentajes sugeridos o importe libre, con informe por empleado."),
          ("Pago con QR", "El cliente escanea el tique y paga desde su móvil."),
          ("Mesas que rotan antes", "Menos tiempo entre el postre y la siguiente reserva.")]),
        ("reservas", "calendario", "Reservas y lista de espera", "Llena el local sin depender del teléfono.",
         [("Reservas online", "Un enlace para tu web, redes y buscadores."),
          ("Lista de espera digital", "Avisa por SMS cuando la mesa está lista."),
          ("Menos plantones", "Pide tarjeta o señal para confirmar la reserva."),
          ("Plano de sala", "Ve de un vistazo qué mesas están libres.")]),
        ("informes", "grafica", "App de gestión e informes", "Tu negocio en el bolsillo.",
         [("Ventas en tiempo real", "Por terminal, por empleado y por hora."),
          ("Cierre de caja", "Informe diario listo para tu gestoría."),
          ("Varios locales", "Todos tus establecimientos en un solo panel."),
          ("Usuarios y permisos", "Decide quién puede hacer devoluciones o ver informes.")]),
        ("cuenta", "banco", "Cuenta de negocio y tarjeta", "Opcional: recibe tus ventas en una cuenta pensada para el negocio.",
         [("Abono de ventas", "Consulta el saldo en la misma app que tus cobros."),
          ("Tarjeta de empresa", "Para compras y pagos a proveedores."),
          ("Control de gastos", "Movimientos categorizados automáticamente."),
          ("Compatible con tu banco", "Si prefieres, sigues recibiendo los abonos en tu cuenta actual.")]),
    ]
    html = cabeza_pagina("Soluciones", "Soluciones de cobro", "Más allá del datáfono: cobros online, pago en mesa, reservas y una app para controlar todo tu negocio desde el móvil.")
    html += '<section><div class="wrap"><div class="grid g4">' + "".join(
        tarjeta(i, t, s, "#" + a, "Ver detalle") for a, i, t, s, _ in bloques) + "</div></div></section>"
    for n, (a, i, t, s, f) in enumerate(bloques):
        html += f'''
<section class="{"alt" if n % 2 == 0 else ""}" id="{a}"><div class="wrap">
  <div class="grid g2" style="align-items:start;gap:44px">
    <div><span class="ico-grande">{ico(i)}</span><h2>{t}</h2><p class="entradilla">{s}</p>
    <a class="btn btn-ghost" href="contacto.html">Solicitar información {ico("flecha")}</a></div>
    {checks(f)}
  </div>
</div></section>'''
    html += panel_cta()
    pagina("soluciones.html", "Soluciones", "Pagos online, enlaces de pago, pago en mesa, reservas, informes de ventas y cuenta de negocio en una sola plataforma.", html)


def sectores():
    s = [
        ("restauracion", "cubiertos", "Restaurantes y cafeterías",
         "En hora punta cada minuto cuenta. Lleva el terminal a la mesa, divide la cuenta y deja que el cliente elija la propina.",
         ["Pago en mesa y con QR", "Cuenta dividida y propinas", "Reservas y lista de espera", "Integración con tu TPV de hostelería"]),
        ("bares", "copa", "Bares y ocio nocturno",
         "Barra llena y poco tiempo: pagos sin contacto en dos segundos y varios terminales trabajando a la vez.",
         ["Cobro sin contacto ultrarrápido", "Varios terminales por local", "Cierre de caja por turno", "Conexión 4G de respaldo"]),
        ("comercio", "bolsa", "Comercio y tiendas",
         "Terminal de mostrador con impresora y, si vendes online, enlaces de pago y pasarela para tu web.",
         ["Impresora de tiques integrada", "Devoluciones sencillas", "Venta online y por WhatsApp", "Informes por producto y hora"]),
        ("belleza", "tijeras", "Peluquerías, estética y bienestar",
         "Pide una señal al reservar para reducir las ausencias y cobra en el sillón sin que el cliente vaya al mostrador.",
         ["Señal al reservar cita", "Propinas por profesional", "Cobro en cabina o sillón", "Bonos y pagos a plazos por enlace"]),
        ("servicios", "maletin", "Autónomos y servicios a domicilio",
         "Fontaneros, técnicos, fisioterapeutas o transportistas: cobra donde estés con un terminal de bolsillo o con tu móvil.",
         ["Terminal de bolsillo o app", "Enlace de pago para presupuestos", "Recibo por correo o SMS", "Sin permanencia en los planes flexibles"]),
        ("alojamiento", "cama", "Hoteles y alojamientos",
         "Preautoriza la tarjeta al hacer el check-in, cobra a distancia y ten un terminal en recepción conectado a tu sistema.",
         ["Preautorizaciones", "Cobro de reservas a distancia", "Terminal en recepción", "Varias monedas en tarjetas extranjeras"]),
    ]
    html = cabeza_pagina("Sectores", "Soluciones por sector", "Cada negocio cobra de una forma. Configuramos terminal, app y tarifa según tu actividad.")
    html += '<section><div class="wrap"><div class="grid g2 sectores">'
    for a, i, t, txt, pts in s:
        html += f'''<article class="card sector" id="{a}"><span class="ico">{ico(i)}</span><h3>{t}</h3><p>{txt}</p>
<ul class="mini-checks">{"".join(f"<li>{ico('check')}{p}</li>" for p in pts)}</ul>
<a class="more" href="contacto.html">Pedir propuesta para mi negocio {ico("flecha")}</a></article>'''
    html += "</div></div></section>" + panel_cta("¿Tu sector no aparece?", "Trabajamos con todo tipo de actividades. Cuéntanos cómo cobras hoy y te decimos qué te conviene.")
    pagina("sectores.html", "Sectores", "Terminales de pago para restaurantes, bares, comercios, peluquerías, autónomos y alojamientos.", html)


def tarifas():
    planes = [
        ("Flexible", "Para empezar o con ventas variables.", "Sin cuota mensual",
         ["Comisión fija por operación", "App de cobro con el móvil", "Enlaces de pago", "Sin permanencia"], False),
        ("Negocio", "Para comercios y hostelería con ventas regulares.", "Cuota mensual + comisión reducida",
         ["Terminal portátil o de mostrador", "Liquidación rápida", "Pago en mesa, propinas y cuenta dividida", "Informes y cierre de caja"], True),
        ("A medida", "Para volúmenes altos o varios locales.", "Tarifa personalizada",
         ["Comisión negociada según volumen", "Varios terminales y locales", "Integración con tu TPV", "Gestor personal"], False),
    ]
    html = cabeza_pagina("Tarifas", "Tarifas claras", "Tres formas de trabajar según tu volumen. Te enviamos la propuesta con los importes exactos por escrito antes de firmar nada.")
    html += '<section><div class="wrap"><div class="grid g3 planes">'
    for n, sub, precio, f, dest in planes:
        html += f'''<div class="card plan{" destacado" if dest else ""}">{'<span class="plan-tag">El más elegido</span>' if dest else ""}
<h3>{n}</h3><p>{sub}</p><div class="plan-precio">{precio}</div>
<ul class="mini-checks">{"".join(f"<li>{ico('check')}{x}</li>" for x in f)}</ul>
<a class="btn {"btn-primary" if dest else "btn-ghost"}" href="contacto.html">Pedir precio</a></div>'''
    html += f'''</div>
<p class="note-inline" style="margin-top:22px">Las comisiones dependen del tipo de tarjeta, del volumen mensual y de la actividad. Por eso no publicamos una cifra única: te damos la tuya, por escrito y sin compromiso.</p>
</div></section>
<section class="alt"><div class="wrap">
  <div class="grid g2" style="align-items:start;gap:44px">
    <div><h2>¿Qué incluye siempre?</h2><p class="entradilla">Sea cual sea el plan, tienes lo esencial para cobrar con tranquilidad.</p></div>
    {checks([
        ("Todas las tarjetas", "Débito, crédito, empresa y extranjeras, además de monederos del móvil."),
        ("Seguridad en cada pago", "Cifrado de extremo a extremo y cumplimiento de la normativa PCI DSS."),
        ("Soporte en español", "Por teléfono, correo y WhatsApp."),
        ("Asesoramiento continuo", "Revisamos tu tarifa si cambia tu volumen de ventas."),
    ])}
  </div>
</div></section>
''' + panel_cta("Pide tu tarifa personalizada", "Envíanos una factura de tu datáfono actual y te decimos cuánto podrías ahorrar.")
    pagina("tarifas.html", "Tarifas", "Planes de cobro con tarjeta sin cuota, con cuota y a medida. Propuesta por escrito y sin compromiso.", html)


def como_funciona():
    pasos = [
        ("Contacto", "Nos llamas, nos escribes por WhatsApp o rellenas el formulario. Te llamamos en menos de 24 horas laborables."),
        ("Análisis", "Revisamos cómo cobras hoy y, si tienes datáfono, tu última factura para compararla."),
        ("Propuesta", "Te enviamos por escrito el terminal recomendado y la tarifa, con todos los costes."),
        ("Alta", "Nos pasas la documentación (DNI o CIF, IBAN y datos de la actividad) y tramitamos el contrato con la entidad de pago."),
        ("Entrega", "Recibes el terminal configurado. Te ayudamos a activarlo y a hacer el primer cobro de prueba."),
        ("Acompañamiento", "Seguimos contigo: nuevos terminales, cambios de plan, incidencias o dudas del día a día."),
    ]
    html = cabeza_pagina("Cómo funciona", "Cómo funciona", "Así es el proceso desde que nos contactas hasta que cobras tu primera venta con tarjeta.")
    html += '<section><div class="wrap"><ol class="pasos pasos-v">' + "".join(
        f'<li><span class="paso-n">{i + 1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(pasos)
    ) + "</ol></div></section>"
    html += f'''<section class="alt"><div class="wrap"><div class="grid g2" style="gap:44px;align-items:start">
<div><h2>Documentación para el alta</h2><p class="entradilla">Ten a mano estos datos y el alta será cuestión de minutos.</p></div>
{checks([
    ("Identificación", "DNI o NIE del titular, o CIF y escrituras si es una sociedad."),
    ("Cuenta bancaria", "Certificado de titularidad de la cuenta donde recibirás los abonos."),
    ("Actividad", "Descripción del negocio y dirección del local, si lo tienes."),
    ("Volumen estimado", "Una idea de cuánto cobras al mes con tarjeta."),
])}
</div></div></section>''' + panel_cta()
    pagina("como-funciona.html", "Cómo funciona", "Proceso de alta de un terminal de pago: contacto, propuesta, documentación, entrega y acompañamiento.", html)


PREGUNTAS = [
    ("¿Qué tarjetas puedo aceptar?", "Tarjetas de débito y crédito de las principales redes internacionales, tarjetas de empresa y extranjeras, y pagos con el móvil o el reloj mediante los monederos digitales más habituales."),
    ("¿Cuándo recibo el dinero de mis ventas?", "En los planes con liquidación rápida, el siguiente día hábil. En otros planes el plazo puede ser distinto; siempre te lo indicamos en la propuesta y en el contrato."),
    ("¿Tengo que cambiar de banco?", "No. Puedes recibir los abonos en tu cuenta actual. La cuenta de negocio es opcional."),
    ("¿Hay permanencia?", "Depende del plan. Los planes flexibles no tienen permanencia; en otros puede haber condiciones que te explicamos antes de firmar."),
    ("¿Qué pasa si se cae el wifi del local?", "Los terminales portátiles y de mostrador tienen conexión 4G y cambian de red automáticamente para seguir cobrando."),
    ("¿Puedo usarlo con mi programa de caja?", "Sí, el terminal de mostrador y el portátil se integran con muchos programas de TPV. Consúltanos el tuyo."),
    ("¿Cuánto tarda el alta?", "Con la documentación completa, normalmente entre 24 y 48 horas laborables, más el envío del terminal."),
    ("¿Qué pasa si el terminal se estropea?", "Te lo sustituimos. Mientras tanto puedes seguir cobrando con la app en el móvil o con enlaces de pago."),
    ("¿Quién presta el servicio de pago?", f"{C['marca']} es un distribuidor comercial independiente. El servicio de pago lo presta una entidad de pago autorizada, que figura en tu contrato. Nosotros te asesoramos, tramitamos el alta y te damos soporte."),
    ("¿Es seguro?", "Cada pago viaja cifrado y la plataforma cumple la normativa de seguridad de la industria de tarjetas (PCI DSS) y la autenticación reforzada exigida en Europa."),
]


def preguntas():
    html = cabeza_pagina("Preguntas frecuentes", "Preguntas frecuentes", "Las dudas que más nos plantean antes de dar el paso. Si la tuya no está aquí, escríbenos.")
    html += '<section><div class="wrap">' + faq(PREGUNTAS) + "</div></section>" + panel_cta("¿Te queda alguna duda?", "Llámanos o escríbenos por WhatsApp y te la resolvemos al momento.")
    pagina("preguntas-frecuentes.html", "Preguntas frecuentes", "Respuestas sobre tarjetas aceptadas, plazos de abono, permanencia, conexión, alta y seguridad de los terminales de pago.", html)


def contacto():
    opciones = lambda xs: "".join(f"<option>{x}</option>" for x in xs)
    html = cabeza_pagina("Contacto", "Contacto", "Cuéntanos cómo es tu negocio y te preparamos una propuesta con el terminal y la tarifa que mejor encajan.")
    html += f'''<section><div class="wrap"><div class="grid g2" style="gap:44px;align-items:start">
  <div class="card form-card" id="escribenos">
  <span class="eyebrow-dark">Respuesta en menos de 24 h laborables</span>
  <h2 style="font-size:24px">Solicita tu propuesta</h2>
  <form class="contact" id="contactForm" data-to="{C["email"]}" action="mailto:{C["email"]}" method="post" enctype="text/plain">
    <div class="row2">
      <div class="field"><label for="nombre">Nombre y apellidos</label><input id="nombre" name="nombre" required></div>
      <div class="field"><label for="negocio">Nombre del negocio</label><input id="negocio" name="negocio"></div>
    </div>
    <div class="row2">
      <div class="field"><label for="tel">Teléfono</label><input id="tel" name="telefono" type="tel" required></div>
      <div class="field"><label for="email">Correo electrónico</label><input id="email" name="email" type="email" required></div>
    </div>
    <div class="row2">
      <div class="field"><label for="sector">Sector</label><select id="sector" name="sector">{opciones(["Selecciona una opción", "Restaurante o cafetería", "Bar u ocio nocturno", "Comercio o tienda", "Peluquería o estética", "Autónomo o servicios", "Alojamiento", "Otro"])}</select></div>
      <div class="field"><label for="interes">Me interesa</label><select id="interes" name="interes">{opciones(["Selecciona una opción", "Kairo Portátil", "Kairo Mostrador", "Kairo Tap (app)", "Pagos online", "Pago en mesa y reservas", "Comparar con mi datáfono actual"])}</select></div>
    </div>
    <div class="field"><label for="msg">Cuéntanos</label><textarea id="msg" name="mensaje" placeholder="Cuánto cobras al mes con tarjeta, cuántos terminales necesitas, qué tienes ahora…"></textarea></div>
    <label class="consent"><input type="checkbox" name="consent" required> <span>He leído y acepto la <a href="politica-de-privacidad.html">política de privacidad</a> y el tratamiento de mis datos para responder a esta solicitud.</span></label>
    <button class="btn btn-primary" type="submit">{ico("mail")}Enviar solicitud</button>
    <p class="form-msg" id="formMsg">Se abrirá tu programa de correo con la solicitud ya redactada. Si no ocurre nada, escríbenos a <a href="mailto:{C["email"]}">{C["email"]}</a>.</p>
  </form>
  </div>
  <div>
    <h2 style="font-size:24px">Otras formas de contactar</h2>
    <ul class="info-list">
      <li><span class="ico">{ico("tel")}</span><div><b>Teléfono</b><a href="tel:{C["telefono_intl"]}">{C["telefono"]}</a></div></li>
      <li><span class="ico">{WA_SVG}</span><div><b>WhatsApp</b><a href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener">{C["whatsapp_txt"]}</a></div></li>
      <li><span class="ico">{ico("mail")}</span><div><b>Correo</b><a href="mailto:{C["email"]}">{C["email"]}</a></div></li>
      <li><span class="ico">{ico("pin")}</span><div><b>Oficina</b><span>{C["direccion"]}</span></div></li>
      <li><span class="ico">{ico("reloj")}</span><div><b>Horario</b><span>{C["horario"]}</span></div></li>
    </ul>
  </div>
</div></div></section>
<script>
// Preselecciona el producto si se llega desde la ficha de un terminal.
(function () {{
  var q = new URLSearchParams(location.search).get('interes');
  var sel = document.getElementById('interes');
  if (!q || !sel) return;
  Array.prototype.forEach.call(sel.options, function (o) {{ if (o.text === q) sel.value = o.value; }});
}})();
</script>'''
    pagina("contacto.html", "Contacto", "Solicita una propuesta de terminal de pago y tarifa para tu negocio.", html)


def legal(archivo, titulo, secciones):
    nav = "".join(f'<li><a href="#s{i}">{t}</a></li>' for i, (t, _) in enumerate(secciones))
    cuerpo = "".join(f'<div class="legal-sec" id="s{i}"><h2>{t}</h2>{txt}</div>' for i, (t, txt) in enumerate(secciones))
    html = cabeza_pagina(titulo, titulo, f"Última actualización: {C['anio']}.")
    html += f'''<section><div class="wrap"><div class="legal-layout">
<aside class="legal-nav"><h3>En esta página</h3><ul class="foot-links dark">{nav}</ul></aside>
<div class="legal-body">{cuerpo}</div></div></div></section>'''
    pagina(archivo, titulo, f"{titulo} de {C['marca']}.", html)


def legales():
    titular = f"<p>Titular: {C['razon_social']}, con {C['cif']} y domicilio en {C['direccion']}. Correo: <a href=\"mailto:{C['email']}\">{C['email']}</a>.</p>"
    legal("aviso-legal.html", "Aviso legal", [
        ("Datos identificativos", titular),
        ("Objeto", f"<p>Este sitio informa sobre los servicios de distribución y asesoramiento de soluciones de cobro con tarjeta que ofrece {C['marca']}. {C['marca']} actúa como distribuidor comercial independiente; los servicios de pago los presta la entidad de pago autorizada que se indique en el contrato de cada cliente.</p>"),
        ("Propiedad intelectual", "<p>Los textos, diseño, ilustraciones y logotipos de este sitio pertenecen a su titular. Las marcas de terceros que puedan citarse pertenecen a sus respectivos propietarios y se mencionan solo a efectos descriptivos.</p>"),
        ("Responsabilidad", "<p>La información de este sitio es orientativa. Las condiciones aplicables a cada cliente son las que figuran en su propuesta y contrato.</p>"),
        ("Legislación aplicable", "<p>Este aviso se rige por la legislación española.</p>"),
    ])
    legal("politica-de-privacidad.html", "Política de privacidad", [
        ("Responsable del tratamiento", titular),
        ("Datos que tratamos", "<p>Los que nos facilitas en el formulario, por teléfono, correo o WhatsApp: nombre, negocio, teléfono, correo y la información que quieras compartir sobre tu actividad.</p>"),
        ("Finalidad", "<p>Responder a tu solicitud, preparar una propuesta comercial y, si la aceptas, tramitar el alta del servicio.</p>"),
        ("Legitimación", "<p>Tu consentimiento al enviar la solicitud y, en su caso, la ejecución de un contrato o de medidas precontractuales.</p>"),
        ("Destinatarios", "<p>Si contratas, la entidad de pago que presta el servicio, para dar de alta tu comercio. No cedemos datos a terceros con otros fines.</p>"),
        ("Conservación", "<p>Mientras dure la relación comercial y, después, durante los plazos legales aplicables.</p>"),
        ("Tus derechos", f"<p>Puedes ejercer los derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a <a href=\"mailto:{C['email']}\">{C['email']}</a>, y reclamar ante la Agencia Española de Protección de Datos.</p>"),
    ])
    legal("cookies.html", "Cookies", [
        ("Qué cookies usamos", "<p>Este sitio no instala cookies propias de análisis ni de publicidad. Solo carga tipografías desde un servicio externo, que puede registrar datos técnicos de la conexión.</p>"),
        ("Cómo desactivarlas", "<p>Puedes bloquear o eliminar cookies desde la configuración de tu navegador.</p>"),
    ])


def mapa_web():
    todas = NAV + [("aviso-legal.html", "Aviso legal"), ("politica-de-privacidad.html", "Política de privacidad"), ("cookies.html", "Cookies")]
    html = cabeza_pagina("Mapa web", "Mapa web", "Todas las páginas del sitio.")
    html += '<section><div class="wrap"><ul class="foot-links dark mapa">' + "".join(
        f'<li><a href="{h}">{ico("flecha")}<span>{t}</span></a></li>' for h, t in todas) + "</ul></div></section>"
    pagina("mapa-web.html", "Mapa web", "Mapa del sitio.", html)
    no_encontrada = cabeza_pagina("Página no encontrada", "Página no encontrada", "La dirección que buscas no existe o ha cambiado.") + \
        f'<section><div class="wrap"><a class="btn btn-primary" href="index.html">{ico("flecha")}Volver al inicio</a></div></section>'
    pagina("404.html", "Página no encontrada", "Página no encontrada.", no_encontrada)


# ---------------------------------------------------------------------------
# Hoja de estilo: parte de la del sitio de referencia, con la paleta propia
# ---------------------------------------------------------------------------
PALETA = {
    "#1C5C41": "#3B2A8C", "#2E7D57": "#5B45C7", "#123D2B": "#251A5E", "#0C2C1E": "#160F3A",
    "#EAF2EE": "#EEEBFB", "#1F6749": "#4A36A8", "#16211C": "#17152A", "#2F3A34": "#2F2D40",
    "#5E6B64": "#62607A", "#E1E8E4": "#E4E2EE", "#F5F7F5": "#F6F5FA", "#D6E6DD": "#DCD8F3",
    "#C4D8CC": "#C9C3EC", "#B6CCC0": "#BDB6E3", "#9FD3B8": "#FFB38A", "#9FB8A8": "#A59ECB",
    "#D8E7DF": "#DEDAF5", "#A9D8C0": "#FFB38A", "#BCD6C8": "#C3BCE8", "#A8C9B7": "#B3ABE0",
    "#D3E4DA": "#D9D4F2", "#CDE0D5": "#D2CCEF", "#D8E2DB": "#DDDAEA", "#E4F0E9": "#EAE7F8",
    "#E7F5EF": "#EFEBFC", "#BCE3D4": "#CFC6F4", "#12604A": "#3B2A8C", "#2C4A3B": "#2E2750",
    "#8FA99A": "#9A93C0", "#8A9A92": "#8E8BA5", "#FAFCFB": "#FBFAFE", "#C9D8E6": "#CFC8EE",
    "rgba(46,125,87,": "rgba(91,69,199,", "rgba(18,61,43,": "rgba(37,26,94,",
}

EXTRA_CSS = r'''
/* ===================== Kairo: componentes propios ===================== */
.logo{height:36px;width:auto;display:block}
@media (max-width:420px){.logo{height:30px}}
.foot-brand{display:inline-block;margin-bottom:16px}
.foot-brand .logo{height:34px}
.main-nav a.btn-primary{background:#FF7A45;border-color:#FF7A45}
.main-nav a.btn-primary:hover{background:#F0642E;border-color:#F0642E}

/* Hero con ilustración */
.hero-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:center;position:relative;z-index:1}
.hero-device{position:relative;justify-self:center;width:min(270px,70vw)}
.hero-device .device{width:100%;height:auto;filter:drop-shadow(0 30px 40px rgba(10,6,40,.45));transform:rotate(-6deg)}
.burbuja{
  position:absolute;left:-18px;bottom:18%;display:inline-flex;align-items:center;gap:8px;
  background:#fff;color:#17152A;border-radius:999px;padding:10px 16px;font-weight:600;font-size:14.5px;
  box-shadow:0 12px 30px rgba(10,6,40,.3);
}
.burbuja svg{width:18px;height:18px;color:#fff;background:#22B07D;border-radius:50%;padding:3px}
.hero-stats{position:relative;z-index:1}
@media (max-width:860px){
  .hero-grid{grid-template-columns:1fr}
  .hero-device{width:190px;order:-1}
  .burbuja{left:auto;right:-40px;font-size:13px}
}
.hero .respaldo{color:#FFB38A}

/* Pasos numerados */
.pasos{list-style:none;margin:0;padding:0;display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));counter-reset:none}
.pasos li{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:24px;box-shadow:var(--shadow)}
.pasos h3{margin:10px 0 .4em}
.pasos p{margin:0;color:var(--muted);font-size:15px}
.paso-n{
  display:grid;place-items:center;width:38px;height:38px;border-radius:50%;
  background:var(--green);color:#fff;font-family:var(--font-display);font-weight:700;
}
.pasos-v{grid-template-columns:1fr;max-width:760px}
.pasos-v li{display:grid;grid-template-columns:38px 1fr;column-gap:18px}
.pasos-v .paso-n{grid-row:span 2}
.pasos-v h3{margin:6px 0 .3em}

/* Calculadora de liquidación */
.calc{background:var(--bg);border:1px solid var(--line);border-radius:var(--radius);padding:20px;margin-top:18px}
.calc-out{font-weight:600;color:var(--green-dark);margin:14px 0 8px}

/* Fichas de terminal */
.ficha{display:grid;grid-template-columns:.7fr 1.3fr;gap:48px;align-items:center}
.ficha.invertida .ficha-img{order:2}
.ficha-img{display:grid;place-items:center;background:linear-gradient(160deg,var(--green-soft),#fff);border-radius:20px;padding:36px 20px;border:1px solid var(--line)}
.ficha-img .device{width:min(220px,60vw);height:auto;filter:drop-shadow(0 18px 26px rgba(37,26,94,.25))}
@media (max-width:820px){.ficha{grid-template-columns:1fr;gap:28px}.ficha.invertida .ficha-img{order:0}}

/* Tabla comparativa */
.tabla-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);background:#fff;box-shadow:var(--shadow)}
table.comparativa{border-collapse:collapse;width:100%;min-width:560px;font-size:15px}
.comparativa th,.comparativa td{padding:13px 16px;border-bottom:1px solid var(--line);text-align:left}
.comparativa thead th{background:var(--green-soft);color:var(--green-dark);font-family:var(--font-display)}
.comparativa td:first-child{font-weight:600;color:var(--ink)}
.comparativa tr:last-child td{border-bottom:0}
.comparativa svg{color:var(--green)}

/* Icono grande de sección */
.ico-grande{display:grid;place-items:center;width:54px;height:54px;border-radius:14px;background:var(--green-soft);color:var(--green);margin-bottom:14px}
.ico-grande svg{width:27px;height:27px}

/* Sectores y planes */
.mini-checks{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:7px;font-size:14.5px;color:var(--body)}
.mini-checks li{display:flex;gap:8px;align-items:flex-start}
.mini-checks svg{width:17px;height:17px;color:var(--green);margin-top:3px}
.sector{display:flex;flex-direction:column;scroll-margin-top:110px}
.sector .more{margin-top:auto;padding-top:16px}
.planes{align-items:stretch}
.plan{display:flex;flex-direction:column;position:relative}
.plan .btn{margin-top:auto}
.plan .mini-checks{margin-bottom:22px}
.plan-precio{font-family:var(--font-display);font-size:20px;font-weight:700;color:var(--green-dark);margin:12px 0 4px}
.plan.destacado{border:2px solid var(--green);box-shadow:var(--shadow-lg)}
.plan-tag{
  position:absolute;top:-13px;left:24px;background:#FF7A45;color:#fff;font-size:12px;font-weight:700;
  letter-spacing:.05em;text-transform:uppercase;padding:4px 12px;border-radius:999px;
}
.mapa{max-width:520px}
section[id]{scroll-margin-top:90px}
@media (min-width:900px){.g3-fijo{grid-template-columns:repeat(3,1fr)}}
'''


def estilos():
    base = pathlib.Path("/home/user/retuertographic/rya/assets/styles.css")
    fuente = RAIZ / "tools" / "base.css"
    css = (fuente if fuente.exists() else base).read_text(encoding="utf-8")
    if not fuente.exists():
        fuente.write_text(css, encoding="utf-8")
    # Se quitan los bloques exclusivos del sitio de seguros.
    css = re.sub(r"/\* Directorio de teléfonos.*?(?=/\* Par de botones)", "", css, flags=re.S)
    css = re.sub(r"/\* Enlaces a los cuadros médicos.*?(?=\.note-inline)", "", css, flags=re.S)
    css = css.replace("/* Retuerto y Asociados — hoja de estilo única del sitio */",
                      "/* Kairo Pagos — hoja de estilo única del sitio */")
    css = css.replace("/* Verde corporativo tomado del logotipo */", "/* Paleta corporativa (se mantienen los nombres de variable) */")
    for viejo, nuevo in PALETA.items():
        css = css.replace(viejo, nuevo)
    css = css.replace('"Jost",', '"Plus Jakarta Sans",').replace('"Playfair Display",Georgia,"Times New Roman",serif', '"Space Grotesk","Plus Jakarta Sans",system-ui,sans-serif')
    css = css.replace("max-width:1300px", "max-width:1100px")
    (RAIZ / "assets" / "styles.css").write_text(css + EXTRA_CSS, encoding="utf-8")
    (RAIZ / "assets" / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36"><rect width="36" height="36" rx="10" fill="#5B45C7"/>'
        '<path d="M12 10v16M12 18l8-8M12 18l8 8" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M24.5 13a7 7 0 0 1 0 10" stroke="#FF8A5B" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg>\n',
        encoding="utf-8")


if __name__ == "__main__":
    (RAIZ / "assets").mkdir(exist_ok=True)
    estilos()
    inicio(); terminales(); soluciones(); sectores(); tarifas(); como_funciona()
    preguntas(); contacto(); legales(); mapa_web()
    print("Sitio generado en", RAIZ)
