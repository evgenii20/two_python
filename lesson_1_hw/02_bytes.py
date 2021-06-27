"""
lesson 1 hw

2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
последовательность кодов (не используя методы encode и decode) и определить тип,
содержимое и длину соответствующих переменных.
"""

word_1 = b'class'
word_2 = b'function'
word_3 = b'method'
print(f'Простой вывод строки "{word_1}":\n{word_1}\nДлинна строки: {len(word_1)}\nТип строки: {type(word_1)}')
# <class 'bytes'>
print('-' * 10)
print(f'Простой вывод строки "{word_2}":\n{word_2}\nДлинна строки: {len(word_2)}\nТип строки: {type(word_2)}')
# <class 'bytes'>
print('-' * 10)
print(f'Простой вывод строки "{word_3}":\n{word_3}\nДлинна строки: {len(word_3)}\nТип строки: {type(word_3)}')
# <class 'bytes'>
print('=' * 15)

#
# # # кодируем в юникод
# enc_str = 'разработка'
# enc_str_bytes = enc_str.encode('unicode-escape')
# print(f'unicode: \n', enc_str_bytes)
# print(f'unicode: \n', type(enc_str_bytes))
# b'\\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0430'
