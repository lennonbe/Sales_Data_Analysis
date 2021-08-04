from bs4 import BeautifulSoup as bs
import requests

page = requests.get('https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films').text
soup = bs(page, "html.parser")

tables = soup.findAll('table', class_="wikitable sortable")
print(tables)

for e in tables:
    print(e)