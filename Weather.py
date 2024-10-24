import requests

API_KEY = "faf7f447ced6e4956101ae20ebe1b69b"
url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

def GetWeather(city):
    response = requests.get(url.format(city, API_KEY))
    answer = "Ошибка при получении погоды для населенного пункта {}. Проверьте правильность названия.".format(city)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        answer = "Температура: {}\nВлажность воздуха: {}\nСкорость ветра: {}".format(temp, humidity, wind_speed)
    return answer
