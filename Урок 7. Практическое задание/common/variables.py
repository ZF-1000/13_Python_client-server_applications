"""Константы"""
import logging

DEFAULT_PORT = 7777                 # Порт по умолчанию для сетевого ваимодействия
DEFAULT_IP_ADDRESS = '127.0.0.1'    # IP адрес по умолчанию для подключения клиента
MAX_CONNECTIONS = 5                 # Максимальная очередь подключений
MAX_PACKAGE_LENGTH = 1024           # Максимальная длинна сообщения в байтах
ENCODING = 'utf-8'                  # Кодировка проекта
LOGGING_LEVEL = logging.DEBUG       # Текущий уровень логирования

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'


"""
Уровень     Значение    Описание
---------------------------------------------
CRITICAL    50          Критические ошибки/сообщения
ERROR       40          Ошибки
WARNING     30          Предупреждения
INFO        20          Информационные сообщения
DEBUG       10          Отладочная информация
NOTSET      0           Уровень не установлен
"""