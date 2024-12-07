import unittest
from unittest.mock import patch, MagicMock

from src.DBCreate_module import save_data_to_db


class TestDatabaseFunctions(unittest.TestCase):
    @patch('psycopg2.connect')
    def test_save_data_to_db_empty_data(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        data = []
        database_name = "test_db"
        params = {"user": "test_user", "password": "test_password", "host": "localhost", "port": "5432"}

        save_data_to_db(data, database_name, params)

        mock_conn.cursor.return_value.execute.assert_not_called()


if __name__ == '__main__':
    unittest.main()
