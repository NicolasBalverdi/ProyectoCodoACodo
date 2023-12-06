
document.addEventListener('scroll', function() {
    var scrollPosition = window.scrollY;

    if (scrollPosition > 50) {
        // Cambiar el fondo y estilo de la barra de navegación al hacer scroll
        header.style.backgroundColor = '#fff'; // Cambia a color de fondo sólido
        header.style.boxShadow = '0 2px 5px rgba(0, 0, 0)'; // Sombra para resaltar
    } else {
        // Restaura el fondo y estilo original al volver arriba
        header.style.backgroundColor = 'rgba(255, 255, 255)';
        header.style.boxShadow = 'none';
    }
});
