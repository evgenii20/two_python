"""
Файл настроек логирования сервера

%(filename)s 	|	Имя исходного файла, откуда была выполнена запись в журнал
%(message)s 	|	Текст журналируемого сообщения (определяется пользователем)
%(levelname)s 	|	Символическое имя уровня важности
%(asctime)s 	|	Время, когда была выполнена запись в журнал, в формате ASCII
"""
# logging - стандартный модуль для организации логирования
import logging
import logging.handlers
import os
import sys
# импорт модуля utils_old
# from lesson_5_hw.utils_old import load_configs

sys.path.append('../')

# CONFIGS = load_configs()
# CONFIGS = sys.path.append('../config.json')

# Создаем объект форматирования:        дата     уровень важн.  имя модуля    сообщение
SERVER_FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(message)s ")

# Настройка пути
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

# Создать обработчик, который выводит сообщения с уровнем ERROR в поток stderr
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
# STREAM_HANDLER.setLevel(logging.CRITICAL)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
# Создаем файловый обработчик логирования для вывода сообщения в файл
HANDLER_LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf-8', interval=1, when='D')
# HANDLER_LOG_FILE.setLevel(logging.DEBUG)
HANDLER_LOG_FILE.setFormatter(SERVER_FORMATTER)

# Создаем объект-логгер(регигстратор) с именем server:
SERVER_LOGGER = logging.getLogger('server')
# Добавляем обработчики событий от объекта логгера
SERVER_LOGGER.addHandler(STREAM_HANDLER)
SERVER_LOGGER.addHandler(HANDLER_LOG_FILE)
# Устанавливаем уровень логирования
SERVER_LOGGER.setLevel(logging.DEBUG)
# LOGGER.setLevel(CONFIGS.get('LOGGING_LEVEL', logging.DEBUG))

if __name__ == '__main__':
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    SERVER_LOGGER.critical('Кртиическое сообщение')
    SERVER_LOGGER.error('Сообщение об ошибке')
    SERVER_LOGGER.warning('Предупреждение')
    SERVER_LOGGER.info('Информационное сообщение')
    SERVER_LOGGER.debug('Отладочная информация')
