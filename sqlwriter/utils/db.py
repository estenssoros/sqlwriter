import os

from sqlwriter.configuration import get_config
from sqlwriter.exceptions import SQLWriterConfigException
from sqlwriter.configuration import SUPPORTED_DATABASES


def connect_db(flavor):
    config_file = os.path.join(os.path.dirname(__file__), 'tests', 'test_conf.yaml')
    print config_file

    try:
        creds = get_config(config_file, 'db_creds')[flavor]
    except KeyError:
        raise SQLWriterConfigException('%s not in db_creds config' % flavor)

    if flavor == 'mysql':
        import MySQLdb as connector
    elif flavor == 'postgres':
        import psycopg2 as connector
    else:
        raise SQLWriterConfigException('%s no supported' % flavor)

    conn = connector.connect(**creds)
    curs = conn.cursor()
    return conn, curs


def initdb(arg):
    for db in SUPPORTED_DATABASES:
        curs, conn = connect_db(db)
        # sql = os.path.
