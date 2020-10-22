"""Конфиг клиентского логгера"""

import sys
import os
import logging
from common.variables import LOGGING_LEVEL
sys.path.append('../')

# создаём формировщик логов (formatter):
FORMATTER_CLIENT = logging.Formatter('%(asctime)-27s %(levelname)-12s %(filename)-24s %(message)s')

# подготовка имени файла для логирования
# os.path.abspath(path) - возвращает нормализованный абсолютный путь
# os.path.dirname(path) - возвращает имя директории пути path
# __file__ - это путь к файлу, из которого загружен модуль
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client_logs/client.log')

# создаём потоки вывода логов
# создаём обработчик, который выводит сообщения в поток (в консоль) stderr
# в консоль будут выводится ERROR и CRITICAL
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(FORMATTER_CLIENT)       # подключаем объект Formatter к обработчику
STREAM_HANDLER.setLevel(logging.ERROR)              # установим уровень логгера

LOG_FILE = logging.FileHandler(PATH, encoding='utf8')   # вывод записи в файл
LOG_FILE.setFormatter(FORMATTER_CLIENT)

# создаём регистратор и настраиваем его
LOGGER = logging.getLogger('messenger.client')
# добавим обработчик к регистратору
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
