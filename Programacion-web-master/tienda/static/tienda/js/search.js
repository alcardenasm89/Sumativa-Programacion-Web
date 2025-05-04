function buscarJuegos() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const juegos = document.querySelectorAll('.juego-card');
    
    juegos.forEach(juego => {
        const titulo = juego.querySelector('h3').textContent.toLowerCase();
        if (titulo.includes(searchTerm)) {
            juego.style.display = 'flex';
        } else {
            juego.style.display = 'none';
        }
    });
}

// Agregar búsqueda al presionar Enter
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                buscarJuegos();
            }
        });
    }
}); 