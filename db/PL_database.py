import pymysql

class Database():
    def __init__(self):
        self.db = pymysql.connect(host='pl-match-db.cfohe632lhjx.ap-northeast-2.rds.amazonaws.com',
                                  user='hkoo',
                                  password='ehfrhfo7',
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
