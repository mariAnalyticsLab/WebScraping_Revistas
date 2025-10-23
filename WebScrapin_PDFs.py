#Extracción de URLS con selenium
#Ejemplo con un URL
import csv
import pandas as pd
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
from threading import Thread
from selenium.webdriver.chrome.options import Options
from urllib.parse import unquote, urlparse, parse_qs
import urllib3

#Abrir archivo 
# df = pd.read_csv(r"C:/Users\maria\OneDrive\Documents\UNIIE\URLS.csv",header=0)
df = pd.read_csv(r"C:/Users\maria\OneDrive\Documents\UNIIE\PDFS2.csv",header=0)
#print(df)
df_p=pd.DataFrame(df)
all_links=df_p["article_url"].dropna().astype(str).tolist()
# all_links = df['URL'].dropna().astype(str).tolist()
prueba=all_links[2001:2250]#Correr
# ejemplo=url.iloc[0]
# print(all_links)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36",
    # "Referer": url
}


chrome_options = Options()

# Add the headless argument
chrome_options.add_argument("--headless=new") # Or "--headless" for older versions
# (Optional) Add other useful arguments for headless mode
chrome_options.add_argument("--disable-gpu") # Recommended for Windows
chrome_options.add_argument("--no-sandbox") # Recommended for Linux environments
chrome_options.add_argument("--window-size=1920,1080")
resultados_totales = []
lock = threading.Lock()

#Inicializar el navegador 
# driver=webdriver.Chrome()
def scrape_pdf(url):
    #driver=webdriver.Chrome()
    driver=webdriver.Chrome(chrome_options)
    links=[]
    # for n,lin in enumerate[all_links]:
    #Abrir página
    driver.get(url)
    print(f"Hilo {threading.current_thread().name} abriendo: {url}")
    time.sleep(20)

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

    time.sleep(5)
    pdfs1 = driver.find_elements("class name", "galley-link")
    pdfs2=driver.find_elements(By.XPATH, "//a[@class='obj_galley_link']")
    pdfs4=driver.find_elements(By.XPATH, "//a[@class='obj_galley_link pdf']")
    pdfs3=driver.find_elements(By.XPATH, "//a[@class='btn btn-primary']")
    # pdfs1 = driver.find_elements("tag name", "a")
    pdfs=pdfs1+pdfs2+pdfs3+pdfs4
    for pdf in pdfs:
        p = pdf.get_attribute('href')
        if p:
            links.append(p)
    driver.quit()
    print(f"Hilo {threading.current_thread().name} finalizado.")
    with lock:
        resultados_totales.extend(links)

from concurrent.futures import ThreadPoolExecutor, as_completed

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(scrape_pdf, url): url for url in prueba}

        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error en {url}: {e}")

    print("\nTodos los PDFs encontrados:")
    for r in resultados_totales:
        print(r)


os.chdir(r"C:/Users\maria\OneDrive\Documents\UNIIE")


# Crear dataframes
# df_pdfs = pd.DataFrame(resultados_totales, columns=['PDFS'])
df_pdfs = pd.DataFrame(resultados_totales)
print(df_pdfs)
# df_pdfs.to_csv('PDFS_CORREOS.csv', header=True, index=True)
df_pdfs.to_csv('PDFS_CORREOS2.csv', mode="a",header=False, index=True)

# correos=[]
# #Extracción de correos
# for i,lin in enumerate(ll):
#     #Abrir página
#     driver.get(lin)
#     time.sleep(5)

#     scrolldown = driver.execute_script(
#         "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
#     match = False
#     while (match == False):
#         last_count = scrolldown
#         time.sleep(4)
#         scrolldown = driver.execute_script(
#             "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
#         if last_count == scrolldown:
#             match = True

#     time.sleep(4)
#     # cor=""
#     spans = driver.find_elements(By.XPATH, "//span")
#     time.sleep(2)
#     for span in spans:
#         text = span.text
#         if "@" in text:
#             correos.append(text)
            
# print(correos)
# C=set(correos)
# cc=list(C) 

