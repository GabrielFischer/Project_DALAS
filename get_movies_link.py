# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# url="https://letterboxd.com/films/popular/"

# films_urls = []

# for i in range(10):
#     if i>1:
#         url+="page/"+str(i+1)+"/"

#     # Ouvrir la page
#     driver.get(url)

#     # attendre que les éléments soient présents (max 10 secondes)
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.CLASS_NAME, "posteritem"))
#         )
#     except Exception as e:
#         print(f"Page {i}: aucun élément trouvé ({e})")
#         continue

#     # Récupérer tous les éléments <li> avec la classe "posteritem"
#     films_elements = driver.find_elements(By.CLASS_NAME, "posteritem")


#     for film in films_elements:
#         link_tag = film.find_element(By.TAG_NAME, "a")
#         films_urls.append(link_tag.get_attribute("href"))
#     print(i)
#     time.sleep(2)


# # Afficher les URLs
# #print(films_urls)
# print(len(films_urls))
# #On est bloqué dès la 3eme page....
# #Voir si on peut récupérer les mean rankings en plus

# # Fermer le navigateur
# driver.quit()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

start_time = time.time()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

films_urls = []

for i in range(1, 11):  # pages 1 à 10
    if i == 1:
        url = "https://letterboxd.com/films/popular/"
    else:
        url = f"https://letterboxd.com/films/popular/page/{i}/"

    driver.get(url)

    # attendre que les éléments soient présents (max 10 secondes)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "posteritem"))
        )
    except Exception as e:
        print(f"⚠️  Page {i}: aucun élément trouvé ({e})")
        continue

    films = driver.find_elements(By.CSS_SELECTOR, ".posteritem a")
    print(f"Page {i}: {len(films)} films trouvés")
    for film in films:
        link = film.get_attribute("href")
        if link:
            print(link)
            films_urls.append(link)


    # for film in films:
    #     print(film) #pas de href là dedans
    #     #voir comment faire 
    #     link = film.get_attribute("href")
    #     if link:
    #         films_urls.append(link)

    # Pause aléatoire entre les pages pour éviter un blocage
    time.sleep(2)

driver.quit()

end_time=time.time()
exec_duration=end_time-start_time

print(f"\nTotal de liens collectés : {len(films_urls)}")
print(f"\nDurée d'execution : {exec_duration}")