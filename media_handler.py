import urllib3

from telebot import TeleBot

import db
import settings


# class PhotoHandler(object):
#
#     def __init__(self, user_id: int, link: str, caption: str):
#         self._user_id = user_id
#         self._link = link
#         self._operator_name = db.get_operator_name(self._user_id)
#         self._operator_group = db.get_operator_group(self._user_id)
#         self._caption = caption
#
#     def handle_photo(self):
#         self._forward_photo_to_user()
#         self._duplicate_message_for_other_operators()
#
#     def _forward_photo_to_user(self):
#         user_bot = TeleBot(settings.USER_BOT_TOKEN)
#         if self._caption:
#             caption = f'<b>{self._operator_group}</b>\n\n{self._caption}'
#         else:
#             caption = f'<b>{self._operator_group}</b>'
#
#         connection_pool = urllib3.PoolManager()
#         photo = connection_pool.request('GET', self._link)
#
#         user_bot.send_photo(settings.CLIENT_ID, photo.data, caption,
#                             parse_mode='HTML')
#         photo.release_conn()
#
#     def _duplicate_message_for_other_operators(self):
#         operators = db.get_operators(settings.CLIENT_ID)
#         try:
#             operators.remove(self._user_id)
#         except ValueError:
#             pass
#         admin_bot = TeleBot(settings.ADMIN_BOT_TOKEN)
#         if self._caption:
#             caption = f'<b>{self._operator_name}</b>\n\n{self._caption}'
#         else:
#             caption = f'<b>{self._operator_name}</b>'
#         connection_pool = urllib3.PoolManager()
#         photo = connection_pool.request('GET', self._link)
#
#         for operator in operators:
#             admin_bot.send_photo(operator, photo.data,
#                                  caption, parse_mode='HTML')
#         photo.release_conn()
#
#
# class DocumentHandler(object):
#
#     def __init__(self, user_id: int, link: str, caption: str):
#         self._user_id = user_id
#         self._link = link
#         self._operator_name = db.get_operator_name(self._user_id)
#         self._operator_group = db.get_operator_group(self._user_id)
#         self._caption = caption
#
#     def handle_document(self):
#         self._forward_document_to_user()
#         self._duplicate_message_for_other_operators()
#
#     def _forward_document_to_user(self):
#         user_bot = TeleBot(settings.USER_BOT_TOKEN)
#         if self._caption:
#             caption = f'<b>{self._operator_group}</b>\n\n{self._caption}'
#         else:
#             caption = f'<b>{self._operator_group}</b>'
#
#         connection_pool = urllib3.PoolManager()
#         document = connection_pool.request('GET', self._link)
#
#         user_bot.send_document(settings.CLIENT_ID, document.data,
#                                parse_mode='HTML', caption=caption)
#         document.release_conn()
#
#     def _duplicate_message_for_other_operators(self):
#         operators = db.get_operators(settings.CLIENT_ID)
#         try:
#             operators.remove(self._user_id)
#         except ValueError:
#             pass
#         admin_bot = TeleBot(settings.ADMIN_BOT_TOKEN)
#         if self._caption:
#             caption = f'<b>{self._operator_name}</b>\n\n{self._caption}'
#         else:
#             caption = f'<b>{self._operator_name}</b>'
#
#         connection_pool = urllib3.PoolManager()
#         document = connection_pool.request('GET', self._link)
#
#         for operator in operators:
#             admin_bot.send_document(operator, document.data,
#                                     caption=caption, parse_mode='HTML')
#         document.release_conn()


class MediaHandler(object):

    def __init__(self, user_id: int, link: str, caption: str, media_type: str):
        self._user_id = user_id
        self._link = link
        self._operator_name = db.get_operator_name(self._user_id)
        self._operator_group = db.get_operator_group(self._user_id)
        self._caption = caption
        self._media_type = media_type

    def handle_media(self):
        self._forward_media_to_user()
        self._duplicate_message_for_other_operators()

    def _forward_media_to_user(self):
        user_bot = TeleBot(settings.USER_BOT_TOKEN)
        if self._caption:
            caption = f'<b>{self._operator_group}</b>\n\n{self._caption}'
        else:
            caption = f'<b>{self._operator_group}</b>'

        actions = {
            'photo': user_bot.send_photo,
            'document': user_bot.send_document,
        }
        send_media = actions.get(self._media_type)

        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET', self._link)
        media = resp.data

        send_media(settings.CLIENT_ID, media, parse_mode='HTML', caption=caption)
        resp.release_conn()

    def _duplicate_message_for_other_operators(self):
        operators = db.get_operators(settings.CLIENT_ID)
        try:
            operators.remove(self._user_id)
        except ValueError:
            pass
        admin_bot = TeleBot(settings.ADMIN_BOT_TOKEN)
        if self._caption:
            caption = f'<b>{self._operator_name}</b>\n\n{self._caption}'
        else:
            caption = f'<b>{self._operator_name}</b>'

        actions = {
            'photo': admin_bot.send_photo,
            'document': admin_bot.send_document,
        }
        send_media = actions.get(self._media_type)

        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET', self._link)
        media = resp.data

        for operator in operators:
            send_media(operator, media, caption=caption, parse_mode='HTML')
        resp.release_conn()
