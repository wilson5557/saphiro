//INICIO

var inicio = document.getElementById("Inicio");
var inicioLabel = document.getElementById("ver-inicio");

//PROPIETARIO

function Inicio()
{
  VerificarModulo();

  if(inicio.classList.contains("d-none") == true)
  {
    inicio.classList.remove("d-none");
    inicioLabel.classList.remove("d-none");
  }
}

function ShowModulosProp(param)
{
  var Opciones = document.getElementById("Opciones");

  //PUBLICACIONES
  var ListaPublicacion = document.getElementById("VerPublicaciones");
  var BtnPublicacion = document.getElementById("BtnShowPublicacion");
  var FormPublicacion = document.getElementById("FormPublicacion");
  var VolverPublicacion = document.getElementById('HidePublicacion');

  switch (param)
  {
    case 'ShowFormPublicacion':

      ListaPublicacion.classList.add("d-none");
      BtnPublicacion.classList.add("d-none");

      FormPublicacion.classList.remove("d-none");
      VolverPublicacion.classList.remove("d-none");
      break;

    case 'HideFormPublicacion':

      FormPublicacion.classList.add("d-none");
      VolverPublicacion.classList.add("d-none");

      ListaPublicacion.classList.remove("d-none");
      BtnPublicacion.classList.remove("d-none");

      break;

  }
}

var tipo_post = document.getElementById('id_tipo_post');
if (tipo_post) {
    tipo_post.addEventListener('change', function() {
        if (tipo_post.value == "ALQUILER") {
            document.getElementById('div_id_categoria_post').classList.remove("d-none")
            document.getElementById('id_categoria_post').disabled = false
            document.getElementById('id_categoria_post').required = false
        } else {
            document.getElementById('div_id_categoria_post').classList.add("d-none")
            document.getElementById('id_categoria_post').disabled = true
            document.getElementById('id_categoria_post').required = true
        }
    });
}

function Perfil(param)
{
    var inicio = document.getElementById("Inicio");
    var inicioLabel = document.getElementById("ver-inicio");
    var userProfileLabel = document.getElementById('perfil-user');
    var viewPerfilUsuario = document.getElementById('ViewUserProfile');
    var ChangePassUsuario = document.getElementById('ChangeUserPassword');
    var userCambioLabel = document.getElementById('user-change-pass');

    if (param == 'ChangePass') {
      inicio.classList.add('d-none');
      inicioLabel.classList.add('d-none');
      userProfileLabel.classList.add('d-none')
      viewPerfilUsuario.classList.add('d-none');
      ChangePassUsuario.classList.remove('d-none');
      userCambioLabel.classList.remove('d-none');
    }

    else if (param == 'CancelChangePass') {
      inicio.classList.remove('d-none');
      inicioLabel.classList.remove('d-none');
      ChangePassUsuario.classList.add('d-none');
      userCambioLabel.classList.add('d-none');
      perfilUser.classList.add('d-none');
      userProfileLabel.classList.add('d-none')
    }
    //---------------------------------------------------------------------------------------
    else if (param == 'Profile') {
      inicio.classList.add('d-none');
      inicioLabel.classList.add('d-none');
      viewPerfilUsuario.classList.remove('d-none');
      userProfileLabel.classList.remove('d-none');
    }
}

