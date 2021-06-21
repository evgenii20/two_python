"""
Задание 3

Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение
данных в файле YAML-формата.
Для этого:
    а)Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
    второму — целое число,
    третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
    отсутствующим в кодировке ASCII (например, €);

    б)Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
    При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить
    возможность работы с юникодом: allow_unicode = True;

    в)Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""
import yaml

data_to_yaml = {
    'key1': [
        'subkey1', 'subkey2', 'subkey3'
    ],
    'key2': 4,
    'key3': {
        '1€': '342',
        '2₱': '7645',
        '3₤': '932'
    }
}

# file.yaml
with open('file.yaml', 'w', encoding='utf-8') as yaml_file:
    # В строку
    yaml.dump(data_to_yaml, yaml_file, allow_unicode=True, default_flow_style=False)

with open('file.yaml', encoding='utf-8') as yaml_file:
    # print(yaml_file.read())
    yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)

# Валидация данных
if yaml_data == data_to_yaml:
    print('Данные совпали')
else:
    print('Данные не совпали')
