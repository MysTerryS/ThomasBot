import requests
from bs4 import BeautifulSoup
from random import choice

def GetCity(letter):
    Request = requests.get("https://geo.koltyrin.ru/spisok_gorodov_mira.php?letter={}".format(letter))
    Soup = BeautifulSoup(Request.content, features = 'html.parser')
    Cities = str(Soup.find_all("p", class_ = "bg_white")[0])
    Cities = Cities[Cities.find('">') + 2: Cities.find('\p') if 'и т. д' not in Cities else Cities.find('и т. д')].split(' ')
    return choice(Cities)

def CheckCity(City):
    Request = requests.get("https://geo.koltyrin.ru/goroda_poisk.php?city={}".format(City))
    Soup = BeautifulSoup(Request.content, features = 'html.parser')
    Result = Soup.find_all("h2")
    Result = [str(i).replace("<h2>", '').replace("</h2>", '') for i in Result]
    return "Город {}".format(City) in Result
