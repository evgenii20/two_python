import json
import pickle
import sys
import socket
import time
from threading import Thread

from logs.client_log_config import CLIENT_LOGGER
# импорт пакета модулей логирования
from utils.decorators import log
# импорт модуля utils из вложенной папки
from utils.utils import load_configs, get_message, send_message, get_arg

# объявляем константу типа словарь
CONFIGS = dict()

# Создаем объект-логгер с именем client:
# CLIENT_LOGGER = logging.getLogger('client')

# в дальнейшем вызываем:
# CLIENT_LOGGER.critical('Кртиическое сообщение')
# LOGGER

# @Log()
@log
def handle_response(message):
    # def handle_response(message, CONFIGS):
    """Статус доставки сообщения"""
    CLIENT_LOGGER.info('Обработка сообщения от сервера')
    if CONFIGS.get('RESPONSE') in message:
        if message[CONFIGS.get('RESPONSE')] == 200:
            CLIENT_LOGGER.info('Сообщение от сервера успешно обработанно')
            return '200 : OK'
        CLIENT_LOGGER.error('Обработка сообщение от сервера провалилась')
        if message[CONFIGS.get('RESPONSE')] == 400:
            CLIENT_LOGGER.debug('Неправильный запрос/JSON-объект')
            return f'400 : {message[CONFIGS.get("ERROR")]}'
    raise ValueError


def message_for_send(transport, username):
    while True:
        message = input('q - выход. Введите сообщение: ')
        if message == 'q':
            break
        msg = create_message(message, username)
        # отправляем сообщение
        send_message(transport, msg, CONFIGS)
        # CLIENT_LOGGER.info(f"Отправлено сообщение серверу {msg[CONFIGS['MESSAGE']]}")
        CLIENT_LOGGER.info(f"Отправлено сообщение серверу CONFIGS['MESSAGE']")


def message_for_write(transport):
    while True:
        msg = get_message(transport, CONFIGS)
        CLIENT_LOGGER.info(f"Получено сообщение от {msg['FROM']} - {msg['MESSAGE']}")
        print(msg)


# @Log()
@log
def create_presence_message(CONFIGS, account_name="Guest"):
    # def create_presence_message(account_name, CONFIGS):
    """создаём сообщение присутствия клиента"""
    message = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    CLIENT_LOGGER.info('Создание сообщения отправки на сервер')
    return message


def create_message(msg, username='Guest'):
    """Создание сообщения"""
    # Отправляем к Test2:
    account_name = 'Test2'
    message = {
        # CONFIGS['ACTION']: CONFIGS['MESSAGE'],
        CONFIGS['ACTION']: 'msg',
        CONFIGS['TIME']: time.time(),
        CONFIGS['TO']: account_name,
        CONFIGS['FROM']: username,
        CONFIGS['MESSAGE']: msg
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message}')
    return message


# @log
def main():
    # блок запуска клиента
    global CONFIGS
    # is_server=False - клиент не сервер
    CONFIGS = load_configs(is_server=False)
    # Получаем
    listen_address, listen_port = get_arg(CONFIGS)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transport:
            # transport.connect(address)
            transport.connect((listen_address, listen_port))
            username = 'Test1'
            # присутствие клиента
            presence_message = create_presence_message(CONFIGS, username)  # "Guest" -сообшение присутствия гостя

            # Отправляем сообщение серверу
            send_message(transport, presence_message, CONFIGS)
            CLIENT_LOGGER.info('Отправка сообщения серверу.')
            # ответ сервера
            response = get_message(transport, CONFIGS)

            # обработанный ответ
            handled_response = handle_response(response, CONFIGS)

            CLIENT_LOGGER.debug(f'Сообщение от сервера: {handled_response}. Соединение установлено')
            print('Server is connect')

    except (ValueError, json.JSONDecodeError):
        # print('Ошибка декодирования сообщения')
        CLIENT_LOGGER.error('Ошибка декодирования сообщения')

    # Запуск потоков
    receiver = Thread(target=message_for_send, args=(transport, username))
    receiver.start()

    user_send = Thread(target=message_for_write, args=transport)
    user_send.start()


if __name__ == '__main__':
    # Создаем объект-логгер с именем client:
    # CLIENT_LOGGER = logging.getLogger('client')
    CLIENT_LOGGER.debug('Начинаем сбор логов!')
    main()
    CLIENT_LOGGER.debug('Заканчиваем сбор логов.')
