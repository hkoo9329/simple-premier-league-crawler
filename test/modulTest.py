from datetime import datetime
from dateutil import rrule
class Test:
    def __init__(self):
        print("update")

    def test(self, year, month):
        for y in year:
            for m in month:
                print(str(y)+" "+str(m))


if __name__ == '__main__':
    month_1 = 8
    month_2 = 5
    dt1=datetime.strptime("2019-08-10 10:00","%Y-%m-%d %H:%M")
    dt2=datetime.strptime("2020-05-13 10:00","%Y-%m-%d %H:%M")
    diff_month = list(rrule.rrule(rrule.MONTHLY, dtstart=datetime.date(dt1), until=datetime.date(dt2)))



    for i in range(month_1-1,month_1+len(diff_month)-1):
        print(i%12+1)