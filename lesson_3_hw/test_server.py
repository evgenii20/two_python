import unittest
# импортируем модуль client для тестирования
from server import handle_response
from utils import load_configs  # , get_message, send_message


# Модульные тесты
class TestServer(unittest.TestCase):
    CONFIGS = load_configs(True)

    error_message = {
        CONFIGS['RESPONSE']: 400,
        CONFIGS['ERROR']: 'Bad request'
    }
    success_message = {CONFIGS['RESPONSE']: 200}

    # whithout - без
    def test_whithout_action(self):
        """тест завершается ошибкой,т.к. мы её ожидаем"""
        self.assertEqual(
            handle_response({
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['TIME']: '1.1',
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Guest'
                }
            }), #self.CONFIGS,
            self.error_message
        )

    def test_wrong_action(self):
        """Неправильное действие"""
        self.assertEqual(
            handle_response({
                self.CONFIGS['ACTION']: 'Wrong',
                self.CONFIGS['TIME']: '1.1',
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Guest'
                }
            }), #self.CONFIGS,
            self.error_message
        )

    def test_whithout_time(self):
        """тест без тега TIME"""
        self.assertEqual(
            handle_response({
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Guest'
                }
            }), #self.CONFIGS,
            self.error_message
        )

    def test_whithout_user(self):
        """тест без пользователя"""
        self.assertEqual(
            handle_response({
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['TIME']: '1.1'
            # }, self.CONFIGS),
            }), #self.CONFIGS,
            self.error_message
        )

    # wrong - непраыильный
    def test_wrong_user(self):
        """wrong - неправильный пользователь"""
        self.assertEqual(
            handle_response({
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['TIME']: '1.1',
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Guest1'
                }
            }), #self.CONFIGS,
            self.error_message
        )

    # def test_server_up_main(self):
    #     if '-p' in sys.argv:
    def test_success_check(self):
        """Проверка на успех"""
        self.assertEqual(
            handle_response({
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['TIME']: 1.1,
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Guest'
                }
            }), #self.CONFIGS,
            self.success_message
        )

    # def test_create_presence_message(self):
    #
    # # equal - равный
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
