import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    parkiarminda_button = types.KeyboardButton('График работы ParkiArMinda')
    markup.row(parkiarminda_button)
    bot.send_message(message.chat.id, 'Привет. Я бот-помощник.', reply_markup=markup)
    bot.register_next_step_handler(message, get_parkiarminda_data)


@bot.message_handler(commands=['check'])
def check(message):
    bot.send_message(message.chat.id, 'Я включен и умею в CI/CD.')


@bot.callback_query_handler(func=lambda callback: True)
def get_parkiarminda_data(message):
    url = 'https://eco-taxi.ge/garage-2'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    rawpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(rawpage.content, 'html.parser')

    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    index_start = text.find('Our Saburtalo')
    index_end = text.find('Our Chugureti')

    bot.send_message(message.chat.id, text[index_start: index_end])


bot.polling(none_stop=True)
