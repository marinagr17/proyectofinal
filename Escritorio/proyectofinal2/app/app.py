import random
import requests
from flask import Flask, render_template
from flask_bootstrap import Bootstrap4

app = Flask(__name__)
bootstrap = Bootstrap4(app)

api_key="84a89a3c08b57ec460c214795878d513"

@app.route('/')
def index():
    # URLs para obtener listas de películas y series
    popular_movies_url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    now_playing_movies_url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}"
    popular_series_url = f"https://api.themoviedb.org/3/tv/popular?api_key={api_key}"

    # Obtener datos de películas y series
    popular_movies_response = requests.get(popular_movies_url)
    now_playing_movies_response = requests.get(now_playing_movies_url)
    popular_series_response = requests.get(popular_series_url)
    
    # Obtener listas de películas y series
    popular_movies = popular_movies_response.json().get("results", []) if popular_movies_response.status_code == 200 else []
    now_playing_movies = now_playing_movies_response.json().get("results", []) if now_playing_movies_response.status_code == 200 else []
    popular_series = popular_series_response.json().get("results", []) if popular_series_response.status_code == 200 else []
    
    # Renderizar la plantilla principal
    return render_template(
        'index.html',
        popular_movies=popular_movies,
        now_playing_movies=now_playing_movies,
        popular_series=popular_series
    )


@app.route('/detalles/<int:movie_id>')  # Ruta para detalles de película
def pelicula(movie_id):
    # Obtener detalles de la película
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=es"
    response = requests.get(movie_url)
    
    if response.status_code == 200:
        pelicula = response.json()
        
        # Obtener el tráiler de la película
        video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"
        video_response = requests.get(video_url)
        
        if video_response.status_code == 200:
            videos = video_response.json().get("results", [])
            trailer = next((video for video in videos if video["type"] == "Trailer"), None)  # Buscar un tráiler
        else:
            trailer = None
        
        return render_template('detalles.html', pelicula=pelicula, trailer=trailer)
    else:
        return "Película no encontrada", 404


@app.route('/detalleserie/<int:serie_id>')  # Ruta para detalles de serie
def serie(serie_id):
    # Obtener detalles de la serie
    serie_url = f"https://api.themoviedb.org/3/tv/{serie_id}?api_key={api_key}&language=es"
    response = requests.get(serie_url)
    
    if response.status_code == 200:
        serie = response.json()
        
        # Obtener el tráiler de la serie
        video_url = f"https://api.themoviedb.org/3/tv/{serie_id}/videos?api_key={api_key}"
        video_response = requests.get(video_url)
        
        if video_response.status_code == 200:
            videos = video_response.json().get("results", [])
            trailer = next((video for video in videos if video["type"] == "Trailer"), None)
        else:
            trailer = None
        
        return render_template('detalleserie.html', serie=serie, trailer=trailer)
    else:
        return "Serie no encontrada", 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)