import json
import os
import sys
import socket

# объявдяем словарь для конфигурации
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
    # если передан тип сообщения - присутствие клиента, то возвращаем ответ
    if CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('USER') in message \
            and message[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        return {CONFIGS.get('RESPONSE'): 200}
    return {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad Request'
    }


def main():
    # блок запуска сервера
    global CONFIGS
    CONFIGS = load_config()
    try:
        # обработка параметра командной строки
        if '-p' in sys.argv:
            # слушаем порт
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = CONFIGS.get('DEFAULT_PORT')
        if not 65535 >= listen_port >= 1024:
            raise ValueError
    except IndexError:
        print('После -\'p\' необходимо указать порт')
        sys.exit(1)
    except ValueError:
        print('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    # обработка параметра командной строки
    try:
        # адрес сервера
        if '-a' in sys.argv:
            # index('-a') - ищет совпадения в строке
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print('После \'a\'- необходимо указать адрес для прослушивания')
        sys.exit(1)

    # s = socket(AF_INET, SOCK_STREAM)  # AF_INET для сетевого протокола IPv4
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # открываем socket для передачи данных
    # s.bind(('', 8888))  # 1 привязываем сокет к IP-адресу и порту машины
    # transport.connect((server_address, server_port))  # привязываем клиента к IP-адресу и порту сервера
    # transport.bind((CONFIGS.get('DEFAULT_IP_ADDRESS'),
    #                 CONFIGS.get('DEFAULT_PORT')))  # привязываем клиента к IP-адресу и порту сервера
    transport.bind((listen_address, listen_port))
    # s.listen(5)  # 5 - количество подключений
    transport.listen(CONFIGS.get('MAX_CONNECTIONS'))

    while True:
        # client, addr = s.accept()  # акцептим запрос на соединение
        client, client_address = transport.accept()  # акцептим запрос на соединение
        # data = client.recv(1024)  # принимаем данные (пакет)
        message = get_message(client, CONFIGS)
        # decoded_data = data.decode('utf-8')  # декодируем данные
        response = handle_response(message)
        # msg_to_client = 'Ответ клиенту'  # сообщение от клиента
        # ответ клиента
        # client.send(msg_to_client.encode('utf-8'))  # кодируем в байты сообшение от клиента в кодировке UTF-8 и отправляем
        send_message(client, response, CONFIGS)
        client.close()  # закрываем соединение клиента

        # print(f'Message from client: {decoded_data}')  # вывели текущее состояние клиента


if __name__ == '__main__':
    main()
