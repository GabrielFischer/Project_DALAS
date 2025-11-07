from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

start_time = time.time()

def default_driver_setup():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_films_url(page_url,nb_pages,type_item,driver=default_driver_setup()):
    
    films_urls = []
    notes_films=[]

    for i in range(1, nb_pages+1):  # pages 1 à n
        if i == 1:
            url = page_url
        else:
            url = page_url+f"/page/{i}/"

        driver.get(url)

        # attendre que les éléments soient présents (max 10 secondes)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, type_item))
            )
        except Exception as e:
            print(f"⚠️  Page {i}: aucun élément trouvé ({e})")
            continue

        films = driver.find_elements(By.CSS_SELECTOR, "." +type_item+ " a")
        flag=False
        if type_item=="griditem": #on prend la note que quand on regarde le profil
            notes = driver.find_elements(By.CSS_SELECTOR, "." +type_item+ " p.poster-viewingdata")
            flag=True
        
        print(f"Page {i}: {len(films)} films trouvés")
        for j,film in enumerate(films):
            link = film.get_attribute("href")
            if link:
                films_urls.append(link[28:-1]) #enlever le début du lien
            if flag:
                    try:
                        span = notes[j].find_element(By.TAG_NAME, "span")
                        class_attr = span.get_attribute("class")
                        #print(class_attr.strip()) 
                        grade=int(class_attr.strip()[-1])
                        if grade==0: #si le dernier caractère est 0 alors la note est 10...
                            grade=10
                        notes_films.append(grade) #note donnée au film (1 à 10)
                    except:
                        #aucun span trouvé (film vu mais non notés)
                        notes_films.append(5) #note moyenne si le film n'est pas noté, a voir si on trouve mieux a faire

            


        # Pause entre les pages pour éviter un blocage
        if i!=nb_pages:
            time.sleep(2)
        print(i)

    driver.quit()

    end_time=time.time()
    exec_duration=end_time-start_time

    print(f"Total de liens collectés : {len(films_urls)}")
    print(f"Durée d'execution : {exec_duration}")
    return films_urls,notes_films
