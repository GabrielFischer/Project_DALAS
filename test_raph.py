import urllib
import bs4
from urllib import request
from selenium import webdriver
import time
import get_movies_link
import json


def get_page_html(link)->bs4.BeautifulSoup:
    req = request.Request(link, headers={"User-Agent": "Mozilla/5.0"})

    request_text = request.urlopen(req).read()
    return bs4.BeautifulSoup(request_text, "lxml")


def get_cast_data(page:bs4.BeautifulSoup):
    actor_dictionnary={}
    try:
        actors_links=page.find('div',id="tab-cast").find_all('a')
        
        for actor in actors_links:
            if 'tooltip' in actor.get("class"):
                actor_link=actor.get("href")[7:-1]
                if actor_link not in actor_dictionnary:
                    actor_dictionnary["ACTOR_"+actor_link]=actor.text
    except:
        print("No actor!!!!")
    return actor_dictionnary


def get_directors_data(page):
    director_dictionnary={}
    try:
        span_directors_links=page.find("span", {"class": "creatorlist"}).find_all('a')
        
        
        for link in span_directors_links:
            director_dictionnary["DIRECTOR_"+link.get("href")[10:-1]]=link.text
    except:
        print("No director!!!")
    return director_dictionnary


def get_release_year(page):
    try:
        year=(int(page.find("span", {"class": "releasedate"}).text)//10)*10
        return {"YEAR_"+str(year):year}
    except:
        print("No year!!!")


def get_details_data(page):
    studio_dictionnary,country_dictionnary,language_dictionnary={},{},{}
    try:
        div_details_links=page.find('div',id="tab-details").find_all('a')
        for link in div_details_links:
            if "/studio/" in link.get("href"):
                studio_dictionnary["STUDIO_"+link.get("href")[8:-1]]=link.text
            elif "/films/country/" in link.get("href"):
                country_dictionnary["COUNTRY_"+link.get("href")[15:-1]]=link.text
            elif "/films/language/" in link.get("href"):
                language_dictionnary["LANGUAGE_"+link.get("href")[16:-1]]=link.text
    
    except:
        print("No details!!!")
            
    return country_dictionnary,studio_dictionnary,language_dictionnary
    

def get_genres_data(page):
    genres_dictionnary={}
    try:
        div_genres_links=page.find('div',id="tab-genres").find_all('a')
        
        for link in div_genres_links:
            if "/films/genre/" in link.get("href"):
                genres_dictionnary["GENRE_"+link.get("href")[13:-1]]=link.text
            else:
                break #All the genres have been found so we skip any links that may be after
    except:
        print("No genres!!!")
    return genres_dictionnary


def get_useful_data(page):
    actor_dict=get_cast_data(page)
    director_dict=get_directors_data(page)
    country_dict,studio_dict,language_dict=get_details_data(page)
    genres_dict=get_genres_data(page)
    release_year=get_release_year(page)
    useful_data={"Actors":actor_dict,
                 "Directors":director_dict,
                 "Countries":country_dict,
                 "Studio":studio_dict,
                 "Language":language_dict,
                 "Genres":genres_dict,
                 "Year":release_year
                 }
    
    return useful_data


page=get_page_html("https://letterboxd.com/film/dune/")
useful=get_useful_data(page)
movie_attribute=[]
for attribute in useful:
    movie_attribute+=list(useful[attribute].keys())[:10]
print(movie_attribute)
"""
start_time = time.time()

#page=get_page_html("https://letterboxd.com/film/film:966962/")
#page=get_page_html("https://letterboxd.com/film/parasite-2019/")




list_movie_link=get_movies_link.get_films_url(page_url="https://letterboxd.com/films/popular/",
                                              nb_pages=1,
                                              type_item="posteritem")
global_data_dico={}

for movie_link in list_movie_link:
    if list_movie_link.index(movie_link)%10==0:
        print(list_movie_link.index(movie_link))
    useful_data_dico=get_useful_data(get_page_html(f"https://letterboxd.com/film/{movie_link}/"))
    movie_attribute=[]
    for attribute in useful_data_dico:
        movie_attribute+=list(useful_data_dico[attribute].keys())[:10]
    global_data_dico[movie_link]=movie_attribute
end_time=time.time()
print(f"Durée d'exécution:{end_time-start_time}s")


with open('data_bis.json','w') as json_file:
    json.dump(global_data_dico,json_file,indent=4)
"""