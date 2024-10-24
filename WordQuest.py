from random import choice
from time import sleep
from pickle import dumps, loads

def QuestLetter(Word, Quest, Letter):
    k = Word.count(Letter)
    QuestArray = list(Quest)
    WordReplaceLetter = list(Word)
    while k>0:
        QuestArray[Word.find(Letter)] = Letter
        WordReplaceLetter[Word.find(Letter)] = "*"
        Word = "".join(WordReplaceLetter)
        k-=1
        if k == 0:
            Word = "".join(WordReplaceLetter).replace("*", Letter)
    return "".join(QuestArray)

f = open(".Words", mode = "rb")

WordArray = f.read()

f.close()

WordArray = loads(WordArray)

Points = 0

WordArray = WordArray[:len(WordArray) - 1]

def GetWord():
    return choice(WordArray).lower()

def QuestWordProcess(Word, Letter, Quest, Letters, Chances):
    if Letter == Word:
        Stars = Quest.count('*')
        Quest = Letter
    elif len(Letter) == len(Word) and Letter != Word:
        Stars = 0
        Chances = 0
    elif Letter in Word:
        Quest = QuestLetter(Word, Quest, Letter)
        Letters|=set(Letter)
        Stars = True
    elif Letter not in Word and Letter not in Letters:
        Letters|=set(Letter)
        Chances-=1
        Stars = False
    elif Letter in Letters:
        Stars = False
    return [Quest, Letters, Chances, Stars]
