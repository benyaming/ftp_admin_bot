from os import environ

GUNICORN_PORT = environ.get('GUNICORN_PORT')

USER_BOT_TOKEN = environ.get('USER_BOT_TOKEN')
ADMIN_BOT_TOKEN = environ.get('ADMIN_BOT_TOKEN')
REPORT_BOT_TOKEN = environ.get('REPORT_BOT_TOKEN')

CLIENT_ID = environ.get('CLIENT_ID')

BOT_HOST = environ.get('BOT_HOST')
BOT_PORT = environ.get('BOT_PORT')
URI = environ.get('URI')

IS_SERVER = environ.get('IS_SERVER')
logs_path = environ.get('logs_path')

# db settings
dbname = environ.get('db_name')
dbuser = environ.get('db_user')
dbpassword = environ.get('db_password')
dbport = environ.get('db_port')
dbhost = environ.get('db_host')  # localhost

db_parameters_string = f'dbname={dbname} ' \
                       f'user={dbuser} ' \
                       f'password={dbpassword} ' \
                       f'host={dbhost} ' \
                       f'port={dbport}'
