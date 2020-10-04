"""
2. Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""

ELEM_1 = b'class'
ELEM_2 = b'function'
ELEM_3 = b'method'

LIST_ELEM = [ELEM_1, ELEM_2, ELEM_3]

print('\n{:^10} {:^23} {:^}'.format('<<Элемент>>', '<<Тип>>', '<<Длина>>'))

for elem in LIST_ELEM:
    print('{:15} {:23} {:20}'.format(str(elem), str(type(elem)), str(len(elem))))
