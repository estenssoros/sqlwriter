import unittest

import MySQLdb
import psycopg2
from utils import get_config


class TestDBConnections(unittest.TestCase):
    def setUp(self):
        self.cfg = get_config('db_creds')
        self.mysql_creds = self.cfg['mysql']
        self.postgres_creds = self.cfg['postgres']

    def test_mysql_can_connect(self):
        try:
            conn = MySQLdb.connect(**self.mysql_creds)
            self.assertTrue(True)
            conn.close()
        except Exception as e:
            print(e)
            self.assertTrue(False)

    def test_postgres_can_connect(self):
        try:
            conn = psycopg2.connect(**self.postgres_creds)
            self.assertTrue(True)
            conn.close()
        except Exception as e:
            print(e)
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
