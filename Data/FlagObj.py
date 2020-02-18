class Flag:
    def __init__(self, flag=1):
        self.flag = flag
    def setRank(self, value):
        self.flag = value
    def getRank(self):
        return self.flag