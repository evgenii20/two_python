import sys
import os
import unittest
# импортируем модуль client для тестирования
from client import create_presence_message, handle_response
from utils import load_configs  # , get_message, send_message

sys.path.append(os.path.join(os.getcwd(), '..'))


# Модульные тесты
class TestClient(unittest.TestCase):
    # атрибут
    # tmp_sum = 0

    #
    # def setUp(self):
    #     # Выполнить настройку тестов (если необходимо)
    #     tmp_sum = sum_of_squares(2, 3)
    #
    # def tearDown(self):
    #     # Выполнить завершающие действия (если необходимо)
    #     pass

    #
    # def mock_send_presence_to_server(self):
    #     """mock - обманка, имитация работы ответа от сервера"""
    #     return {
    #         'key1': 'values1'
    #     }
    # def test_mock(self):
    #
    #     with (...):
    #         ed = True
    # Подгружаем настройки иначе тест не отработает корректно
    CONFIGS = load_configs()

    def test_create_presence_message(self):
        """вызываем функцию присутствия сообщения для 'Guest' с передачей в именованном аргументе ссылки на настройки"""
        # test = create_presence_message('Guest', CONFIGS=self.CONFIGS)
        test = create_presence_message('Guest')
        test[self.CONFIGS['TIME']] = '1.1'  # время необходимо приравнять принудительно
        # иначе тест никогда не будет пройден
        self.assertEqual(
            test,
            {
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['TIME']: '1.1',
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Guest'
                }
            }
        )

    def test_correct_answer(self):
        """Проверка корректного сообщения"""
        self.assertEqual(
            # handle_response({self.CONFIGS['RESPONSE']: 200}, self.CONFIGS),
            handle_response({self.CONFIGS['RESPONSE']: 200}), self.CONFIGS,
            '200: OK'
        )

    def test_bad_request(self):
        """Получение плохого ответа"""
        self.assertEqual(
            handle_response({
                self.CONFIGS['RESPONSE']: 400,
                self.CONFIGS['ERROR']: 'Bad request'
            }), self.CONFIGS, #}, self.CONFIGS)
            '400: Bad request'
        )

    def test_no_response(self):
        """Вызов ошибки при неправильных ответах"""
        self.assertRaises(
            ValueError,
            handle_response,
            {self.CONFIGS['ERROR']: 'Bad request'},
            self.CONFIGS
        )

    # equal - равный
    # def test_equal(self, EXPECTED_RESULT=None):
    #     self.assertEqual(self.tmp_sum, EXPECTED_RESULT)
    #
    # def test_not_equal(self):
    #     self.assertNotEqual(sum_of_squares(2, 3), 13)

    # def testtypeconvert(self):
    #     r = splitter.split('GOOG 100 490.50', [str, int, float])
    #     self.assertEqual(r, ['GOOG', 100, 490.5])

    # def testdelimiter(self):
    #     r = splitter.split('GOOG,100,490.50', delimiter=',')
    #     self.assertEqual(r, ['GOOG', '100', '490.50'])


# Запустить тестирование
if __name__ == '__main__':
    unittest.main()
