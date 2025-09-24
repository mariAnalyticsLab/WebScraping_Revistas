#Extracción de URLS con selenium

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
df = pd.read_csv(r"C:\Users\maria\OneDrive\Documents\UNIIE\URLS.csv",header=0)

print(df)
df_p=pd.DataFrame(df)
url=df_p["URL"]
ejemplo=url.iloc[0]
print(ejemplo)

#Inicializar el navegador 
driver=webdriver.Chrome()
time.sleep(5)

#Abrir página
driver.get(ejemplo)
time.sleep(3)

scrolldown = driver.execute_script(
    "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
match = False
while (match == False):
    last_count = scrolldown
    time.sleep(3)
    scrolldown = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    if last_count == scrolldown:
        match = True

time.sleep(4)
links=[]
pdfs = driver.find_elements("class name", "galley-link")
for pdf in pdfs:
    p = pdf.get_attribute('href')
    if p:
        links.append(p)

# for i, link in enumerate(url):
#     print(link)

print(links)    