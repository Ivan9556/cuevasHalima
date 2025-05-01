//Darle funcion al boton desplegable en movil
const desplegable = document.getElementById('menuDesplegable');
const menu = document.getElementById('menu');
//Añadirmos un listener al icono del desplegable
desplegable.addEventListener('click', ()=> {
    menu.classList.toggle('show'); // Alterna la clase 'show' en el menú
});

//Otra función
