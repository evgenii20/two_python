"""
Файл настроек логирования клиента

%(filename)s 	|	Имя исходного файла, откуда была выполнена запись в журнал
%(message)s 	|	Текст журналируемого сообщения (определяется пользователем)
%(levelname)s 	|	Символическое имя уровня важности
%(asctime)s 	|	Время, когда была выполнена запись в журнал, в формате ASCII
"""
# logging - стандартный модуль для организации логирования
import logging
import os
import sys

# импорт модуля utils
# from utils import load_configs

sys.path.append('../')

# CONFIGS = load_configs()
# CONFIGS = sys.path.append('../config.json')

# Создаем объект форматирования:        дата     уровень важн.  имя модуля    сообщение
CLIENT_FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(message)s ")

# Настройка пути
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

# Создаём обработчик, который выводит сообщения с уровнем ERROR в поток stderr
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
# STREAM_HANDLER.setLevel(logging.CRITICAL)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
# Создаем файловый обработчик логирования для вывода сообщения в файл
HANDLER_LOG_FILE = logging.FileHandler(PATH, encoding='utf-8')
# HANDLER_LOG_FILE.setLevel(logging.DEBUG)
HANDLER_LOG_FILE.setFormatter(CLIENT_FORMATTER)

# Создаем объект-логгер(регигстратор) с именем client:
# LOGGER = logging.getLogger('client')
CLIENT_LOGGER = logging.getLogger('client')
# Добавляем обработчики событий от объекта логгера
CLIENT_LOGGER.addHandler(STREAM_HANDLER)
CLIENT_LOGGER.addHandler(HANDLER_LOG_FILE)
# Устанаыливаем уровень логирования
CLIENT_LOGGER.setLevel(logging.DEBUG)
# LOGGER.setLevel(CONFIGS.get('LOGGING_LEVEL', logging.DEBUG))

# отладка
if __name__ == '__main__':
    # CONFIGS.get.main()
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    CLIENT_LOGGER.critical('Кртиическое сообщение')
    CLIENT_LOGGER.error('Сообщение об ошибке')
    CLIENT_LOGGER.warning('Предупреждение')
    CLIENT_LOGGER.info('Информационное сообщение')
    CLIENT_LOGGER.debug('Отладочная информация')
