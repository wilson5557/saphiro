// CODIGO PARA PARTE DE PROPIETARIOS E INQUILINOS
// Dom de modulos
var inicio = document.getElementById("Inicio");
var alquiler = document.getElementById("Alquiler");
var venta = document.getElementById("Venta");
var servicios = document.getElementById("Servicios");
var pagos = document.getElementById("Pagos");
var recibos = document.getElementById("Recibos")
var perfilUser = document.getElementById('User-Profile');

// Label de modulos
var inicioLabel = document.getElementById("ver-inicio");
var alquilerLabel = document.getElementById("publicar-alquiler");
var ventaLabel = document.getElementById("publicar-venta");
var serviciosLabel = document.getElementById("publicar-servicios");
var reportarLabel = document.getElementById("reportar-pago");
var recibosLabel = document.getElementById("ver-recibos");
var userProfileLabel = document.getElementById('perfil-user');
var userCambioLabel = document.getElementById('user-change-pass');

// BOTON DE MOSTRAR PERFIL Y CAMBIAR CONTRASEÑA
var BtnShowPerfilUsuario = document.getElementById('ShowUserProfile');
var btnShowCambiarPassUsuario = document.getElementById('CambiarUserPass')
var btnCancelCambiarPassUsuario = document.getElementById('CancelPasswordChangeUsuario');
// MODULOS
var ChangePassUsuario = document.getElementById('ChangeUserPassword');
var viewPerfilUsuario = document.getElementById('ViewUserProfile');

// Funciones
// Esta función verifica si el modulo no tiene la clase d-none (display: none) y la coloca en caso de cumplirse la condición
function VerificarModulo()
{
  if(inicio.classList.contains("d-none") == false)
  {
    inicio.classList.add("d-none");
    inicioLabel.classList.add("d-none");
  }
  else if(pagos.classList.contains("d-none") == false)
  {
    pagos.classList.add("d-none");
    reportarLabel.classList.add("d-none");
  }
  else if(recibos.classList.contains("d-none") == false)
  {
    recibos.classList.add("d-none");
    recibosLabel.classList.add("d-none");
  }
  else if(alquiler.classList.contains("d-none") == false)
  {
    alquiler.classList.add("d-none");
    alquilerLabel.classList.add("d-none");
  }
  else if(venta.classList.contains("d-none") == false)
  {
    venta.classList.add("d-none");
    ventaLabel.classList.add("d-none");
  }
  else if(servicios.classList.contains("d-none") == false)
  {
    servicios.classList.add("d-none");
    serviciosLabel.classList.add("d-none");
  }
  else if(perfilUser.classList.contains("d-none") == false)
  {
    perfilUser.classList.add("d-none");
    userProfileLabel.classList.add("d-none");
    userCambioLabel.classList.add("d-none");
    viewPerfilUsuario.classList.add('d-none');
  }
}

function Publicar(modulo)
{
  // Verificamos el modulo y lo escondemos
  VerificarModulo();
  // Luego mediante el switch vemos el caso que se cumpla y lo mostramos
  switch (modulo)
  {
    case 'alquiler':
      alquiler.classList.remove("d-none");
      alquilerLabel.classList.remove("d-none");
      break;

    case 'venta':
      venta.classList.remove("d-none");
      ventaLabel.classList.remove("d-none");
      break;

    case 'servicios':
      servicios.classList.remove("d-none");
      serviciosLabel.classList.remove("d-none");
      break;
  }
}

function Inicio()
{
  VerificarModulo();

  if(inicio.classList.contains("d-none") == true)
  {
    inicio.classList.remove("d-none");
    inicioLabel.classList.remove("d-none");
  }
}

function Pagos()
{
  VerificarModulo();

  if(pagos.classList.contains("d-none") == true)
  {
    pagos.classList.remove("d-none");
    reportarLabel.classList.remove("d-none");
  }
}

function Recibos()
{
  VerificarModulo();

  if(recibos.classList.contains("d-none") == true)
  {
    recibos.classList.remove("d-none");
    recibosLabel.classList.remove("d-none");
  }
}

function Perfil(param)
{
    if (param === 'ChangePass') {
      inicio.classList.add('d-none');
      inicioLabel.classList.add('d-none');
      userProfileLabel.classList.add('d-none')
      viewPerfilUsuario.classList.add('d-none');
      ChangePassUsuario.classList.remove('d-none');
      userCambioLabel.classList.remove('d-none');
    }

    else if (param === 'CancelChangePass') {
      inicio.classList.remove('d-none');
      inicioLabel.classList.remove('d-none');
      ChangePassUsuario.classList.add('d-none');
      userCambioLabel.classList.add('d-none');
      perfilUser.classList.add('d-none');
      userProfileLabel.classList.add('d-none')
    }
    //---------------------------------------------------------------------------------------
    else if (param === 'Profile') {
      inicio.classList.add('d-none');
      inicioLabel.classList.add('d-none');
      viewPerfilUsuario.classList.remove('d-none');
      userProfileLabel.classList.remove('d-none');
    }
}

// ------------------------------------------------------------------------------------------------------
// CODIGO PARA PARTE DE ADMINISTRADOR

