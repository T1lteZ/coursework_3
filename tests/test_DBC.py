import unittest
from unittest.mock import patch, MagicMock
from src.DBCreate_module import DBConnection


class TestDBConnection(unittest.TestCase):
    @patch('psycopg2.connect')
    def test_connect_to_db_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        db_connection = DBConnection()
        conn = db_connection._connect_to_db()

        mock_connect.assert_called_once()
        self.assertEqual(conn, mock_conn)

    @patch('psycopg2.connect')
    def test_connect_to_db_error(self, mock_connect):
        mock_connect.side_effect = Exception("Ошибка подключения")

        db_connection = DBConnection()

        with self.assertRaises(Exception):
            db_connection._connect_to_db()

    @patch.object(DBConnection, '_execute_query')
    def test_create_db_success(self, mock_execute_query):
        db_connection = DBConnection()

        mock_execute_query.return_value = None

        db_connection.create_db()

        mock_execute_query.assert_any_call("DROP DATABASE IF EXISTS employers_vacancy;")
        mock_execute_query.assert_any_call("CREATE DATABASE employers_vacancy;")
        print("Метод create_db выполнен успешно.")

    @patch.object(DBConnection, '_execute_query')
    def test_db_creating_employers(self, mock_execute_query):
        db_connection = DBConnection()

        mock_execute_query.return_value = None

        db_connection.db_creating_employers()

        mock_execute_query.assert_called_with("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id VARCHAR PRIMARY KEY,
                company_name VARCHAR(50) UNIQUE,
                vacancies_count INT
            );
        """)
