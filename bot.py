import telebot
from telebot.types import Message
from flask import request, Flask

import settings
import text_handler


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
        'Welcome! Input station ID'
    )


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text_message(message: Message):
    # bot.send_chat_action(message.from_user.id, 'typing')
    text_handler.TextHandler(message).handle_text()


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
