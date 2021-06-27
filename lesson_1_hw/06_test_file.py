"""
lesson 1 hw

6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

# Работа с файловой системой

# Чтобы обратиться к определенному файлу и прочесть его содержимое, применяется следующая
# конструкция:

# with open(file_name) as f_n:
#     for el_str in f_n:
#         print(el_str)

# import locale
#
# # определяем установленную в ОС кодировку по умолчанию
# def_coding = locale.getpreferredencoding()
# print(def_coding)
# cp1251

# При работе с файлами также можно определить наименование кодировки, которая будет
# использоваться при операциях с ними

STR = ['сетевое программирование', 'сокет', 'декоратор']

# with open("test_file.txt", "w") as f:
file = open("test_file.txt", "r+")
for el in range(len(STR)):
    # file = file.write(STR[el] +'\n')
    # file1 = file.write(STR[el] + '\n')
    file.write(STR[el] + '\n')
    # file.write(STR[el])

print(f'Кодировка в файле по умолчанию:\n{file.encoding}')
file.close()

# op_file = open("test_file.txt", 'r', encoding='cp1251').read()
op_file = open("test_file.txt", 'r', encoding='unicode-escape').read()
# op_file = open("test_file.txt", 'r', encoding='utf-8').read()
print(op_file)
# op_file.close()

# При использовании utf-8 выходит ошибка декодирования юникода:
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf1 in position 0: invalid continuation byte
# Кодировка utf-8, для декодирования не подходит, не допустимый байт продолжения в позиции 0 
