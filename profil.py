from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib
import bs4
from urllib import request
import get_movies_link
import test_raph
import json


start_time = time.time()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#trouver le nombre de films vu par l'utilisateur, nécéssaire pour savoir le nombre de page a scrapper
debut_url="https://letterboxd.com/"
profil_link=debut_url+"gaby93/"

req = request.Request(profil_link, headers={"User-Agent": "Mozilla/5.0"})
request_text = request.urlopen(req).read()
page = bs4.BeautifulSoup(request_text, "lxml")
stats=page.find("h4",{"class":"profile-statistic statistic"})
nb_films=int(stats.find('span', class_='value').text)
print(nb_films)


nb_pages=(nb_films//72)+1
print("jzheafzrgharzgig")
print(nb_pages)


list_movie_link=get_movies_link.get_films_url(profil_link+"/films/",nb_pages,"griditem")

global_data_dico={}

for movie_link in list_movie_link:
    if list_movie_link.index(movie_link)%10==0:
        print(list_movie_link.index(movie_link))
    useful_data_dico=test_raph.get_useful_data(test_raph.get_page_html(f"https://letterboxd.com/film/{movie_link}/"))
    movie_attribute=[]
    for attribute in useful_data_dico:
        movie_attribute+=list(useful_data_dico[attribute].keys())[:10]
    global_data_dico[movie_link]=movie_attribute
end_time=time.time()
print(f"Durée d'exécution:{end_time-start_time}s")


with open('data_profil_gab.json','w') as json_file:
    json.dump(global_data_dico,json_file,indent=4)




