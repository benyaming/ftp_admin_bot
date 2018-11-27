from telebot import TeleBot
from telebot.types import Message

import settings
import db


class TextHandler(object):

    def __init__(self, user: int, text: str):
        self._user_id = user
        self._text = text

    def handle_text(self):
        self._forward_message_to_user()
        self._duplicate_message_for_other_operators()

    def _forward_message_to_user(self):
        user_bot = TeleBot(settings.USER_BOT_TOKEN)
        user_bot.send_message(
            settings.CLIENT_ID,
            self._text,
            parse_mode='HTML'
        )

    def _duplicate_message_for_other_operators(self):
        operators = db.get_operators(settings.CLIENT_ID)
        operators.remove(self._user_id)
        admin_bot = TeleBot(settings.ADMIN_BOT_TOKEN)
        res = f'<b>{self._user_id}</b>\n\n{self._text}'
        for operator in operators:
            admin_bot.send_message(
                operator,
                res,
                parse_mode='HTML'
            )
