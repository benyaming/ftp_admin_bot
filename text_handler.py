from telebot import TeleBot
from telebot.types import Message

import settings
import db


class TextHandler(object):

    def __init__(self, message: Message):
        self._user_id = message.from_user.id
        self._text = message.text

    def handle_text(self):
        self._forward_message_to_user()
        self._duplicate_message_for_other_operators()

    def _forward_message_to_user(self):
        user_bot = TeleBot(settings.USER_BOT_TOKEN)
        user_bot.send_message(
            self._user_id,
            self._text
        )

    def _duplicate_message_for_other_operators(self):
        operators = db.get_operators()
        operators.remove(self._user_id)
        admin_bot = TeleBot(settings.ADMIN_BOT_TOKEN)
        res = f'*{self._user_id}*\n\n{self._text}'
        for operator in operators:
            admin_bot.send_message(
                operator,
                res
            )
