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

#Abrir archivo 
df = pd.read_csv(r"C:/Users\maria\OneDrive\Documents\UNIIE\URLS.csv",header=0)

print(df)
df_p=pd.DataFrame(df)
all_links=df_p["URL"]
# ejemplo=url.iloc[0]
print(all_links)

#Inicializar el navegador 
driver=webdriver.Chrome()
links=[]
for n,lin in enumerate[all_links]:
    #Abrir página
    driver.get(lin)
    time.sleep(5)

    scrolldown = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    match = False
    while (match == False):
        last_count = scrolldown
        time.sleep(4)
        scrolldown = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        if last_count == scrolldown:
            match = True

    time.sleep(4)
    pdfs = driver.find_elements("class name", "galley-link")
    for pdf in pdfs:
        p = pdf.get_attribute('href')
        if p:
            links.append(p)

L=set(links)
ll=list(L)

df_pdfs = pd.DataFrame(ll, columns=['PDFS'])
print(df_pdfs)
df_pdfs.to_csv('PDFS_CORREOS.csv', header=True, index=True)

correos=[]
#Extracción de correos
for i,lin in enumerate(ll):
    #Abrir página
    driver.get(lin)
    time.sleep(5)

    scrolldown = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    match = False
    while (match == False):
        last_count = scrolldown
        time.sleep(4)
        scrolldown = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        if last_count == scrolldown:
            match = True

    time.sleep(4)
    # cor=""
    spans = driver.find_elements(By.XPATH, "//span")
    time.sleep(2)
    for span in spans:
        text = span.text
        if "@" in text:
            correos.append(text)
            
print(correos)
C=set(correos)
cc=list(C) 

