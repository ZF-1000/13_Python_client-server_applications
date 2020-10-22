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

        PROCESS.append(subprocess.Popen('python server.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(5):
            PROCESS.append(subprocess.Popen('python client.py',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
