class Line:
    def __init__(self, score=0.0, rank=0, text="", lineNo=0,weight = 0):
        self.score = score
        self.rank = rank
        self.text = text
        self.lineNo = lineNo
        self.weight = weight

    def setScore(self, score):
        self.score = score

    def setRank(self, rank):
        self.rank = rank

    def setText(self, text):
        self.text = text

    def setLineNo(self, lineNo):
        self.lineNo = lineNo

    def setWeight(self, weight):
        self.weight = weight

    def __gt__(self, line2):
        return self.rank > line2.rank