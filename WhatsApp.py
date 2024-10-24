from whatsapp_chatbot_python import GreenAPIBot, BaseStates, Notification
from InfoSearch import GetInfoFromWiki
from Book import *
from random import choice
from QuestNmb import *
from WordQuest import *
from CitiesGame import *
from Weather import *
from News import *
from ExchangeRate import *

statesVar = dict()
letters = [chr(i) for i in range(ord('А'), ord('Я'))]

class Bot:
    def __init__(self, idInstance, apiTokenInstance):
        self.__idInstance = idInstance
        self.__apiTokenInstance = apiTokenInstance

    def Create(self):
        return GreenAPIBot(self.__idInstance, self.__apiTokenInstance)
 
class States(BaseStates):
    WORD_GAME = "WORD_GAME"
    NUMBER_GAME = "NUMBER_GAME"
    CITIES_GAME = "CITIES_GAME"
    WIKIPEDIA = "WIKIPEDIA"
    CALC = "CALC"
    SEARCH_BOOK = "SEARCH_BOOK"
    WEATHER = "WEATHER"
    NEWS = "NEWS"
    RATEBase = "RATEBase"
    RATETarget = "RATETarget"

ID_INSTANCE = ""                                                        # YOUR ID_INSTANCE
API_TOKEN_INSTANCE = ""                                                 # YOUR API_TOKEN_INSTANCE

bot = Bot(ID_INSTANCE, API_TOKEN_INSTANCE)
bot = bot.Create()

@bot.router.message(command = "menu")
def menu_handler(notification:Notification) -> None:
    sender = notification.sender
    state = notification.state_manager.get_state(sender)
    if not state:
        return MainHandler(notification)
    else:
        notification.state_manager.delete_state(sender)

@bot.router.message(text_message = ["/start", "start", "hello"], state = None)
def MainHandler(notification: Notification) -> None:
    notification.answer(
            ("Пожалуйста, выберите действие:\n"
             "1. Википедия\n"
             "2. Калькулятор\n"
             "3. Найди мне книгу\n"
             "4. Что бы почитать сегодня\n"
             "5. Загадай число\n"
             "6. Загадай слово\n"
             "7. Поиграем в города\n"
             "8. Погода\n"
             "9. Последние новости\n"
             "10. Курс валют\n")
            )

@bot.router.message(text_message = ["1", "Википедия"], state = None)
def Wikipedia(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, States.WIKIPEDIA.value)
    notification.answer(
            "Окей, о чем вы хотите узнать в Википедии?"
            )

@bot.router.message(text_message = ["2", "Калькулятор"], state = None)
def Calc(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, States.CALC.value)
    notification.answer(
            "Введите выражение"
            )

@bot.router.message(text_message = ["3", "Найди мне книгу"], state = None)
def SearchBook(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, States.SEARCH_BOOK.value)
    notification.answer(
            "На какую тему ищем?"
            )

@bot.router.message(text_message = ["4", "Что бы почитать сегодня"], state = None)
def SearchBook(notification: Notification) -> None:
    notification.answer(GetBook())

@bot.router.message(text_message = ["5", "Загадай число"], state = None)
def NumberGame(notification: Notification) -> None:
    global statesVar
    sender = notification.sender
    notification.state_manager.update_state(sender, States.NUMBER_GAME.value)
    start = choice(range(0, 1000))
    end = start + choice(range(1, 100))
    statesVar = {'numbers': Quest(start, end), 'chances': 3}
    notification.answer("Загадано число на отрезке [{}; {}]. Ваша задача отгадать.\nУ вас всего три попытки".format(start, end))

@bot.router.message(text_message = ["6", "Загадай слово"], state = None)
def WordGame(notification: Notification) -> None:
    global statesVar
    sender = notification.sender
    notification.state_manager.update_state(sender, States.WORD_GAME.value)
    word = GetWord()
    quest = '*' * len(word)
    statesVar = {"word": word, "quest": quest, "letters": set(), "chances": 10}
    notification.answer("Загадано слово {}. Ваша задача отгадать его.\nУ вас всего десяток попыток.\nВы можете вводить слово по буквам, можете целиком, но если ошибетесь то проиграете.".format(statesVar["quest"]))

@bot.router.message(text_message = ["7", "Поиграем в города"])
def CityGame(notification: Notification) -> None:
    global statesVar
    city = GetCity(choice(letters))
    statesVar = {"city": city}
    sender = notification.sender
    notification.state_manager.update_state(sender, States.CITIES_GAME.value)
    notification.answer(city)

@bot.router.message(text_message = ["8", "Погода"])
def Weather(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, States.WEATHER.value)
    notification.answer("В каком населенном пункте вы находитесь?")

@bot.router.message(text_message = ["9", "Последние новости"])
def News(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, States.NEWS.value)
    notification.answer(
            ("1. Политика\n"
             "2. Экономика\n"
             "3. Бизнес\n"
             "4. Развлечения\n"
             "5. Здоровье\n"
             "6. Наука\n"
             "7. Технологии\n"
             "8. Спорт"
             )
            )

@bot.router.message(text_message = ["10", "Курс валют"])
def Rates(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, States.RATEBase.value)
    notification.answer("Базовая валюта(чтобы получить список кодов - list)")

