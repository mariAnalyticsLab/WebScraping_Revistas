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

#Abrir archivo 
df = pd.read_csv(r"C:\Users\maria\Downloads\AUTHORS_master.csv",header=0)
urls=df['article_url']
# ejemplo=urls[1]
ejemplo="https://acreditas.com/index.php/acreditas/article/view/257"

# r = requests.get(ejemplo, auth=('user', 'pass'))
# r.status_code
# r.headers
# r.encoding
# html=r.text
# soup = BeautifulSoup(html, 'html.parser')
# paragraphs = soup.find_all('orcid')

# print(paragraphs)

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
    time.sleep(4)
    scrolldown = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    if last_count == scrolldown:
        match = True

time.sleep(6)
or_links=[]
orcids = driver.find_elements("class name", "orcid" or "ocridImage")
for orcid in orcids:
    p = orcid.get_attribute('href')
    if p:
        or_links.append(p)

# for i, link in enumerate(url):
#     print(link)

print(set(or_links))      
