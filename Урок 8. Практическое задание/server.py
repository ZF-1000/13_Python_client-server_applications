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
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, \
    TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, RESPONSE_400, \
    EXIT, DESTINATION
from common.utils import get_message, send_message
from decos import log

# инициализация логирования сервера
LOGGER = logging.getLogger('messenger.server')


@log
def process_client_message(message, messages_list, client_sock, clients_sock, names):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта,
    проверяет корректность, отправляет словарь-ответ для клиента с результатом приёма.
    :param message:
    :param messages_list:
    :param client_sock:
    :param clients_sock:
    :param names:
    :return:
    """
    LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # Если это сообщение о присутствии, принимаем и отвечаем, если успех
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message:
        # Если такой пользователь ещё не зарегистрирован, регистрируем,
        # иначе отправляем ответ и завершаем соединение.
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client_sock
            send_message(client_sock, {RESPONSE: 200})
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            send_message(client_sock, response)
            clients_sock.remove(client_sock)
            client_sock.close()
        return
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and \
            SENDER in message and TIME in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    # Если клиент выходит
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients_sock.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    # Иначе отдаём Bad request
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен.'
        send_message(client_sock, response)
        return


@log
def process_message(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
    :param message:
    :param names:
    :param listen_socks:
    :return:
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                    f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


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

    LOGGER.info(
        f'Запущен сервер, порт для подключений: {listen_port}, '
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

    # Словарь, содержащий имена пользователей и соответствующие им сокеты.
    names = dict()

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
                                           messages, client_with_message, clients, names)
                except Exception:
                    LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        for i in messages:
            try:
                process_message(i, names, send_data_lst)
            except Exception:
                LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
            messages.clear()


if __name__ == '__main__':
    main()
