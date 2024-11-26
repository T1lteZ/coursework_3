import unittest
from unittest.mock import patch
from src.api_class_module import FindVacancyFromHHApi, FindEmployerFromHHApi


class TestFindVacancyFromHHApi(unittest.TestCase):
    @patch('requests.get')
    def test_get_vacancies_success(self, mock_get):
        mock_response = {
            "items": [
                {"id": "1", "name": "Vacancy 1"},
                {"id": "2", "name": "Vacancy 2"}
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        api = FindVacancyFromHHApi()
        vacancies = api._FindVacancyFromHHApi__get_vacancies('developer')

        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0]['id'], "1")
        self.assertEqual(vacancies[1]['name'], "Vacancy 2")

    @patch('requests.get')
    def test_get_vacancies_empty(self, mock_get):
        mock_response = {"items": []}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        api = FindVacancyFromHHApi()
        vacancies = api._FindVacancyFromHHApi__get_vacancies('developer')

        self.assertEqual(len(vacancies), 0)

    @patch('requests.get')
    def test_get_vacancies_error(self, mock_get):
        mock_get.return_value.status_code = 404

        api = FindVacancyFromHHApi()
        vacancies = api._FindVacancyFromHHApi__get_vacancies('developer')

        self.assertEqual(len(vacancies), 0)


class TestFindEmployerFromHHApi(unittest.TestCase):
    @patch('requests.get')
    def test_get_employer_info_success(self, mock_get):
        mock_response = {
            "items": [
                {"id": "1001", "name": "Employer 1"},
                {"id": "1002", "name": "Employer 2"}
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        api = FindEmployerFromHHApi()
        employers = api.get_employer_info(2)

        self.assertEqual(len(employers), 2)
        self.assertEqual(employers[0]['id'], "1001")
        self.assertEqual(employers[1]['name'], "Employer 2")

    @patch('requests.get')
    def test_get_employer_info_empty(self, mock_get):
        mock_response = {"items": []}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        api = FindEmployerFromHHApi()
        employers = api.get_employer_info(2)

        self.assertEqual(len(employers), 0)

    @patch('requests.get')
    def test_get_employer_info_error(self, mock_get):
        mock_get.return_value.status_code = 404

        api = FindEmployerFromHHApi()
        employers = api.get_employer_info(2)

        self.assertEqual(len(employers), 0)


if __name__ == '__main__':
    unittest.main()
