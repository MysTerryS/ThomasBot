from random import choice

def Quest(start, end):
    return [choice(range(start, end)), choice(range(start, end)), choice(range(start, end))]

def PlayDo(quest, ans):
    return ans in quest
