


var imgShow = [
  "static/img-aptos/apto.jpg",
  "static/img-aptos/apto1.jpg",
  "static/img-aptos/apto2.jpg",
  "static/img-aptos/apto3.jpg",
  "static/img-aptos/apto4.jpg"
];
var imgShow2 = [
  "static/img-aptos/apto11.jpg",
  "static/img-aptos/apto5.jpg",
  "static/img-aptos/apto6.jpg",
  "static/img-aptos/apto7.jpg",
  "static/img-aptos/apto8.jpg"
];
var imgShow3 = [
  "static/img-aptos/piscina.jpg",
  "static/img-aptos/piscina2.jpg",
  "static/img-aptos/salon.jpg",
  "static/img-aptos/salon2.jpg",
  "static/img-aptos/canchita.jpg"
];

if (document.ftt1) document.ftt1.src = imgShow[0];
if (document.ftt2) document.ftt2.src = imgShow2[0];
if (document.ftt3) document.ftt3.src = imgShow3[0];
if (document.fttAlquier1) document.fttAlquier1.src = imgShow2[0];
var SliderIzquierdo = document.querySelector(".slider-izquierdo");
var SliderDerecho = document.querySelector(".slider-derecho");
var SliderIzquierdo1 = document.querySelector(".slider-izquierdo1");
var SliderDerecho1 = document.querySelector(".slider-derecho1");
var SliderIzquierdo2 = document.querySelector(".slider-izquierdo2");
var SliderDerecho2 = document.querySelector(".slider-derecho2");
var Contador = 0;
var contador2 = 0;
var contador3 = 0;



function MoverDerecha() {
  if (!document.ftt1) return;
  Contador++;
  if (Contador > imgShow.length - 1) { Contador = 0; }
  document.ftt1.src = imgShow[Contador];
}
function MoverDerecha2() {
  if (!document.ftt2) return;
  contador2++;
  if (contador2 > imgShow2.length - 1) { contador2 = 0; }
  document.ftt2.src = imgShow2[contador2];
}
function MoverDerecha3() {
  if (!document.ftt3) return;
  contador3++;
  if (contador3 > imgShow3.length - 1) { contador3 = 0; }
  document.ftt3.src = imgShow3[contador3];
}
function MoverDerecha4() {
  Contador4++;
  if (Contador4 > imgShow.length - 1) { Contador4 = 0; }
  document.ftt4.src = imgShow[Contador4];
}
function MoverDerecha5() {
  contador5++;
  if (contador5 > imgShow2.length - 1) { contador5 = 0; }
  document.ftt5.src = imgShow2[contador5];
}
function MoverDerecha6() {
  contador6++;
  if (contador6 > imgShow3.length - 1) { contador6 = 0; }
  document.ftt6.src = imgShow3[contador6];
}




var Intervalo = setInterval(MoverDerecha, 10000);

SliderDerecho.addEventListener("click", function () {
  clearInterval(Intervalo);
  MoverDerecha();
  Intervalo = setInterval(MoverDerecha, 10000);
})

SliderDerecho1.addEventListener("click", function () {
  clearInterval(Intervalo);
  MoverDerecha2();
  Intervalo = setInterval(MoverDerecha2, 10000);
})
SliderDerecho2.addEventListener("click", function(){
  clearInterval(Intervalo);
  MoverDerecha3();
  Intervalo = setInterval(MoverDerecha3, 10000);
})
;




function MoverIzquierda() {
  Contador--;
  if (Contador < 0) { Contador = imgShow.length - 1; }
  document.ftt1.src = imgShow[Contador];
}
function MoverIzquierda2() {
  contador2--;
  if (contador2 < 0){
  contador2 = imgShow2.length - 1; }
  document.ftt2.src = imgShow2[contador2];
}
function MoverIzquierda3() {
  contador3--;
  if (contador3 < 0){
  contador3 = imgShow3.length - 1; }
  document.ftt3.src = imgShow3[contador3];
}




SliderIzquierdo.addEventListener("click", function () {
  clearInterval(Intervalo);
  MoverIzquierda();
  Intervalo = setInterval(MoverIzquierda, 10000);
})

SliderIzquierdo1.addEventListener("click", function () {
  clearInterval(Intervalo);
  MoverIzquierda2();
  Intervalo = setInterval(MoverIzquierda2, 10000);
})
SliderIzquierdo2.addEventListener("click", function() {
  clearInterval(Intervalo);
  MoverIzquierda3();
  Intervalo = setInterval(MoverIzquierda3, 10000);
});








var side_general = document.getElementById("side-menu");
var content = document.getElementById("content");

function openNav() {

  if (side_general.style.width == "250px") {
    side_general.style.width = "0px";
    content.style.marginLeft = "63px";
    content.style.paddingLeft = "0px";

  } else {
    side_general.style.width = "250px";
    content.style.marginLeft = "250px";
    content.style.paddingLeft = "10px";
  }
}

if (content) {
  content.addEventListener('click', function (event) {
    side_general.style.width = "0px";
    content.style.marginLeft = "63px";
    content.style.paddingLeft = "0px";
  });
}

function lastHistory() {
  window.location.href = document.referrer;
}

function clearForm(id_form) {
  document.getElementById(id_form).reset();
}


