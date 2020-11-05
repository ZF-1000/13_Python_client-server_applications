"""Лаунчер"""

import subprocess

PROCESSES = []

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

        PROCESSES.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESSES.append(subprocess.Popen('python client.py -n test1',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESSES.append(subprocess.Popen('python client.py -n test2',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESSES.append(subprocess.Popen('python client.py -n test3',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
