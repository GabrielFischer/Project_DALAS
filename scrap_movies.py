import get_movie_data
import get_movie_links
import time
import json

start_time = time.time()

list_movie_link=get_movie_links.get_films_url(page_url="https://letterboxd.com/films/popular/",
                                              nb_pages=1,
                                              type_item="posteritem")
global_data_dico={}

for movie_link in list_movie_link:
    if list_movie_link.index(movie_link)%10==0:
        print(f"{movie_link} ({list_movie_link.index(movie_link)})")
    movie_tokens=get_movie_data.get_movie_tokens(movie_link)
    global_data_dico[movie_link]=movie_tokens
end_time=time.time()
print(f"Durée d'exécution:{end_time-start_time}s")


with open("./data/json/data_bis.json",'w') as json_file:
    json.dump(global_data_dico,json_file,indent=4)