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
      ') llega a tu cuenta el ' + DIAS[siguienteHabil(d)] + '.';
  }
  importe.addEventListener('input', pintar);
  dia.addEventListener('change', pintar);
  pintar();
})();

// Simulador de tarifas: tramo según la facturación anual con tarjeta,
// comisión por cobro = máximo(ticket × tarifa, 0,05 €), +0,03 € por
// operación si hay integración y mínimo mensual de 29,95 € sobre las comisiones.
(function () {
  var caja = document.getElementById('simTarifa');
  if (!caja) return;
  var TRAMOS = JSON.parse(caja.dataset.tramos);
  var MIN_OP = 0.05, INTEGRACION = 0.03, MIN_MES = 29.95;
  var cto = caja.querySelector('[name=cto]');
  var ticket = caja.querySelector('[name=ticket]');
  var integ = caja.querySelector('[name=integracion]');
  var r = function (k) { return caja.querySelector('[data-r=' + k + ']'); };
  function num(el) { return parseFloat(String(el.value).replace(/\./g, '').replace(',', '.')) || 0; }
  function eur(x) { return x.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' }); }
  function eur3(x) { x = Math.floor(x * 1000 + 1e-6) / 1000; return x.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 3 }) + ' €'; }
  function pct(x) { return (x * 100).toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' %'; }
  function pintar() {
    var anual = num(cto), tk = num(ticket);
    if (anual <= 0 || tk <= 0) {
      ['ventas', 'ops', 'tarifa', 'porop', 'total', 'efectivo'].forEach(function (k) { r(k).textContent = '—'; });
      r('nota').textContent = 'Introduce tu facturación anual y tu ticket medio.';
      return;
    }
    var tramo = TRAMOS[TRAMOS.length - 1];
    for (var i = 0; i < TRAMOS.length; i++) {
      if (anual <= TRAMOS[i][1]) { tramo = TRAMOS[i]; break; }
    }
    var tarifa = tramo[2];
    var ventas = anual / 12;
    var ops = ventas / tk;
    var porOp = Math.max(tk * tarifa, MIN_OP);
    var comisiones = porOp * ops;
    var aplicaMinimo = comisiones < MIN_MES;
    var total = Math.max(comisiones, MIN_MES) + (integ.checked ? INTEGRACION * ops : 0);
    r('ventas').textContent = eur(ventas);
    r('ops').textContent = Math.round(ops).toLocaleString('es-ES');
    r('tarifa').textContent = pct(tarifa);
    r('porop').textContent = eur3(porOp) + (integ.checked ? ' + 0,03 €' : '');
    r('total').textContent = eur(total);
    r('efectivo').textContent = pct(total / ventas);
    var notas = [];
    if (tk * tarifa < MIN_OP) notas.push('Con este ticket se aplica el mínimo de 0,05 € por cobro.');
    if (aplicaMinimo) notas.push('Tus comisiones no llegan al mínimo mensual de 29,95 €, así que se aplica el mínimo.');
    if (anual > TRAMOS[TRAMOS.length - 1][1]) notas.push('Con más de 1.200.000 € al año te preparamos una tarifa a medida; el cálculo usa el último tramo como referencia.');
    r('nota').textContent = notas.join(' ');
  }
  [cto, ticket].forEach(function (el) { el.addEventListener('input', pintar); });
  integ.addEventListener('change', pintar);
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
