import requests
from datetime import datetime, timedelta

API_KEY = "6ba2a85b95064fbe8cb8b95c0331e762"
url = "https://newsapi.org/v2/everything?q={}&apikey={}&language=ru&from={}-{}-{}&to={}-{}-{}"

def GetNews(topic):
    previousDay = datetime.today() - timedelta(days = 1)
    today = datetime.today()
    response = requests.get(url.format(topic, API_KEY, previousDay.year, previousDay.month, previousDay.day, today.year, today.month, today.day))
    answer = ''
    if response.status_code == 200:
        data = response.json()
        articles = data["articles"]
        for i, article in enumerate(articles, 1):
            answer += "{}. {}\n".format(i, article["title"])
            answer += "Источник: {}\n".format(article["source"]["name"])
            answer += "Описание: {}\n".format(article["description"])
            answer += "Ссылка: {}\n".format(article["url"])
            answer += " " * 20 + "-" * 40 + " " * 20 + "\n"
            if i >= 8:
                break
    else:
        answer = "Ошибка при получении новостей. Проверьте правильность запроса."
    return answer
