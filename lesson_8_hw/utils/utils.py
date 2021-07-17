import inspect
import json
import os
import pickle
import sys
import time
import traceback
from argparse import ArgumentParser
from functools import wraps

import logging

from lesson_8_hw.logs.server_log_config import SERVER_LOGGER
from lesson_8_hw.logs.client_log_config import CLIENT_LOGGER

sys.path.append('../')

# # Определяем источник клиент или сервер
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    SERVER_LOGGER.debug(f'Выполняем переключение на серверный лог:\n{SERVER_LOGGER.name}')
else:
    CLIENT_LOGGER.debug(f'Выполняем переключение на лог клиента:\n{CLIENT_LOGGER.name}')

if SERVER_LOGGER:
    name_log = SERVER_LOGGER
else:
    name_log = CLIENT_LOGGER

# @log
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
        print(os.getcwd())
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

def create_message(msg, CONFIGS):
    message = {
        CONFIGS['ACTION']: CONFIGS['MESSAGE'],
        CONFIGS['SENDER']: msg[0][0],
        CONFIGS['TIME']: time.time(),
        CONFIGS['MESSAGE_TEXT']: msg[0][1]
    }
    # logger.info(f'Сформировано msg от клиента')
    return message

def get_arg(CONFIGS):
    """Парсер аргументов в командной строке
    Принимаем на вход конфигурациию, а возвращаем порт и адрес
    """
    SERVER_LOGGER = logging.getLogger('server')
    parser = ArgumentParser()
    parser.add_argument('-p', help='Listen port', default=CONFIGS['DEFAULT_PORT'], type=int, nargs='?')
    # parser.add_argument('-a', help='Listen address', default=CONFIGS['DEFAULT_ADDRESS'], type=str, nargs='?')
    parser.add_argument('-a', help='Listen address', default='', type=str, nargs='?')
    args = parser.parse_args(sys.argv[1:])
    listen_port = args.p
    listen_address = args.a

    if not 65535 >= listen_port >= 1024:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с некорректного порта: '
                               f'{listen_port}\nПорт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)
    return listen_address, listen_port
