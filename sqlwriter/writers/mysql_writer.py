from sqlwriter.writers.base_writer import BaseWriter


class MySQLWriter(BaseWriter):
    def __init__(self, *args, **kwargs):
        super(MySQLWriter, self).__init__(*args, **kwargs)

    @property
    def description(self):
        self.curs.execute('SELECT %s FROM %s LIMIT 1' % (','.join(self.cols), self.db_table))
        return self.curs.description

    def _make_fields(self):
        import MySQLdb
        pass
