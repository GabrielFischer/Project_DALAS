import get_movie_data
import get_movie_links_profile
import time
import json

start_time = time.time()
#gaby93 nailuujj
user="gaby93"
list_movie_link, list_movie_grade=get_movie_links_profile.get_movies_watched(user)

#il faudrait rajouter un token "GRADE_x" pour après dans embedding

profile_data_dico={}
for movie_link in list_movie_link:
    if list_movie_link.index(movie_link)%10==0:
        print(f"{movie_link} ({list_movie_link.index(movie_link)})")
    movie_tokens=get_movie_data.get_movie_tokens(movie_link)
    profile_data_dico[movie_link]=movie_tokens
end_time=time.time()
print(f"Durée d'exécution:{end_time-start_time}s")


with open(f"./data/json/data_profile_{user}.json",'w') as json_file:
    json.dump(profile_data_dico,json_file,indent=4)
