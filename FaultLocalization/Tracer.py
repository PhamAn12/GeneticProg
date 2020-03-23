import collections
import os
import sys

sys.path.append('..')
from FaultLocalization.DataReader import DataReader
from FaultLocalization.TestCaseReader import ReadFile

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
    # print(weightPathMap)
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

    def getLineToTest(self, fname,funName,x):
        exec(x)
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

        # funName = os.path.splitext('mid5.py')[0]
        # print(funName)
        # print(len(tests))
        for i in range(1, numOfLine):
            if i not in lineToTest.keys():
                lineToTest[i] = []
        for i in list(lineToTest):
            lineToTest[i] = []
        for i in list(testToLines):
            testToLines[i] = []
        for i in range(len(tests)):
            current = tests[i]
            testToLines[tests[i]] = []
            tracer = Tracer()
            sys.settrace(tracer.traceit)

            try:
                exec('%s(*(tests[i]))' % funName)
            except:
                print("something wrong")

        # print(numOfLine)
        # for i in range(1, numOfLine):
        #     if i not in lineToTest.keys():
        #         lineToTest[i] = []
        # print(tests)
        # print(results)
        # print(lineToTest)
        # print(testToLines)

        # for key in testToLines.keys():
        #     if results[key] == True:
        #         for line in testToLines[key]:
        #             weightPathMap[line] = 0
        #     elif results[key] == False:
        #         for line in testToLines[key]:
        #             if line in weightPathMap:
        #                 weightPathMap[line] = 0.5
        #             else:
        #                 weightPathMap[line] = 1
        # print(results)
        firstLineToTestpairs = {k: lineToTest[k] for k in list(lineToTest)[:numOfLine]}
        firstTestToLinespairs = {}
        for i in range(len(tests)):
           firstTestToLinespairs[tests[i]] = []
        for key,val in firstLineToTestpairs.items():
            for r in results.keys():
                if results[r] == False and r in val:
                    weightPathMap[key] = 1
                elif results[r] == True and r in val:
                    weightPathMap[key] = 0
        for key,val in firstLineToTestpairs.items():
            for r in results.keys():
                if results[r] == True and r in val and weightPathMap[key] == 1:
                    weightPathMap[key] = 0.5
        return weightPathMap, firstLineToTestpairs

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

    def getLineInfor(self, fname,funName,x):
        tracer = Tracer()
        weightPathMap, dictLtoT = self.getLineToTest(fname,funName,x)
        # print(weightPathMap)

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
        # print(len(arrLines))
        for i in range(len(arrLines)):
            try:
                arrLines[i].setScore(scoreList[i])
                #arrLines[i].setRank(ranked[i])
                if i in weightPathMap.keys():
                    arrLines[i].setWeight(weightPathMap[i])
            except IndexError:
                continue
        #return arrLines
        return weightPathMap,arrLines


if __name__ == '__main__':
    tracer = Tracer()
    # funName5 = os.path.splitext('mid5.py')[0]
    # funName4 = os.path.splitext('mid4.py')[0]
    # funName3 = os.path.splitext('mid3.py')[0]
    # funName2 = os.path.splitext('mid2.py')[0]
    # funName1 = os.path.splitext('mid1.py')[0]

    x = "from Variant.Pop1 import mid"
    # y = "from Variant.Pop5 import mid"
    # exec(y)
    tracer.getLineInfor("D:\docu\KL\Variant\Pop1.py","mid",x)
    # tracer.getLineInfor("D:\docu\KL\Variant\Pop4.py", funName4)
    # tracer.getLineInfor("D:\docu\KL\Variant\Pop3.py", funName3)
    # tracer.getLineInfor("D:\docu\KL\Variant\Pop2.py", funName2)
    # tracer.getLineInfor("D:\docu\KL\Variant\Pop1.py", funName1)
    # tracer = Tracer()
    # # tracer.getLineToTest("D:\docu\KL\Data\mid.py")
    # # print(testToLines)
    # funName5 = os.path.splitext('mid5.py')[0]
    # funName4 = os.path.splitext('mid4.py')[0]
    # tracer.getLineToTest("D:\docu\KL\Variant\Pop5.py",funName5)
    #
    # tracer.getLineToTest("D:\docu\KL\Variant\Pop4.py",funName4)
    # # print(testToLines)
    # # sys.settrace(tracer.traceCode)
    # # funName = os.path.splitext('mid.py')[0]
    # # exec('%s(*(2,3))' % funName)

