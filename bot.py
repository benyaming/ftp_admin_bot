import telebot
from telebot.types import Message
from flask import request, Flask

import db
import settings
from text_handler import TextHandler


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


# todo приветствие, авторизация
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(
        message.from_user.id,
        'Welcome!'
    )


@bot.message_handler(commands=['бух'])
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
def handle_text_message(message: Message):
    if db.check_operator_access(message.from_user.id):
        TextHandler(message.from_user.id, message.text).handle_text()
    else:
        response = '`Клиент у другого оператора, сообщение не доставлено!`'
        bot.send_message(message.from_user.id, response, parse_mode='Markdown')


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
