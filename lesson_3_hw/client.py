import json
import os
import sys
import socket
import time

# from socket import *

# объявдяем константу типа словарь
from socket import socketpair

CONFIGS = dict()


def load_config(is_server=True):
    """Загрузка файла конфигурации"""

    config_keys = [
        'DEFAULT_PORT',
        'MAX_CONNECTIONS',
        'MAX_PACKAGE_LENGTH',
        'ENCODING',
        'ACTION',
        'TIME',
        'USER',
        'ACCOUNT_NAME',
        'PRESENCE',
        'RESPONSE',
        'ERROR'
    ]
    # если не сервер, то добавляем "DEFAULT_IP_ADDRESS"
    if not is_server:
        config_keys.append('DEFAULT_IP_ADDRESS')
    # если файл не найден: сообщение
    if not os.path.exists('config.json'):
        print('Файл конфигурации не найден')
        sys.exit(1)
    # если файл найден, отрываем для чтения настроек
    with open('config.json') as config_file:
        # записываем в глообальную константу-словарь CONFIGS
        CONFIGS = json.load(config_file)
    load_config_keys = list(CONFIGS.keys())
    # проверяем корректность списка ключей
    for key in config_keys:
        # если ключ не в списке загруженных ключей, то уведомление
        if key not in load_config_keys:
            print(f'В файле конфигурации не хватает ключа: {key}')
            sys.exit(1)
    return CONFIGS


def get_message(opened_socket, CONFIGS):
    """Получение сообщений от клиента к серверу и наоборот"""
    # получаем пакет данных
    response = opened_socket.recv(CONFIGS.get('MAX_PACKAGE_LENGTH'))
    # если экземпляр класса response в байтах, то
    if isinstance(response, bytes):
        json_response = response.decode(CONFIGS.get('ENCODING'))
        response_dict = json.loads(json_response)
        # если экземпляр класса словаря словарь, то возвращаем его, иначе Err
        if isinstance(response_dict, dict):
            return response_dict
        raise ValueError
    raise ValueError


def send_message(opened_socket, message, CONFIGS):
    """Отправка сообщений от клиента к серверу и наоборот"""
    # читаем сообщение JSON
    json_message = json.dumps(message)
    # формируем ответ (response)
    response = json_message.encode(CONFIGS.get('ENCODING'))
    # response = json_message.encode('utf-8')
    opened_socket.send(response)


def handle_response(message):
    """Статус доставки сообщения"""
    if CONFIGS.get('RESPONSE') in message:
        if message[CONFIGS.get('RESPONSE')] == 200:
            return '200 : OK'
        return f'400 : {message[CONFIGS.get("ERROR")]}'
    raise ValueError


def create_presence_message(account_name):
    # создаём сообщение присутствия клиента
    # message = {
    #         CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),

    # message = {
    #     "action": "presence",
    #     "time": time.time(),
    #     "type": "status",
    #     "user": {
    #         "account_name": account_name,
    #         "status": "Yep, I am here!"
    #     }
    # }
    message = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    return message


def main():
    # блок запуска клиента
    global CONFIGS
    # is_server=False - клиент не сервер
    CONFIGS = load_config(is_server=False)
    try:
        # server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
        # разбираем строку запуска клиента на части в виде списка:
        server_address = sys.argv[1]
        # server_port = CONFIGS.get('DEFAULT_PORT')
        server_port = int(sys.argv[2])
        # от 1024 до 65535 свободные порты
        if not 65535 >= server_port >= 1024:
            raise ValueError
    except IndexError:
        server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
        server_port = CONFIGS.get('DEFAULT_PORT')
    except ValueError:
        print('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    try:
        # s = socket(AF_INET, SOCK_STREAM)  # открываем socket для передачи данных
        # открываем socket для передачи данных
        # transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect(('localhost', 8888))  # привязываем клиента к IP-адресу и порту сервера
        transport.connect((server_address, server_port))  # привязываем клиента к IP-адресу и порту сервера
    except ConnectionRefusedError:
        print('Вы ввели неверные данные для подключения!\nОбратитесь в службу поддержки.')
        sys.exit(1)

    # msg_to_server = 'Сообщение для сервера'
    presence_message = create_presence_message('Guest')  # "Guest" -сообшение присутствия гостя
    # s.send(msg_to_server.encode('utf-8'))
    send_message(transport, presence_message, CONFIGS)
    try:
        # data = s.recv(1024)  # получаем данные (пакет)
        # decoded_data = data.decode('utf-8')  # декодируем данные
        response = get_message(transport, CONFIGS)
        # обработанный ответ
        handled_response = handle_response(response)
        print(f'Message from server: {response}')
        print(handled_response)
        # s.close()
        # transport.close()
    except (ValueError, json.JSONDecodeError):
        print('Ошибка декодирования сообщения')


if __name__ == '__main__':
    main()
