"""
lesson 1 hw

1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
проверить тип и содержание соответствующих переменных. Затем с помощью
онлайн-конвертера преобразовать строковые представление в формат Unicode и также
проверить тип и содержимое переменных.
"""

word_1 = 'разработка'
word_2 = 'сокет'
word_3 = 'декоратор'
print(f"Простой вывод строки '{word_1}':\n{word_1}\nТип строки: {type(word_1)}")
# разработка
print('-' * 10)
print(f"Простой вывод строки '{word_2}':\n{word_2}\nТип строки: {type(word_2)}")
# сокет
print('-' * 10)
print(f"Простой вывод строки '{word_3}':\n{word_3}\nТип строки: {type(word_3)}")
# декоратор
print('=' * 15)

unicod_word_1 = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
unicod_word_2 = '\u0441\u043e\u043a\u0435\u0442'
unicod_word_3 = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

print(f'Тип данных слова "{unicod_word_1}" в "unicode":\n', type(unicod_word_1))
# <class 'bytes'>
print('-' * 10)
print(f'Тип данных слова "{unicod_word_2}" в "unicode":\n', type(unicod_word_2))
# <class 'bytes'>
print('-' * 10)
print(f'Тип данных слова "{unicod_word_3}" в "unicode":\n', type(unicod_word_3))
# <class 'bytes'>
print('=' * 15)

# Первое слово и слово в кодировке unicode равны
print(word_1 == unicod_word_1)
print(word_2 == unicod_word_2)
print(word_3 == unicod_word_3)

# # # кодируем в юникод
# enc_str = 'разработка'
# enc_str_bytes = enc_str.encode('unicode-escape')
# print(f'unicode: \n', enc_str_bytes)
# print(f'unicode: \n', type(enc_str_bytes))
# b'\\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0430'
