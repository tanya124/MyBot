import vkapi
import requests
from settings import key_appid
import time

def get_weather_today(city):
    url = 'http://api.openweathermap.org/data/2.5/weather'

    try:
        data = requests.get(url, params={'lang': 'ru', 'appid': key_appid, 'q': city}).json()
    except ValueError:
        return

    result = ''

    try:
        if data['cod'] == '404':
            result = 'Город не найден.'
        else:
            weather = data['weather']
            result += weather[0]['description'].capitalize() + '\n'
            temp = data['main']
            result += 'Температура воздуха: ' + str(round(temp['temp']-273, 1)) + ' °С' + '\n'

    except KeyError:
        return

    return result

def get_weather_not_today(body):
    if len(body.split()) > 1:
        city = body.split()[0][0:-1]
        day = body.split()[1].split('.')[0]
        month = body.split()[1].split('.')[1]
        url = 'http://api.openweathermap.org/data/2.5/forecast'
    else:
        return 'Данные введены некорректно. Формат ввода: город, DD.MM'

    try:
        data = requests.get(url, params={'lang': 'ru', 'appid': key_appid, 'q': city}).json()
    except ValueError:
        return

    result = ''

    try:
        for i in data['list']:
            date = time.strptime(i['dt_txt'], "%Y-%m-%d %H:%M:%S")
            #date = i['dt_txt'].split()[0]
            i_day = date.tm_mday
            i_month = date.tm_mon

            if int(day)==i_day and int(month)==i_month:
                result += city.capitalize() + ' погода на ' + day + '.' + month + ':' + '\n'
                weather = i['weather']
                result += weather[0]['description'].capitalize() + '\n'
                temp = i['main']
                result += 'Температура воздуха: ' + str(round(temp['temp']-273, 1)) + ' °С' + '\n'
                break

            else:
                pass

        cod = data['cod']

    except KeyError:
        return



    if cod == '404':
        return 'Город не найден.'
    elif result == '':
        return 'Данные введены некорректно. Формат ввода: город, DD.MM. Прогноз погоды доступен только на 5 дней вперёд.'
    else:
        return result



def create_answer(data, token):
    user_id = data['user_id']

    if data['body'].split()[0][-1] != ',':
        message = get_weather_today(data['body'].lower())
    else:
        message = get_weather_not_today(data['body'].lower())

    vkapi.send_message(user_id, token, message)
