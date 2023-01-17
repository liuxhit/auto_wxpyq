# coding; utf-8
import logging
import sqlite3
from sqlite3 import Connection
from contextlib import contextmanager
import os


# TODO: orm or impl this
class SqliteStore:
    logger = logging.getLogger(__name__)

    def __init__(self, db_file='sqlite3.db'):
        self.db_file = os.path.abspath(db_file)
        self.logger.info(f'my db file: {self.db_file}')

    def setup_tbl(self):
        with self.make_conn() as conn:
            self.sql_execute(conn, sql='''CREATE TABLE input_record
                                          (id INTEGER PRIMARY KEY , 
                                           pyq_text_content varchar(1000) NOT NULL, 
                                           pyq_pic_path vchar(1000) )''')

    def sql_execute(self, conn: Connection, sql):
        c = conn.cursor()
        res = c.execute(sql)
        return res

    def sql_execute_many(self, conn: Connection, sql, data):
        c = conn.cursor()
        c.executemany(sql, data)

    @contextmanager
    def make_conn(self):
        conn = sqlite3.connect(self.db_file)
        try:
            with conn:
                yield
        except Exception as e:
            self.logger.exception(f'sql报错: {e}')
        conn.close()
