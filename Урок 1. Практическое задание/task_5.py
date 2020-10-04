"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet
"""

import subprocess
import chardet

# Chardet - модуль предназначеный для автоматического распознавания кодировок символов в тексте
# detect принимает один параметр, строку и возвращает словарь, содержащий
# автоматически обнаруженную кодировку (строка)

print('\n--------------------------------Пинг yandex.ru--------------------------------')
ARGS = ['ping', 'yandex.ru']
PROCESS_YA = subprocess.Popen(ARGS, stdout=subprocess.PIPE)
for line in PROCESS_YA.stdout:
    result = chardet.detect(line)
    print(result)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))


print('\n--------------------------------Пинг youtube.com--------------------------------')
ARGS = ['ping', 'youtube.com']
PROCESS_YOU = subprocess.Popen(ARGS, stdout=subprocess.PIPE)
for line in PROCESS_YOU.stdout:
    result = chardet.detect(line)
    print(result)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))
