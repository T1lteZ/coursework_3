import psycopg2
import logging


class DBManager:
    def __init__(self, db_params):
        self.db_params = db_params

    def _connect(self):
        """Создает подключение к базе данных."""
        try:
            return psycopg2.connect(**self.db_params)
        except Exception as e:
            logging.error(f"Ошибка подключения к базе данных: {e}")
            raise

    def get_companies_and_vacancies_count(self):
        """Получает список компаний и количество вакансий у каждой компании."""
        query = """
        SELECT c.name, COUNT(v.id) AS vacancy_count
        FROM companies c
        LEFT JOIN vacancies v ON c.id = v.company_id
        GROUP BY c.name;
        """
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Ошибка выполнения запроса get_companies_and_vacancies_count: {e}")
            return []

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием компании, названия вакансии, зарплаты и ссылки на вакансию."""
        query = """
        SELECT c.name, v.title, v.salary_min, v.salary_max, v.salary_currency, v.url
        FROM vacancies v
        JOIN companies c ON v.company_id = c.id;
        """
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Ошибка выполнения запроса get_all_vacancies: {e}")
            return []

    def get_avg_salary(self):
        """Получает среднюю зарплату по всем вакансиям."""
        query = """
        SELECT AVG((salary_min + salary_max) / 2.0) AS avg_salary
        FROM vacancies;
        """
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchone()
                    return result[0] if result else 0
        except Exception as e:
            logging.error(f"Ошибка выполнения запроса get_avg_salary: {e}")
            return 0

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        query = """
        SELECT c.name, v.title, v.salary_min, v.salary_max, v.salary_currency, v.url
        FROM vacancies v
        JOIN companies c ON v.company_id = c.id
        WHERE (v.salary_min + v.salary_max) / 2.0 > %s;
        """
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (avg_salary,))
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Ошибка выполнения запроса get_vacancies_with_higher_salary: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        query = """
        SELECT c.name, v.title, v.salary_min, v.salary_max, v.salary_currency, v.url
        FROM vacancies v
        JOIN companies c ON v.company_id = c.id
        WHERE v.title ILIKE %s;
        """
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (f'%{keyword}%',))
                    return cursor.fetchall()
        except Exception as e:
            logging.error(f"Ошибка выполнения запроса get_vacancies_with_keyword: {e}")
            return []
