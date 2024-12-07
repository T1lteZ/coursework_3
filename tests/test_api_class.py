import unittest
from unittest.mock import patch, Mock

from src.api_class_module import get_companies, get_vacancies


class TestCompanyFunctions(unittest.TestCase):
    def test_get_companies(self):
        expected_result = [
            {'company_id': 78638, 'company_name': 'Тиньков', 'company_url': 'https://hh.ru/employer/78638'},
            {'company_id': 1740, 'company_name': 'Яндекс', 'company_url': 'https://hh.ru/employer/1740'},
            {'company_id': 1057, 'company_name': 'Лаборатория Касперского',
             'company_url': 'https://hh.ru/employer/1057'},
            {'company_id': 1473866, 'company_name': 'Сбербанк', 'company_url': 'https://hh.ru/employer/1473866'},
            {'company_id': 4181, 'company_name': 'Банк ВТБ', 'company_url': 'https://hh.ru/employer/4181'},
            {'company_id': 39305, 'company_name': 'Газпромнефть', 'company_url': 'https://hh.ru/employer/39305'},
            {'company_id': 80, 'company_name': 'Альфа-банк', 'company_url': 'https://hh.ru/employer/80'},
            {'company_id': 15478, 'company_name': 'VK', 'company_url': 'https://hh.ru/employer/15478'},
            {'company_id': 2748, 'company_name': 'ПАО Ростелеком', 'company_url': 'https://hh.ru/employer/2748'},
            {'company_id': 1429999, 'company_name': 'Циан', 'company_url': 'https://hh.ru/employer/1429999'}
        ]

        result = get_companies()
        self.assertEqual(result, expected_result)

    @patch('requests.get')
    def test_get_vacancies(self, mock_get):
        company_data = [{'company_id': 78638, 'company_name': 'Тиньков', 'company_url': 'https://hh.ru/employer/78638'}]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': [{'name': 'Вакансия 1'}, {'name': 'Вакансия 2'}]}
        mock_get.return_value = mock_response

        result = get_vacancies(company_data)
        expected_result = [{'name': 'Вакансия 1'}, {'name': 'Вакансия 2'}]

        self.assertEqual(result, expected_result)
        mock_get.assert_called_once_with('https://api.hh.ru/vacancies?employer_id=78638')

    @patch('requests.get')
    def test_get_vacancies_error(self, mock_get):
        company_data = [{'company_id': 78638, 'company_name': 'Тиньков', 'company_url': 'https://hh.ru/employer/78638'}]

        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = get_vacancies(company_data)
        self.assertEqual(result, [])
