fetch('/static/js/admin.js').then(response => response.text()).then(script => {

    function takeID() {
        var div = event.target.closest('div.form_domicilio');
        var valorDeseado = div.querySelector('.id_dom').value;

        alert(valorDeseado)

        if (valorDeseado != "") {
            let nuevoInput = $('#id_dom').clone();
            nuevoInput.val(valorDeseado);
            nuevoInput.find('input').each(function() {
                this.value = valorDeseado;
            });
            $(nuevoInput).attr('name', 'eliminar_apto');
            $(nuevoInput).insertAfter('#item-add');
        }
    }

    // Escuchar clic en botones para borrar
    $(document.body).on('click', '.item-delete', takeID);

    // Escuchar clic en botones para borrar
    $(document.body).on('click', '.item-clean', takeID);

    function chargeDeletebutton() {
        let existForm = $('.form_domicilio');
        let lastForm = $('.form_domicilio:last');

        duplicaciones = existForm.length - 1;

        if (existForm.length > 1) {
          lastForm.addClass('nuevo_campo');
          $(lastForm).append('<div class="delete-button-right"><button class="item-delete btn border btn-option-admin col-1 center-all" style="height: 30px;">X</button></div>');
        }
    }

    document.addEventListener("DOMContentLoaded", function() {
        chargeDeletebutton();
    });

}).catch(error => console.log(error));