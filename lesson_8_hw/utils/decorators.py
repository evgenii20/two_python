import inspect
import logging
import sys
import traceback
from functools import wraps



SERVER_LOGGER = logging.getLogger('server')
CLIENT_LOGGER = logging.getLogger('client')

# Определяем источник клиент или сервер
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    SERVER_LOGGER.debug(f'Выполняем переключение на серверный лог:\n{SERVER_LOGGER.name}')
else:
    CLIENT_LOGGER.debug(f'Выполняем переключение на лог клиента:\n{CLIENT_LOGGER.name}')

if SERVER_LOGGER:
    name_log = SERVER_LOGGER
else:
    name_log = CLIENT_LOGGER

class Log:
    ''' Фабрика декораторов-замедлителей
    '''

    def __call__(self, func):
        ''' вызываем функцию
        '''

        def wrapper(*args, **kwargs):
            name_log.debug('Запущена Функция-обёртка!')
            # print('Оборачиваемая функция: {}'.format(func))
            name_log.debug('Выполняем обёрнутую функцию...')
            r = func(*args, **kwargs)
            name_log.debug(f'Оборачиваемая функция: {func.__name__}\n'
                           f'\tс аргументами: {args}, {kwargs}.\n'
                           f'Модуль: {func.__module__}.\n'
                           f'Вызов из функции: {traceback.format_stack()[0].strip().split()[-1]}.\n'
                           f'Вызов из: {inspect.stack()[1][3]}.')
            # name_log.debug(f'Функция {func.__name__} вернула:\n{r}')
            name_log.debug('Выходим из обёртки')
            return r

        return wrapper

# На вход принимаем функцию
def log(func):
    # в функции обёртке принимаем аргументы
    @wraps(func)
    def wrapper(*args, **kwargs):
        name_log.debug('Запущена Функция-обёртка!')
        # print('Оборачиваемая функция: {}'.format(func))
        name_log.debug('Выполняем обёрнутую функцию...')
        r = func(*args, **kwargs)
        name_log.debug(f'Оборачиваемая функция: {func.__name__}\n'
                       f'\tс аргументами: {args}, {kwargs}.\n'
                       f'Модуль: {func.__module__}.\n'
                       f'Вызов из функции: {traceback.format_stack()[0].strip().split()[-1]}.\n'
                       f'Вызов из: {inspect.stack()[1][3]}.')
        # name_log.debug(f'Функция {func.__name__} вернула:\n{r}')
        name_log.debug('Выходим из обёртки')
        return r

    return wrapper
