"""
4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

print('\n------------Преобразование из строкового представления в байтовое <<ENCODE>>------------')

ELEM_1 = 'разработка'
ELEM_2 = 'администрирование'
ELEM_3 = 'protocol'
ELEM_4 = 'standard'

LIST_ELEM = [ELEM_1, ELEM_2, ELEM_3, ELEM_4]

ENCODE_LIST = []
for elem in LIST_ELEM:
    el = elem.encode('utf-8')
    ENCODE_LIST.append(el)

for var in ENCODE_LIST:
    print(var)


print('\n------------Преобразование из байтового представления в строковое <<DECODE>>------------')

DECODE_LIST = []
for elem in ENCODE_LIST:
    el = elem.decode('utf-8')
    DECODE_LIST.append(el)

for var in DECODE_LIST:
    print(var)