// FUNCIONES
// Esta función verifica si el modulo no tiene la clase d-none (display: none) y la coloca en caso de cumplirse la condición
function VerificarAdminModulo()
{
  // Modulos
  var inicioAdmin = document.getElementById("InicioAdmin");
  var nuevaNoticia = document.getElementById("Nueva-Noticia");
  var listaNoticia = document.getElementById("Lista-Noticias");
  var notificacion = document.getElementById("Notificacion");
  var bancos = document.getElementById("Bancos");
  var gastos = document.getElementById("Gastos");
  var ingresos = document.getElementById("Ingresos");
  var deudas = document.getElementById("Deudas");
  var propietarios = document.getElementById("Propietarios");
  var edificio = document.getElementById("Edificio");
  var reportes = document.getElementById("Reportes")
  var cuentas = document.getElementById("Cuentas");
  var perfilAdmin = document.getElementById('Profile');

  if(!inicioAdmin.classList.contains("d-none"))
  {
    inicioAdmin.classList.add("d-none");
    inicioAdminLabel.classList.add("d-none");
  }
  else if(!nuevaNoticia.classList.contains("d-none"))
  {
    nuevaNoticia.classList.add("d-none");
    nuevaNoticiaLabel.classList.add("d-none");
  }
  else if(!listaNoticia.classList.contains("d-none"))
  {
    listaNoticia.classList.add("d-none");
    listaNoticiaLabel.classList.add("d-none");
    listaNoticiaLabel.classList.add("d-none");
  }
  else if(!bancos.classList.contains("d-none"))
  {
    bancos.classList.add("d-none");
    bancosLabel.classList.add("d-none");
  }
  else if(!gastos.classList.contains("d-none"))
  {
    gastos.classList.add("d-none");
    gastosLabel.classList.add("d-none");
  }
  else if(!ingresos.classList.contains("d-none"))
  {
    ingresos.classList.add("d-none");
    ingresosLabel.classList.add("d-none");
  }
  else if(!deudas.classList.contains("d-none"))
  {
    deudas.classList.add("d-none");
    deudasLabel.classList.add("d-none");
  }
  else if(!propietarios.classList.contains("d-none"))
  {
    propietarios.classList.add("d-none");
    propietariosLabel.classList.add("d-none")
    Opciones.classList.remove("d-none")
  }
  else if(!edificio.classList.contains("d-none"))
  {
    edificio.classList.add("d-none");
    edificioLabel.classList.add("d-none");
  }
  else if(!reportes.classList.contains("d-none"))
  {
    reportes.classList.add("d-none");
    reportesLabel.classList.add("d-none");
  }
  else if(!cuentas.classList.contains("d-none"))
  {
    cuentas.classList.add("d-none");
    cuentasLabel.classList.add("d-none");
  }
  else if(!perfilAdmin.classList.contains("d-none"))
  {
    perfilAdmin.classList.add("d-none");
    profileLabel.classList.add("d-none");
    cambioLabel.classList.add("d-none");
    viewPerfil.classList.add('d-none');
  }
}

var section_piso = document.getElementById('Pisos');
var section_torres = document.getElementById('cantidad_torres');
var yes_or_no = document.querySelectorAll('.radio_yes_or_no');
var OptionApartamento = document.getElementById('OptionApartamento');
var pisos_value = document.getElementById('pisos_value');
var cant_torres_value = document.getElementById('cant_torres_value');
var tipo_unidad = document.querySelector('.opTipoUnidad');

if(tipo_unidad)
{
  tipo_unidad.addEventListener('change',function () {
  if (tipo_unidad.value == "APARTAMENTOS")
  {
    OptionApartamento.classList.remove('d-none');
    section_piso.classList.remove('d-none');
    pisos_value.value = "";
    yes_or_no.forEach(function(radio) {
        radio.checked = false;
    });
  } else {
    OptionApartamento.classList.add('d-none');
    section_piso.classList.add('d-none');
    section_torres.classList.add('d-none');
    pisos_value.value = 0;
    cant_torres_value.value = 0;
    yes_or_no.forEach(function(radio) {
        radio.checked = false;
    });
  }
});
}

function OpcionesCondominio(param)
{
  var ver_unidad_condo = document.getElementById('VerCondominios');
  var agregar_unidad_condo = document.getElementById('AgregarCondominio');

  switch (param)
  {
    case 'form_condo':
      agregar_unidad_condo.classList.remove('d-none');
      ver_unidad_condo.classList.add('d-none');
      break;

    case 'list_condo':
      ver_unidad_condo.classList.remove('d-none');
      agregar_unidad_condo.classList.add('d-none');
      break;
  }
}

function SetApartamento(param)
{
  switch (param) {
    case 'Si':
      cant_torres_value.value = "";
      section_torres.classList.remove('d-none');
      break;

    case 'No':
      cant_torres_value.value = 0;
      section_torres.classList.add('d-none');
      break;
  }
}

function Gestionar(modulo)
{
  VerificarAdminModulo();

  // Modulos
  var inicioAdmin = document.getElementById("InicioAdmin");
  var nuevaNoticia = document.getElementById("Nueva-Noticia");
  var listaNoticia = document.getElementById("Lista-Noticias");
  var notificacion = document.getElementById("Notificacion");
  var bancos = document.getElementById("Bancos");
  var gastos = document.getElementById("Gastos");
  var ingresos = document.getElementById("Ingresos");
  var deudas = document.getElementById("Deudas");
  var propietarios = document.getElementById("Propietarios");
  var edificio = document.getElementById("Edificio");
  var reportes = document.getElementById("Reportes")
  var cuentas = document.getElementById("Cuentas");
  var perfilAdmin = document.getElementById('Profile');

  // Label de modulos
  var inicioAdminLabel = document.getElementById("inicio-admin");
  var nuevaNoticiaLabel = document.getElementById("publicar-noticia");
  var listaNoticiaLabel = document.getElementById("gestionar-noticias");
  var notificacionLabel = document.getElementById("publicar-notificacion");
  var bancosLabel = document.getElementById("gestionar-bancos");
  var gastosLabel = document.getElementById("gestionar-gastos");
  var ingresosLabel = document.getElementById("gestionar-ingresos");
  var deudasLabel = document.getElementById("gestionar-deudas");
  var propietariosLabel = document.getElementById("gestionar-propietarios");
  var edificioLabel = document.getElementById("gestionar-edificio");
  var cuentasLabel = document.getElementById("gestionar-usuarios");
  var reportesLabel = document.getElementById('gestionar-reportes');
  var profileLabel = document.getElementById('perfil-admin');
  var cambioLabel = document.getElementById('change-pass');

  switch(modulo)
  {
    case 'inicio':
      inicioAdmin.classList.remove("d-none");
      inicioAdminLabel.classList.remove("d-none");
      break;

    case 'nueva-noticia':
      nuevaNoticia.classList.remove("d-none");
      nuevaNoticiaLabel.classList.remove("d-none");
      break;

    case 'lista-noticia':
      listaNoticia.classList.remove("d-none");
      listaNoticiaLabel.classList.remove("d-none");
      break;

    case 'bancos':
      bancos.classList.remove("d-none");
      bancosLabel.classList.remove("d-none");
      break;

    case 'gastos':
      gastos.classList.remove("d-none");
      gastosLabel.classList.remove("d-none");
      break;

    case 'ingresos':
      ingresos.classList.remove("d-none");
      ingresosLabel.classList.remove("d-none");
      break;

    case 'propietarios':
      propietarios.classList.remove("d-none");
      propietariosLabel.classList.remove("d-none");
      Opciones.classList.add("d-none");
      break;

    case 'edificio':
      edificio.classList.remove("d-none");
      edificioLabel.classList.remove("d-none");
      break;

    case 'cuentas':
      cuentas.classList.remove("d-none");
      cuentasLabel.classList.remove("d-none");
      break;

    case 'reportes':
      reportes.classList.remove("d-none");
      reportesLabel.classList.remove("d-none");
      break;
  }
}

