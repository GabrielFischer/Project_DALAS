from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

start_time = time.time()

def driver_setup():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_films_url(page_url,nb_pages,type_item,driver=driver_setup()):
    
    films_urls = []

    for i in range(1, nb_pages+1):  # pages 1 à n
        print(i)
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
        print(f"Page {i}: {len(films)} films trouvés")
        for film in films:
            link = film.get_attribute("href")
            if link:
                #print(link)
                films_urls.append(link[28:-1]) #enlever le début du lien


        # Pause entre les pages pour éviter un blocage
        if i!=nb_pages:
            time.sleep(2)

    driver.quit()

    end_time=time.time()
    exec_duration=end_time-start_time

    print(f"\nTotal de liens collectés : {len(films_urls)}")
    print(f"\nDurée d'execution : {exec_duration}")
    return films_urls
