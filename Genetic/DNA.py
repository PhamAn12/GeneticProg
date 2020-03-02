class DNA:
    def __init__(self, context="", fitnessPoint = 0, weightPath = {}):
        self.context = context
        self.fitnessPoint = fitnessPoint
        self.weightPath = weightPath
    def setScore(self, context):
        self.context = context
    def setFitnessPoint(self,fitnessPoint):
        self.fitnessPoint = fitnessPoint
    def setWeightPath(self,weightPath):
        self.weightPath = weightPath
