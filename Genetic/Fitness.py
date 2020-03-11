import sys
import runpy
import ast
import astor
import importlib.util
sys.path.append('..')
from FaultLocalization.Tracer import Tracer
from FaultLocalization.TestCaseReader import ReadFile
from FaultLocalization.DataReader import DataReader
from AstTree.AstHelper import AstHelper
from Data.mid import mid

class Fitness:
    def FitnessFunction(self,funName):
        global a
        fitnessPoint = 0.0
        WPRate = 0.2
        WFRate = 0.8
        countTestPass = 0
        countTestFail = 0
        currentResult = []
        dT = DataReader()
        testReader = ReadFile()
        ctx = dT.getContextFileWithPath("D:\\docu\\KL\\Data\\unitTest1.py")
        results, testCaseResuts, tests, totalPassed, totalFailed = testReader.importResultsFile()
        TestCaseResult,resultsTestCaseMap = testReader.ImportResultTestCase()
        # print(TestCaseResult)
        # print(resultsTestCaseMap)
        # print(results)
        # print(testCaseResuts)
        # print(tests)
        for i in range(len(tests)):
            print(tests[i])
            try:
                exec('global a; a = %s(*(tests[i]))' % funName)
            except:
                print("something wrong")
            currentResult.append(a)

        for i in range(len(currentResult)):
            if currentResult[i] == list(resultsTestCaseMap.keys())[i][0]:
                if resultsTestCaseMap[list(resultsTestCaseMap.keys())[i][0], list(resultsTestCaseMap.keys())[i][1]] == True:
                    countTestPass = countTestPass + 1
                elif resultsTestCaseMap[list(resultsTestCaseMap.keys())[i][0], list(resultsTestCaseMap.keys())[i][1]] == False:
                    countTestFail = countTestFail + 1
        print(countTestPass)
        print(countTestFail)
        fitnessPoint = WPRate * countTestPass + WFRate * countTestFail
        # for res in currentResult:
        #     if res in resultsTestCaseMap.keys()[1]:
        #         print(res)
        return fitnessPoint
if __name__ == '__main__':
    f = Fitness()
    ctxx = f.FitnessFunction("mid")
    print(ctxx)
    # dT = DataReader()
    # ctx = dT.getContextFileWithPath("D:\\docu\\KL\\Data\\unitTest1.py")
    # runpy.run_path("D:\\docu\\KL\\Data\\unitTest1.py")
    # print(ctx)
    # exec("a = %s(2,3)" %"mid")
    # print(a)

