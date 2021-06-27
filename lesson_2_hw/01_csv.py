"""
Задание 1

Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
«отчетный» файл в формате CSV. Для этого:

а) Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью
регулярных выражений извлечь значения параметров «Изготовитель системы»,  «Название ОС»,
«Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка — например,
os_prod_list,
os_name_list,
os_code_list,
os_type_list.
В этой же функции создать главный список для хранения данных отчета — например, main_data — и
поместить в него названия столбцов отчета в виде списка:
«Изготовитель системы»,
«Название ОС»,
«Код продукта»,
«Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

б) Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции
реализовать получение данных через вызов функции get_data(), а также сохранение подготовленных
данных в соответствующий CSV-файл;

в) Проверить работу программы через вызов функции write_to_csv().
"""
import csv

# import re

PUTH_CSV = 'report.csv'


def get_data():
    """
    Функция get_data(), в цикле осуществляет перебор файлов с данными, их открытие и считывание данных.
    :return: result_data
    """

    FILES_LIST = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    result_data = [['Название ОС', 'Изготовитель системы', 'Код продукта', 'Тип системы']]

    # list_files_end = 0
    # while True:
    for file_name in FILES_LIST:
        print(f'\n52:file_name: {file_name}\n')
        # if list_files_end < len(FILES_LIST):
        #     for file in range(len(FILES_LIST)):
        #         list_files_end += 1
        with open(file_name, encoding='cp1251') as data_file:
            data = data_file.read().split('\n')
            # str1 = []
            # os_name_list = re.search(os_name_list_pattern, data)
            for row in data:
                row_list = row.split(':')
                if result_data[0][0] in row_list[0]:
                    # strip() Удаляет пробельные символы в начале и в конце строки
                    os_name_list.append(row_list[1].strip())
                    print(f'67: os_name_list: {os_name_list}')
                if result_data[0][1] in row_list[0]:
                    os_prod_list.append(row_list[1].strip())
                    print(f'70: os_prod_list: {os_prod_list}')
                if result_data[0][2] in row_list[0]:
                    os_code_list.append(row_list[1].strip())
                    print(f'73: os_code_list: {os_code_list}')
                if result_data[0][3] in row_list[0]:
                    os_type_list.append(row_list[1].strip())
                    print(f'76: os_type_list: {os_type_list}')

            result_data.append(
                [
                    os_name_list[-1],
                    os_prod_list[:1][0],
                    os_code_list[:1][0],
                    os_type_list[:1][0]

                ]
            )
    return result_data


def write_to_csv(file_name):
    """
    Функция получения данных через вызов функции get_data(), а также сохранение подготовленных
    данных в соответствующий CSV-файл;
    :param file_name:
    """
    with open(file_name, 'w', encoding='cp1251') as csv_file:
        csv_writer = csv.writer(csv_file)
        print(get_data())
        for row in get_data():
            csv_writer.writerow(row)
        print(f'Запись в "{file_name}" выполнена успешно!')


write_to_csv(PUTH_CSV)
