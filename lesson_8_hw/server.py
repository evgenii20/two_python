import argparse
import json
import logging
import select
import sys
import socket

# импорт конфигурации для SERVER_LOGGER
import logs.server_log_config
# импорт класса Log
from utils.decorators import Log
# импорт модуля utils
from utils.utils import load_configs, get_message, send_message, create_message, get_arg 
from argparse import ArgumentParser

# объявдяем словарь для конфигурации
CONFIGS = dict()

# Создаем объект-логгер с именем server:
SERVER_LOGGER = logging.getLogger('server')

# @log
@Log()
def handle_response(message, list_mess, client, CONFIGS):
    """Статус доставки сообщения"""
    SERVER_LOGGER.info(f'Обработка сообщения от клиента: {message}')
    # если передан тип сообщения - присутствие клиента, то возвращаем ответ
    if CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('USER') in message \
            and message[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        # return {CONFIGS.get('RESPONSE'): 200}
        list_mess.append({CONFIGS.get('RESPONSE'): 200})
    # return {
    list_mess.append({
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad Request'
    })


# @Log()
def read_requests(r_clients, all_clients):
    """
    Чтение запросов из списка клиентов
    :param r_clients: читающие клиенты
    :param all_clients: все читающие клиенты
    :return: responses - возвращает словарь запросов на чтение
    """
    # ответы клиентов
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            # пишем в словарь
            responses[sock] = data
        except:
            SERVER_LOGGER.debug(f'Клиент {sock.fileno()} {sock.getpeername()} больше не читает, отключился')
            all_clients.remove(sock)

    return responses

# @Log()
def write_responses(requests, w_clients, all_clients):
    """
    Эхо-ответ сервера клиентам, от которых были запросы
    :param requests:
    :param w_clients:
    :param all_clients:
    :return:
    """
    for sock in w_clients:
        if sock in requests:
            try:
                # Подготовить и отправить ответ сервера
                resp = requests[sock].encode('utf-8')
                # Эхо-ответ сделаем чуть непохожим на оригинал
                sock.send(resp.upper())
            except:  # Сокет недоступен, клиент отключился
                SERVER_LOGGER.debug(f'Клиент {sock.fileno()} {sock.getpeername()} больше не пишет, отключился')
                sock.close()
                all_clients.remove(sock)

def new_listen_socket(listen_addres, listen_ports):
    # SERVER_LOGGER.info(f'Сервер запущен на порту {listen_port}, по адресу: {listen_address}.')
    SERVER_LOGGER.info(f'Сервер запущен на порту {listen_ports}, по адресу: {listen_addres}.')
    # открываем socket для передачи данных
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_addres, listen_ports))  # привязываем адрес и порт к клиенту
    transport.settimeout(0.5)  # Таймаут необходим, чтобы не ждать появления данных в сокете

    transport.listen(CONFIGS.get('MAX_CONNECTIONS'))
    return transport

# @Log()
def main():
    # блок запуска сервера
    global CONFIGS
    CONFIGS = load_configs()
    # # Получаем адрес и порт сервера
    listen_address, listen_port = get_arg(CONFIGS)
    # # transport - будет содержать возвращаемый результат из new_listen_socket
    transport = new_listen_socket(listen_address, listen_port)
    # # -------

    # список клиентов и сообщений
    clients = []
    messages = []

    while True:
        try:
            # client, addr = s.accept()  # акцептим запрос на соединение
            client, client_address = transport.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            SERVER_LOGGER.debug(f'Получен запрос на соединение от {client_address}')
            # добавляем в общий список клиентов
            clients.append(client)
        finally:
            # Проверяем наличие событий ввода-вывода
            wait = 5
            recv_list = []  # получить
            send_list = []  # отправить
            e_list = []
            try:
                if clients:  # все читают, все пишут
                    recv_list, send_list, e_list = select.select(clients, clients, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился

            if recv_list:
                for client_message_list in recv_list:
                    mesg = get_message(client_message_list, CONFIGS)

                    try:
                        # в сообщение присутствия оборачиваем
                        handle_response(mesg, messages, client_message_list, CONFIGS)  # читаем запросы клиентов
                        # handle_response(get_message(client_message_list, CONFIGS), messages, client_message_list, CONFIGS)  # читаем запросы клиентов
                    except:
                        SERVER_LOGGER.info(f'Клиент {client_message_list} больше не читает, отключился.')
                        clients.remove(client_message_list)

            if send_list and messages:
                # message = create_message(messages, username="Guest", CONFIGS)
                msg = create_message(messages, CONFIGS)
                # write_responses(requests, send_list, clients)  # Выполним отправку ответов клиентам
                del messages[0]
                # for msg in messages:
                for waiting_client in send_list:
                    try:
                        send_message(waiting_client, msg, CONFIGS)
                    except:
                        SERVER_LOGGER.info(f'Клиент {waiting_client} больше не пишет, отключился.')
                        clients.remove(waiting_client)

if __name__ == '__main__':
    SERVER_LOGGER.debug('Start LOG write')
    main()
    SERVER_LOGGER.debug('Close LOG write')
