"""Константы"""

DEFAULT_PORT = 7777                 # Порт по умолчанию для сетевого ваимодействия
DEFAULT_IP_ADDRESS = '127.0.0.1'    # IP адрес по умолчанию для подключения клиента
MAX_CONNECTIONS = 5                 # Максимальная очередь подключений
MAX_PACKAGE_LENGTH = 1024           # Максимальная длинна сообщения в байтах
ENCODING = 'utf-8'                  # Кодировка проекта

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
