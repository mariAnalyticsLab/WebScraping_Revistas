#Web Scraping de Correos y ORCIDs
import requests
import csv 
import pandas as pd
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.chrome.options import Options
import threading
from threading import Thread

#Abrir archivo 
df = pd.read_csv(r"C:\Users\maria\Downloads\AUTHORS_master.csv",header=0)
urls=df['article_url']
# print(urls)
si=urls[60:70]
# ejemplo=urls[1]
# ejemplo="https://acreditas.com/index.php/acreditas/article/view/257"

# r = requests.get(ejemplo, auth=('user', 'pass'))
# r.status_code
# r.headers
# r.encoding
# html=r.text
# soup = BeautifulSoup(html, 'html.parser')
# paragraphs = soup.find_all('orcid')

# print(paragraphs)

# # Create ChromeOptions object
chrome_options = Options()

# Add the headless argument
chrome_options.add_argument("--headless=new") # Or "--headless" for older versions
# (Optional) Add other useful arguments for headless mode
chrome_options.add_argument("--disable-gpu") # Recommended for Windows
chrome_options.add_argument("--no-sandbox") # Recommended for Linux environments
chrome_options.add_argument("--window-size=1920,1080")


resultados_totales = []
lock = threading.Lock()

def scrape(url):
    or_links=[]
    driver=webdriver.Chrome(chrome_options)
    # driver=webdriver.Chrome()
    time.sleep(10)  
    # for i, url in enumerate(urls):
    driver.get(url)
    print(f"Hilo {threading.current_thread().name} abriendo: {url}")
    time.sleep(8)
    #Scroll a lo largo de la página
    scrolldown = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    match = False
    while (match == False):
        last_count = scrolldown
        time.sleep(5)
        scrolldown = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        if last_count == scrolldown:
            match = True           

            time.sleep(6)
            or_l=[]
            orcids1 = driver.find_elements(By.XPATH, "//span[contains(@class, 'orcid')]//a")
            orcids2 = driver.find_elements(By.XPATH, "//span[contains(@class, 'orcidImage')]//a")
            orcids=orcids1+orcids2
            for orcid in orcids:
                p = orcid.get_attribute('href')
                if p:
                    or_l.append(p)
        # or_.append(or_l)
        print(or_l)
        time.sleep(5)
        driver.quit()
        print(f"Hilo {threading.current_thread().name} finalizado.")
        with lock:
            resultados_totales.extend(or_l)

# OL=[]
# for i,url in enumerate(si):
#     resultado=scrape(url)
#     time.sleep(5)
#     print("resultado", resultado)
#     OL.append(resultado)




if __name__ == "__main__":
    hilos = []

    for url in si:
        # Se puede añadir un nombre al hilo para mejor identificación
        hilo = threading.Thread(target=scrape, args=(url,), name=f"WebDriver-{url.split('//')[1].split('/')[0]}")
        hilos.append(hilo)
        hilo.start() # Inicia la ejecución del hilo

    # Espera a que todos los hilos terminen
    for hilo in hilos:
        hilo.join()

    print("\nTodos los ORCID encontrados:")
    for r in resultados_totales:
        print(r)
        
os.chdir(r"C:/Users\maria\OneDrive\Documents\UNIIE")


# Crear dataframes
df_orcids = pd.DataFrame(resultados_totales, columns=['ClaveOrcid'])
print(df_orcids)
# df_correos = pd.DataFrame(correos, columns=['Correos'])


df_orcids.to_csv('ClavesOrcid.csv', header=True, index=True)
