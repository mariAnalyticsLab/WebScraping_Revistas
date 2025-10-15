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
import re
import requests
import io
import fitz  # PyMuPDF
from urllib.parse import unquote, urlparse, parse_qs
import urllib3
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import threading
from threading import Thread
import re, io, time, requests, fitz, urllib3
from urllib.parse import urlparse, parse_qs, unquote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# === Configuración general ===
df = pd.read_csv(r"C:\Users\maria\OneDrive\Documents\UNIIE\PDFS_CORREOS2.csv", header=0)
pdfs = df['pdf']
print(df)

# === Función principal ===
def scrape_emails(url):
    print(f"\n[INICIO] Procesando: {url}")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    def get_orcids_from_page(driver):
        orcids = set()
        correos = set()
        try:
            time.sleep(15)
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframe)
            scrollable_div = driver.find_element(By.ID, "viewerContainer")

            step = 2000
            delay = 1
            scroll_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
            current_scroll = 0

            while current_scroll < scroll_height:
                current_scroll += step
                driver.execute_script("arguments[0].scrollTop = arguments[1]", scrollable_div, current_scroll)
                time.sleep(delay)

                # Buscar ORCID
                links = driver.find_elements(By.XPATH, "//a[contains(@href, 'orcid.org/')]")
                for link in links:
                    href = link.get_attribute("href")
                    if href and "orcid.org" in href:
                        orcids.add(href)

                # Buscar correos
                spans = driver.find_elements(By.XPATH, "//span[contains(text(), '@')]")
                for span in spans:
                    text = span.text.strip()
                    emails_found = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
                    for email in emails_found:
                        correos.add(email)
        except Exception as e:
            print("[ERROR en get_orcids_from_page]:", e)
        return orcids, correos

    def get_emails_from_article(url):
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(20)

        pdf_url = ""
        try:
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            pdf_url = iframe.get_attribute("src")
            print("[INFO] PDF detectado en iframe:", pdf_url)
        except NoSuchElementException:
            try:
                pdf_object = driver.find_element(By.TAG_NAME, "object")
                pdf_url = pdf_object.get_attribute("data")
                print("[INFO] PDF detectado en object:", pdf_url)
            except NoSuchElementException:
                print("[ERROR] No se encontró PDF en la página.")
                pass

        orcids, correos = get_orcids_from_page(driver)
        driver.quit()
        return pdf_url, orcids, correos

    # === Obtener PDF URL y texto ===
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    def get_pdf_url(input_url):
        parsed = urlparse(input_url)
        params = parse_qs(parsed.query)
        if "file" in params:
            pdf_url = unquote(params["file"][0])
            return pdf_url
        return input_url

    def extract_text_from_pdf_url(pdf_url):
        if not pdf_url:
            return ""
        try:
            r = requests.get(pdf_url, headers=headers, verify=False)
            doc = fitz.open(stream=io.BytesIO(r.content), filetype="pdf")
            return "".join(page.get_text() for page in doc)
        except Exception as e:
            print("[ERROR PDF]:", e)
            return ""

    # === Lógica ===
    viewer_url, orcids, correos = get_emails_from_article(url)
    pdf_url = get_pdf_url(viewer_url)
    text = extract_text_from_pdf_url(pdf_url)

    # Extraer emails y orcids del texto
    match_emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    match_orcids = re.findall(r"(?:https?://orcid\.org/)?\d{4}-\d{4}-\d{4}-\d{3}[0-9X]", text)

    correos_finales = list(set(correos) | set(match_emails))
    orcids_finales = list(set(orcids) | set(match_orcids))

    print(f"[OK] {url} => {len(correos_finales)} correos, {len(orcids_finales)} ORCIDs")
    return {
        "url": url,
        "pdf": pdf_url,
        "emails": correos_finales,
        "orcids": orcids_finales
    }

# === Ejecución con hilos ===
if __name__ == "__main__":
    resultados_totales = []
    prueba1 = pdfs[:20]  # prueba pequeña primero

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(scrape_emails, url): url for url in prueba1}

        for future in as_completed(futures):
            url = futures[future]
            try:
                resultado = future.result()
                resultados_totales.append(resultado)
            except Exception as e:
                print(f"[ERROR en {url}]: {e}")

    print("\n===== RESULTADOS TOTALES =====")
    for r in resultados_totales:
        print(f"{r['url']} -> {len(r['emails'])} correos, {len(r['orcids'])} ORCIDs")




    
# prueba1=pdfs[0:200]  
# os.chdir(r"C:/Users\maria\OneDrive\Documents\UNIIE")
# #CORREOS
# df_correos = pd.DataFrame(correos_finales, columns=['Correos'])
# print(df_correos)
# df_correos.to_csv('CORREOS.csv', mode="a", header=False, index=True)
# #ORCIDS
# df_orcids = pd.DataFrame(orcids_finales, columns=['ClaveOrcid'])
# print(df_orcids)
# df_orcids.to_csv('ClavesOrcid.csv', mode="a", header=False, index=True)


if __name__ == "__main__":
    resultados_totales = []
    # prueba1 = pdfs[201:500] #Listo
    prueba1=pdfs[0:100]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(scrape_emails, url): url for url in prueba1}

        for future in as_completed(futures):
            url = futures[future]
            try:
                resultado = future.result()
                resultados_totales.append(resultado)
            except Exception as e:
                print(f"[ERROR en {url}]: {e}")

    # === Guardar resultados ===
    os.chdir(r"C:/Users/maria/OneDrive/Documents/UNIIE")

    # Combinar todos los correos y ORCIDs
    todos_correos = []
    todos_orcids = []

    for r in resultados_totales:
        todos_correos.extend(r["emails"])
        todos_orcids.extend(r["orcids"])

    # Eliminar duplicados
    todos_correos = list(set(todos_correos))
    todos_orcids = list(set(todos_orcids))

    # Crear y guardar DataFrames
    df_correos = pd.DataFrame(todos_correos, columns=["Correos"])
    df_orcids = pd.DataFrame(todos_orcids, columns=["ClaveOrcid"])

    # Guardar (append sin duplicar cabeceras)
    df_correos.to_csv("CORREOS.csv", mode="a", header=not os.path.exists("CORREOS.csv"), index=True)
    df_orcids.to_csv("ClavesOrcid.csv", mode="a", header=not os.path.exists("ClavesOrcid.csv"), index=True)







# # ======= Ejemplo con 10 documentos =====
# orcids_final=[]
# correos_final=[] 
# prueba1=pdfs[11:15]
# for i, prueba in enumerate(prueba1):
#     url,orcids,correos=get_emails_from_article(prueba)
#     orcids=list(orcids)
#     print("URL",url)
#     pdf=get_pdf_url(url)
#     print("PDF", pdf)
#     texto=extract_text_from_pdf_url(pdf)
#     print("Parte del texto", texto[0:100])
#     correo=re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+',texto)
#     orcid_2 = re.findall(r"(?:https?://orcid\.org/)?\d{4}-\d{4}-\d{4}-\d{3}[0-9X]", texto)
#     print("Correos encontrados", correo)
#     if correo:
#         correos_final.extend(correo)
#     orcids=list(orcids)
#     orcid = re.findall(r"\b\d{4}-\d{4}-\d{4}-\d{3}[0-9X]\b", texto_pdf)
#     orcid_mejorado=[]
#     if orcid or orcids:
#         orcids_final.extend(orcid)
#         orcids_final.extend(orcids)
# print("Correos encontrados",correos_final)
# print("ORCID encontrados", orcids_final)
