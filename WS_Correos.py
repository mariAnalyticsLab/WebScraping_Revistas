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

chrome_options = Options()

# Add the headless argument
chrome_options.add_argument("--headless=new") # Or "--headless" for older versions
# (Optional) Add other useful arguments for headless mode
chrome_options.add_argument("--disable-gpu") # Recommended for Windows
chrome_options.add_argument("--no-sandbox") # Recommended for Linux environments
chrome_options.add_argument("--window-size=1920,1080")

df = pd.read_csv(r"C:\Users\maria\OneDrive\Documents\UNIIE\PDFS_CORREOS.csv",header=0)
pdfs=df['PDFS']
ejemplo=pdfs[0]

def get_orcids_from_page(driver):
    orcids = set()
    correos=set()
    try:
        time.sleep(10)
        # --- cambiar al iframe donde está el PDF ---
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)

        # --- encontrar el contenedor scrollable ---
        scrollable_div = driver.find_element(By.ID, "viewerContainer")
        # --- hacer scroll de forma gradual ---
        step = 2000   # píxeles por salto
        delay = 1    # segundos de espera entre saltos

        scroll_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

        current_scroll = 0
        while current_scroll < scroll_height:
            current_scroll += step
            driver.execute_script("arguments[0].scrollTop = arguments[1]", scrollable_div, current_scroll)
            time.sleep(delay) 
            try:
                # Buscar todos los <a> que apunten a orcid.org
                links = driver.find_elements(By.XPATH, "//a[contains(@href, 'orcid.org/')]")
                for link in links:
                    href = link.get_attribute("href")
                    if href and "orcid.org" in href:
                        orcids.add(href)
            except Exception as e:
                print("[ERROR] No se pudieron extraer ORCIDs:", e)
            try:
                # Buscar todos los <span> que contengan posibles correos
                spans = driver.find_elements(By.XPATH, "//span[contains(text(), '@')]")
                for span in spans:
                    text = span.text.strip()
                    # Verificar con regex si el texto parece un correo válido
                    emails_found = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
                    for email in emails_found:
                        correos.add(email)
            except Exception as e:
                print("Error al extraer correos de los spans:", e)
    except:
        pass
    return orcids,correos

def get_emails_from_article(url):
    driver=webdriver.Chrome(chrome_options)
    # driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
    pdf_url = ""

    try:
        # --- Caso 1: buscar iframe con PDF ---
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        pdf_url = iframe.get_attribute("src")
        print("[INFO] PDF detectado en iframe:", pdf_url)

    except NoSuchElementException:
        try:
            # --- Caso 2: buscar object/embed con PDF ---
            pdf_object = driver.find_element(By.TAG_NAME, "object")
            pdf_url = pdf_object.get_attribute("data")
            print("[INFO] PDF detectado en object:", pdf_url)

        except NoSuchElementException:
            try:
                # --- Caso 3: PDF.js viewer (div#viewerContainer) ---
                viewer = driver.find_element(By.ID, "viewerContainer")
                print("[INFO] Detectado PDF.js, necesitas URL de descarga")

                # en PDF.js, buscar <a id="download"> o similar
                download_link = driver.find_element(By.ID, "download")
                pdf_url = download_link.get_attribute("href")
                print("[INFO] PDF detectado en PDF.js:", pdf_url)

            except NoSuchElementException:
                print("[ERROR] No se pudo localizar PDF en la página.")
                pass
    orcids,correos=get_orcids_from_page(driver)
    if orcids:
        print("Orcids encontrados")
        print(orcids)
        orcids=orcids
    driver.quit()
    return pdf_url,orcids,correos



# Ignorar warnings SSL si hay problemas de certificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36",
    # "Referer": url
}

def get_pdf_url(input_url):
    if isinstance(input_url, tuple):
        input_url = input_url[0]
    parsed = urlparse(input_url)
    params = parse_qs(parsed.query)
    
    if "file" in params:
        # Visor PDF.js
        pdf_url_encoded = params["file"][0]
        pdf_url = unquote(pdf_url_encoded)
        print("[INFO] Detectado visor PDF.js. URL real del PDF:", pdf_url)
        return pdf_url
    else:
        # PDF directo
        print("[INFO] URL directa de PDF:", input_url)
        return input_url

def extract_text_from_pdf_url(pdf_url):
    if not pdf_url:
        print("[ERROR] URL del PDF vacía")
        return ""
    
    try:
        response = requests.get(pdf_url, headers=headers, verify=False)
        response.raise_for_status()
        doc = fitz.open(stream=io.BytesIO(response.content), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        print("[ERROR] No se pudo procesar el PDF:", e)
        return ""


prueba1=pdfs[0:10]
orcids_finales=[]
correos_finales=[]
for i,ejemplo in enumerate(prueba1):
    viewer_url,orcids,correos = get_emails_from_article(ejemplo)
    # # pdf_url= get_emails_from_article(viewer_url)
    # # parsed = urlparse(pdf_url)
    pdf_url= get_pdf_url(viewer_url)
    # # print("Orcids", orcids)
    # # print("pdf", pdf_url)
    texto_pdf = extract_text_from_pdf_url(pdf_url)
    print(texto_pdf[:1000])
    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', texto_pdf)
    orcids=list(set(orcids))
    orcid = re.findall(r"\b\d{4}-\d{4}-\d{4}-\d{3}[0-9X]\b", texto_pdf)
    orcids_finales.extend(orcids)
    correos=list(set(correos))
    correos_finales.extend(correos)
    correos_finales.extend(match)
    if orcid:
        for m in orcid: 
            orcid="https://orcid" + m
            orcids_finales.extend(orcid)
    orcid_2 = re.findall(r"(?:https?://orcid\.org/)?\d{4}-\d{4}-\d{4}-\d{3}[0-9X]", texto_pdf)
    orcids_finales.extend(orcid_2)
    print("Orcids",orcids)
    print("Correos",match)
    
print("Todos orcids",orcids_finales)
print("todos correos",correos_finales)
    
    
os.chdir(r"C:/Users\maria\OneDrive\Documents\UNIIE")
#CORREOS
df_correos = pd.DataFrame(correos_finales, columns=['Correos'])
print(df_correos)
df_correos.to_csv('CORREOS.csv', mode="a", header=False, index=True)
#ORCIDS
df_orcids = pd.DataFrame(orcids_finales, columns=['ClaveOrcid'])
print(df_orcids)
df_orcids.to_csv('ClavesOrcid.csv', mode="a", header=False, index=True)









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
