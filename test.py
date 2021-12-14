# Prueba Data Engineer | OMD
# Elaborado por: Fredy Esteban Coronado Romero
# Fecha: 13-12-2021
# Ejecutar como: python3 test.py

from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
url_falabella = 'https://www.falabella.com.co/falabella-co/category/cat1361001/Computadores--Portatiles-?sred=computador-port%C3%A1til&page=1'


service = Service(
    executable_path="/home/develop/Descargas/chromedriver/chromedriver")
driver = webdriver.Chrome(service=service)

factories = []
refers = []
processors = []
rams = []
screens = []
hardDisks = []
solids = []
prices = []


driver.get(url_falabella)
content = driver.page_source
soup = BeautifulSoup(content)
last_page = int(soup.find_all(
    'li', attrs={'class': 'pagination-item'})[-1].text)+1

for page in range(1, last_page):

    url_falabella = 'https://www.falabella.com.co/falabella-co/category/cat1361001/Computadores--Portatiles-?sred=computador-port%C3%A1til&page={}'.format(
        page)
    print(url_falabella)
    driver.get(url_falabella)
    content = driver.page_source
    soup = BeautifulSoup(content)

    # get factory
    for factory in soup.find_all('b', attrs={'class': 'pod-title'}):
        factories.append(factory.text)

    # get refs
    for ref in soup.find_all('b', attrs={'class': 'pod-subTitle'}):
        refers.append(ref.text)

    # get details
    for detail in soup.find_all('ul', attrs={'class': 'section__pod-bottom-description'}):
        if(len(detail.contents) > 0):
            item = detail.contents
            processors.append(item[0].text[12:])
            rams.append(item[1].text[13:])
            screens.append(item[2].text[23:])
            hardDisks.append(item[3].text[16:]) if item[3].text[:15] == 'Disco duro HDD:' else hardDisks.append(
                'No tiene dato.')
            solids.append(item[4].text[29:]) if item[4].text[:28] == 'Unidad de estado sólido SSD:' else solids.append(
                'No tiene dato.')
        else:
            processors.append('No tiene dato.')
            rams.append('No tiene dato.')
            screens.append('No tiene dato.')
            hardDisks.append('No tiene dato.')
            solids.append('No tiene dato.')

    # get prices
    for price in soup.find_all('span', attrs={'class': 'high'}):
        prices.append(price.text[0:13])


df = pd.DataFrame({'MARCA': factories, 'REFERENCIA': refers, 'PROCESADOR': processors, 'RAM': rams,
                  'PANTALLA': screens, 'DISCODURO': hardDisks, 'DISCOSSOLIDOS': solids, 'PRECIOS': prices})
df.to_csv('laptops.csv', index=False, encoding='utf-8')

print('Termino')
