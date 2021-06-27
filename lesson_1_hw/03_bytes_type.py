"""
lesson 1 hw

3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
байтовом типе.
"""

word_1 = b'attribute'
word_2 = b'класс'
"""
Невозможно записать в байтовом типе не относящийся к ASCII код:
word_2 = b'класс'
         ^    
SyntaxError: bytes can only contain ASCII literal characters.
"""
word_3 = b'функция'
"""
Невозможно записать в байтовом типе не относящийся к ASCII код:
word_2 = b'функция'
         ^    
SyntaxError: bytes can only contain ASCII literal characters.
"""
word_4 = b'type'

"""
Определение ошибки происходит на уровне интерпретатора при выполнении кода. Слова на кирилице нельзя записать 
в байтовом типе, т.к. они не относятся к ASCII кодам.  
"""

# print(f'Простой вывод строки "{word_1}":\n{word_1}\nДлинна строки: {len(word_1)}\nТип строки: {type(word_1)}')
# # <class 'bytes'>
# print('-' * 10)
# print(f'Простой вывод строки "{word_4}":\n{word_4}\nДлинна строки: {len(word_4)}\nТип строки: {type(word_4)}')
# # <class 'bytes'>
# print('=' * 15)


