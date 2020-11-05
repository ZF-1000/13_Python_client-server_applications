"""Лаунчер"""

import subprocess

PROCESS = []

while True:
    ACTION = input('Выберите действие: '
                   'q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        # Popen - выполняет дочернюю программу в новом процессе (не дожидается конца выполнения
        # вызванного процесса в отличие от метода call)
        # creationflags=None - один или несколько констант Windows
        # subprocess.CREATE_NEW_CONSOLE: Новый процесс имеет новую консоль вместо того,
        # чтобы наследовать консоль своего родителя (по умолчанию).
        # два типа скриптов: 1- на чтение, 2-ой на запись

        PROCESS.append(subprocess.Popen('python server.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        # -m - мод (режим).
        # 2 клиента на чтение (send)
        for i in range(2):
            PROCESS.append(subprocess.Popen('python client.py -m send',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
        # 2 клиента на запись (listen)
        for i in range(2):
            PROCESS.append(subprocess.Popen('python client.py -m listen',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