// Variables de sección de gestion (Bancos, cuotas extras, noticias y usuarios)

function ShowOrHide(param)
{
  var Opciones = document.getElementById("Opciones");

  //INICIO
  var inicioAdmin = document.getElementById("InicioAdmin");
  var inicioAdminLabel = document.getElementById("inicio-admin");
  var perfilAdmin = document.getElementById('Profile');
  var profileLabel = document.getElementById('perfil-admin');
  var cambioLabel = document.getElementById('change-pass');

  //DOMICILIOS
  var domicilios = document.getElementById("Bancos");
  var BtnShowDom = document.getElementById("ShowDomicilios");
  var BtnHideDom = document.getElementById("HideDomicilios");
  var ListaDom = document.getElementById("VerDomicilios");
  var FormDom = document.getElementById("AgregarDomicilio");

  //BANCOS
  var bancos = document.getElementById("Bancos");
  var BtnShowBank = document.getElementById("ShowBank");
  var BtnHideBank = document.getElementById("HideBank");
  var ListaBank = document.getElementById("VerBancos");
  var FormBank = document.getElementById("AgregarBancos");

  //GASTOS
  var gastos = document.getElementById("Gastos");
  var BtnShowGastos = document.getElementById("ShowGastos");
  var BtnHideGastos = document.getElementById("HideGastos");
  var ListaGastos = document.getElementById("VerGastos");
  var FormGastos = document.getElementById("AgregarGastos");

  //INGRESOS
  var ingresos = document.getElementById("Ingresos");
  var BtnShowIngresos = document.getElementById("ShowIngresos");
  var BtnHideIngresos = document.getElementById("HideIngresos");
  var ListaIngresos = document.getElementById("VerIngresos");
  var FormIngresos = document.getElementById("AgregarIngresos");

  //DEUDAS
  // var BtnShowDeudas = document.getElementById("ShowDeudas");
  var BtnHideDeudas = document.getElementById("HideDeudas");
  var ListaDeudas = document.getElementById("VerDeudas");
  var FormDeudas = document.getElementById("AgregarDeudas");
  var VerPropietariosMorosos = document.getElementById("VerPropietariosMorosos");
  var BtnShowMorosoPropietarios = document.getElementById("ShowMorosoPropietarios");

  //FONDOS
  var fondos = document.getElementById("Fondos");
  var BtnShowFondos = document.getElementById("ShowFondos");
  var ShowAgregarFondos = document.getElementById("ShowAgregarFondos")
  var BtnHideFondos = document.getElementById("HideFondos");
  var ListaFondos = document.getElementById("VerFondos");
  var FormFondos = document.getElementById("AgregarFondos");
  var HideModuloFondos = document.getElementById("HideModuloFondos");

  //PROPIETARIOS
  var BtnShowPropietarios = document.getElementById("ShowPropietarios");
  var BtnHidePropietarios = document.getElementById("HidePropietarios");
  var BtnShowMovPropietarios = document.getElementById("ShowMovPropietarios");
  var ListaPropietarios = document.getElementById("VerPropietarios");
  var ListaMovimientos = document.getElementById("VerMovimientos");
  var FormPropietarios = document.getElementById("AgregarPropietarios");
  var BtnShowPropietariosConf = document.getElementById("ShowPropietariosConf");
  var BtnHidePropietariosConf = document.getElementById("HidePropietariosConf");
  var FormPropietariosConf = document.getElementById("AgregarPropietariosConf");

  //TORRES
  var BtnShowTorres = document.getElementById("ShowTorres");
  var BtnHideTorres = document.getElementById("HideTorres");
  var ListaTorres = document.getElementById("VerTorres");
  var FormTorres = document.getElementById("AgregarTorres");

  //NOTICIAS
  var BtnShowNoticia = document.getElementById("ShowNoticia");
  var BtnHideNoticia = document.getElementById("HideNoticia");
  var ListaNoticia = document.getElementById("VerNoticias");
  var FormNoticia = document.getElementById("AgregarNoticias");

  //CUENTAS DE USUARIOS
  var BtnShowUsuarios = document.getElementById("ShowUsuarios");
  var BtnHideUsuarios = document.getElementById("HideUsuarios");
  var ListaUsuarios = document.getElementById("VerUsuarios");
  var FormUsuarios = document.getElementById("AgregarUsuarios");

  //PERFIL Y CAMBIAR CONTRASEÑA
  var BtnShowPerfil = document.getElementById('ShowProfile');
  var btnShowCambiarPass = document.getElementById('CambiarPass');
  var btnCancelCambiarPass = document.getElementById('CancelPasswordChange');
  var ChangePass = document.getElementById('ChangePassword');
  var viewPerfil = document.getElementById('ViewProfile');

  //FORMULARIO DE ACTUALIZACION DE DATOS DEL EDIFICIO
  var BtnShowEdificioForm = document.getElementById('EditEdificioInfo');
  var FormEdificioInfo = document.getElementById('FormEdificioInfo');
  var EdificioInfo = document.getElementById('EdificioInfo');

  switch (param)
  {
    case 'HideListaDomicilios':

      BtnHideDom.classList.add("d-none");
      ListaDom.classList.add("d-none");

      FormDom.classList.remove("d-none");
      BtnShowDom.classList.remove("d-none");
      break;

    case 'ShowFormPropietariosConf':
      if (FormPropietariosConf) FormPropietariosConf.classList.remove("d-none");
      if (BtnShowPropietariosConf) BtnShowPropietariosConf.classList.add("d-none");
      if (BtnHidePropietariosConf) BtnHidePropietariosConf.classList.remove("d-none");
      break;

    case 'HideFormPropietariosConf':
      if (FormPropietariosConf) FormPropietariosConf.classList.add("d-none");
      if (BtnShowPropietariosConf) BtnShowPropietariosConf.classList.remove("d-none");
      if (BtnHidePropietariosConf) BtnHidePropietariosConf.classList.add("d-none");
      break;

    case 'ShowListaDomicilios':

      BtnShowDom.classList.add("d-none");
      FormDom.classList.add("d-none");

      ListaDom.classList.remove("d-none");
      BtnHideDom.classList.remove("d-none");
      break;
    //-----------------------------------------------------------------------------

    case 'HideListaBancos':

      BtnHideBank.classList.add("d-none");
      ListaBank.classList.add("d-none");

      FormBank.classList.remove("d-none");
      BtnShowBank.classList.remove("d-none");
      Opciones.classList.remove('d-none');
      break;

    case 'ShowListaBancos':

      BtnShowBank.classList.add("d-none");
      FormBank.classList.add("d-none");

      bancos.classList.remove('col-lg-9');
      ListaBank.classList.remove("d-none");
      BtnHideBank.classList.remove("d-none");

      break;
    //-----------------------------------------------------------------------------
    case 'HideListaGastos':

      BtnHideGastos.classList.add("d-none");
      ListaGastos.classList.add("d-none");

      FormGastos.classList.remove("d-none");
      BtnShowGastos.classList.remove("d-none");

      break;

    case 'ShowListaGastos':

      BtnShowGastos.classList.add("d-none");
      FormGastos.classList.add("d-none");

      ListaGastos.classList.remove("d-none");
      BtnHideGastos.classList.remove("d-none");

      break;
    //----------------------------------------------------------------------------------
    case 'HideListaIngresos':

      BtnHideIngresos.classList.add("d-none");
      ListaIngresos.classList.add("d-none");

      FormIngresos.classList.remove("d-none");
      BtnShowIngresos.classList.remove("d-none");

      break;

    case 'ShowListaIngresos':

      BtnShowIngresos.classList.add("d-none");
      FormIngresos.classList.add("d-none");

      ListaIngresos.classList.remove("d-none");
      BtnHideIngresos.classList.remove("d-none");

      break;
    //----------------------------------------------------------------------------------
    case 'HideListaFondos':

      BtnHideFondos.classList.add("d-none");
      ListaFondos.classList.add("d-none");

      FormFondos.classList.remove("d-none");
      BtnShowFondos.classList.remove("d-none");
      ShowAgregarFondos.classList.remove("d-none");
      break;

    case 'ShowListaFondos':

      BtnShowFondos.classList.add("d-none");
      FormFondos.classList.add("d-none");

      ListaFondos.classList.remove("d-none");
      BtnHideFondos.classList.remove("d-none");

      break;
    //----------------------------------------------------------------------------------
    case 'HideFormPropietarios':

      FormPropietarios.classList.add("d-none");
      BtnShowPropietarios.classList.add("d-none");
      ListaMovimientos.classList.add("d-none");

      BtnHidePropietarios.classList.remove('d-none');
      ListaPropietarios.classList.remove("d-none");
      BtnShowMovPropietarios.classList.remove("d-none");

      break;

    case 'ShowFormPropietarios':

      BtnHidePropietarios.classList.add("d-none");
      ListaPropietarios.classList.add("d-none");
      ListaMovimientos.classList.add("d-none");

      BtnShowPropietarios.classList.remove("d-none");
      BtnShowMovPropietarios.classList.remove("d-none");
      FormPropietarios.classList.remove("d-none");

      break;

    case 'HideAllPropietarios':

      ListaPropietarios.classList.add("d-none");
      BtnShowPropietarios.classList.add("d-none");
      FormPropietarios.classList.add("d-none");
      BtnShowMovPropietarios.classList.add("d-none");

      BtnHidePropietarios.classList.remove('d-none');
      BtnShowPropietarios.classList.remove("d-none");
      ListaMovimientos.classList.remove("d-none");

      break;

    case 'HideListaTorres':

      BtnHideTorres.classList.add("d-none");
      ListaTorres.classList.add("d-none");

      FormTorres.classList.remove("d-none");
      BtnShowTorres.classList.remove("d-none");
      break;

    case 'ShowListaTorres':

      BtnShowTorres.classList.add("d-none");
      FormTorres.classList.add("d-none");

      ListaTorres.classList.remove("d-none");
      BtnHideTorres.classList.remove("d-none");
      break;

    //----------------------------------------------------------------------------------
    case 'HideUsuarios':

      BtnHideUsuarios.classList.add("d-none");
      ListaUsuarios.classList.add("d-none");

      FormUsuarios.classList.remove("d-none");
      BtnShowUsuarios.classList.remove("d-none");

      break;

    case 'ShowUsuarios':

      BtnShowUsuarios.classList.add("d-none");
      FormUsuarios.classList.add("d-none");

      ListaUsuarios.classList.remove("d-none");
      BtnHideUsuarios.classList.remove("d-none");

      break;

    case 'HideListaNoticias':

      BtnHideNoticia.classList.add("d-none");
      ListaNoticia.classList.add("d-none");

      FormNoticia.classList.remove("d-none");
      BtnShowNoticia.classList.remove("d-none");

      break;

    case 'ShowListaNoticias':

      FormNoticia.classList.add("d-none");
      BtnShowNoticia.classList.add("d-none");

      BtnHideNoticia.classList.remove("d-none");
      ListaNoticia.classList.remove("d-none");

      break;

    //-------------------------------------------------------------------------------------
    case 'ChangePass':
      inicioAdmin.classList.add('d-none');
      inicioAdminLabel.classList.add('d-none');
      profileLabel.classList.add('d-none')
      perfilAdmin.classList.remove('d-none');
      ChangePass.classList.remove('d-none');
      cambioLabel.classList.remove('d-none');
      break;
    case 'CancelChangePass':
      ChangePass.classList.add('d-none');
      cambioLabel.classList.add('d-none');
      perfilAdmin.classList.add('d-none');
      profileLabel.classList.add('d-none')
      inicioAdmin.classList.remove('d-none');
      inicioAdminLabel.classList.remove('d-none');
      break;
    //---------------------------------------------------------------------------------------
    case 'Profile':
      inicioAdmin.classList.add('d-none');
      inicioAdminLabel.classList.add('d-none');
      perfilAdmin.classList.remove('d-none');
      viewPerfil.classList.remove('d-none');
      profileLabel.classList.remove('d-none');
      break;

    case 'EditEdificioInfo':
      EdificioInfo.classList.add('d-none');
      FormEdificioInfo.classList.remove('d-none');
      break;

    //---------------------------------------------------------------------------------------

    case 'ShowListaDeudas':
      // BtnShowDeudas.classList.add('d-none');
      FormDeudas.classList.add('d-none');
      VerPropietariosMorosos.classList.add('d-none');

      BtnShowMorosoPropietarios.classList.remove('d-none');
      BtnHideDeudas.classList.remove('d-none');
      ListaDeudas.classList.remove('d-none');
      break;

    case 'HideListaDeudas':
      BtnHideDeudas.classList.add('d-none');
      ListaDeudas.classList.add('d-none');
      VerPropietariosMorosos.classList.add('d-none');

      BtnShowMorosoPropietarios.classList.remove('d-none');
      // BtnShowDeudas.classList.remove('d-none');
      FormDeudas.classList.remove('d-none');
      break;

    case 'ShowMoroPropietarios':
      ListaDeudas.classList.add('d-none');
      BtnShowMorosoPropietarios.classList.add('d-none');
      FormDeudas.classList.add('d-none');

      VerPropietariosMorosos.classList.remove('d-none');
      BtnHideDeudas.classList.remove('d-none');
      // BtnShowDeudas.classList.remove('d-none');
      break;
  }
}

