class Flag:
    def __init__(self, flag=1,failed = 0,passed = 0):
        self.flag = flag
        self.failed = failed
        self.passed = passed
    def setRank(self, value):
        self.flag = value
    def getRank(self):
        return self.flag
    def setFailed(self,value):
        self.failed = value
    def setPassed(self,value):
        self.passed = value