import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Lista de videos de YouTube con géneros, IDs, títulos y miniaturas
videos = [
    {"id": 1, "title": "Video 1", "genres": ["Documental", "Terror", "VidaReal"], "watch_time": 12},
    {"id": 2, "title": "Video 2", "genres": ["Pelicula", "VidaReal", "Suspenso"], "watch_time": 10},
    {"id": 3, "title": "Video 3", "genres": ["Tecnologia", "Informacion", "Documental"], "watch_time": 10},
    {"id": 4, "title": "Video 4", "genres": ["Informacion", "Tecnologia", "Comedia"], "watch_time": 20},
    {"id": 5, "title": "Video 5", "genres": ["Pelicula", "Comedia", "Fantasia"], "watch_time": 5},
    {"id": 6, "title": "Video 6", "genres": ["CienciaFiccion", "Accion", "Aventura"], "watch_time": 5},
    {"id": 7, "title": "Video 7", "genres": ["Documental", "Musica", "Informacion"], "watch_time": 2},
    {"id": 8, "title": "Video 8", "genres": ["Drama", "Suspenso", "Terror"], "watch_time": 5},
    {"id": 9, "title": "Video 9", "genres": ["Terror", "Comedia", "Documental"], "watch_time": 4},
    {"id": 10, "title": "Video 10", "genres": ["Fantasia", "Aventuras", "Accion"], "watch_time": 14},
    {"id": 11, "title": "Video 11", "genres": ["Accion", "Comedia", "Fantasia"], "watch_time": 11},
    {"id": 12, "title": "Video 12", "genres": ["Romantica", "Comedia", "Drama"], "watch_time": 11},    
    {"id": 13, "title": "Video 13", "genres": ["Drama", "Suspenso", "Accion"], "watch_time": 3},    
]

# Convertir la lista de videos a un DataFrame
df = pd.DataFrame(videos)

# Función para limpiar y preparar el texto
def clean_text(text):
    return ' '.join(str(text).lower().replace(' ', '') for text in text)

df['genres'] = df['genres'].apply(clean_text)
df['title'] = df['title'].str.lower()

# Crear una matriz de características basada en los géneros
vectorizer = CountVectorizer()
genre_matrix = vectorizer.fit_transform(df['genres'])

# Calcular las similitudes de coseno entre los géneros
genre_similarities = cosine_similarity(genre_matrix)

# Normalizar el tiempo de visualización
scaler = MinMaxScaler()
df['normalized_watch_time'] = scaler.fit_transform(df[['watch_time']])

# Función para obtener recomendaciones de videos basadas en el tiempo de visualización y el género
def get_video_recommendations(video_id):
    # Obtener el índice del video actual
    current_video_idx = df.index[df['id'] == video_id][0]
    
    # Calcular la similitud de género entre el video actual y todos los demás videos
    genre_similarity_scores = genre_similarities[current_video_idx]
    
    # Calcular la puntuación de afinidad para cada video
    affinity_scores = []
    for idx, video in enumerate(videos):
        if idx != current_video_idx:
            watch_time = df.loc[idx, 'normalized_watch_time']
            genre_similarity_score = genre_similarity_scores[idx]
            affinity_score = watch_time * genre_similarity_score
            affinity_scores.append((video['title'], affinity_score))
    
    # Ordenar las recomendaciones por la puntuación de afinidad en orden descendente
    sorted_recommendations = sorted(affinity_scores, key=lambda x: x[1], reverse=True)
    
    return [recommendation[0] for recommendation in sorted_recommendations]

# Ejemplo de uso
if __name__ == '__main__':
    # Obtener recomendaciones para un video específico (id = 2)
    video_id = int(input("Ingrese el ID del video: "))
    recommendations = get_video_recommendations(video_id)
    print("Recomendaciones:")
    for video in recommendations:
        print(video)
