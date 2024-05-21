// Función para mostrar detalles de la película
function showMovieDetails(movieId) {
    const detailsElement = document.getElementById(`details-${movieId}`);
    const isHidden = detailsElement.style.display === 'none';
    detailsElement.style.display = isHidden ? 'block' : 'none';
}

// Función para ampliar el cartel al pasar el ratón por encima
function enlargePoster(posterId) {
    const posterElement = document.getElementById(posterId);
    if (posterElement) {
        posterElement.style.transform = 'scale(1.2)';  // Ampliar la imagen
        posterElement.style.transition = 'transform 0.3s';  // Efecto suave
    }
}

// Función para restaurar el tamaño del cartel al quitar el ratón
function resetPoster(posterId) {
    const posterElement = document.getElementById(posterId);
    if (posterElement) {
        posterElement.style.transform = 'scale(1.0)';  // Restaurar el tamaño original
    }
}