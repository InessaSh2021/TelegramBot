import logging     # импорт модуля logging
import os          # импорт модуля os
from aiogram import Bot, Dispatcher, executor, types   # из aiogram импорт Bot, Dispatcher, executor, types
import requests    # импорт requests
from pprint import pprint      # из pprint импорт  pprint
import json        # импорт json

BOT_API_TOKEN = 'MY-API-TOKEN'   # секретный токен telegram-бота, получила с помощью @BotFather

logging.basicConfig(level=logging.INFO)   # Устанавливаем уровень логов на INFO, чтобы видеть сообщения об ошибках

WEATHER_API_KEY = 'MY_WEATHER_API_KEY'  # секретный WEATHER_API_KEY погоды, получила после регистрации на сайте https://home.openweathermap.org/

url_weather = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'     # добавить флаг units со значением metric, чтобы температура показывалась в градусах Цельсия. По умолчанию дается в Кельвинах.

URL_cats = 'http://thecatapi.com/api/images/get?format=src'   # переменная URL_cats содержит ссылку на сайт с картинками котиков. После "?" идут параметры. В параметр format добавляем src (картинку)

bot = Bot(token=BOT_API_TOKEN)    # Создание бота

dp = Dispatcher(bot)  # Создание диспетчера, который будет обрабатывать входящие сообщения

@dp.message_handler(commands=['start'])     # Создаем обработчик для команды /start
async def send_welcome(message: types.Message):    # функция def send_welcome принимает сообщение (и тип переменной: сообщение)
    await message.reply("Здравствуйте!\nЯ - Pythonbot!\nкоманда /help - справка что я умею ")     # функция возвращает сообщение от бота (текст в скобках, в кавычках)

@dp.message_handler(commands=['help'])    # Создаем обработчик для команды /help
async def send_help(message: types.Message):        # функция def send_help принимает сообщение (и тип переменной: сообщение)
    await message.reply("Список команд \nкоманды /image или /img - загружают картинки с котиками \n /weather - данные о погоде \n /exchange - список валют \n /survey - пройти опрос\nкоманда /by - бот, пока!")    # функция возвращает сообщение от бота (текст в скобках, в кавычках)

@dp.message_handler(commands=['image', 'img'])                 # Создаем обработчик для команд /img и /image
async def cmd_image(message: types.Message):                   # функция def cmd_image принимает сообщение (и тип переменной: сообщение)
    await bot.send_photo(message.chat.id, types.InputFile.from_url(URL_cats))   # бот загружает в чат картинки котиков по указанной ссылке URL_cats

@dp.message_handler(commands=['weather'])                       # Создаем обработчик для команды /weather
async def get_weather(message: types.Message):                  # функция def get_weather принимает сообщение (и тип переменной: сообщение)
    city = input("Введите город: ")                             # переменная city содержит ссылку на введенный пользователем объект (на ячейку с введенным значением)
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric')    # переменная response содержит ответ по запросу get(получить). Это информация  с сайта по указанному url
    data = response.json()                                      # переменная data содержит ответ по запросу response в формате словаря
    pprint(data)                                                # красивый вывод значений переменной data
    await message.reply(f'Сводка погоды в городе {city} в PyCharm', get_weather(city, WEATHER_API_KEY))   # сообщение бота в чат (используется f-строка) и запуск функции get_weather(она принимает на вход город и API сайта погоды, указанного по ссылке)

@dp.message_handler(commands=['exchange'])                       # Создаем обработчик для команды /exchange
async def cmd_exchange(message: types.Message):                  # функция def cmd_exchange принимает сообщение (и тип переменной: сообщение)
    date = requests.get("https://www.cbr-xml-daily.ru/latest.js")  # переменная date содержит запрос GET(получить) по указанному url
    await bot.send_message(message.chat.id,  date.content)         # бот возвращает в чат содержимое(content) переменной date

@dp.message_handler(commands=['survey'])                       # Создаем обработчик для команды /survey
async def survey(message: types.Message):                      # функция def cmd_exchange принимает сообщение (и тип переменной: сообщение)
    count = 0                                                  # переменной count присвоено значение "0"
    answer1 = 1                                                # переменной answer1 присвоено значение "1"
    answer2 = 2                                                # переменной answer2 присвоено значение "2"
    answer3 = 3                                                # переменной answer3 присвоено значение "3"
    answer4 = 4                                                # переменной answer4 присвоено значение "4"

    name = input("Как вас зовут?\n")                           # переменная name содержит ссылку на введенный пользователем объект - имя пользователя
    print("Здравствуйте: ", name)                              # вывод сообщения бота с использованием имени пользователя

    questions = int(input("Ваш любимый жанр фильмов? \n 1- боевики 2-детективы 3-фантастика\n"))    # переменной questions  подяется на вход число
    if (questions == answer1) or (questions == answer2) or (questions == answer3):                  # УСЛОВИЕ if. Если значение переменной questions равно числу любого из предложенных ответов,
        count += 1                                                                                  # то к значению счетчика прибавить "1"
    questions = int(input("Ваша любимая музыка? \n 1- классика 2-рэп 3-поп\n"))                     # переменной questions  подяется на вход число
    if (questions == answer1) or (questions == answer2) or (questions == answer3):                  # УСЛОВИЕ if. Если значение переменной questions равно числу любого из предложенных ответов,
         count += 1                                                                                 # то к значению счетчика прибавить "1"
    questions = int(input("Ваш любимый цвет? \n 1- красный 2-желтый 3-зеленый\n"))                  # переменной questions  подяется на вход число
    if (questions == answer1) or (questions == answer2) or (questions == answer3):                  # УСЛОВИЕ if. Если значение переменной questions равно числу любого из предложенных ответов,
         count += 1                                                                                 # то к значению счетчика прибавить "1"
    questions = int(input("Ваше любимый время года? \n 1- осень 2-зима 3-весна 4- лето\n"))         # переменной questions  подяется на вход число
    if (questions == answer1) or (questions == answer2) or (questions == answer3) or (questions == answer4):   # УСЛОВИЕ if. Если значение переменной questions равно числу любого из предложенных ответов,
         count += 1                                                                                 # то к значению счетчика прибавить "1"
    if count <= 2:          # если значение счетчика больше или равно двум
        print(f'{name}, ', "мы с вами очень разные")         # вывести надпись в скобках и кавычках с использованием имени пользователя
    else:                                                    #  в противном случае  (if - else)
        print(f'{name}, ', "мы с вами подружимся")           # вывести другую надпись в скобках и кавычках с использованием имени пользователя
    await bot.send_message(message.chat.id, survey())        # бот вводит сообщение в чат, и происходит запуск функции def survey()

@dp.message_handler(commands=['by'])     # Создаем обработчик для команды /by
async def send_welcome(message: types.Message):     # функция def send_welcome принимает сообщение (и тип переменной: сообщение)
    await message.reply("До скорой встречи!")       # функция возвращает сообщение от бота (текст в скобках, в кавычках)

if __name__ == '__main__':    # если имя файла main, то запустить файл
    try:                      # обработчик исключений try-txcept/ Запускается "цикл обработки входящих сообщений", в случае ошибки выбрасывается ошибка (except Exception) и происходит выход из цикла с кодом "0" (os.exit(0))
        executor.start_polling(dp, skip_updates=True)  # Запускаем цикл обработки входящих сообщений
    except Exception:
        os.exit(0)


# Работала в IDE PyCharm, версия aiogram 2.0
# в Terminal установила aiorram pip install -U aiogram
# в Terminal установила библиотеку requests  pip install requests