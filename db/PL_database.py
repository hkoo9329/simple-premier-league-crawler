import pymysql
import bz2
class Database():
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='hkoo',
                                  password='hkoo',
                                  db='pl_match')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row
    def commit(self):
        self.db.commit()
    def close(self):
        self.db.close()