const aptoBoton = document.querySelectorAll('.apto');
aptoBoton.forEach(function(boton) {
  boton.addEventListener('click', function() {

    // Obtener todos los checkboxes con la misma clase
    var checkboxes = document.querySelectorAll('.checkbox');

    // Recorrer todos los checkboxes y deseleccionarlos
    if (checkboxes) {
        checkboxes.forEach(function(checkbox) {
          checkbox.checked = false;
        });
    }

    // Acciones a realizar cuando se seleccione un botón
    const aptoDeuda = boton.value;

    if (boton.classList.contains('square_selected')) {
        boton.classList.remove('square_selected');
    }

    boton.classList.add('square_selected');

    // Quitar la clase de los demás botones
    aptoBoton.forEach(function(otroBoton) {
      if (otroBoton !== boton) {
        otroBoton.classList.remove('square_selected');
      }
    });

    $.ajax({
        url: '/obtener_deudas/',
        data: {
            'aptoDeuda': aptoDeuda
        },
        success: function(response) {

            id_contenido = 'contenido_dom'+aptoDeuda.toString();
            var contenido = document.getElementById(id_contenido);

            const data_inmueble = document.getElementById('data_inmueble');

            if (response.cantidad_deudas > "0") {

                elemento = 'data_inmueble' + response.domicilio.id

                const data_inmueble = document.getElementById(elemento);

                if (data_inmueble) {
                    console.log('existe')
                } else {

                    var datos = "<div id='data_inmueble" + response.domicilio.id + "' class='col-sm-12' style='text-align: center;'><strong>Datos del Inmueble</strong></div>" +
                                "<div class='divider'></div>" +
                                "<div class='col-sm-6 mt-2'><strong>Ubicado en la torre:</strong> " + response.domicilio.torre + "</div>" +
                                "<div class='col-sm-6 mt-2'><strong>Piso:</strong> " + response.domicilio.piso + "</div>" +
                                "<div class='col-sm-6 mt-2'><strong>Tamaño:</strong> " + response.domicilio.size + "</div>" +
                                "<div class='col-sm-6 mt-2'><strong>Estacionamientos:</strong> " + response.domicilio.estacionamientos + "</div>" +
                                "<div class='col-sm-6 mt-2'><strong>Alicuota:</strong> " + response.domicilio.alicuota + "</div>" +
                                "<div class='col-sm-6 mt-2'><strong>Saldo (BS):</strong> " + response.domicilio.saldo_bs + "</div>" +
                                "<div class='col-sm-6 mt-2'><strong>Saldo (USD):</strong> " + response.domicilio.saldo_usd + "</div>" +
                                "<div class='col-sm-6 mt-2'><strong>Saldo (EUR):</strong> " + response.domicilio.saldo_eur + "</div>" +
                                "<div class='question col-sm-12 mt-3 align-left' id='question'><strong>Usted posee " + response.cantidad_deudas + " deudas pendientes. ¿Desea pagar las deudas o acreditar al saldo de la cuenta?</strong></div>"

                    contenido.insertAdjacentHTML('afterbegin', datos);

                    var btns = "<div class='col-sm-12 mt-2 d-flex text-center' style='justify-content: space-around;'>" +
                                "<a class='ver_deudas btn border btn-option text-center' style='width: 170px;' id='Ver_deudas'>Ver deudas</a>" +
                                "<a class='abonar btn border btn-option text-center btn-disabled' style='width: 170px;' id='Abonar'>Acreditar a la cuenta</a>"
                                "</div>"

                    contenido.querySelector('.select_moneda').insertAdjacentHTML('beforeend', btns);

                    var condoDiv = contenido.querySelector('#condo'); // Reemplaza '.pagar' con el selector del botón correspondiente
                    var cuotaDiv = contenido.querySelector('#cuota');

                    var deuda_condominio = contenido.querySelector('.condo');
                    var deuda_cuota = contenido.querySelector('.cuota');

                    let condo_id = 0
                    let cuota_id = 0

                    for (i = 0; i < response.deudas.length; i++) {

                        if (response.deudas[i].categoria_deuda == "CONDOMINIO") {

                            condoDiv.classList.remove('d-none');

                            var datos_deuda = "<li class='list-group-item d-flex' style='justify-content: space-between;'>" + response.deudas[i].concepto_deuda + "<div class='d-flex'><div id='monto_condo"+ condo_id +"' class='monto_condo'>"+ response.deudas[i].monto_deuda +"</div> <div id='tipo_moneda_condo"+ condo_id +"' class='tipo_moneda_condo ml-1'>" + response.deudas[i].tipo_moneda + "</div> <input id='seleccion_condominio"+ condo_id +"' type='checkbox' class='seleccion_condominio ml-3 checkbox' value='" + response.deudas[i].monto_deuda + "' data-id-deuda='" + response.deudas[i].id_deuda + "' name='montos_deudas' disabled></div></li>"
                            deuda_condominio.insertAdjacentHTML('beforeend', datos_deuda);
                            condo_id++;

                        } else {

                            cuotaDiv.classList.remove('d-none');

                            var datos_deuda = "<li class='list-group-item d-flex' style='justify-content: space-between;'>" + response.deudas[i].concepto_deuda + "<div class='d-flex'><div id='monto_cuota"+ cuota_id +"' class='monto_cuota'>"+ response.deudas[i].monto_deuda +"</div> <div id='tipo_moneda_cuota"+ cuota_id +"' class='tipo_moneda_cuota ml-1'>" + response.deudas[i].tipo_moneda + "</div> <input id='seleccion_cuota"+ cuota_id +"' type='checkbox' class='seleccion_cuota ml-3 checkbox' value='" + response.deudas[i].monto_deuda + "' data-id-deuda='" + response.deudas[i].id_deuda + "' name='montos_deudas' disabled></div></li>"
                            deuda_cuota.insertAdjacentHTML('beforeend', datos_deuda);
                            cuota_id++;
                        }

                    }

                    //Ver deudas
                    const deudasBoton = contenido.querySelector('.ver_deudas');
                    const abonarBoton = contenido.querySelector('.abonar');
                    const opcionesDiv = contenido.querySelector('.opcionesBtn');
                    deudasBoton.addEventListener('click', function() {
                        deudasBoton.classList.add('d-none');
                        opcionesDiv.appendChild(abonarBoton);
                        contenido.querySelector('.question').classList.add('d-none');
                        contenido.querySelector('.deudas_dom').classList.remove('d-none');
                    });
                }

            } else {

                elemento = 'data_inmueble_sin_deudas' + response.domicilio.id
                const data_inmueble_sin_deudas = document.getElementById(elemento);
                const abonarExistenteBtn = contenido.querySelector('.abonar');

                if (data_inmueble_sin_deudas || abonarExistenteBtn) {
                    return;
                }

                var datos = "<div class='col-sm-12' style='text-align: center;'><strong>Datos del Inmueble</strong></div>" +
                            "<div class='divider'></div>" +
                            "<div class='col-sm-6 mt-2'><strong>Ubicado en la torre:</strong> " + response.domicilio.torre + "</div>" +
                            "<div class='col-sm-6 mt-2'><strong>Piso:</strong> " + response.domicilio.piso + "</div>" +
                            "<div class='col-sm-6 mt-2'><strong>Tamaño:</strong> " + response.domicilio.size + "</div>" +
                            "<div class='col-sm-6 mt-2'><strong>Estacionamientos:</strong> " + response.domicilio.estacionamientos + "</div>" +
                            "<div class='col-sm-6 mt-2'><strong>Alicuota:</strong> " + response.domicilio.alicuota + "</div>" +
                            "<div class='col-sm-6 mt-2'><strong>Saldo (BS):</strong> " + response.domicilio.saldo_bs + "</div>" +
                            "<div class='col-sm-6 mt-2'><strong>Saldo (USD):</strong> " + response.domicilio.saldo_usd + "</div>" +
                            "<div class='col-sm-6 mt-2'><strong>Saldo (EUR):</strong> " + response.domicilio.saldo_eur + "</div>" +
                            "<div class='col-sm-12 mt-3 text-center'><strong>Usted no posee deudas pendientes. ¿Desea abonar al saldo de la cuenta?</strong></div>"

                contenido.insertAdjacentHTML('afterbegin', datos);
                // contenido.innerHTML = datos;

                btn = "<div class='col-sm-12 mt-2 d-flex text-center' style='justify-content: space-around;'>" +
                      "<a class='abonar btn border btn-option btn-disabled text-center' style='width: 170px;' id='Abonar' disabled>Acreditar a la cuenta</a>" +
                      "</div>"

                contenido.insertAdjacentHTML('beforeend', btn)

            }

            const pagarBoton = contenido.querySelectorAll('.pagar');
            const abonarBoton = contenido.querySelectorAll('.abonar');
            const checkboxes = contenido.querySelectorAll('.checkbox');
            const montoPago = document.getElementById('montoFinal');
            let ids = []
            const tipo_transaccion = document.getElementById('tipo_transaccion');

            //Pagar
            pagarBoton.forEach(pago => {
                pago.addEventListener('click', function() {
                    tipo_transaccion.value = "PAGO";
                    var deudas_seleccionadas = ids.join(',');
                    document.getElementById('deudas').value = deudas_seleccionadas
                    document.getElementById('SeleccionarDomicilio').classList.add('d-none');
                    document.getElementById('PagoDeudas').classList.remove('d-none');
                });
            });

            //Abonar
            abonarBoton.forEach(abono => {
                abono.addEventListener('click', function() {
                    if (abono.classList.contains('btn-disabled')) {
                        alert('Seleccione primero un tipo de moneda');
                    } else {
                        tipo_transaccion.value = "ABONO";
                        document.getElementById('SeleccionarDomicilio').classList.add('d-none');
                        document.getElementById('PagoDeudas').classList.remove('d-none');
                    }
                });
            });

            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', () => {
                    let total = 0;
                    checkboxes.forEach(checkbox => {
                        if (checkbox.checked) {
                            total += parseFloat(checkbox.value);
                            const id = checkbox.getAttribute('data-id-deuda');
                            if (ids.includes(id)) {
                                console.log('Ya está.');
                            } else {
                                ids.push(id);
                            }
                        }
                    });
                    montoPago.value = total;
                    montoPago.max = total;
                    const container = checkbox.closest('.data_domicilio');
                    const pagar = container.querySelector('.pagar');
                    if (montoPago.value == 0) {
                        pagar.classList.add('d-none')
                    } else {
                        pagar.classList.remove('d-none')
                    }
                });
            });
        },
        error: function() {
            // Manejo de errores
            alert('Hubo un inconveniente al obtener los datos del inmueble. Por favor intente más tarde.');
        }
    });
  });
});





