import json
from datetime import date


def find_birthdays():
    with open('data.json') as f:
        d = json.load(f)

    today = date.today()
    today_ru = today.strftime("%d.%m.%Y")
    birthdays_today = []
    anniversary_today = []

    for item in d['data']:
        if item['birthday'][:-4] == today_ru[:-4]:
            age = date.today().year - int(item['birthday'][-4:])
            if (age > 49) and (age % 5 == 0):
                anniversary_today.append(item)
            else:
                birthdays_today.append(item)

    return birthdays_today, anniversary_today
