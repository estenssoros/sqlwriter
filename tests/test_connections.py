import subprocess as sp
import unittest

from sqlwriter import SQLWriter

from utils import DBRouter, connect_db, create_test_dataframe

p = sp.Popen('docker ps', shell=True, stdout=sp.PIPE)
p.wait()
msg, _ = p.communicate()

SKIP_MYSQL = True
SKIP_POSTGRES = True

if 'sqlwriter_postgres_1' in msg:
    SKIP_POSTGRES = False
if 'sqlwriter_mysql_1' in msg:
    SKIP_MYSQL = False


class TestDBConnections(unittest.TestCase):

    @unittest.skipIf(SKIP_MYSQL, 'Could not find running MySQL docker container')
    def test_mysql_can_connect(self):
        try:
            curs, conn = connect_db('mysql')
            self.assertTrue(True)
            curs.close()
            conn.close()
        except Exception as e:
            print(e)
            self.assertTrue(False)

    @unittest.skipIf(SKIP_POSTGRES, 'Could not find running Postgres docker container')
    def test_postgres_can_connect(self):
        try:
            curs, conn = connect_db('postgres')
            self.assertTrue(True)
            curs.close()
            conn.close()
        except Exception as e:
            print(e)
            self.assertTrue(False)


class TestCreatePostgres(unittest.TestCase):
    def setUp(self):
        self.db = DBRouter('postgres')

    def test_create_table(self):
        curs, conn = self.db['postgres']
        curs.execute('DROP TABLE IF EXISTS test')
        conn.commit()
        sql = '''
        CREATE TABLE test (
            id SERIAL
            , astring VARCHAR(50)
            , aninteger INTEGER
            , afloat FLOAT
            , adate DATE
            , adatetime TIMESTAMP WITHOUT TIME ZONE
        )
        '''
        curs.execute(sql)
        conn.commit()

    def tearDown(self):
        self.db.close()


class TestCreateMySQL(unittest.TestCase):
    def setUp(self):
        self.db = DBRouter('mysql')

    def test_create_dbmysql(self):
        curs, conn = self.db['mysql']
        curs.execute('CREATE DATABASE IF NOT EXISTS sqlwriter')
        conn.commit()

        curs.execute('DROP TABLE IF EXISTS sqlwriter.test')
        conn.commit()
        sql = '''
        CREATE TABLE test (
            id SERIAL
            , astring VARCHAR(50)
            , aninteger INTEGER
            , afloat FLOAT
            , adate DATE
            , adatetime DATETIME
        )
        '''
        curs.execute(sql)
        conn.commit()

    def tearDown(self):
        self.db.close()


class TestInsertMySQL(unittest.TestCase):
    def setUp(self):
        self.df = create_test_dataframe()
        self.db = DBRouter('mysql')

    def test_insert_mysql(self):
        curs, conn = self.db['mysql']
        writer = SQLWriter(conn, 'sqlwriter', 'test', self.df.columns)
        writer.write(self.df.values)
        writer.close()


if __name__ == '__main__':
    unittest.main()