function ConfMenu(param) {
  function clearConfigTabParam() {
    if (param === 'ShowPropietarios') return;
    if (window.location.pathname.indexOf('/home/administrar/configuracion/') === -1) return;

    var url = new URL(window.location.href);
    if (!url.searchParams.has('tab')) return;

    url.searchParams.delete('tab');
    var next = url.pathname;
    var search = url.searchParams.toString();
    if (search) next += '?' + search;
    if (url.hash) next += url.hash;
    window.history.replaceState({}, '', next);
  }

  clearConfigTabParam();

  function resetPropietariosConf() {
    var verPropConf = document.getElementById("VerPropietariosConf");
    var formPropConf = document.getElementById("AgregarPropietariosConf");
    var btnShowPropConf = document.getElementById("ShowPropietariosConf");
    var btnHidePropConf = document.getElementById("HidePropietariosConf");
    if (verPropConf) verPropConf.classList.add("d-none");
    if (formPropConf) formPropConf.classList.add("d-none");
    if (btnShowPropConf) btnShowPropConf.classList.remove("d-none");
    if (btnHidePropConf) btnHidePropConf.classList.add("d-none");
  }

  var condominio = document.getElementById("Condominio");
  var bancos = document.getElementById("Bancos");
  var torres = document.getElementById("Torres");
  var domicilios = document.getElementById("Domicilios");
  var precios = document.getElementById("Precios");
  var tasas = document.getElementById("Tasas");
  var recargos = document.getElementById("Recargos");
  var propietarios = document.getElementById("Propietarios");
  var btn_condominio = document.getElementById("btn_condominio");
  var btn_banco = document.getElementById("btn_bancos");
  var btn_torre = document.getElementById("btn_torres");
  var btn_domicilio = document.getElementById("btn_domicilios");
  var btn_precio = document.getElementById("btn_precios");
  var btn_tasa = document.getElementById("btn_tasas");
  var btn_recargo = document.getElementById("btn_recargos");
  var btn_propietarios = document.getElementById("btn_propietarios_conf");

  function resetConfigButtons() {
    if (btn_condominio) btn_condominio.classList.remove("btn-option-selected");
    if (btn_banco) btn_banco.classList.remove("btn-option-selected");
    if (btn_torre) btn_torre.classList.remove("btn-option-selected");
    if (btn_domicilio) btn_domicilio.classList.remove("btn-option-selected");
    if (btn_precio) btn_precio.classList.remove("btn-option-selected");
    if (btn_tasa) btn_tasa.classList.remove("btn-option-selected");
    if (btn_recargo) btn_recargo.classList.remove("btn-option-selected");
    if (btn_propietarios) btn_propietarios.classList.remove("btn-option-selected");
  }

  switch (param)
  {
    default:
      resetConfigButtons();
      break;
    case 'ShowCondominio':
      resetConfigButtons();

      bancos.classList.add("d-none");
      torres.classList.add("d-none");
      domicilios.classList.add("d-none");
      precios.classList.add("d-none");
      tasas.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");
      recargos.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");

      condominio.classList.remove("d-none");
      btn_condominio.classList.add("btn-option-selected");

      btn_banco.classList.remove("btn-option-selected");
      btn_torre.classList.remove("btn-option-selected");
      btn_domicilio.classList.remove("btn-option-selected");
      btn_precio.classList.remove("btn-option-selected");
      btn_tasa.classList.remove("btn-option-selected");
      if (btn_propietarios) btn_propietarios.classList.remove("btn-option-selected");
      btn_recargo.classList.remove("btn-option-selected");
      if (btn_propietarios) btn_propietarios.classList.remove("btn-option-selected");
      if (btn_propietarios) btn_propietarios.classList.remove("btn-option-selected");
      if (btn_propietarios) btn_propietarios.classList.remove("btn-option-selected");
      if (btn_propietarios) btn_propietarios.classList.remove("btn-option-selected");
      if (btn_propietarios) btn_propietarios.classList.remove("btn-option-selected");
      break;

    case 'ShowBancos':
      resetConfigButtons();

      condominio.classList.add("d-none");
      torres.classList.add("d-none");
      domicilios.classList.add("d-none");
      precios.classList.add("d-none");
      tasas.classList.add("d-none");
      recargos.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");
      resetPropietariosConf();

      bancos.classList.remove("d-none");
      btn_banco.classList.add("btn-option-selected");

      btn_condominio.classList.remove("btn-option-selected");
      btn_torre.classList.remove("btn-option-selected");
      btn_domicilio.classList.remove("btn-option-selected");
      btn_precio.classList.remove("btn-option-selected");
      btn_tasa.classList.remove("btn-option-selected");
      btn_recargo.classList.remove("btn-option-selected");
      break;

    case 'ShowTorres':
      resetConfigButtons();

      condominio.classList.add("d-none");
      bancos.classList.add("d-none");
      domicilios.classList.add("d-none");
      precios.classList.add("d-none");
      tasas.classList.add("d-none");
      recargos.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");
      resetPropietariosConf();

      torres.classList.remove("d-none");
      btn_torre.classList.add("btn-option-selected");

      btn_condominio.classList.remove("btn-option-selected");
      btn_banco.classList.remove("btn-option-selected");
      btn_domicilio.classList.remove("btn-option-selected");
      btn_precio.classList.remove("btn-option-selected");
      btn_tasa.classList.remove("btn-option-selected");
      btn_recargo.classList.remove("btn-option-selected");
      break;

    case 'ShowDomicilios':
      resetConfigButtons();

      condominio.classList.add("d-none");
      bancos.classList.add("d-none");
      torres.classList.add("d-none");
      precios.classList.add("d-none");
      tasas.classList.add("d-none");
      recargos.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");
      resetPropietariosConf();

      domicilios.classList.remove("d-none");
      btn_domicilio.classList.add("btn-option-selected");

      btn_condominio.classList.remove("btn-option-selected");
      btn_banco.classList.remove("btn-option-selected");
      btn_torre.classList.remove("btn-option-selected");
      btn_precio.classList.remove("btn-option-selected");
      btn_tasa.classList.remove("btn-option-selected");
      btn_recargo.classList.remove("btn-option-selected");
      break;

    case 'ShowPrecios':
      resetConfigButtons();

      condominio.classList.add("d-none");
      bancos.classList.add("d-none");
      torres.classList.add("d-none");
      domicilios.classList.add("d-none");
      tasas.classList.add("d-none");
      recargos.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");
      resetPropietariosConf();

      precios.classList.remove("d-none");
      btn_precio.classList.add("btn-option-selected");

      btn_condominio.classList.remove("btn-option-selected");
      btn_banco.classList.remove("btn-option-selected");
      btn_torre.classList.remove("btn-option-selected");
      btn_domicilio.classList.remove("btn-option-selected");
      btn_tasa.classList.remove("btn-option-selected");
      btn_recargo.classList.remove("btn-option-selected");
      break;

    case 'ShowTasas':
      resetConfigButtons();

      condominio.classList.add("d-none");
      bancos.classList.add("d-none");
      torres.classList.add("d-none");
      domicilios.classList.add("d-none");
      precios.classList.add("d-none");
      recargos.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");
      resetPropietariosConf();

      tasas.classList.remove("d-none");
      btn_tasa.classList.add("btn-option-selected");

      btn_condominio.classList.remove("btn-option-selected");
      btn_banco.classList.remove("btn-option-selected");
      btn_torre.classList.remove("btn-option-selected");
      btn_domicilio.classList.remove("btn-option-selected");
      btn_precio.classList.remove("btn-option-selected");
      btn_recargo.classList.remove("btn-option-selected");
      if (btn_propietarios) btn_propietarios.classList.remove("btn-option-selected");
      break;

    case 'ShowRecargos':
      resetConfigButtons();

      condominio.classList.add("d-none");
      bancos.classList.add("d-none");
      torres.classList.add("d-none");
      domicilios.classList.add("d-none");
      precios.classList.add("d-none");
      tasas.classList.add("d-none");
      if (propietarios) propietarios.classList.add("d-none");
      resetPropietariosConf();

      recargos.classList.remove("d-none");
      btn_recargo.classList.add("btn-option-selected");

      btn_condominio.classList.remove("btn-option-selected");
      btn_banco.classList.remove("btn-option-selected");
      btn_torre.classList.remove("btn-option-selected");
      btn_domicilio.classList.remove("btn-option-selected");
      btn_precio.classList.remove("btn-option-selected");
      btn_tasa.classList.remove("btn-option-selected");
      if (btn_propietarios) btn_propietarios.classList.remove("btn-option-selected");
      break;

    case 'ShowPropietarios':
      resetConfigButtons();

      if (condominio) condominio.classList.add("d-none");
      if (bancos) bancos.classList.add("d-none");
      if (torres) torres.classList.add("d-none");
      if (domicilios) domicilios.classList.add("d-none");
      if (precios) precios.classList.add("d-none");
      if (tasas) tasas.classList.add("d-none");
      if (recargos) recargos.classList.add("d-none");

      if (propietarios) propietarios.classList.remove("d-none");
      resetPropietariosConf();
      var verPropConf = document.getElementById("VerPropietariosConf");
      if (verPropConf) verPropConf.classList.remove("d-none");
      if (btn_propietarios) btn_propietarios.classList.add("btn-option-selected");

      if (btn_condominio) btn_condominio.classList.remove("btn-option-selected");
      if (btn_banco) btn_banco.classList.remove("btn-option-selected");
      if (btn_torre) btn_torre.classList.remove("btn-option-selected");
      if (btn_domicilio) btn_domicilio.classList.remove("btn-option-selected");
      if (btn_precio) btn_precio.classList.remove("btn-option-selected");
      if (btn_tasa) btn_tasa.classList.remove("btn-option-selected");
      if (btn_recargo) btn_recargo.classList.remove("btn-option-selected");
      break;
  }
}

