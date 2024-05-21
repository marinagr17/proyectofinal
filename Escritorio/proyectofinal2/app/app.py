import os
import random
import requests
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap4

app = Flask(__name__)
bootstrap = Bootstrap4(app)

api_key = os.getenv("API")

#api_key="84a89a3c08b57ec460c214795878d513"

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
    
@app.route('/buscar', methods=['GET'])
def buscar():
    # Obtener la consulta de búsqueda
    query = request.args.get('query', '')  # Obtener la consulta de búsqueda desde la URL
    
    if not query:
        return render_template('resultados.html', resultados=[], mensaje="No se ingresó una consulta.")
    
    # URL de búsqueda para películas y series
    search_url = f"https://api.themoviedb.org/3/search/multi?api_key={api_key}&query={query}"
    
    # Hacer la solicitud a la API
    response = requests.get(search_url)
    
    if response.status_code == 200:
        resultados = response.json().get("results", [])
    else:
        resultados = []
    
    return render_template('buscar.html', resultados=resultados, query=query)

@app.route('/peliculas')  # Nueva ruta para la página de películas
def peliculas():
    # Obtener películas en tendencia
    trending_url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}"
    trending_response = requests.get(trending_url)
    
    # Obtener próximas películas
    upcoming_url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}"
    upcoming_response = requests.get(upcoming_url)

    # obtener los resultados
    if trending_response.status_code == 200 and upcoming_response.status_code == 200:
        trending_movies = trending_response.json().get("results", [])
        upcoming_movies = upcoming_response.json().get("results", [])
    else:
        trending_movies = []
        upcoming_movies = []
    
    # Renderizar la plantilla y pasar las listas de películas
    return render_template('peliculas.html', trending_movies=trending_movies, upcoming_movies=upcoming_movies)

@app.route('/peliculas', methods=['GET', 'POST'])
def mostrar_peliculas():
    genre = request.args.get('genre', '')
    release_date = request.args.get('release_date', '')
    platform = request.args.get('platform', '')

    # URL base para obtener las películas populares
    base_url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=es-ES"

    # Filtrar por género y fecha de estreno 
    if genre:
        base_url += f"&with_genres={genre}"
    if release_date:
        base_url += f"&primary_release_date.gte={release_date}"
    if platform:
        # Añadir lógica de filtrado por plataforma 
        base_url += f"&with_watch_providers={platform}&watch_region=ES"

    response = requests.get(base_url)
    if response.status_code == 200:
        peliculas = response.json().get('results', [])
    else:
        peliculas = []

    # películas en tendencia
    trending_url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}"
    trending_response = requests.get(trending_url)
    
    # próximas películas
    upcoming_url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}"
    upcoming_response = requests.get(upcoming_url)

    # obtener los resultados
    if trending_response.status_code == 200 and upcoming_response.status_code == 200:
        trending_movies = trending_response.json().get("results", [])
        upcoming_movies = upcoming_response.json().get("results", [])
    else:
        trending_movies = []
        upcoming_movies = []

    return render_template('peliculas.html', peliculas=peliculas, trending_movies=trending_movies, upcoming_movies=upcoming_movies, genre=genre, release_date=release_date, platform=platform)



# Diccionario para mapear plataformas a sus IDs en TMDb
PLATFORM_IDS = {
    'netflix': 8,
    'amazon': 9,
    'apple': 10,
    'hbo': 384,
    'rakuten': 35,
    'atres': 350
}

@app.route('/series', methods=['GET', 'POST'])
def mostrar_series():
    genre = request.args.get('genre', '')
    release_date = request.args.get('release_date', '')
    platform = request.args.get('platform', '')

    # URL base para obtener las series populares
    base_url = f"https://api.themoviedb.org/3/discover/tv?api_key={api_key}&language=es-ES"

    # Filtrar por género, fecha de estreno y plataforma si se proporcionan
    if genre:
        base_url += f"&with_genres={genre}"

    if release_date:
        base_url += f"&first_air_date.gte={release_date}"

    if platform and platform in PLATFORM_IDS:
        base_url += f"&with_watch_providers={PLATFORM_IDS[platform]}&watch_region=ES"

    response = requests.get(base_url)
    if response.status_code == 200:
        series = response.json().get('results', [])
    else:
        series = []

    return render_template('series.html', series=series, genre=genre, release_date=release_date, platform=platform)

if __name__ == '__main__':
    app.run(debug=True)