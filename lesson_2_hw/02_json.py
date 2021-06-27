"""
Задание 2

Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией
о заказах. Написать скрипт, автоматизирующий его заполнение данными.
Для этого:
    а)Создать функцию write_order_to_json(), в которую передается 5 параметров —
    товар (item),
    количество (quantity),
    цена (price),
    покупатель (buyer),
    дата (date).

    Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных
    указать величину отступа в 4 пробельных символа;

    б)Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений
    каждого параметра.
"""
import json


def write_order_to_json(item, quantity, price, buyer, date):
    # Объявляем словарь
    orders_data = dict()
    with open('orders.json') as json_file:
        # json_file_content = json_file.read()
        orders_data = json.load(json_file)
        # print(f'29: orders_data::\n{orders_data}')
    if 'orders' not in orders_data:
        orders_data['orders'] = []
    # 1-й вариант
    dict_to_json = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }
    orders_data['orders'].append(dict_to_json)

    # 2-й вариант
    # orders_data['orders'].append(
    #     {
    #         'item': item,
    #         'quantity': quantity,
    #         'price': price,
    #         'buyer': buyer,
    #         'date': date
    #     }
    # )
    with open('orders.json', 'w') as json_file:
        json.dump(orders_data, json_file, indent=4)


# Заполнение несколькими товарами
for i in range(6):
    i += 1
    write_order_to_json(f'Product №{i}', 3 * 1, 99 * 1, 'Kolya', '14-11-2020')
