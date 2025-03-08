function validarSeleccion() {
    var opciones = document.getElementsByName('answer');
    var seleccionado = false;

    for (let i = 0; i < opciones.length; i++) {
        if (opciones[i].checked) {
            seleccionado = true;
            break;
        }
    }

    if (!seleccionado) {
        mensajeError.style.display = "block"; 
        return false; 
    }
    return true; 
}