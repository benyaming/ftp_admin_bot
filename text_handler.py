from telebot import TeleBot, types

import settings
import db


class TextHandler:
    # _actions_kb: types.InlineKeyboardMarkup
    _callback_data: str
    _confirm_message_id: int

    def __init__(self, msg: types.Message, *, is_notification: bool = False, is_action: bool = False,
                 custom_text: str = None):
        """
        :param msg: Original admin's message instance
        :param is_notification: sends action description to user in a special format
        :param is_action: if enabled, message will sent only to admins
        :param custom_text:
        """
        self._user_id = msg.chat.id
        self._text = msg.text if not custom_text else custom_text
        self._origin_message_id = msg.message_id
        self._notification = is_notification
        self._operator_name = db.get_operator_name(self._user_id)
        self._operator_group = db.get_operator_group(self._user_id)
        self._action = is_action
        self._user_bot = TeleBot(settings.USER_BOT_TOKEN)
        self._admin_bot = TeleBot(settings.ADMIN_BOT_TOKEN)

    def handle_text(self):
        if not self._notification:
            self._forward_message_to_user()
        if self._action:
            self._send_action_for_all_admins()
        self._duplicate_message_for_other_operators()

    def _get_actions_kb(self) -> types.InlineKeyboardMarkup:
        return types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton(
                text='Удалить сообщение',
                callback_data=self._callback_data
            )
        )

    def _after_send(self, msg_sent: types.Message):
        sent_description = '<code>Сообщение пользователю отправлено.</code>'
        self._callback_data = f'delete:{msg_sent.chat.id}:' \
                              f'{msg_sent.message_id}:' \
                              f'{self._operator_name}'

        self._confirm_message_id = self._admin_bot.send_message(
            self._user_id,
            sent_description,
            parse_mode='HTML',
            reply_markup=self._get_actions_kb(),
            reply_to_message_id=self._origin_message_id
        ).message_id

    def _forward_message_to_user(self):
        user_bot = TeleBot(settings.USER_BOT_TOKEN)
        if self._action:
            response = f'{self._text}'
        else:
            response = f'<b>{self._operator_group}</b>\n\n{self._text}'
        sent = user_bot.send_message(settings.CLIENT_ID, response, parse_mode='HTML')
        self._after_send(sent)

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
        # admin_messages = []
        for operator in operators:
            admin_bot.send_message(
                operator,
                res,
                parse_mode='HTML',
                reply_markup=self._get_actions_kb()
            )

    def _send_action_for_all_admins(self):
        admins = db.get_operators(settings.CLIENT_ID)
        for admin in admins:
            admin_bot = TeleBot(settings.ADMIN_BOT_TOKEN)
            admin_bot.send_message(
                admin,
                self._text,
                parse_mode='HTML'
            )
