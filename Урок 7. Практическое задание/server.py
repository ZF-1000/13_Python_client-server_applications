"""Программа-сервер"""

import socket
import sys
import json
import argparse
import logging
import select
import time
import logs.server_log_config
from errors import IncorrectDataRecivedError
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message
from decos import log

# инициализация логирования сервера
LOGGER = logging.getLogger('messenger.server')


@log
def process_client_message(message, messages_list, client_sock):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта,
    проверяет корректность, отправляет словарь-ответ для клиента с результатом приёма.
    :param message:
    :param messages_list:
    :param client_sock:
    :return:
    """
    LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # Если это сообщение о присутствии, принимаем и отвечаем, если успех
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client_sock, {RESPONSE: 200})
        return
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    # Иначе отдаём Bad request
    else:
        send_message(client_sock, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def create_arg_parser():
    """
    Парсер аргументов коммандной строки
    :return:
    """
    # argparse - это модуль для обработки аргументов командной строки
    parser = argparse.ArgumentParser()  # создание парсера
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')  # добавление аргументов
    parser.add_argument('-a', default='', nargs='?')
    # sys.argv – это список аргументов командной строки, которые причастны к скрипту
    namespace = parser.parse_args(sys.argv[1:])     # namespace: Namespace(a='', p=7777)
    listen_address = namespace.a                    # listen_address: ''
    listen_port = namespace.p                       # listen_port: 7777

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        LOGGER.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        # exit(0) означает чистый выход без ошибок/проблем
        # exit(1) означает, что была проблема с проблемой/ошибкой/проблемой, поэтому программа выходит.
        sys.exit(1)

    return listen_address, listen_port


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умолчанию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.1.164
    :return:
    """
    listen_address, listen_port = create_arg_parser()

    LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                f'адрес с которого принимаются подключения: {listen_address}. '
                f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Создаем сокет
    # socket() - создаёт конечную точку соединения и возвращает файловый дескриптор
    # - domain указывающий семейство протоколов создаваемого сокета (AF_INET для сетевого протокола IPv4)
    # - type (SOCK_STREAM (надёжная потокоориентированная служба (сервис) или потоковый сокет))

    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.bind((listen_address, listen_port))       # bind — привязывает сокет к IP-адресу и порту машины
    serv_sock.settimeout(0.5)

    # список клиентов, очередь сообщений
    clients = []
    messages = []

    serv_sock.listen(MAX_CONNECTIONS)       # Переходит в режим ожидания запросов. Слушаем порт

    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client_sock, client_address = serv_sock.accept()  # Принять запрос на соединение
        except OSError:
            pass
        else:
            LOGGER.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client_sock)

        recv_data_lst = []  # клиенты которые пишут
        send_data_lst = []  # клиенты которые читают
        err_lst = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
