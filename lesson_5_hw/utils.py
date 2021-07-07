import json
import os
import sys


def load_configs(is_server=True):
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
