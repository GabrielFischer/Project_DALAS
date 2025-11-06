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
import get_movie_links
import get_movie_data
import json


global debut_url
debut_url="https://letterboxd.com/"
start_time = time.time()

def default_driver_setup():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_movies_watched_number(user):
    #trouver le nombre de films vu par l'utilisateur, nécéssaire pour savoir le nombre de page a scrapper
    account=user
    profil_link=debut_url+account+"/"

    req = request.Request(profil_link, headers={"User-Agent": "Mozilla/5.0"})
    request_text = request.urlopen(req).read()
    page = bs4.BeautifulSoup(request_text, "lxml")
    stats=page.find("h4",{"class":"profile-statistic statistic"})
    nb_films=int(stats.find('span', class_='value').text)
    print(nb_films)
    nb_pages=(nb_films//72)+1
    return nb_pages

def get_movies_watched(user):
    user
    profil_link=debut_url+user+"/"
    return get_movie_links.get_films_url(profil_link+"/films/",get_movies_watched_number(user),"griditem")





