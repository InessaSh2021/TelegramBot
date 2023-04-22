import telebot   # импорт библиотеки telebot
import time      # импорт библиотеки time
import requests  # импорт библиотеки requests

token = "MY_TOKEN"   # секретный токен telegram-бота, получила с помощью @BotFather

bot = telebot.TeleBot(token)  # команда, привязывающая к переменной "bot" значение токена (token) / bot - ключевая переменная

chat_id = MY_CHAT_ID    # chat_id моего Pythonbot'а. Его можно получить с помощью Эхо-бота или Telegram Bot Raw, работает так же, как Эхо-бот. Нужно отправить ему сообщение и взять chat_id из поля message.chat.id

MSG = "Спасибо за внимание! До свидания!"  # переменная MSG с текстом, которая будет использоваться позже

HELP = """                                 
помощь - вывести список доступных команд.
погода - погода на сегодня.
курсы валют - курсы валют на сегодня.
создать опрос - создать и пройти опрос.
загрузить картинки котиков - загрузить случайную картинку с котиками"""   # переменная HELP с текстом, который используется в функции  echo

@bot.message_handler(content_types=["text"])       # декоратор -  обработчик для всех сообщений, имеющих тип text
def echo(message):                                 # определение функции echo
    bot.send_message(message.chat.id, message.text)   # bot.send_message -  функция обработки сообщений / message.chat.id - чат/ message.text - текст сообщения
    if "помощь" in message.text:                      # УСЛОВИЕ. ЕСЛИ слово "помощь" есть в тексте сообщения в чате,
        bot.send_message(message.chat.id, HELP)       # то функция обработки сообщений чата выводит переменную HELP с текстом (командами)
    elif "загрузить картинки котиков" in message.text: # ИЛИ ЕСЛИ в тексте сообщения в чате есть слово(выражение) "загрузить картинки котиков"
        url = f'https://cataas.com/cat?t=${time.time()}'   # переменная url содержит f-строку с ссылкой на картинку https://cataas.com/cat. После "?" идут параметры. В параметр t добавляем временную метку. Она нужна, чтобы картинка при каждом новом запросе менялась.
        bot.send_photo(chat_id, url)                      # функция обработки сообщений загружает в чат картинку по указанной ссылке url
    elif "погода" in message.text:                      # ИЛИ ЕСЛИ в тексте сообщения в чате есть слово "погода", то
        params = {                                      # параметры для get-запроса взяты с сайта https://www.gismeteo.ru/api/
            'X-Gismeteo-Token': '56b30cb255.3443075',   # api_token взят с сайта https://www.gismeteo.ru/api/
            'Accept-Encoding': 'gzip',
            'curl': '-H',
            'X-Yandex-API-Key': 'My_Yandex_API-Key',   # зарегистрировалась в кабинете разработчика, получила API-KEY Яндекс.Погоды
            'city_name': 'Tambov',
            }
        url = "https://api.gismeteo.net/v2/weather/current/4368/?lang=en"   # url сайта, с которого будут браться данные
        response = requests.get(url=url, params=params)                     # переменная response, которая содержит ответ по запросу get(получить). Это информация  с сайта по указанному url
        bot.send_message(message.chat.id, response)                         # функция обработки сообщений обрабатывает сообщения чата и возвращает ответ в переменной response
    elif "курсы валют" in message.text:                                     # ИЛИ ЕСЛИ в тексте сообщения в чате есть словосочетание "курсы валют", то
        date = requests.get("https://www.cbr-xml-daily.ru/latest.js")       # переменная date содержит запрос GET(получить) по указанному url
        bot.send_message(message.chat.id, date.content)                     # функция обработки сообщений чата выводит содержимое переменной date в чат
    elif "создать опрос" in message.text:           # ИЛИ ЕСЛИ в тексте сообщения в чате есть словосочетание "создать опрос", то
        def survey():                               # определение функции survey
            questions1 = input("Ваше имя: ")         # вопрос1
            questions2 = input("Ваш возраст: ")      # вопрос2
            questions3 = input("Ваше хобби: ")       # вопрос3
            return MSG                               # функция возвращает переменную MSG с сообщением (описана выше)
        bot.send_message(message.chat.id, survey())   # bot.send_message -  функция обработки сообщений / message.chat.id - чат/ survey() - вызов функции

bot.polling(none_stop=True)  # Запуск long-polling  функция не будет останавливаться даже в случае ошибки