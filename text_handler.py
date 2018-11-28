from telebot import TeleBot

import settings
import db


class TextHandler(object):

    def __init__(self, user: int, text: str, notification=False, action=False):
        self._user_id = user
        self._text = text
        self._notification = notification
        self._operator_name = db.get_operator_name(self._user_id)
        self._action = action

    def handle_text(self):
        if not self._notification:
            self._forward_message_to_user()
        self._duplicate_message_for_other_operators()

    def _forward_message_to_user(self):
        user_bot = TeleBot(settings.USER_BOT_TOKEN)
        if self._action:
            response = f'{self._text}'
        else:
            response = f'<b>{self._operator_name}</b>\n\n{self._text}'
        user_bot.send_message(settings.CLIENT_ID, response, parse_mode='HTML')

    def _duplicate_message_for_other_operators(self):
        operators = db.get_operators(settings.CLIENT_ID)
        try:
            operators.remove(self._user_id)
        except ValueError:
            pass
        admin_bot = TeleBot(settings.ADMIN_BOT_TOKEN)
        if self._action:
            res = f'{self._text}'
        else:
            res = f'<b>{self._operator_name}</b>\n\n{self._text}'
        for operator in operators:
            admin_bot.send_message(
                operator,
                res,
                parse_mode='HTML'
            )