window.addEventListener('load', function () {
const pathname = window.location.pathname;
const path = pathname.split('/').filter(Boolean);
const modulo = path[path.length - 1];
const params = new URLSearchParams(window.location.search);

switch(modulo) {
    case 'gastos':
        if (params.get('lista') === '1') {
            ShowOrHide('ShowListaGastos');
        }
        if (params.get('lista') === '1') {
            params.delete('lista');
            var cleanedGastos = window.location.pathname;
            var nextGastos = params.toString();
            if (nextGastos) cleanedGastos += '?' + nextGastos;
            window.history.replaceState({}, '', cleanedGastos);
        }
        break;
    case 'ingresos':
        if (params.get('lista') === '1') {
            ShowOrHide('ShowListaIngresos');
        }
        if (params.get('lista') === '1') {
            params.delete('lista');
            var cleanedIngresos = window.location.pathname;
            var nextIngresos = params.toString();
            if (nextIngresos) cleanedIngresos += '?' + nextIngresos;
            window.history.replaceState({}, '', cleanedIngresos);
        }
        break;
    case 'tasa':
        ConfMenu('ShowTasas');
        break;

    case 'precios':
        ConfMenu('ShowPrecios');
        break;

    case 'recargos':
        ConfMenu('ShowRecargos');
        break;

    case 'domicilios':
        ConfMenu('ShowDomicilios');
        break;

    case 'bancos':
        ConfMenu('ShowBancos');
        break;

    case 'torres':
        ConfMenu('ShowTorres');
        break;
    case 'condominio':
        if (params.get('tab') === 'propietarios') {
            ConfMenu('ShowPropietarios');
        } else if (params.get('tab') === 'domicilios') {
            ConfMenu('ShowDomicilios');
            if (params.get('lista') === '1') {
                ShowOrHide('ShowListaDomicilios');
            }
        } else if (params.get('tab') === 'bancos') {
            ConfMenu('ShowBancos');
            if (params.get('form') === '1') {
                ShowOrHide('HideListaBancos');
            } else if (params.get('lista') === '1') {
                ShowOrHide('ShowListaBancos');
            }
        } else if (params.get('tab') === 'torres') {
            ConfMenu('ShowTorres');
            if (params.get('lista') === '1') {
                ShowOrHide('ShowListaTorres');
            }
        }
        if (params.get('lista') === '1' || params.get('form') === '1') {
            params.delete('lista');
            params.delete('form');
            var cleaned = window.location.pathname;
            var nextQuery = params.toString();
            if (nextQuery) cleaned += '?' + nextQuery;
            window.history.replaceState({}, '', cleaned);
        }
        break;

}
});

