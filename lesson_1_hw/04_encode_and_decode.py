"""
lesson 1 hw

4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование (используя
методы encode и decode).
"""

# Чтобы зашифровать строку в набор байтов, применяем метод "encode"
enc_str_1 = 'разработка'
enc_str_2 = 'администрирование'
enc_str_3 = 'protocol'
enc_str_4 = 'standard'

UTF8 = 'utf-8'
# UTF8 = 'unicode-escape'

# кодируем
enc_str_bytes_1 = enc_str_1.encode(UTF8)
enc_str_bytes_2 = enc_str_2.encode(UTF8)
enc_str_bytes_3 = enc_str_3.encode(UTF8)
enc_str_bytes_4 = enc_str_4.encode(UTF8)

print(f'Кодируемая строка "{enc_str_1}" методом "encode({UTF8})":\n{enc_str_bytes_1}')
print('-' * 10)
print(f'Кодируемая строка "{enc_str_2}" методом "encode({UTF8})":\n{enc_str_bytes_2}')
print('-' * 10)
print(f'Кодируемая строка "{enc_str_3}" методом "encode({UTF8})":\n{enc_str_bytes_3}')
print('-' * 10)
print(f'Кодируемая строка "{enc_str_4}" методом "encode({UTF8})":\n{enc_str_bytes_4}')
# b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
print('=' * 15)

# За выполнение обратного процесса отвечает метод "decode"
dec_str_1 = enc_str_bytes_1.decode(UTF8)
dec_str_2 = enc_str_bytes_2.decode(UTF8)
dec_str_3 = enc_str_bytes_3.decode(UTF8)
dec_str_4 = enc_str_bytes_4.decode(UTF8)

# print(f'Для расшифровки используют метод "decode(\'utf-8\')":\n', dec_str)
print(f'Декодируемая строка "{enc_str_1}" методом "decode({UTF8})":\n{dec_str_1}')
print('-' * 10)
print(f'Декодируемая строка "{enc_str_2}" методом "decode({UTF8})":\n{dec_str_2}')
print('-' * 10)
print(f'Декодируемая строка "{enc_str_3}" методом "decode({UTF8})":\n{dec_str_3}')
print('-' * 10)
print(f'Декодируемая строка "{enc_str_4}" методом "decode({UTF8})":\n{dec_str_4}')

