"""Декораторы"""

import sys
import logging
import logs.server_log_config
import logs.client_log_config
import traceback
import inspect

# метод определения модуля, источника запуска.
# Метод find () возвращает индекс первого вхождения искомой подстроки,
# если он найден в данной строке.
# Если его не найдено, - возвращает -1.
# sys.argv - содержит полный путь к скрипту или к названию файла
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    LOGGER = logging.getLogger('messenger.server')
else:
    # ну, раз не сервер, то клиент
    LOGGER = logging.getLogger('messenger.client')


# Реализация в виде функции
def log(func):
    """Функция-декоратор"""
    def wrap_log(*args, **kwargs):
        """Обертка"""
        res = func(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func.__module__}. Вызов из'
                     f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
        return res
    return wrap_log


# Реализация в виде класса
# class Log:
#     """Класс-декоратор"""
#     def __call__(self, func):
#         def wrap_log(*args, **kwargs):
#             """Обертка"""
#             res = func(*args, **kwargs)
#             LOGGER.debug(f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}. '
#                          f'Вызов из модуля {func.__module__}. Вызов из'
#                          f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
#                          f'Вызов из функции {inspect.stack()[1][3]}')
#             return res
#         return wrap_log
