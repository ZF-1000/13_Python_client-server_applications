"""Программа-клиент"""

import sys
import json
import socket
import time
import argparse
import logging
import logs.client_log_config
from errors import ReqFieldMissingError
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message

# Инициализация клиентского логера
LOGGER_CLIENT = logging.getLogger('messenger.client')


def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: PRESENCE,   # присутствие клиента
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOGGER_CLIENT.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


def process_ans(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """
    LOGGER_CLIENT.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


def create_arg_parser():
    """
    Создаём парсер аргументов коммандной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


def main():
    """Загружаем параметы командной строки"""
    # client.py 192.168.1.164 8079

    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        LOGGER_CLIENT.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    LOGGER_CLIENT.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')

    # Инициализация сокета и обмен
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(client_sock, message_to_server)
        answer = process_ans(get_message(client_sock))
        LOGGER_CLIENT.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        LOGGER_CLIENT.error('Не удалось декодировать полученную Json строку.')

    except ReqFieldMissingError as missing_error:
        LOGGER_CLIENT.error(f'В ответе сервера отсутствует необходимое поле '
                        f'{missing_error.missing_field}')

    except ConnectionRefusedError:
        LOGGER_CLIENT.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                           f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
