//Darle funcion al boton desplegable en movil
const desplegable = document.getElementById('menuDesplegable');
const menu = document.getElementById('menu');
//Añadirmos un listener al icono del desplegable
desplegable.addEventListener('click', ()=> {
    menu.classList.toggle('show'); // Alterna la clase 'show' en el menú
});

//Funcion carrusel
const img = document.querySelectorAll('.carrusel img');
let indice = 0;
function siguienteImagen(){
    //Quita la clase "active" a todas para ocultarlas (opacity: 0 en CSS)
    img.forEach(img => img.classList.remove('active'));
    //Añade la clase "active" hace visible la img (opacity: 1 con transición suave) 
    img[indice].classList.add('active');
    //% (módulo) sirve para volver a 0 
    indice = (indice + 1) % img.length;
}
siguienteImagen();
setInterval(siguienteImagen, 10000);

//
