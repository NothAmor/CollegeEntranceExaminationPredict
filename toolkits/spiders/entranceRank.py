import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "http://www.creditsailing.com"

rankingUrl = "http://www.creditsailing.com/school/yfyd/11/2022/3/2691352.html"
response = requests.get(rankingUrl)
response.encoding = "GBK"
soup = BeautifulSoup(response.text, "html.parser")

locationList = soup.find_all(name="a", attrs={"class": "sch-cell"})

for location in locationList[-5:]:
    print(location.string)
    print(location["href"])