import json
import logging
import select
import sys
import socket
# импортируем объект logger для клиента, при этом не надо дополнительно прописывать объект-логгер в 14-й строке
from logs.server_log_config import SERVER_LOGGER
# import logs.server_log_config
# from utils_old.decorators import Log
# импорт модуля utils_old
# from lesson_7_hw.utils_old import load_configs, get_message, send_message
from utils import load_configs, get_message, send_message, Log, log

# объявдяем словарь для конфигурации
CONFIGS = dict()


# Создаем объект-логгер с именем client:
# SERVER_LOGGER = logging.getLogger('server')
# SERVER_LOGGER = logs.server_config.logging.getLogger('server')
# в дальнейшем вызываем:
# SERVER_LOGGER.critical('Кртиическое сообщение')

# @log
@Log()
def handle_response(message):
    # global SERVER_LOGGER
    # def handle_response(message, CONFIGS):
    """Статус доставки сообщения"""
    SERVER_LOGGER.info(f'Обработка сообщения от клиента: {message}')
    # если передан тип сообщения - присутствие клиента, то возвращаем ответ
    if CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('USER') in message \
            and CONFIGS.get('MESSAGE') in message \
            and message[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        return {CONFIGS.get('RESPONSE'): 200}
    return {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad Request'
    }


# @Log()
def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    # ответы клиентов
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except:
            SERVER_LOGGER.debug(f'Клиент {sock.fileno()} {sock.getpeername()} больше не читает, отключился')
            all_clients.remove(sock)

    return responses

# @Log()
def write_responses(requests, w_clients, all_clients):
    """ Эхо-ответ сервера клиентам, от которых были запросы
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


def listen_port():
    """Слушаем порт"""
    try:
        # обработка параметра командной строки
        if '-p' in sys.argv:
            # слушаем порт
            listen_ports = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_ports = CONFIGS.get('DEFAULT_PORT')
        if not 65535 >= listen_ports >= 1024:
            raise ValueError
        return listen_ports
    except IndexError:
        # print('После -\'p\' необходимо указать порт')
        SERVER_LOGGER.critical('После -\'p\' необходимо указать порт')
        sys.exit(1)
    except ValueError:
        # print('Порт должен быть указан в пределах от 1024 до 65535')
        SERVER_LOGGER.critical(f'Попытка запуска сервера с некорректного порта: '
                               f'{listen_ports}\nПорт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)


def listen_addres():
    """Слушаем адрес"""
    # обработка параметра командной строки
    try:
        # адрес сервера
        if '-a' in sys.argv:
            # index('-a') - ищет совпадения в строке
            listen_address = sys.argv[sys.argv.index('-a') + 1]
            return listen_address
        else:
            listen_address = ''
            return listen_address
    except IndexError:
        # print('После \'a\'- необходимо указать адрес для прослушивания')
        SERVER_LOGGER.critical('После \'a\'- необходимо указать адрес')
        sys.exit(1)


# @Log()
def main():
    # блок запуска сервера
    global CONFIGS
    CONFIGS = load_configs()
    # вызов функции определения IP и № порта
    # listen(listen_address, listen_port)
    # listen_addres(listen_address=listen_addres)
    # Получаем адрес и порт сервера
    address = (listen_addres(), listen_port())
    # список клиентов
    clients = []

    # SERVER_LOGGER.info(f'Сервер запущен на порту {listen_port}, по адресу: {listen_address}.')
    SERVER_LOGGER.info(f'Сервер запущен на порту {address[1]}, по адресу: {address[0]}.')
    # s = socket(AF_INET, SOCK_STREAM)  # AF_INET для сетевого протокола IPv4
    # открываем socket для передачи данных
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(('', 8888))  # 1 привязываем сокет к IP-адресу и порту машины
    # transport.connect((server_address, server_port))  # привязываем клиента к IP-адресу и порту сервера
    # transport.bind((CONFIGS.get('DEFAULT_IP_ADDRESS'),
    #                 CONFIGS.get('DEFAULT_PORT')))  # привязываем клиента к IP-адресу и порту сервера
    # transport.bind((listen_address, listen_port))
    transport.bind(address)  # привязываем адрес
    # s.listen(5)  # 5 - количество подключений
    transport.listen(CONFIGS.get('MAX_CONNECTIONS'))
    transport.settimeout(0.2)  # Таймаут для операций с сокетом

    while True:
        try:
            # client, addr = s.accept()  # акцептим запрос на соединение
            client, client_address = transport.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            SERVER_LOGGER.debug(f'Получен запрос на соединение от {client_address}')
            clients.append(client)
        finally:
            # Проверяем наличие событий ввода-вывода
            wait = 2
            r = []
            w = []
            try:
                # data = client.recv(1024)  # принимаем данные (пакет)
                # message = get_message(clients, CONFIGS)
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился
                # decoded_data = data.decode('utf-8')  # декодируем данные
                # response = handle_response(message)
                # msg_to_client = 'Ответ клиенту'  # сообщение от клиента
                # ответ клиента
                # client.send(msg_to_client.encode('utf-8'))  # кодируем в байты сообшение от клиента в кодировке UTF-8 и отправляем
                # send_message(client, response, CONFIGS)
                # client.close()  # закрываем соединение клиента
            # except (ValueError, json.JSONDecodeError):
            #     SERVER_LOGGER.error('Принято некорректное сообщение от клиента')
            #     client.close()  # закрываем соединение клиента
            # print(f'Message from client: {decoded_data}')  # вывели текущее состояние клиента

            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            if requests:
                write_responses(requests, w, clients)  # Выполним отправку ответов клиентам
            # requests = response

if __name__ == '__main__':
    SERVER_LOGGER.debug('Start LOG write')
    main()
    SERVER_LOGGER.debug('Close LOG write')
