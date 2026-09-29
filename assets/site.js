// Kairo Pagos — script único del sitio.

// Menú responsive
(function () {
  var btn = document.getElementById('navToggle');
  var nav = document.getElementById('mainNav');
  if (!btn || !nav) return;
  btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  });
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') nav.classList.remove('open');
  });
})();

// Menú principal con desbordamiento: los elementos que no caben se recogen
// en «Más», y vuelven al menú al ensanchar la ventana.
(function () {
  var nav = document.getElementById('mainNav');
  if (!nav) return;
  var lista = nav.querySelector('ul');
  var mas = lista.querySelector('.nav-mas');
  var drop = mas && mas.querySelector('.nav-drop');
  var cta = lista.querySelector('.cta');
  var wrap = document.querySelector('.site-header .wrap');
  if (!mas || !drop || !wrap) return;
  var movil = window.matchMedia('(max-width:1100px)');

  function restaurar() {
    while (drop.firstElementChild) lista.insertBefore(drop.firstElementChild, mas);
    mas.hidden = true;
    cerrar();
  }
  function cerrar() {
    mas.classList.remove('abierto');
    mas.querySelector('button').setAttribute('aria-expanded', 'false');
  }
  function ajustar() {
    restaurar();
    if (movil.matches) return;
    var items = Array.prototype.filter.call(
      lista.children, function (li) { return li !== mas && li !== cta; }
    );
    // Se recogen desde el final; «Inicio» no se mueve nunca.
    var i = items.length - 1;
    while (wrap.scrollWidth > wrap.clientWidth + 1 && i >= 1) {
      mas.hidden = false;
      drop.insertBefore(items[i], drop.firstChild);
      i--;
    }
    if (!drop.children.length) { mas.hidden = true; return; }
    mas.classList.toggle('tiene-activo', !!drop.querySelector('a.active'));
  }

  mas.querySelector('button').addEventListener('click', function (e) {
    e.stopPropagation();
    var abierto = mas.classList.toggle('abierto');
    this.setAttribute('aria-expanded', String(abierto));
  });
  document.addEventListener('click', function (e) {
    if (!mas.contains(e.target)) cerrar();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') cerrar();
  });

  var pendiente;
  window.addEventListener('resize', function () {
    clearTimeout(pendiente);
    pendiente = setTimeout(ajustar, 120);
  });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(ajustar);
  ajustar();
})();

// Botón de volver arriba. Se coloca sobre el de WhatsApp, nunca encima.
(function () {
  var boton = document.getElementById('irArriba');
  if (!boton) return;
  var visible = false;
  function revisar() {
    var debe = window.scrollY > 600;
    if (debe !== visible) { visible = debe; boton.hidden = !debe; }
  }
  boton.addEventListener('click', function () {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });
  window.addEventListener('scroll', revisar, { passive: true });
  revisar();
})();

// Calculadora orientativa de liquidación: muestra cuánto se ha cobrado con
// tarjeta y cuándo llega al banco según el día de la venta.
(function () {
  var caja = document.getElementById('calcLiq');
  if (!caja) return;
  var importe = caja.querySelector('[name=importe]');
  var dia = caja.querySelector('[name=dia]');
  var salida = caja.querySelector('[data-salida]');
  var DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
  function siguienteHabil(d) {
    var n = (d + 1) % 7;
    while (n === 0 || n === 6) n = (n + 1) % 7;
    return n;
  }
  function pintar() {
    var v = parseFloat(String(importe.value).replace(',', '.')) || 0;
    var d = parseInt(dia.value, 10);
    var fmt = v.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' });
    salida.textContent = 'Lo que cobres el ' + DIAS[d] + ' (' + fmt +
      ') se abona, en los planes con liquidación rápida, el ' + DIAS[siguienteHabil(d)] + '.';
  }
  importe.addEventListener('input', pintar);
  dia.addEventListener('change', pintar);
  pintar();
})();

// Formulario de contacto: compone un correo con los datos introducidos.
// El sitio es estático, así que no hay servidor donde enviarlo.
(function () {
  var form = document.getElementById('contactForm');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = function (n) { var el = form.elements[n]; return el ? el.value.trim() : ''; };
    var cuerpo = [
      'Nombre: ' + v('nombre'),
      'Negocio: ' + v('negocio'),
      'Teléfono: ' + v('telefono'),
      'Correo: ' + v('email'),
      'Sector: ' + v('sector'),
      'Me interesa: ' + v('interes'),
      '',
      v('mensaje')
    ].join('\n');
    var url = 'mailto:' + form.dataset.to +
      '?subject=' + encodeURIComponent('Solicitud de propuesta — ' + (v('negocio') || v('nombre') || 'web')) +
      '&body=' + encodeURIComponent(cuerpo);
    var msg = document.getElementById('formMsg');
    if (msg) msg.classList.add('show');
    window.location.href = url;
  });
})();
