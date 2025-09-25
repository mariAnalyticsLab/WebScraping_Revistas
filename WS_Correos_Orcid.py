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
import time
import os

#Abrir archivo 
df = pd.read_csv(r"C:\Users\maria\Downloads\AUTHORS_master.csv",header=0)
urls=df['article_url']
print(urls)
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

or_links=[]
driver=webdriver.Chrome()
time.sleep(5)  
for i, url in enumerate(urls):
    driver.get(url)
    time.sleep(5)
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

    time.sleep(4)
    or_l=[]
    orcids1 = driver.find_elements(By.XPATH, "//span[contains(@class, 'orcid')]//a")
    orcids2 = driver.find_elements(By.XPATH, "//span[contains(@class, 'orcidImage')]//a")
    orcids=orcids1+orcids2
    for orcid in orcids:
        p = orcid.get_attribute('href')
        if p:
            or_l.append(p)
    or_l.append(or_links)
       
OL=set(or_links)
OLS=list(OL)

#Directorio
os.chdir(r"C:/Users\maria\OneDrive\Documents\UNIIE")


# Crear dataframes
df_orcids = pd.DataFrame(OLS, columns=['ClaveOrcid'])
print(df_orcids)
# df_correos = pd.DataFrame(correos, columns=['Correos'])


df_orcids.to_csv('ClavesOrcid.csv', header=True, index=True)
