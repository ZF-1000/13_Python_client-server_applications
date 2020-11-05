"""Утилиты"""

import json
import sys
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from errors import IncorrectDataRecivedError, NonDictInputError
from decos import log
sys.path.append('../')


@log
def get_message(client_sock):
    """
    Утилита приёма и декодирования сообщения. Принимает байты выдаёт словарь,
    если принято что-то другое, отдаёт ошибку значения.
    :param client_sock:
    :return:
    """

    data_client_sock = client_sock.recv(MAX_PACKAGE_LENGTH)     # recv — получить данные. На входе байты
    # isinstance - возвращает флаг, указывающий на то, является ли указанный объект экземпляром указанного класса
    if isinstance(data_client_sock, bytes):
        dec_data_client_sock = data_client_sock.decode(ENCODING)   # из байтов получаем json объект
        # json.loads() - метод считывает строку в формате JSON и возвращает объекты Python
        dict_data = json.loads(dec_data_client_sock)        # распарсили словарь
        if isinstance(dict_data, dict):
            return dict_data
        raise ValueError
    raise ValueError


@log
def send_message(sock, message):
    """
    Утилита кодирования и отправки сообщения. Принимает словарь и отправляет его
    :param sock:
    :param message:
    :return:
    """
    if not isinstance(message, dict):
        raise NonDictInputError
    json_message = json.dumps(message)        # json.dumps() - метод возвращает строку в формате JSON
    encoded_message = json_message.encode(ENCODING)     # из json объекта получаем байты
    sock.send(encoded_message)                # байты шлём по сети
