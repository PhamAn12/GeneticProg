import collections
import os
import sys

sys.path.append('..')
from FaultLocalization.DataReader import DataReader
from FaultLocalization.TestCaseReader import ReadFile
from Data.mid import mid

global testToLines
testToLines = {}
lineToTest = {}


# current = []
def getWeightPath(fname):
    global weightPathMap
    tracer = Tracer()
    weightPathMap = {}
    testReader = ReadFile()
    resultsMap, testCaseResuts, tests, totalPassed, totalFailed = testReader.importResultsFile()
    # testToLinesMap = tracer.getTestToLine(fname)
    for key in testToLines.keys():
        if resultsMap[key] == True:
            for line in testToLines[key]:
                weightPathMap[line] = 0
        elif resultsMap[key] == False:
            for line in testToLines[key]:
                if line in weightPathMap:
                    weightPathMap[line] = 0.5
                else:
                    weightPathMap[line] = 1
    print(weightPathMap)
    return weightPathMap


class Tracer:
    def traceit(self, frame, event, arg):

        if event == "line":
            lineno = frame.f_lineno
            # filename = frame.f_globals["__file__"]
            # print(current)

            testToLines[current].append(str(lineno))
            if lineno in lineToTest.keys():
                lineToTest[lineno].append(current)
            else:
                lineToTest[lineno] = [current]
        return self.traceit

    def getLineToTest(self, fname):
        global current
        global results
        global totalPassed
        global totalFailed
        global numOfLine
        global arrLines
        weightPathMap = {}
        dataReader = DataReader()
        testReader = ReadFile()
        results, testCaseResuts, tests, totalPassed, totalFailed = testReader.importResultsFile()
        dataProg = dataReader.file_len(fname)
        numOfLine, arrLines = dataProg
        funName = os.path.splitext('mid.py')[0]
        # print(funName)
        # print(len(tests))
        for i in range(len(tests)):
            current = tests[i]
            testToLines[tests[i]] = []
            tracer = Tracer()
            sys.settrace(tracer.traceit)
            exec('%s(*(tests[i]))' % funName)

        for i in range(1, numOfLine):
            if i not in lineToTest.keys():
                lineToTest[i] = []
        # print(tests)
        # print(results)
        # print(lineToTest)
        # print(testToLines)
        for key in testToLines.keys():
            if results[key] == True:
                for line in testToLines[key]:
                    weightPathMap[line] = 0
            elif results[key] == False:
                for line in testToLines[key]:
                    if line in weightPathMap:
                        weightPathMap[line] = 0.5
                    else:
                        weightPathMap[line] = 1
        print(weightPathMap)
        return weightPathMap, lineToTest

    def scores(self, line, lineToTestDict):

        failed = 0
        passed = 0
        cases = lineToTestDict[line]
        # print(cases)
        for l in cases:
            if results[l]:
                passed += 1
            else:
                failed += 1
        suspiciousness = (failed / totalFailed) / ((passed / totalPassed) + (failed / totalFailed))

        return round(suspiciousness, 3)

    def rank(self, lineToTest):
        Ranks = {}
        count = 0
        rev = reversed(collections.OrderedDict(sorted(lineToTest.items())))
        for i in rev:
            count += len(lineToTest[i])
            for j in lineToTest[i]:
                Ranks[j] = count
        return Ranks

    def getLineInfor(self, fname):
        tracer = Tracer()
        weightPathMap, dictLtoT = self.getLineToTest(fname)
        suspiciousness = {}
        scoreList = []
        for k in list(dictLtoT):
            try:
                score = tracer.scores(k, dictLtoT)
                scoreList.append(score)
            except:
                score = 0.0
                scoreList.append(score)
            finally:
                if score in suspiciousness.keys():
                    suspiciousness[score].append(k)
                else:
                    suspiciousness[score] = [k]
        # print(scoreList)
        ranked = tracer.rank(suspiciousness)
        # print(suspiciousness)
        # print(ranked)
        print(len(arrLines))
        for i in range(len(arrLines)):
            try:
                arrLines[i].setScore(scoreList[i])
                arrLines[i].setRank(ranked[i + 1])
                if str(i) in weightPathMap.keys():
                    arrLines[i].setWeight(weightPathMap[str(i)])
            except IndexError:
                continue
        return arrLines


if __name__ == '__main__':
    tracer = Tracer()
    arrr = tracer.getLineInfor("D:\docu\KL\Data\mid.py")
    for line in range(len(arrr)):
        print(arrr[line].weight)
    # getWeightPath("D:\docu\KL\Data\mid.py")
#     print(arrr[1].text.rsplit())
# dictLtoT = tracer.getLineToTest()
# print(dictLtoT)
# suspiciousness = {}
# scoreList = []
# for k in list(dictLtoT):
#     try:
#         score = tracer.scores(k,dictLtoT)
#         scoreList.append(score)
#     except:
#          score = 0.0
#          scoreList.append(score)
#     finally:
#         if score in suspiciousness.keys():
#             suspiciousness[score].append(k)
#         else:
#             suspiciousness[score] = [k]
# print(scoreList)
# ranked = tracer.rank(suspiciousness)
# print(suspiciousness)
# print(ranked)
