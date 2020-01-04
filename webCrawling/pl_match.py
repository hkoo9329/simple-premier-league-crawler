class match:
    def __init__(self, datetime, left_team, right_team, score):
        self.datetime = datetime
        self.left_team = left_team
        self.right_team = right_team
        self.score = score

    def getDatetime(self):
        return self.datetime

    def getLeftTeam(self):
        return self.left_team

    def getRightTeam(self):
        return self.right_team

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score

    def compareToEqual(self, datetime,left_team):
        if str(self.datetime) == str(datetime) and str(self.left_team) == str(left_team):
            return True
        else:
            return False