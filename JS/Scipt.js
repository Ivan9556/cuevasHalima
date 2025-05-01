//Darle funcion al boton desplegable en movil
const desplegable = document.getElementById('menuDesplegable');
const menu = document.getElementById('menu');
//Añadirmos un listener al icono del desplegable
desplegable.addEventListener('click', ()=> {
    menu.classList.toggle('show'); // Alterna la clase 'show' en el menú
});

//Funcion carrusel
let indice = 0;
mostrarImagenes();
function mostrarImagenes(){
    const img = document.getElementsByClassName("diapositiva");
    for(let i = 0; i < img.length; i++){
        //img[i].style.display = "none"; oculta todas las imagenes
        img[i].classList.remove("visible");
    }
    /*
    indice++;
    if(indice > img.length) indice = 1;
    */
    indice = (indice + 1) % img.length;
    img[indice].classList.add("visible");
    //img[indice -1].style.display = "block"; //Muestra solo una
    setTimeout(mostrarImagenes, 5000) //Cambia cada 3 seg
}