#@bot.router.message(text_message = "list", state = [States.RATEBase.value, States.RATETarget.value])
@bot.router.message(text_message = "list")
def RateHelp(notification: Notification) -> None:
    for each in rates:
        answer = ''
        for rate in each:
            answer += rate + " - " + each[rate] + "\n"
        notification.answer(answer)

@bot.router.message(state = States.RATEBase.value)
def Rates_(notification: Notification) -> None:
    global statesVar
    statesVar["base"] = notification.message_text
    sender = notification.sender
    notification.state_manager.update_state(sender, States.RATETarget.value)
    notification.answer("Целевая валюта(чтобы получить список кодов - list)")

@bot.router.message(state = States.RATETarget.value)
def Rates__(notification: Notification) -> None:
    global statesVar
    statesVar["target"] = notification.message_text
    sender = notification.sender
    notification.state_manager.update_state(sender, None)
    notification.answer(str(GetRate(statesVar["base"], statesVar["target"])))

@bot.router.message(state = States.NEWS.value)
def News_(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, None)
    nmbrToTopic = {"1": "Политика", "2": "Экономика", "3": "Бизнес", 
                   "4": "Развлечения", "5": "Здоровье", "6": "Наука",
                   "7": "Технологии", "8": "Спорт"
                   }
    if notification.message_text in nmbrToTopic.keys():
        topic = nmbrToTopic[notification.message_text]
    else:
        topic = notification.message_text
    notification.answer(GetNews(topic))

@bot.router.message(state = States.WEATHER.value)
def Weather_(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, None)
    notification.answer(GetWeather(notification.message_text))

@bot.router.message(state = States.CITIES_GAME.value)
def CityGame_(notification: Notification) -> None:
    global statesVar
    text = notification.message_text
    text_ = statesVar["city"]
    if CheckCity(text) and (text[0].lower() == text_[-1] or (text_[-1] == 'ь' or text_[-1] == "ы") and text[0].lower() == text_[-2]):
        lastLetter = text[-1].upper() if text[-1] != 'ь' and text[-1] != 'ы' else text[-2].upper()
        statesVar["city"] = GetCity(lastLetter)
        notification.answer(statesVar["city"])
    else:
        notification.answer("Игра окончена")
        sender = notification.sender
        notification.state_manager.update_state(sender, None)
        statesVar.clear()

@bot.router.message(state = States.WORD_GAME.value)
def WordGame_(notification: Notification) -> None:
    global statesVar
    newValue = QuestWordProcess(statesVar["word"], notification.message_text.lower(),
                                statesVar["quest"], statesVar["letters"],
                                statesVar["chances"])
    
    statesVar["quest"] = newValue[0]
    statesVar["letters"] = newValue[1]
    statesVar["chances"] = newValue[2]

    if statesVar["chances"] != 0:
        if statesVar["quest"] == statesVar["word"]:
            notification.answer("Вы выиграли! Это слово {}".format(statesVar["word"]))
            sender = notification.sender
            notification.state_manager.update_state(sender, None)
            statesVar.clear()
        else:
            if newValue[3]:
                notification.answer("Вы отгадали букву. Слово {}.\nУ вас осталось {} попыт{}. Использованные буквы: {}".format(statesVar["quest"], statesVar["chances"], "ок" if statesVar["chances"] >= 5 else "ка" if statesVar["chances"] == 1 else "ки", statesVar["letters"]))
            else:
                notification.answer("Вы не отгадали букву. Слово {}.\nУ вас осталось {} попыт{}. Использованные буквы: {}".format(statesVar["quest"], statesVar["chances"], "ок" if statesVar["chances"] >= 5 else "ка" if statesVar["chances"] == 1 else "ки", statesVar["letters"]))
    else:
        notification.answer("Вы проиграли. Это было слово {}.".format(statesVar["word"]))
        sender = notification.sender
        notification.state_manager.update_state(sender, None)
        statesVar.clear()

@bot.router.message(state = States.NUMBER_GAME.value)
def NumberGame_(notification: Notification) -> None:
    global statesVar
    if PlayDo(statesVar["numbers"], notification.message_text):
        notification.answer("Вы верно отгадали число!")
        sender = notification.sender
        notification.state_manager.update_state(sender, None)
        statesVar.clear()
    else:
        statesVar["chances"] -= 1
        if statesVar["chances"] > 0:
            notification.answer("Неверно. У вас осталось {} попыт{}".format(statesVar["chances"], "ки" if statesVar["chances"] == 2 else "ка"))
        else:
            notification.answer("Вы проиграли.")
            sender = notification.sender
            notification.state_manager.update_state(sender, None)
            statesVar.clear()

@bot.router.message(state = States.SEARCH_BOOK.value)
def SearchBook_(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, None)
    notification.answer(FindBooks(notification.message_text))

@bot.router.message(state = States.CALC.value)
def Calc_(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, None)
    notification.answer(str(eval(notification.message_text)))

@bot.router.message(state = States.WIKIPEDIA.value)
def SearchWiki(notification: Notification) -> None:
    sender = notification.sender
    notification.state_manager.update_state(sender, None)
    notification.answer(GetInfoFromWiki(notification.message_text))

bot.run_forever()
