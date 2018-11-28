import urllib3

from telebot import TeleBot

import db
import settings


class PhotoHandler(object):

    def __init__(self, user_id: int, link: str, caption: str):
        self._user_id = user_id
        self._link = link
        self._operator_name = db.get_operator_name(self._user_id)
        self._caption = caption

    def handle_photo(self):
        self._forward_photo_to_user()

    def _forward_photo_to_user(self):
        user_bot = TeleBot(settings.USER_BOT_TOKEN)
        if self._caption:
            caption = f'<b>{self._operator_name}</b>\n\n{self._caption}'
        else:
            caption = f'<b>{self._operator_name}</b>'

        connection_pool = urllib3.PoolManager()
        photo = connection_pool.request('GET', self._link)

        user_bot.send_photo(settings.CLIENT_ID, photo.data, caption,
                            parse_mode='HTML')
        photo.release_conn()


class DocumentHandler(object):

    def __init__(self, user_id: int, link: str, caption: str):
        self._user_id = user_id
        self._link = link
        self._operator_name = db.get_operator_name(self._user_id)
        self._caption = caption

    def handle_document(self):
        self._forward_document_to_user()

    def _forward_document_to_user(self):
        user_bot = TeleBot(settings.USER_BOT_TOKEN)
        if self._caption:
            caption = f'<b>{self._operator_name}</b>\n\n{self._caption}'
        else:
            caption = f'<b>{self._operator_name}</b>'

        connection_pool = urllib3.PoolManager()
        document = connection_pool.request('GET', self._link)

        user_bot.send_document(settings.CLIENT_ID, document.data,
                               parse_mode='HTML', caption=caption)
        document.release_conn()
