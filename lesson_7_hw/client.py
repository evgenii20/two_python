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
    message = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    CLIENT_LOGGER.info('Создание сообщения отправки на сервер')
    return message


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
   

    address = (listen_addres(), listen_port())

    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transport:
            transport.connect(address)
            while True:
                msg = input('q - выход. Ваше сообщение: ')
                if msg == 'q':
                    break
                # presence_message = create_presence_message('Guest')  # "Guest" -сообшение присутствия гостя

                transport.send(msg.encode(CONFIGS.get('ENCODING')))
                
                data = json.dumps(transport.recv(1024).decode('utf-8'))
                

                print('Ответ сервера:', data)
                CLIENT_LOGGER.info('Отправка сообщения серверу.')
                

    except (ValueError, json.JSONDecodeError):
        # print('Ошибка декодирования сообщения')
        CLIENT_LOGGER.error('Ошибка декодирования сообщения')


if __name__ == '__main__':
    # Создаем объект-логгер с именем client:
    # CLIENT_LOGGER = logging.getLogger('client')
    CLIENT_LOGGER.debug('Начинаем сбор логов!')
    main()
    CLIENT_LOGGER.debug('Заканчиваем сбор логов.')
