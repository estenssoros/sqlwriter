# -*- coding: utf-8 -*-

import re
import pandas as pd

from .utils import detect_data_type, get_config


def binary_search_for_error(insert_part, queries, server):
    """Attempt to find errors in sql query using binary search method

    Parameters
    ----------
    insert_part : string
        ''INSERT INTO <table> (<columns>) VALUES''
    queries : list of strings
        ['(<values>)', '(<values>)', '(<values>)', '(<values>)', ...]
    server : string

    Returns
    -------
    insert_value : string
    insert_column : string
    """

    if not insert_part.endswith(' '):
        insert_part += ' '

    for i in range(len(queries)):
        if queries[i].endswith(','):
            queries[i] = queries[i][:-1]

    curs, conn = connect_db(server)

    try:
        curs.execute(insert_part + ','.join(queries))
        conn.rollback()
        raise Exception('no error in query')
    except:
        pass

    length = None
    while len(queries) > 1:
        if len(queries) == length:
            raise Exception('exiting to escape infinite loop')

        length = len(queries)
        index = len(queries) / 2

        try:
            curs.execute(insert_part + ','.join(queries[:index]))
            conn.rollback()
        except:
            queries = queries[:index]
            continue

        try:
            curs.execute(insert_part + ','.join(queries[index:]))
            conn.rollback()
        except:
            queries = queries[index:]
            continue

    insert_columns = re.findall(r'.+ \((.+)\).+', insert_part)[0]
    insert_values = re.findall(r'\((.+)\)', queries[0])[0].split(',')
    insert_string = insert_part.replace(insert_columns, '{}')
    insert_columns = insert_columns.split(',')

    length = None
    while len(insert_values) > 1:
        if len(insert_values) == length:
            raise Exception('exiting to escape infinite loop')

        length = len(insert_values)
        index = len(insert_values) / 2

        try:
            sql = insert_string.format(','.join(insert_columns[:index])) + '(%s)' % ','.join(insert_values[:index])
            curs.execute(sql)
            conn.rollback()
        except:
            insert_columns = insert_columns[:index]
            insert_values = insert_values[:index]
            continue

        try:
            sql = insert_string.format(','.join(insert_columns[index:])) + '(%s)' % ','.join(insert_values[index:])
            curs.execute(sql)
            conn.rollback()
        except:
            insert_columns = insert_columns[index:]
            insert_values = insert_values[index:]
            continue
    try:
        curs.execute(sql)
        conn.rollback()
    except:
        print('Error found:\n{}'.format(sql))
    return insert_columns[0], insert_values[0]



def create_schema(df, flavor='postgres', output='strings'):
    """
    Parameters
    ----------
    df : pandas dataframe
    flavor : the output schema data types
    """
    schema_heirarchy = ('string', 'text', 'float', 'bigint', 'int', 'date', 'datetime')
    flavor_dict = {
        'postgres': ('varchar', 'text', 'double precision', 'bigint', 'int', 'date', 'timestamp'),
        'microsoft_sql': ('nvarchar', 'text', 'float', 'int', 'int', 'date', 'datetime'),
        'elasticsearch': ('string', 'string', 'float', 'long', 'integer', 'date', 'date')
    }
    flavor_dict = {k: dict(zip(schema_heirarchy, v)) for k, v in flavor_dict.iteritems()}
    df = df.copy()
    df = df.fillna('')
    for col in df.columns:
        df[col] = df[col].astype(str)
    data_types = []
    for col in df.columns:
        sub = df[col][df[col] != '']
        if sub.empty:
            data_types.append([col, 'string'])
        sub = set([detect_data_type(x) for x in set(sub)])
        if len(sub) == 1:
            data_types.append([col, sub.pop()])
        else:
            vc_lst = list(sub)
            for typ in schema_heirarchy:
                if typ in vc_lst:
                    data_types.append([col, typ])
                    break
    for row in data_types:
        if row[1] == 'string':
            sub = df[[row[0]]][df[row[0]] != '']
            if len(sub) == 0:
                row.append(1)
                continue
            max_len = sub.apply(lambda x: len(x[row[0]]), axis=1).max()
            if max_len > 4000:
                row[1] = 'text'
                row.append(False)
            else:
                row.append(int(max_len * 1.5))
        else:
            row.append(False)
        if row[1] == 'int':
            sub = df[row[0]][df[row[0]] != '']
            try:
                sub = sub.astype(int)
            except OverflowError:
                row[1] = 'bigint'

    new = pd.DataFrame(data=data_types, columns=['col', 'type', 'constraint'])
    new['type'] = new.apply(lambda x: flavor_dict[flavor][x['type']], axis=1)
    if output == 'strings':
        create = []
        for i, r in new.iterrows():
            if r['constraint']:
                create.append('{col} {type}({constraint}) DEFAULT NULL'.format(**r))
            else:
                create.append('{col} {type} DEFAULT NULL'.format(**r))
        return create
    elif output == 'df':
        return new


def connect_db(server, conn_only=False):
    """Connects to a sepcified server given credentials in config.yaml

    Parameters
    ----------
    server : string
    """
    db_conn = get_config('db_creds')[server]

    flavor = db_conn.pop('flavor')

    if flavor == 'microsoft_sql':
        import pymssql as connector
    elif flavor == 'postgres':
        import psycopg2 as connector
    elif flavor == 'oracle':
        import cx_Oracle as connector
    else:
        raise KeyError('{} not supported'.format(flavor))

    conn = connector.connect(**db_conn)
    if conn_only:
        return conn

    curs = conn.cursor()
    return curs, conn

def main():
    pass


if __name__ == '__main__':
    main()