var dni = document.getElementById('dni_titular');
var tipo_id = document.getElementById('tipo_dni_titular');

if (tipo_id)
{
  tipo_id.addEventListener('change',function () {
      if (tipo_id.value == "J")
      {
        dni.type = "text";
      } else {
        dni.type = "number";
      };
  });
};

function CheckMoneda(moneda, banco, tipo)
{
  var SoloNacional = document.getElementById('BancosNacionalesInfo')
  var Titular = document.getElementById('titular')
  var Cedula = document.getElementById('cedula')

  var BancosBS = document.getElementById('BancosBS');
  var BancosUSD = document.getElementById('BancosUSD');
  var BancosEUR = document.getElementById('BancosEUR');

  var banco_gasto_BS = document.getElementById('banco_gasto_BS');
  var banco_gasto_USD = document.getElementById('banco_gasto_USD');
  var banco_gasto_EUR = document.getElementById('banco_gasto_EUR');

  var BancosBS_INGRESO = document.getElementById('BancosBS_INGRESO');
  var BancosUSD_INGRESO = document.getElementById('BancosUSD_INGRESO');
  var BancosEUR_INGRESO = document.getElementById('BancosEUR_INGRESO');

  var banco_ingreso_BS = document.getElementById('banco_ingreso_BS');
  var banco_ingreso_USD = document.getElementById('banco_ingreso_USD');
  var banco_ingreso_EUR = document.getElementById('banco_ingreso_EUR');

  var BancosBS_FONDO = document.getElementById('BancosBS_FONDO');
  var BancosUSD_FONDO = document.getElementById('BancosUSD_FONDO');
  var BancosEUR_FONDO = document.getElementById('BancosEUR_FONDO');

  var banco_fondo_BS = document.getElementById('banco_BS');
  var banco_fondo_USD = document.getElementById('banco_USD');
  var banco_fondo_EUR = document.getElementById('banco_EUR');

  if(banco == '')
  {
    switch (moneda)
    {
      case 'Bs':
        if(SoloNacional.classList.contains('d-none'))
        {
          SoloNacional.classList.remove('d-none')
        }
      break;

      case 'Usd':
        Titular.value = ''
        Cedula.value = ''
        if(!SoloNacional.classList.contains('d-none'))
        {
          SoloNacional.classList.add('d-none')

        }
      break;

      case 'Eur':
        Titular.value = ''
        Cedula.value = ''
        if(!SoloNacional.classList.contains('d-none'))
        {
          SoloNacional.classList.add('d-none')
        }
      break;
    }
  }
  else if(banco != '')
  {
    switch (moneda, banco)
    {
      case 'Bs', 'BancosBS':
        if(BancosBS.classList.contains('d-none'))
        {
          banco_gasto_BS.disabled = false;
          BancosBS.classList.remove('d-none');
          banco_gasto_USD.disabled = true;
          BancosUSD.classList.add('d-none');
          banco_gasto_EUR.disabled = true;
          BancosEUR.classList.add('d-none');
        }
      break;

      case 'Usd', 'BancosUSD':
        if(BancosUSD.classList.contains('d-none'))
        {
          banco_gasto_USD.disabled = false;
          BancosUSD.classList.remove('d-none');
          banco_gasto_BS.disabled = true;
          BancosBS.classList.add('d-none');
          banco_gasto_EUR.disabled = true;
          BancosEUR.classList.add('d-none');
        }
      break;

      case 'Eur', 'BancosEUR':
        if(BancosEUR.classList.contains('d-none'))
        {
          banco_gasto_EUR.disabled = false;
          BancosEUR.classList.remove('d-none');
          banco_gasto_BS.disabled = true;
          BancosBS.classList.add('d-none');
          banco_gasto_USD.disabled = true;
          BancosUSD.classList.add('d-none');
        }
      break;

      case 'Bs', 'BancosBS_INGRESO':
        if(BancosBS_INGRESO.classList.contains('d-none'))
        {
          banco_ingreso_BS.disabled = false;
          BancosBS_INGRESO.classList.remove('d-none');
          banco_ingreso_USD.disabled = true;
          BancosUSD_INGRESO.classList.add('d-none');
          banco_ingreso_EUR.disabled = true;
          BancosEUR_INGRESO.classList.add('d-none');
        }
      break;

      case 'Usd', 'BancosUSD_INGRESO':
        if(BancosUSD_INGRESO.classList.contains('d-none'))
        {
          banco_ingreso_USD.disabled = false;
          BancosUSD_INGRESO.classList.remove('d-none');
          banco_ingreso_BS.disabled = true;
          BancosBS_INGRESO.classList.add('d-none');
          banco_ingreso_EUR.disabled = true;
          BancosEUR_INGRESO.classList.add('d-none');
        }
      break;

      case 'Eur', 'BancosEUR_INGRESO':
        if(BancosEUR_INGRESO.classList.contains('d-none'))
        {
          banco_ingreso_EUR.disabled = false;
          BancosEUR_INGRESO.classList.remove('d-none');
          banco_ingreso_BS.disabled = true;
          BancosBS_INGRESO.classList.add('d-none');
          banco_ingreso_USD.disabled = true;
          BancosUSD_INGRESO.classList.add('d-none');
        }
      break;

      case 'Bs', 'BancosBS_FONDO':
        if(BancosBS_FONDO.classList.contains('d-none'))
        {
          banco_fondo_BS.disabled = false;
          BancosBS_FONDO.classList.remove('d-none');
          banco_fondo_USD.disabled = true;
          BancosUSD_FONDO.classList.add('d-none');
          banco_fondo_EUR.disabled = true;
          BancosEUR_FONDO.classList.add('d-none');
        }
      break;

      case 'Usd', 'BancosUSD_FONDO':
        if(BancosUSD_FONDO.classList.contains('d-none'))
        {
          banco_fondo_USD.disabled = false;
          BancosUSD_FONDO.classList.remove('d-none');
          banco_fondo_BS.disabled = true;
          BancosBS_FONDO.classList.add('d-none');
          banco_fondo_EUR.disabled = true;
          BancosEUR_FONDO.classList.add('d-none');
        }
      break;

      case 'Eur', 'BancosEUR_FONDO':
        if(BancosEUR_FONDO.classList.contains('d-none'))
        {
          banco_fondo_EUR.disabled = false;
          BancosEUR_FONDO.classList.remove('d-none');
          banco_fondo_BS.disabled = true;
          BancosBS_FONDO.classList.add('d-none');
          banco_fondo_USD.disabled = true;
          BancosUSD_FONDO.classList.add('d-none');
        }
      break;
    }
  }
}

