import requests
from bs4 import BeautifulSoup
from random import choice

def GetBook():
    Request = requests.get("http://readly.ru/books/i_am_lucky/?show=1")
    Soup = BeautifulSoup(Request.content, features = 'html.parser')
    First = str(Soup.find_all("h3", class_ = "blvi__title")[0])
    Link = First[First.find('href="') + 6: First.find('/"') + 1]
    Name = First[First.find('/">') + 3: First.find("</a>\n</h3>")]
    First = str(Soup.find_all("div", class_ = "blvi__book_info")[0])
    Author = First[First.find('/">') + 3: First.find('</a>,')]
    Date = First[First.find('год') - 5: First.find(' год')]
    Genre = str(Soup.find_all("div", class_ = "blvi__book_info")[0]).replace('  ', '').replace('\n', '')
    Genre = Genre[Genre.find('год,') + 4:]
    Genre = Genre.split(',')
    Genre = [Genre[i][Genre[i].find('">') + 2: Genre[i].find('</a>')] for i in range(len(Genre))]
    Description = str(Soup.find_all("div", class_ = "book--desc")[0])
    Description = Description[Description.find('">') + 2: Description.find('</div>')]
    return "Вот что я тебе рекомендую:\n{}\nАвтор: {}\nГод издания: {}\nЖанр: {}\nОписание: {}\nБолее подробную информацию смотри по ссылке ниже:\nhttp://readly.ru{}".format(Name, Author, Date, ', '.join(Genre), Description, Link)

def FindBooks(Dates):
    Request = requests.get('https://fbsearch.ru/search.php?q={}&field=text&sort=&minSize=&modified=&minRate=&includeSite%5B%5D=fanfics.me&includeSite%5B%5D=ficbook.net&includeSite%5B%5D=flibusta.net&includeSite%5B%5D=samlib.ru&searchCheckHosts=fanfics.me%2Cficbook.net%2Cflibusta.net%2Csamlib.ru'.format(Dates))
    Soup = BeautifulSoup(Request.text, features = 'html.parser')
    First = Soup.find_all('h3')
    Second = Soup.find_all('div', class_ = 'col-sm-12 annotation')
    First, Second = [str(i) for i in First], [str(i) for i in Second]
    Second = [i[i.find('</b>') + 4: i.find('</span>')] for i in Second]
    Second = [i.replace('  ', '') for i in Second]
    First = [i[i.find('href="') + 6 : i.find('</a>')] for i in First]
    Links, Names = [i[:i.find('">')] for i in First], [i[i.find('">') + 2:] for i in First]
    Third = Soup.find_all('a', class_ = 'serp-host away')
    Third = [str(i) for i in Third]
    Third = [i[i.find('">') + 2: i.find('</a>')] for i in Third]
    Result = ['{}\nСерия: {}\nАннотации: {}\nИсточник: https://fbsearch.ru/{}'.format(i, j, k, t) for (i, j, k, t) in zip(Names, Third, Second, Links)]
    if len(Result) == 0:
        return 'По вашему запросу ничего не найдено'
    else:
        n = choice(range(3, 6))
        return 'Вот что было найдено по вашему запросу:\n{}'.format('\n\n\n'.join(['{}. {}'.format(i + 1, Result.pop()) for i in range(n)]))
