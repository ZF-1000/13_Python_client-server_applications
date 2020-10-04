"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но открыть нужно ИМЕННО в формате Unicode (utf-8)

например, with open('test_file.txt', encoding='utf-8') as t_f
невыполнение условия - минус балл
"""
from chardet import detect

LINES_LST = ['сетевое программирование', 'сокет', 'декоратор']

# откроем файл по умолчанию и запишем данные
with open('test_file.txt', 'w') as t_f:     # w - открывает файл только для записи
    for line in LINES_LST:
        t_f.write(f'{line}\n')
t_f.close()

print(f'Кодировка файла по умолчанию - {t_f.encoding}')

with open('test_file.txt', 'rb') as t_file:    # rb - открывает файл для чтения в двоичном формате
    content_bytes = t_file.read()
detected = detect(content_bytes)
encoding = detected['encoding']
content_text = content_bytes.decode(encoding)
with open('test_file.txt', 'w', encoding='utf-8') as t_file:
    t_file.write(content_text)

# открываем файл в правильной кодировке
with open('test_file.txt', 'r', encoding='utf-8') as file:      # r - открывает файл только для чтения
    CONTENT = file.read()
print(CONTENT)
