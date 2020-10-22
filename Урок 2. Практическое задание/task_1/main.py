"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

import csv
import re


def get_data():

    os_prod_list = []   # список изготовителя системы
    os_name_list = []   # список названия ОС
    os_code_list = []   # список кода продукта
    os_type_list = []   # список типа системы
    main_data = []      # главный список для хранения данных отчета

    count_txt = 3       # количество txt - файлов для открытия

    for i in range(1, count_txt + 1):
        with open(f'info_{i}.txt') as f:
            data = f.read()
            # print(data)

        # Получаем список изготовителей системы
        # Функция compile() преобразует выражение в объект RegexObject
        # Можно собрать регулярное выражение в отдельный объект, который можно использовать для поиска
        # findall - найдёт все вхождения заданного шаблона в строку
        # \s - любой пробельный символ, как например \n, \t, а также сам пробел
        # \S - любой не пробельный одиночный символ
        # *	- ноль или больше символов

        os_prod_reg = re.compile(r'Изготовитель системы:\s*\S*')
        os_prod_list.append(os_prod_reg.findall(data)[0].split()[2])
        # print(os_prod_reg.findall(data)[0].split()[2])            # для отладки
        # print(type(os_prod_reg.findall(data)[0].split()[2]))      # для отладки
        # print(os_prod_list)                                       # для отладки
        # print(type(os_prod_list))                                 # для отладки


        # Название ОС
        os_name_reg = re.compile(r'Название ОС:\s*\S*\s*\S*\s*\S*\s*\S*')
        os_name_str = ' '.join(os_name_reg.findall(data)[0].split()[2:6])
        os_name_list.append(os_name_str)
        # print(os_name_reg.findall(data)[0].split()[2:6])  # для отладки
        # print(os_name_list)                               # для отладки
        # print(type(os_name_list))                         # для отладки

        # Код продукта
        os_code_reg = re.compile(r'Код продукта:\s*\S*')
        os_code_list.append(os_code_reg.findall(data)[0].split()[2])
        # print(os_code_list)
        # print(type(os_code_list))

        # Тип системы
        os_type_reg = re.compile(r'Тип системы:\s*\S*')
        os_type_list.append(os_type_reg.findall(data)[0].split()[2])
        # print(os_type_list)

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)
    # print(main_data)

    j = 1
    for i in range(0, count_txt):
        row_data = []
        row_data.append(j)                  # добавим нумерацию строк
        row_data.append(os_prod_list[i])
        row_data.append(os_name_list[i])
        row_data.append(os_code_list[i])
        row_data.append(os_type_list[i])
        main_data.append(row_data)
        j += 1
    return main_data

# print(get_data())


def write_to_csv(data_file):
    """Запись данных в csv"""

    main_data = get_data()
    with open(data_file, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in main_data:
            writer.writerow(row)


write_to_csv('data_report.csv')

# --------------Проверка--------------
with open('data_report.csv', encoding='utf-8') as f_n:
    F_N_READER = csv.reader(f_n)
    for row in F_N_READER:
        print(row)
