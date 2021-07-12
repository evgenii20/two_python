import json
import pickle
import sys
import socket
import time
# импорт стандартного модуля
# импортируем объект logger для клиента, при этом не надо дополнительно прописывать объект-логгер в 19-й строке
from logs.client_log_config import CLIENT_LOGGER
# импорт пакета модулей логирования
# from utils_old.decorators import log
# импорт модуля utils_old из вложенной папки
from utils import load_configs, get_message, send_message, log, Log  #, messagess

# объявдяем константу типа словарь
# from socket import socketpair

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

# @Log()
@log
def create_presence_message(account_name="Guest"):
    # def create_presence_message(account_name, CONFIGS):
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
    CLIENT_LOGGER.info('Создание сообщения отправки на сервер')
    return message

# @log
# def create_message(time: datetime, input_msg: str, name="Guest") -> dict:
#     """формирует presence-сообщение"""
#     _msg = {
#         "action": "msg",
#         "time": time,
#         "to": "#group_name",
#         "from": name,
#         "message": input_msg
#     }
#     return _msg
# {
#     "action": "msg",
#     "time": <unix timestamp>,
#     "to": "#room_name",
#     "from": "account_name",
#     "message": "Hello World"
# }

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
        CLIENT_LOGGER.critical('После -\'p\' необходимо указать порт')
        sys.exit(1)
    except ValueError:
        # print('Порт должен быть указан в пределах от 1024 до 65535')
        CLIENT_LOGGER.critical(f'Попытка запуска сервера с некорректного порта: '
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
        CLIENT_LOGGER.critical('После \'a\'- необходимо указать адрес')
        sys.exit(1)

# @log
def main():
    # блок запуска клиента
    global CONFIGS
    # is_server=False - клиент не сервер
    CONFIGS = load_configs(is_server=False)
    # try:
    #     # server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
    #     # разбираем строку запуска клиента на части в виде списка:
    #     # обработка параметра командной строки
    #     if '-p' in sys.argv:
    #         # слушаем порт
    #         server_port = int(sys.argv[sys.argv.index('-p') + 1])
    #     else:
    #         server_port = CONFIGS.get('DEFAULT_PORT')
    #     # server_address = sys.argv[1]
    #     # server_port = CONFIGS.get('DEFAULT_PORT')
    #     # server_port = int(sys.argv[2])
    #     # от 1024 до 65535 свободные порты
    #     if not 65535 >= server_port >= 1024:
    #         raise ValueError
    # except IndexError:
    #     # server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
    #     server_port = CONFIGS.get('DEFAULT_PORT')
    # except ValueError:
    #     # print('Порт должен быть указан в пределах от 1024 до 65535')
    #     CLIENT_LOGGER.warning('Порт должен быть указан в пределах от 1024 до 65535')
    #     sys.exit(1)
    #
    # # обработка параметра командной строки
    # try:
    #     # адрес сервера
    #     if '-a' in sys.argv:
    #         # index('-a') - ищет совпадения в строке
    #         server_address = sys.argv[sys.argv.index('-a') + 1]
    #     else:
    #         server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
    #
    # except IndexError:
    #     # print('После \'a\'- необходимо указать адрес для прослушивания')
    #     CLIENT_LOGGER.critical('После \'a\'- необходимо указать адрес')
    #     sys.exit(1)

    address = (listen_addres(), listen_port())

    # try:
    #     # s = socket(AF_INET, SOCK_STREAM)  # открываем socket для передачи данных
    #     # открываем socket для передачи данных
    #     # transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     # Создать сокет TCP
    #     # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transport:
    #     #     transport.connect(address)
    #         # привязываем клиента к IP-адресу и порту сервера
    #     # s.connect(('localhost', 8888))  # привязываем клиента к IP-адресу и порту сервера
    #     # transport.connect((server_address, server_port))  # привязываем клиента к IP-адресу и порту сервера
    # except ConnectionRefusedError:
    #     # print('Вы ввели неверные данные для подключения!\nОбратитесь в службу поддержки.')
    #     CLIENT_LOGGER.info(f'Клиент ввёл неверные данные для подключения! Сервер: {server_address}, порт: {server_port}')
    #     sys.exit(1)

    # msg_to_server = 'Сообщение для сервера'
    # presence_message = create_presence_message('Guest')  # "Guest" -сообшение присутствия гостя

    # s.send(msg_to_server.encode('utf-8'))
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transport:
            transport.connect(address)
            while True:
                msg = input('q - выход. Ваше сообщение: ')
                if msg == 'q':
                    break
                # presence_message = create_presence_message('Guest')  # "Guest" -сообшение присутствия гостя

                transport.send(msg.encode(CONFIGS.get('ENCODING')))
                # transport.send(messagess.encode(CONFIGS.get('ENCODING')))
                # transport.send(messagess(msg, username="Guest"))
                # transport.send(msg.encode('utf-8'))
                # data = transport.recv(1024).decode(CONFIGS.get('ENCODING'))
                # send_message(transport, presence_message, CONFIGS)
                data = json.dumps(transport.recv(1024).decode('utf-8'))
                # pickle.loads
                # for el in data:
                #     if 'MESSAGE' in data:
                # json_message = json.dumps(message)
                #     # формируем ответ (response)
                #     response = json_message.encode(CONFIGS.get('ENCODING'))
                #     # response = json_message.encode('utf-8')
                #     opened_socket.send(response)

                print('Ответ сервера:', data)
                CLIENT_LOGGER.info('Отправка сообщения серверу.')
                # data = s.recv(1024)  # получаем данные (пакет)
                # decoded_data = data.decode('utf-8')  # декодируем данные

                # response = get_message(transport, CONFIGS)

                # обработанный ответ
                # handled_response = handle_response(response)

                # print(f'Message from server: {response}')
                # CLIENT_LOGGER.debug(f'Сообщение от сервера: {response}')
                # print(handled_response)

                # CLIENT_LOGGER.info(f'Обработанный ответ от сервера: {handled_response}')

                # s.close()
                # transport.close()

    except (ValueError, json.JSONDecodeError):
        # print('Ошибка декодирования сообщения')
        CLIENT_LOGGER.error('Ошибка декодирования сообщения')


if __name__ == '__main__':
    # Создаем объект-логгер с именем client:
    # CLIENT_LOGGER = logging.getLogger('client')
    CLIENT_LOGGER.debug('Начинаем сбор логов!')
    main()
    CLIENT_LOGGER.debug('Заканчиваем сбор логов.')
