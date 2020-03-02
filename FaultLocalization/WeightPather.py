import collections
import os
import sys

sys.path.append('..')
from FaultLocalization.DataReader import DataReader
from FaultLocalization.TestCaseReader import ReadFile
from Variant.Pop5 import mid5
from Variant.Pop4 import mid4
from Variant.Pop3 import mid3
from Variant.Pop1 import mid1
global testToLines
testToLines = {}
lineToTest = {}


# current = []

class Tracer:
    def traceit(self, frame, event, arg):
        if event == "line":
            lineno = frame.f_lineno

            testToLines[current].append(str(lineno))

            if lineno in lineToTest.keys():
                lineToTest[lineno].append(current)
            else:
                lineToTest[lineno] = [current]
            # print(lineno)
            # print(testToLines)
        return self.traceit


    # def getLineToTest(self, fname,funName):
    #     global current
    #     global results
    #     global totalPassed
    #     global totalFailed
    #     global numOfLine
    #     global arrLines
    #     weightPathMap = {}
    #     dataReader = DataReader()
    #     testReader = ReadFile()
    #     results, testCaseResuts, tests, totalPassed, totalFailed = testReader.importResultsFile()
    #     dataProg = dataReader.file_len(fname)
    #     numOfLine, arrLines = dataProg
    #     for i in range(1, numOfLine):
    #         if i not in lineToTest.keys():
    #             lineToTest[i] = []
    #     for i in range(len(tests)):
    #         current = tests[i]
    #         testToLines[tests[i]] = []
    #         tracer = Tracer()
    #         sys.settrace(tracer.traceit)
    #         exec('%s(*(tests[i]))' % funName)
    #
    #
    #     print(lineToTest)
    #     return weightPathMap, lineToTest

    # def getLineInfor(self, fname):
    #     tracer = Tracer()
    #     weightPathMap, dictLtoT = self.getLineToTest(fname)
    #     suspiciousness = {}
    #     scoreList = []
    #     for k in list(dictLtoT):
    #         try:
    #             score = tracer.scores(k, dictLtoT)
    #             scoreList.append(score)
    #         except:
    #             score = 0.0
    #             scoreList.append(score)
    #         finally:
    #             if score in suspiciousness.keys():
    #                 suspiciousness[score].append(k)
    #             else:
    #                 suspiciousness[score] = [k]
    #     # print(scoreList)
    #     ranked = tracer.rank(suspiciousness)
    #     # print(suspiciousness)
    #     # print(ranked)
    #     print(len(arrLines))
    #     for i in range(len(arrLines)):
    #         try:
    #             arrLines[i].setScore(scoreList[i])
    #             arrLines[i].setRank(ranked[i + 1])
    #             if str(i) in weightPathMap.keys():
    #                 arrLines[i].setWeight(weightPathMap[str(i)])
    #         except IndexError:
    #             continue
    #     return arrLines

    def getLineToTest2(self,funName,fname):
        global current
        dataReader = DataReader()
        testReader = ReadFile()
        results, testCaseResuts, tests, totalPassed, totalFailed = testReader.importResultsFile()
        dataProg = dataReader.file_len(fname)
        numOfLine, arrLines = dataProg
        # init lineToTest
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
            sys.settrace(self.traceit)
            exec('%s(*(tests[i]))' % funName)

        # print(lineToTest)
        first2pairs = {k: lineToTest[k] for k in list(lineToTest)[:15]}
        print(first2pairs)
        # print(testToLines)


if __name__ == '__main__':


    tracer = Tracer()
    funName5 = os.path.splitext('mid5.py')[0]
    funName4 = os.path.splitext('mid4.py')[0]
    funName3 = os.path.splitext('mid3.py')[0]
    funName1 = os.path.splitext('mid1.py')[0]
    tracer.getLineToTest2(funName5,"D:\docu\KL\Variant\Pop5.py")
    # #
    tracer.getLineToTest2(funName4,"D:\docu\KL\Variant\Pop4.py")

    #tracer.getLineToTest2(funName3, "D:\docu\KL\Variant\Pop3.py")
    # #
    tracer.getLineToTest2(funName1, "D:\docu\KL\Variant\Pop1.py")
    # dataReader = DataReader()
    # testReader = ReadFile()
    # results, testCaseResuts, tests, totalPassed, totalFailed = testReader.importResultsFile()
    # for i in range(len(tests)):
    #     current = tests[i]
    #     testToLines[tests[i]] = []
    #     sys.settrace(traceit)
    #     exec('%s(*(tests[i]))' % funName4)
    # for i in range(1, 15):
    #     if i not in lineToTest.keys():
    #         lineToTest[i] = []
    # print(lineToTest)
    # for i in lineToTest.keys():
    #     lineToTest[i] = []
    # for i in range(len(tests)):
    #     current = tests[i]
    #     testToLines[tests[i]] = []
    #     sys.settrace(traceit)
    #     exec('%s(*(tests[i]))' % funName5)
    # for i in range(1, 15):
    #     if i not in lineToTest.keys():
    #         lineToTest[i] = []
    # print(lineToTest)
