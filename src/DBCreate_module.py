import os
import psycopg2
from dotenv import load_dotenv
from contextlib import closing


load_dotenv()


class DBConnection:
    """Класс для подключения к базе данных PostgreSQL"""

    def __init__(self):
        self._host = os.getenv("HOST")
        self._database = os.getenv("DATABASE")
        self._username = os.getenv("USERNAME")
        self._port = os.getenv("PORT")
        self._password = os.getenv("PASSWORD")

    def _connect_to_db(self):
        """Метод для подключения к базе данных"""
        return psycopg2.connect(
            host=self._host,
            database=self._database,
            user=self._username,
            port=self._port,
            password=self._password
        )

    def _execute_query(self, query, params=None):
        """Общий метод для выполнения SQL-запроса"""
        try:
            with closing(self._connect_to_db()) as conn, closing(conn.cursor()) as cur:
                cur.execute(query, params)
                conn.commit()
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")

    def create_db(self):
        """Метод для создания базы данных"""
        try:
            self._database = "postgres"
            execute_message_drop = "DROP DATABASE IF EXISTS employers_vacancy;"
            self._execute_query(execute_message_drop)

            execute_message_create = "CREATE DATABASE employers_vacancy;"
            self._execute_query(execute_message_create)
            print("База данных создана успешно.")
        except Exception as e:
            print(f'Ошибка при создании базы данных: {e}')

    def db_creating_employers(self):
        """Метод для создания таблицы работодателей"""
        execute_message = """
            CREATE TABLE IF NOT EXISTS employers (
                employer_id VARCHAR PRIMARY KEY,
                company_name VARCHAR(50) UNIQUE,
                vacancies_count INT
            );
        """
        self._execute_query(execute_message)

    def db_filling_columns_for_emps(self, employers_id_list: list, employers_list: list):
        """Метод для заполнения таблицы работодателей"""
        filtered_employers_list = [
            emp for emp in employers_list if emp["id"] in employers_id_list
        ]

        execute_message = """INSERT INTO employers (employer_id, company_name, vacancies_count) 
                             VALUES (%s, %s, %s) ON CONFLICT (employer_id) DO NOTHING"""
        for employer in filtered_employers_list:
            params = (
                employer.get("id"),
                employer.get("name"),
                employer.get("open_vacancies"),
            )
            self._execute_query(execute_message, params)

    def db_creating_vacancies(self):
        """Метод для создания таблицы вакансий"""
        execute_message = """
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id VARCHAR PRIMARY KEY,
                vacancy_name VARCHAR NOT NULL,
                salary_from INT,
                salary_to INT,
                requirement TEXT,
                url VARCHAR NOT NULL,
                employer_id VARCHAR,
                FOREIGN KEY (employer_id) REFERENCES employers (employer_id)
            );
        """
        self._execute_query(execute_message)

    def db_filling_vacancies(self, vacancies_list: list):
        """Метод для заполнения таблицы вакансий"""
        execute_message = """
            INSERT INTO vacancies (vacancy_id, vacancy_name, salary_from, salary_to, 
                                  requirement, url, employer_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING
        """
        for vacancy in vacancies_list:
            params = (
                vacancy.get("id"),
                vacancy.get("name"),
                vacancy.get("salary").get("from") if vacancy.get("salary") else 0,
                vacancy.get("salary").get("to") if vacancy.get("salary") else 0,
                vacancy.get("snippet").get("requirement") if vacancy.get("snippet") else '',
                vacancy.get("url"),
                vacancy.get("employer").get("id") if vacancy.get("employer") else None,
            )
            self._execute_query(execute_message, params)
