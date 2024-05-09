// Función para mostrar detalles de la película
function showMovieDetails(movieId) {
    const detailsElement = document.getElementById(`details-${movieId}`);
    const isHidden = detailsElement.style.display === 'none';
    detailsElement.style.display = isHidden ? 'block' : 'none';
}

// Función para cambiar el tema de la página (claro/oscuro)
function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.contains('dark-theme');
    body.classList.toggle('dark-theme', !isDark);
}
