import pandas as pd

from sqlwriter.utils.utils import chunks


class BaseWriter(object):
    def __init__(self,
                 conn,
                 database,
                 table_name,
                 cols,
                 write_limit=200,
                 truncate=False):
        self.conn = conn
        self.curs = conn.cursor()
        self.database = database
        self.table_name = table_name
        self.cols = cols
        self.write_limit = write_limit
        self.truncate = truncate

        self.insert_part = 'INSERT INTO {} ('.format(self.db_table) + ','.join(cols) + ') VALUES '
        self.fields = self._make_fields()

    @property
    def flavor(self):
        flavor_map = {
            'MySQLdb': 'mysql',
            'psycopg2': 'postgres',
            'cx_Oracle': 'oracle',
            'pymssql': 'mssql'
        }
        module = self.conn.__class__.__module__
        if '.' in module:
            module = module.split('.')[0]
        return flavor_map[module]

    @property
    def db_table(self):
        return '.'.join([self.database, self.table_name])

    @property
    def description(self):
        raise NotImplementedError()

    def _make_fields(self):
        raise NotImplementedError()

    def _mogrify(self, row):
        """String formats data based on fields to be able to multi-insert into
        MySQL

        Parameters
        ---------
        row : array-like
            An array of data to be written to the columns in the target table

        Returns
        -------
        string:
            row formatted as string tuple for easy mysql writing
        """
        if isinstance(row, tuple):
            row = list(row)  # needs to be mutable
        for idx in self.fields['string']:
            try:
                row[idx] = "'{}'".format(str(row[idx]).replace("'", "")) if row[idx] else 'NULL'
            except UnicodeEncodeError:
                row[idx] = "'{}'".format(unidecode(row[idx])) if row[idx] else 'NULL'
        for idx in self.fields['datetime']:
            try:
                row[idx] = row[idx].strftime("'%Y-%m-%d %H:%M:%S'") if row[idx] else 'NULL'
            except AttributeError:
                row[idx] = parser.parse(row[idx])
                row[idx] = row[idx].strftime("'%Y-%m-%d %H:%M:%S'")
            except:
                row[idx] = 'NULL'
        for idx in self.fields['date']:
            row[idx] = "'{}'".format(row[idx]) if row[idx] else 'NULL'
            # row[idx] = row[idx].strftime("'%Y-%m-%d'") if row[idx] else 'NULL'
        for idx in self.fields['numeric']:
            if row[idx] == '':
                row[idx] = 'NULL'
            else:
                row[idx] = str(row[idx])
        for idx in self.fields['other']:
            row[idx] = str(row[idx]) if row[idx] else 'NULL'
        return '(%s)' % ','.join(row)

    def _truncate(self):
        # NOTE: I'm pretty sure this syntax is universal
        if self.truncate:
            self.curs.execute('TRUNCATE TABLE {}'.format(self.db_table))
            self.conn.commit()

    def write(self, rows):
        """Truncates table, formats strings in data and multi-inserts into MySQL

        Parameters
        ----------
        rows: array-like
            An array of arrays of data to be written to the target table
        """
        if isinstance(rows, pd.DataFrame):
            rows = rows.values

        self._truncate()
        if len(rows) == 0:
            return
        queries = chunks(rows, self.write_limit)
        for query in queries:
            query = [self._mogrify(x) for x in query]

            self.curs.execute(self.insert_part + ','.join(query))
            self.conn.commit()

    def close(self):
        self.curs.close()
        self.conn.close()
