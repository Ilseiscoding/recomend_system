import pandas as pd
from flask import Flask, render_template, request
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
import pickle

# Inicializa la aplicación Flask
app = Flask(__name__)

# Función para cargar los datos de calificaciones y películas
def load_data(ratings_path, movies_path):
    # Carga el archivo de calificaciones con las columnas especificadas
    ratings = pd.read_csv(ratings_path, sep='\t', names=['user_id', 'item_id', 'rating', 'timestamp'])
    # Carga el archivo de películas con las columnas especificadas
    movies = pd.read_csv(movies_path, sep='|', encoding='latin-1', names=[
        'item_id', 'title', 'release_date', 'video_release_date', 'IMDb_URL', 'unknown', 'Action',
        'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama',
        'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
        'War', 'Western'], usecols=range(24))
    # Devuelve los dataframes de calificaciones y películas
    return ratings, movies

# Función para generar la matriz de similitud de cosenos basada en géneros de películas
def generate_cosine_similarity(movies_gen):
    # Calcula y devuelve la similitud de cosenos entre las filas de la matriz de géneros
    return cosine_similarity(movies_gen, movies_gen)

# Función para encontrar el título de película más cercano al ingresado
def movie_finder(title, movie_titles):
    # Encuentra la coincidencia más cercana al título dado utilizando coincidencia difusa
    closest_match = process.extractOne(title, movie_titles)
    # Devuelve el título más cercano encontrado
    return closest_match[0]

# Función para obtener recomendaciones basadas en contenido
def get_content_based_recommendations(title_string, movie_idx, movies, cosine_sim, n_recommendations=10):
    # Encuentra el título de película más cercano
    title = movie_finder(title_string, movies['title'].tolist())
    # Obtiene el índice de la película en el dataframe
    idx = movie_idx[title]
    # Calcula la similitud de la película con todas las demás
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Ordena las películas por similitud en orden descendente
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Selecciona las películas más similares (excluyendo la misma película)
    sim_scores = sim_scores[1:(n_recommendations+1)]
    # Obtiene los índices de las películas similares
    similar_movies = [i[0] for i in sim_scores]
    # Devuelve los títulos de las películas recomendadas
    return movies['title'].iloc[similar_movies]

# Carga y procesamiento inicial de datos
ratings_path = 'ml-100k/u.data'
movies_path = 'ml-100k/u.item'

# Carga los datos de calificaciones y películas
ratings, movies = load_data(ratings_path, movies_path)

# Selecciona las columnas de géneros para calcular la similitud
selected_columns = ['unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy',
                    'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                    'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

# Filtra la matriz de películas para incluir solo las columnas de géneros
movies_gen = movies[selected_columns]
# Genera la matriz de similitud de cosenos
cosine_sim = generate_cosine_similarity(movies_gen)

# Guarda la matriz de similitud de cosenos en un archivo pickle para uso futuro
with open('cosine_similarity.pkl', 'wb') as file:
    pickle.dump(cosine_sim, file)

# Crea un diccionario que mapea los títulos de películas a sus índices en el dataframe
movie_idx = dict(zip(movies['title'], list(movies.index)))

# Define la ruta principal de la aplicación Flask
@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = None
    # Si se envía un formulario con un nombre de película
    if request.method == 'POST':
        moviename = request.form['moviename']
        # Genera recomendaciones basadas en el título ingresado
        recommendations = get_content_based_recommendations(moviename, movie_idx, movies, cosine_sim, n_recommendations=10)
        # Convierte las recomendaciones a una lista
        recommendations = recommendations.tolist()
    
    # Renderiza la plantilla HTML index.html, pasando las recomendaciones si existen
    return render_template('index.html', recommendations=recommendations)

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=False)
