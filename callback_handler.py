from telebot import TeleBot
from telebot.types import CallbackQuery
from telebot.apihelper import ApiException

from settings import USER_BOT_TOKEN


def delete_message(call: CallbackQuery, admin_bot: TeleBot):
    _, chat_id, message_id, op_name = call.data.split(':')
    user_bot = TeleBot(USER_BOT_TOKEN)
    try:
        user_bot.delete_message(chat_id, message_id)
    except ApiException:
        resp = '`Это сообщение уже удалено!`'
    else:
        resp = '`Вы удалили это собщение`'

    # print(resp)
    admin_bot.edit_message_text(resp,
                                call.from_user.id,
                                call.message.message_id,
                                parse_mode='Markdown')

'''
def strike(text: str):
    return ''.join([f'{c}\u0336' for c in text])
'''
