#Extracción de URLS con selenium
#Ejemplo con un URL
import csv
import pandas as pd
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
from threading import Thread
from selenium.webdriver.chrome.options import Options

#Abrir archivo 
df = pd.read_csv(r"C:/Users\maria\OneDrive\Documents\UNIIE\URLS.csv",header=0)

print(df)
df_p=pd.DataFrame(df)
# all_links=df_p["URL"]
all_links = df['URL'].dropna().astype(str).tolist()
prueba=all_links[151:] 
# ejemplo=url.iloc[0]
# print(all_links)

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
    driver=webdriver.Chrome(chrome_options)
    links=[]
    # for n,lin in enumerate[all_links]:
    #Abrir página
    driver.get(url)
    print(f"Hilo {threading.current_thread().name} abriendo: {url}")
    time.sleep(10)

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
    pdfs = driver.find_elements("class name", "galley-link")
    for pdf in pdfs:
        p = pdf.get_attribute('href')
        if p:
            links.append(p)
    driver.quit()
    print(f"Hilo {threading.current_thread().name} finalizado.")
    with lock:
        resultados_totales.extend(links)

if __name__ == "__main__":
    hilos = []

    for url in prueba:
        # Se puede añadir un nombre al hilo para mejor identificación
        hilo = threading.Thread(target=scrape_pdf, args=(url,), name=f"WebDriver-{url.split('//')[1].split('/')[0]}")
        hilos.append(hilo)
        hilo.start() # Inicia la ejecución del hilo

    # Espera a que todos los hilos terminen
    for hilo in hilos:
        hilo.join()

    print("\nTodos los PDFs encontrados:")
    for r in resultados_totales:
        print(r)


os.chdir(r"C:/Users\maria\OneDrive\Documents\UNIIE")


# Crear dataframes
# df_pdfs = pd.DataFrame(resultados_totales, columns=['PDFS'])
df_pdfs = pd.DataFrame(resultados_totales)
print(df_pdfs)
# df_pdfs.to_csv('PDFS_CORREOS.csv', header=True, index=True)
df_pdfs.to_csv('PDFS_CORREOS.csv', mode="a", header=False, index=True)

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

