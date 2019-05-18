from json import dumps
from shutil import copyfileobj

import telebot
import requests
from telebot.types import Message
from flask import request, Flask

import db
import settings
from text_handler import TextHandler
from media_handler import MediaHandler


WEBHOOK_HOST = settings.BOT_HOST
WEBHOOK_PORT = settings.BOT_PORT
ssl_cert = '/hdd/certs/webhook_cert.pem'
ssl_cert_key = '/hdd/certs/webhook_pkey.pem'
base_url = f'{WEBHOOK_HOST}:{WEBHOOK_PORT}'
route_path = f'/{settings.URI}/'

bot = telebot.TeleBot(settings.ADMIN_BOT_TOKEN)

app = Flask(__name__)


@app.route(route_path, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'ok'


def report(message: Message):
    report_bot = telebot.TeleBot(settings.REPORT_BOT_TOKEN)
    formatted_message = dumps(message.json, indent=2, ensure_ascii=False)
    report_msg = f'<b>Попытка доступа в операторский бот!</b>\n\n' \
                 f'Клиент бота: ' \
                 f'{db.get_client_name(settings.CLIENT_ID)}\n\n<code>' \
                 f'{formatted_message}</code>'
    report_bot.send_message(5979588, report_msg, parse_mode='HTML')


def check_auth(func):
    def wrapper(message):
        if db.check_auth(message.from_user.id):
            return func(message)
        else:
            response = '`Доступ запрещен. Обратитесь к администратору`'
            bot.send_message(message.from_user.id, response,
                             parse_mode='Markdown')
            report(message)
    return wrapper


def download_file(file_id: str, filename: str):
    link = f'https://api.telegram.org/file/bot{settings.ADMIN_BOT_TOKEN}/' \
        f'{bot.get_file(file_id).file_path}'
    with open(filename, 'wb') as out:
        r = requests.get(link, stream=True)
        for chunk in r:
            out.write(chunk)


@bot.message_handler(commands=['start'])
@check_auth
def handle_start(message):
    bot.send_message(message.from_user.id, 'Welcome!')


@bot.message_handler(commands=['name'])
@check_auth
def handle_name_command(message: Message):
    resp = f'`name: {settings.CLIENT_NAME}`\n`id: {settings.CLIENT_ID}`'
    bot.send_message(message.from_user.id, resp, parse_mode='Markdown')


@bot.message_handler(commands=['бух'])
@check_auth
def handle_buch_command(message: telebot.types.Message):
    if db.check_operator_access(message.from_user.id):
        comment = message.text.split('/бух')[1]
        if comment:
            response = '<i>Перевод в бухгалтерию</i>'
            TextHandler(message.from_user.id, response,
                        action=True).handle_text()
            db.change_worker(settings.CLIENT_ID, 'buch')
            TextHandler(message.from_user.id, comment, True).handle_text()
        else:
            response = '`Вы не ввели комментарий!`'
            bot.send_message(message.from_user.id, response,
                             parse_mode='Markdown')
    else:
        response = '`Клиент у другого оператора, действие не выполнено!`'
        bot.send_message(message.from_user.id, response, parse_mode='Markdown')


@bot.message_handler(commands=['док'])
@check_auth
def handle_buch_command(message: telebot.types.Message):
    if db.check_operator_access(message.from_user.id):
        comment = message.text.split('/док')[1]
        if comment:
            response = '<i>Перевод в документы</i>'
            TextHandler(message.from_user.id, response,
                        action=True).handle_text()
            db.change_worker(settings.CLIENT_ID, 'doc')
            TextHandler(message.from_user.id, comment, True).handle_text()
        else:
            response = '`Вы не ввели комментарий!`'
            bot.send_message(message.from_user.id, response,
                             parse_mode='Markdown')
    else:
        response = '`Клиент у другого оператора, действие не выполнено!`'
        bot.send_message(message.from_user.id, response, parse_mode='Markdown')


@bot.message_handler(commands=['оп'])
@check_auth
def handle_buch_command(message: telebot.types.Message):
    if db.check_operator_access(message.from_user.id):
        comment = f'Передано оператору. ' \
                  f'Коммент: {message.text.split("/оп")[1]}'
        response = '<i>Перевод на оператора</i>'
        TextHandler(message.from_user.id, response, action=True).handle_text()
        db.change_worker(settings.CLIENT_ID, 'op')
        TextHandler(message.from_user.id, comment, True).handle_text()
    else:
        response = '`Клиент у другого оператора, действие не выполнено!`'
        bot.send_message(message.from_user.id, response, parse_mode='Markdown')


@bot.message_handler(func=lambda message: True, content_types=['text'])
@check_auth
def handle_text_message(message: Message):
    if db.check_operator_access(message.from_user.id):
        TextHandler(message.from_user.id, message.text).handle_text()
    else:
        response = '`Клиент у другого оператора, сообщение не доставлено!`'
        bot.send_message(message.from_user.id, response, parse_mode='Markdown')


@bot.message_handler(func=lambda message: True, content_types=['photo'])
@check_auth
def handle_photo(message: Message):
    if db.check_operator_access(message.from_user.id):
        file_id = message.photo[-1].file_id
        download_file(file_id, file_id)
        caption = message.caption
        MediaHandler(message.from_user.id, file_id, caption, 'photo').handle_media()
    else:
        response = '`Клиент у другого оператора, фото не доставлено!`'
        bot.send_message(message.from_user.id, response, parse_mode='Markdown')


@bot.message_handler(func=lambda message: True, content_types=['document'])
@check_auth
def handle_text_message(message: Message):
    if db.check_operator_access(message.from_user.id):
        file_id = message.document.file_id
        filename = message.document.file_name
        download_file(file_id, filename)
        caption = message.caption
        MediaHandler(message.from_user.id, filename, caption, 'document').handle_media()
    else:
        response = '`Клиент у другого оператора, фото не доставлено!`'
        bot.send_message(message.from_user.id, response, parse_mode='Markdown')


ignoring_types = ['voice', 'sticker', 'audio', 'video', 'video_note',
                  'location', 'contact', '']


@bot.message_handler(func=lambda message: True, content_types=ignoring_types)
@check_auth
def handle_text_message(message: Message):
    response = '<code>Бот не поддерживает отправку сообщений такого ' \
               'типа. Пожалуйста, отправьте текст, фото или документ.</code>'
    bot.send_message(message.from_user.id, response, parse_mode='HTML')


if __name__ == '__main__':
    if settings.IS_SERVER:
        bot.remove_webhook()
        bot.set_webhook(
            url=f'{base_url}{route_path}',
            certificate=open(ssl_cert, 'r')
        )
    else:
        bot.remove_webhook()
        bot.polling(True, timeout=50)
