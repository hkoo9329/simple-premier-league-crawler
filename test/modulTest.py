import datetime
from db.PL_database import Database
day = [1.1, 1.2, 1.3, 1.11, 1.12, 1.13, 1.18, 1.19, 1.20, 1.22, 1.23, 1.24, 1.30]


class DatetimeFormatTest:

    def test(self):
        dt = datetime.datetime
        s = dt.strptime("2019-1-2 10:20", "%Y-%m-%d %H:%M")
        a = str(s)
        print(a)


class DB쿼리_테스트():

    def __init__(self):
        self.db = Database()

    def db에서_팀검색_테스트(self):
        team = "토트넘"
        rows=self.db.executeAll("select * from pl_match_db where left_team = '{team}' or right_team = '{team}'".format(team=team))
        print(rows)


if __name__=='__main__':
    dbTest=DB쿼리_테스트()
    dbTest.db에서_팀검색_테스트()
