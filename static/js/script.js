// Regresa a la lista de contactos sin guardar cambios
function cancelar() {
    location.href = "/lista_contactos";
}

// Pide confirmación antes de borrar un contacto
function confirmarBorrado() {
    return confirm("¿Seguro que quieres borrar este contacto?");
}

// Muestra una vista previa de la foto seleccionada
const inputFoto = document.getElementById("foto");
const vistaPrevia = document.getElementById("vista_previa");

if (inputFoto && vistaPrevia) {
    inputFoto.addEventListener("change", function () {
        const archivo = inputFoto.files[0];
        if (archivo) {
            vistaPrevia.src = URL.createObjectURL(archivo);
            vistaPrevia.hidden = false;
        } else {
            vistaPrevia.hidden = true;
        }
    });
}
