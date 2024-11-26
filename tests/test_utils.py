import unittest
from unittest.mock import MagicMock
from src.utils import get_top_vacancies


class TestVacancyFunctions(unittest.TestCase):

    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.vacancy_1 = MagicMock()
        self.vacancy_1.get_vacancy_info.return_value = {
            "id": "1",
            "name": "Python Developer",
            "salary_from": 50000,
            "salary_to": 70000,
            "requirement": "Experience with Python, Django, Flask",
            "url": "http://example.com/python"
        }

        self.vacancy_2 = MagicMock()
        self.vacancy_2.get_vacancy_info.return_value = {
            "id": "2",
            "name": "Java Developer",
            "salary_from": 60000,
            "salary_to": 80000,
            "requirement": "Experience with Java, Spring, Hibernate",
            "url": "http://example.com/java"
        }

        self.vacancy_3 = MagicMock()
        self.vacancy_3.get_vacancy_info.return_value = {
            "id": "3",
            "name": "Data Scientist",
            "salary_from": 70000,
            "salary_to": 90000,
            "requirement": "Experience with Python, Data Analysis, Machine Learning",
            "url": "http://example.com/data_scientist"
        }

        self.vacancies = [self.vacancy_1, self.vacancy_2, self.vacancy_3]

    def test_get_top_vacancies(self):
        """Тестируем вывод топовых вакансий"""
        sorted_vacancies = [
            {"name": "Data Scientist", "salary_from": 70000, "salary_to": 90000, "requirement": "ML", "url": "url1"},
            {"name": "Java Developer", "salary_from": 60000, "salary_to": 80000, "requirement": "Spring",
             "url": "url2"},
            {"name": "Python Developer", "salary_from": 50000, "salary_to": 70000, "requirement": "Flask",
             "url": "url3"}
        ]

        result = get_top_vacancies(sorted_vacancies, 2)

        self.assertIn("Data Scientist", result)
        self.assertIn("Java Developer", result)
        self.assertNotIn("Python Developer", result)