var tipo_saldo = document.querySelectorAll('.tipo_saldo');

tipo_saldo.forEach(boton => {

  boton.addEventListener('change',function () {

    var bs = document.getElementById('saldo')
    var usd = document.getElementById('saldo_usd');
    var eur = document.getElementById('saldo_eur');

    if (boton.value == "BS")
    {
      bs.classList.remove('d-none');

      usd.classList.add('d-none');
      usd.value = 0;

      eur.classList.add('d-none');
      eur.value = 0;

    } else if (boton.value == "USD") {

      bs.classList.add('d-none');
      bs.value = 0;

      usd.classList.remove('d-none');

      eur.classList.add('d-none');
      eur.value = 0;

    } else if (boton.value == "EUR") {
      bs.classList.add('d-none');
      bs.value = 0;

      usd.classList.add('d-none');
      usd.value = 0;

      eur.classList.remove('d-none');

    }
  });
});

var tipo_gasto = document.querySelector('.option_tipo_gasto');
var tipoCobro = document.getElementById('tipo_cobro_gasto');

if (tipoCobro) {
  tipoCobro.addEventListener('change', function () {

    var sectionTipoGasto = document.getElementById('showTipoGasto');
    var showProp = document.getElementById('showProp');
    var prop_selected = document.querySelector('.prop_selected');

    if (tipoCobro.value == "Condominio") {
      sectionTipoGasto.classList.add('d-none');
      showProp.classList.add('d-none');
      tipo_gasto.selectedIndex = 0;
      prop_selected.selectedIndex = 0;

    } else if (tipoCobro.value == "Cuota") {
      sectionTipoGasto.classList.remove('d-none');

    } else {
      alert('Ocurrió un error al seleccionar la forma de anexo. Por favor recargue la página en intente nuevamente.')

    }
  })
}

