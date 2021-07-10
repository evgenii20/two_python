import json
import os
import sys
from functools import wraps

from logs.server_log_config import SERVER_LOGGER
from logs.client_log_config import CLIENT_LOGGER
"""
def decorator_function(func):
    def wrapper():
        print('Функция-обёртка!')
        print('Оборачиваемая функция: {}'.format(func))
        print('Выполняем обёрнутую функцию...')
        func()
        print('Выходим из обёртки')
    return wrapper
    
Здесь decorator_function() является функцией-декоратором. Как вы могли заметить, 
она является функцией высшего порядка, так как принимает функцию в качестве аргумента, а 
также возвращает функцию. Внутри decorator_function() мы определили другую функцию, обёртку, 
так сказать, которая обёртывает функцию-аргумент и затем изменяет её поведение. Декоратор возвращает эту 
обёртку. Теперь посмотрим на декоратор в действии:

>>> @decorator_function
... def hello_world():
...     print('Hello world!')
...
>>> hello_world()
Оборачиваемая функция: <function hello_world at 0x032B26A8>
Выполняем обёрнутую функцию...
Hello world!
Выходим из обёртки
"""


# class log():
#     ''' Фабрика декораторов-замедлителей
#     '''
#
#     def __init__(self, timeout):
#         # self.timeout = timeout
#         pass
#
#     def __call__(self, func):
#         ''' вызываем функцию
#         '''
#
#         # @wraps(func)
#         def decorated(*args, **kwargs):
#             ''' Декорированная функция
#             '''
#             time.sleep(self.timeout)
#             res = func(*args, **kwargs)
#             print('Function {} was sleeping in class'.format(func.__name__))
#             return res
#
#         return decorated
# #-

# На вход принимаем функцию
def log(func):
    # Определяем источник клиент или сервер
    if sys.argv[0].find('client') == -1:
        # если не клиент то сервер!
        # server_log = logging.getLogger('server')
        # print(SERVER_LOGGER.getEffectiveLevel())
        # SERVER_LOGGER.debug(f'Выполняем переключение на серверный лог:\n{SERVER_LOGGER.getEffectiveLevel()}')
        SERVER_LOGGER.debug(f'Выполняем переключение на серверный лог:\n{SERVER_LOGGER.name}')
    else:
        # client_log = logging.getLogger('client')
        # print(CLIENT_LOGGER.getEffectiveLevel())
        # CLIENT_LOGGER.debug(f'Выполняем переключение на лог клиента:\n{CLIENT_LOGGER.getEffectiveLevel()}')
        CLIENT_LOGGER.debug(f'Выполняем переключение на лог клиента:\n{CLIENT_LOGGER.name}')

    # в функции обёртке принимаем аргументы
    @wraps(func)
    def wrapper(*args, **kwargs):
        if SERVER_LOGGER:
            name_log = SERVER_LOGGER
        else:
            name_log = CLIENT_LOGGER
        # print('Функция-обёртка!')
        name_log.debug('Запущена Функция-обёртка!')
        # print('Оборачиваемая функция: {}'.format(func))
        name_log.debug(f'Оборачиваемая функция: {func.__name__} :'
                       f'\n\tс позиционными\t{args} :'
                       f'\n\tи именованными аргументами\t{kwargs}')
        name_log.debug('Выполняем обёрнутую функцию...')
        # func()
        r = func(*args, **kwargs)
        name_log.debug(f'Функция {func.__name__} вернула:\n{r}')
        name_log.debug('Выходим из обёртки')
        return r

    return wrapper


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
