from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import json


file_path = 'data.json'
with open(file_path, 'r') as f:
    films_tokens = json.load(f)

# films_tokens = {
#     "Inception": ["ACTOR_DiCaprio", "ACTOR_Hardy", "ACTOR_Cotillard",
#                   "DIRECTOR_Nolan", "GENRE_SciFi", "GENRE_Action",
#                   "COUNTRY_USA", "COUNTRY_UK", "DECADE_2010s"],

#     "Parasite": ["ACTOR_KangHoSong", "ACTOR_SunKyunLee",
#                  "DIRECTOR_BongJoonHo", "GENRE_Drama", "GENRE_Thriller",
#                  "COUNTRY_Korea", "DECADE_2010s"],

#     "Amelie": ["ACTOR_Tautou", "ACTOR_Kassovitz",
#                "DIRECTOR_Jeunet", "GENRE_Romance", "GENRE_Comedy",
#                "COUNTRY_France", "DECADE_2000s"],

#     "12YearsASlave": ["ACTOR_Pitt", "ACTOR_Fassbender", "ACTOR_Cumberbatch",
#                       "DIRECTOR_McQueen", "GENRE_Drama", "GENRE_History",
#                       "COUNTRY_USA", "DECADE_2010s"],

#     "LaLaLand": ["ACTOR_Gosling", "ACTOR_Stone",
#                  "DIRECTOR_Chazelle", "GENRE_Musical", "GENRE_Romance",
#                  "COUNTRY_USA", "DECADE_2010s"]
# }




# =========================================================
# 1. Préparer les données
# =========================================================

# On extrait simplement les listes de tokens (les "phrases") et les titres
film_titles = list(films_tokens.keys())
sentences = list(films_tokens.values())

# =========================================================
# 2. Entraîner le modèle Word2Vec
# =========================================================
model = Word2Vec(
    sentences,
    vector_size=128,
    window=5,
    min_count=1,
    sg=1,
    workers=4,
    epochs=100
)

# =========================================================
# 3. Créer le vecteur de chaque film
# =========================================================
def film_vector(tokens, model):
    vecs = [model.wv[t] for t in tokens if t in model.wv]
    if len(vecs) == 0:
        return np.zeros(model.vector_size)
    return np.mean(vecs, axis=0)

film_embeddings = np.array([
    film_vector(tokens, model) for tokens in sentences
])

# =========================================================
# 4. Calculer les similarités
# =========================================================
sim_matrix = cosine_similarity(film_embeddings)
df_sim = pd.DataFrame(sim_matrix, index=film_titles, columns=film_titles)

print("\nSimilarité cosinus entre les films :\n")
print(df_sim.round(3))

# =========================================================
# 5. Trouver les films similaires
# =========================================================
def films_similaires(titre, top_n=3):
    idx = film_titles.index(titre)
    sims = list(enumerate(sim_matrix[idx]))
    sims = sorted(sims, key=lambda x: -x[1])[1:top_n+1]
    return [(film_titles[i], round(score, 3)) for i, score in sims]


# print("\nFilms similaires à 'Inception' :")
# print(films_similaires("Inception"))


df_sim.to_csv('data_embedding.csv', index=True)



example_film = film_titles[0]
print(f"\nFilms les plus similaires à '{example_film}' :")
print(films_similaires(example_film))

print(np.min(df_sim))
#print(film_titles[np.argmin(df_sim)//720],film_titles[np.argmin(df_sim)%720])