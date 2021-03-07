import re
import time

import requests
from bs4 import BeautifulSoup

import telebot

import requests

MOODLE_LOGIN=student = ""
MOODLE_PASSWORD=       ""

token = "1655734764:AAETg5UAi3HbPpdGlWqxXuunefAqZtOjut4"
student = ""

url_login = 'https://moodle.zp.edu.ua/login/index.php'
url_main = 'https://moodle.zp.edu.ua/course/view.php?id=334'

"""

КГ +
СПЗ+
КС +
КМ +
МС 
СИОЗОТ
"""


class ParsingMoodle:
    client = ''
    logintoken = ''

    def __init__(self, username, password):
        print("Объект создан")
        self.client = requests.Session()
        html = self.client.get(url_login)
        soup = BeautifulSoup(html.text, 'lxml')
        logintoken = soup.find("input", {"name": "logintoken"})['value']
        payload = {
            'anchor': '',
            'logintoken': logintoken,
            'username': username,
            'password': password,
            'rememberusername': 1,
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)  Safari/537.36',
            'Connection': 'keep-alive',
        }
        r = self.client.post(url_login, data=payload, headers=headers)

    def subjectKg(self):
        print("________________________________________")
        html = self.client.get("https://moodle.zp.edu.ua/course/view.php?id=334")
        soup = BeautifulSoup(html.text, 'lxml')
        result = soup.find(class_="no-overflow")
        pre_line = ''
        getResult = 'Компьютерная графика: \n \n'
        for item in result:
            temp = str(item).replace("<br/>", "\n").replace("<div>", '').replace("</div>", "")

            if temp.rstrip():
                if (str(pre_line) != str(temp)):
                    getResult += str(temp) + "\n"
                pre_line = temp
        # getResult = getResult.replace("<br/>", "\n").replace("<div>Код доступа:", 'Код доступа:').replace("<div>", '\n').replace("</div>", "").split('\n', 1)[1]

        print(getResult)
        return (getResult)

    def subjectKm(self):
        """subjectKm.
            result_url: Первая ссылка которая указывает на последнюю записть  по парам
            getResult: Результат записи преподователя
                """

        first_url = self.client.get("https://moodle.zp.edu.ua/mod/forum/view.php?id=28677")
        soup = BeautifulSoup(first_url.text, 'lxml')
        result_url = soup.find(class_="w-100 h-100 d-block")['href']
        print(result_url)

        html = self.client.get(result_url)
        soup = BeautifulSoup(html.text, 'lxml')
        result = soup.find(class_="post-content-container").findAll()
        pre_line = ''
        getResult = 'Компьютерные сети: \n \n'
        for item in result:
            if item.text.rstrip():
                if (str(pre_line) != str(item.text)):
                    getResult += item.text + "\n"
                pre_line = item.text
        print(getResult)
        return (getResult)
        # print(soup)

    def subjectKs(self):
        print("________________________________________")
        html = self.client.get("https://moodle.zp.edu.ua/course/view.php?id=1488")
        soup = BeautifulSoup(html.text, 'lxml')
        result = soup.find(class_="summary").findAll()
        pre_line = ''
        getResult = ''
        for item in result:
            if item.text.rstrip():
                if str(pre_line) != str(item.text):
                    getResult += str(item) + "\n"
                pre_line = item.text

        getResult = \
            getResult.replace("<br/>", "\n").replace("<div>Код доступа:", 'Код доступа:').replace("<div>",
                                                                                                  '\n').replace(
                "</div>", "").split('\n', 1)[1]
        print(getResult)
        return ('Компьютерные системы: \n \n' + getResult)

    def subjectSPZ(self):
        print("________________________________________")
        html = self.client.get("https://moodle.zp.edu.ua/course/view.php?id=2584")
        soup = BeautifulSoup(html.text, 'lxml')
        result = soup.find(id="module-31006").find("a")['onclick']
        result = re.search("(?P<url>https?://[^\s]+)", result).group("url")

        print(result)
        return ("Современное программное обеспечение: \n\n " + result)


student = ParsingMoodle(MOODLE_LOGIN, MOODLE_PASSWORD)

student.subjectKg()

bot = telebot.TeleBot(token)
print("Бот запущен...")


@bot.message_handler(commands=['start'])
def start_menu(message):
    start_str = """
    Навигация в боте:
    /kg - Комп. Графика
    /km - Комп. Сети
    /ks - Комп. Системы
    /spz- И так понятно

    /monday - Все пары в понедельник
    /tuesday - Все пары во вторник
    /wednesday - Все пары в среду
    /friday - Все пары в пятницу



    /reload - перезайти в аккаунт
    """
    bot.send_message(message.chat.id, start_str)


@bot.message_handler(commands=['kg'])
def start_menu(message):
    bot.send_message(message.chat.id, student.subjectKg())
    time.sleep(10000)


@bot.message_handler(commands=['km'])
def start_menu(message):
    bot.send_message(message.chat.id, student.subjectKm())
    time.sleep(10000)


@bot.message_handler(commands=['ks'])
def start_menu(message):
    bot.send_message(message.chat.id, student.subjectKs())
    time.sleep(10000)


@bot.message_handler(commands=['spz'])
def start_menu(message):
    bot.send_message(message.chat.id, student.subjectSPZ())
    time.sleep(10000)


@bot.message_handler(commands=['monday'])
def start_menu(message):
    bot.send_message(message.chat.id, student.subjectKm())
    bot.send_message(message.chat.id, "И 3 пара мс, жди Кудерметова в ТГ")
    time.sleep(10000)


@bot.message_handler(commands=['tuesday'])
def start_menu(message):
    bot.send_message(message.chat.id, student.subjectSPZ())
    time.sleep(10000)


@bot.message_handler(commands=['wednesday'])
def start_menu(message):
    bot.send_message(message.chat.id, "2 пара по СИОЗОТ ожидай в тг")
    time.sleep(10000)


@bot.message_handler(commands=['friday'])
def start_menu(message):
    bot.send_message(message.chat.id, student.subjectKg())
    bot.send_message(message.chat.id, "---------------------------")
    bot.send_message(message.chat.id, student.subjectKs())
    time.sleep(10000)


@bot.message_handler(commands=['reload'])
def start_menu(message):
    global student
    student = ParsingMoodle(MOODLE_LOGIN, MOODLE_PASSWORD)
    time.sleep(10000)


bot.polling()
