"""Программа-сервер"""

import socket
import sys
import json
import argparse
import logging
import logs.server_log_config
from errors import IncorrectDataRecivedError
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message


# инициализация логирования сервера
LOGGER_SERVER = logging.getLogger('messenger.server')


def process_client_message(message):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента,
    проверяет корректность, возвращает словарь-ответ для клиента

    :param message:
    :return:
    """
    LOGGER_SERVER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def create_arg_parser():
    """
    Парсер аргументов коммандной строки
    :return:
    """
    # argparse - это модуль для обработки аргументов командной строки
    parser = argparse.ArgumentParser()  # создание парсера
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')  # добавление аргументов
    parser.add_argument('-a', default='', nargs='?')
    return parser


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умолчанию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.1.164
    :return:
    """

    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        LOGGER_SERVER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    LOGGER_SERVER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Создаем сокет
    # socket() - создаёт конечную точку соединения и возвращает файловый дескриптор
    # - domain указывающий семейство протоколов создаваемого сокета (AF_INET для сетевого протокола IPv4)
    # - type (SOCK_STREAM (надёжная потокоориентированная служба (сервис) или потоковый сокет))

    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.bind((listen_address, listen_port))       # bind — привязывает сокет к IP-адресу и порту машины
    serv_sock.listen(MAX_CONNECTIONS)       # Переходит в режим ожидания запросов. Слушаем порт

    while True:
        client_sock, client_address = serv_sock.accept()        # Принять запрос на соединение
        LOGGER_SERVER.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_client = get_message(client_sock)
            LOGGER_SERVER.debug(f'Получено сообщение {message_from_client}')
            print(message_from_client)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            # print(f'User {client_sock} connected')  # информация о клиенте
            response = process_client_message(message_from_client)
            LOGGER_SERVER.info(f'Cформирован ответ клиенту {response}')
            send_message(client_sock, response)
            LOGGER_SERVER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client_sock.close()
        except json.JSONDecodeError:
            LOGGER_SERVER.error(f'Не удалось декодировать JSON строку, полученную от '
                                f'клиента {client_address}. Соединение закрывается.')
            client_sock.close()
        except IncorrectDataRecivedError:
            LOGGER_SERVER.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client_sock.close()


if __name__ == '__main__':
    main()