// function CheckTipoCobro(param)
// {

//   var sectionTipoGasto = document.getElementById('showTipoGasto');
//   var showProp = document.getElementById('showProp');
//   var prop_selected = document.querySelector('.prop_selected');

//   switch (param) {
//     case 'Condominio':
//       sectionTipoGasto.classList.add('d-none');
//       showProp.classList.add('d-none');
//       tipo_gasto.selectedIndex = 0;
//       prop_selected.selectedIndex = 0;
//       break;

//     case 'Cuota':
//       sectionTipoGasto.classList.remove('d-none');
//       break;
//   }
// }

// var metodo_pago = document.querySelectorAll('.metodo_pago');
// var num_factura = document.getElementById('num_factura');
// var factura = document.getElementById('factura_require')

// metodo_pago.forEach(boton => {
//   boton.addEventListener('change',function () {
//     if (boton.value == 0) {
//       num_factura.classList.remove('d-none');
//       factura.required = true;
//     } else {
//       num_factura.classList.add('d-none');
//       factura.required = false;
//     }
//   });
// });

if(tipo_gasto)
{
  tipo_gasto.addEventListener('change',function () {
      if (tipo_gasto.value == "NO COMÚN")
      {
        showProp.classList.remove('d-none');
      } else {
        showProp.classList.add('d-none');
        prop_selected.selectedIndex = 0;
      }
  });
}

var t_mon = document.querySelectorAll('input[name="tipo_moneda"]');
var n_cuenta = document.getElementById('nro_cuenta');
var numcuenta = document.getElementById('numcuenta');

if(t_mon)
{
  t_mon.forEach(boton => {
    boton.addEventListener('change',function () {
      if (boton.value == "BS")
      {
        n_cuenta.required = true;
      } else if (boton.value == "USD") {
        n_cuenta.required = false;
      } else if (boton.value == "EUR") {
        n_cuenta.required = false;
      }
    });
  });
}

var max_value = document.getElementById('max_value');
var input_abono = document.getElementById('input_abono');

if(input_abono) {
  alert("xd")
    input_abono.max = max_value.value.replace(/\s/g,"").replace(".","").replace(",",".");
}

let duplicaciones = 0;
let inmueble = 1

function add() {
    // Si estamos en la página de propietarios (donde hay #tabla_datos), dejar que la función de propietarios.html maneje el evento
    if ($('#tabla_datos').length > 0) {
        return;
    }

    // Obtener la última opción seleccionada en los selects existentes
    var ultimaOpcionSeleccionada = [];

    $('.domicilio').each(function() {
        var valorSeleccionado = $(this).val();
        ultimaOpcionSeleccionada.push(valorSeleccionado);
    });

    let ultimoDom = $('.domicilio:last');
    ultimoDom.prop('disabled', true);

    let nuevoForm = $('#domicilio0').clone();
    nuevoForm.attr('id', 'domicilio0');
    nuevoForm.addClass('domicilio');
    nuevoForm.addClass('mt-2');
    nuevoForm.addClass('nuevo_campo');
    nuevoForm.find('input').each(function() {
        this.value = '';
    });

    duplicaciones++;
    inmueble++;

    if (typeof dom_disp !== 'undefined' && inmueble >= dom_disp) {
        let item_add = $('#item-add')
        item_add.addClass('d-none');
    }

    $('.nuevo_campo').find('.item-delete').remove();

    if (duplicaciones > 0 || existForm.length > 1) {
        // Agregar botón para eliminar
        $('#domicilios').addClass('nuevo_campo');
        $('#domicilios').append('<div class="delete-button-right col-sm-12 pt-2"><button type="button" class="item-delete btn border btn-option-admin center-all" style="width: 40px; height: 35px;">X</button></div>');
    }

    $(nuevoForm).insertAfter('.domicilio:last');

    let findDom = $('.domicilio:last');
    var newId = 'domicilio' + duplicaciones;
    findDom.attr("id", newId);
    findDom.prop('disabled', false);
    for (i = 0; i < ultimaOpcionSeleccionada.length; i++) {
        findDom.find('option[value="' + ultimaOpcionSeleccionada[i] + '"]').remove();
    }
}

// Función para eliminar
function removeThisFile() {
    let nuevoForm = $('.domicilio');

    if (nuevoForm.length > 1) {

        let lastForm = nuevoForm.last();

        $(lastForm).remove();

        duplicaciones = 0;
        inmueble = 1;

        $('#domicilios').html(divInicial);
    }
}

// Escuchar clic en botón Agregar
$('#item-add .button').on('click', add);

// Escuchar clic en botones para borrar
$(document.body).on('click', '.item-delete', removeThisFile);