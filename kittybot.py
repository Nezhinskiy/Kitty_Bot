import logging
import os

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

load_dotenv()

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='{asctime} - {name} - {levelname} - {message}',
    style='{',
    level=logging.INFO
)

URL = 'https://api.thecatapi.com/v1/images/search'
NEW_URL = 'https://api.thedogapi.com/v1/images/search'


def get_new_image():
    """Получает нового котика или,
    если есть ошибка, собачку"""
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(NEW_URL)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    """Отправляет нового котика по команде"""
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def wake_up(update, context):
    """Отправляет приветственного котика и фразу
    по команде"""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Посмотри, какого котика я тебе нашёл',
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())


def main():
    """Исполняемый код"""
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
