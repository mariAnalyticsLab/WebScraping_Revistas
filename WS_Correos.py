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


chrome_options = Options()

# Add the headless argument
chrome_options.add_argument("--headless=new") # Or "--headless" for older versions
# (Optional) Add other useful arguments for headless mode
chrome_options.add_argument("--disable-gpu") # Recommended for Windows
chrome_options.add_argument("--no-sandbox") # Recommended for Linux environments
chrome_options.add_argument("--window-size=1920,1080")

df = pd.read_csv(r"C:\Users\maria\OneDrive\Documents\UNIIE\PDFS_CORREOS.csv",header=0)
pdfs=df['PDFS']
ejemplo="https://www.revistas.uneb.br/baeducmatematica/article/view/23636/15556"

def get_emails_from_article(url):
    driver = webdriver.Chrome()
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
                driver.quit()
    return pdf_url



# Ignorar warnings SSL si hay problemas de certificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36",
    "Referer": "https://www.revistas.uneb.br/"
}

def get_pdf_url(input_url):
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

# ======== Ejemplo ========
viewer_url = get_emails_from_article(ejemplo)

pdf_url = get_pdf_url(viewer_url)
texto_pdf = extract_text_from_pdf_url(pdf_url)
# print(texto_pdf[:1000])

match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', texto_pdf)
print(match)