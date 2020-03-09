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
from Variant.Pop2 import mid

class Fitness:
    def FitnessFunction(self,funName):
        global a
        currentResult = []
        dT = DataReader()
        testReader = ReadFile()
        ctx = dT.getContextFileWithPath("D:\\docu\\KL\\Data\\unitTest1.py")
        results, testCaseResuts, tests, totalPassed, totalFailed = testReader.importResultsFile()
        print(results)
        print(testCaseResuts)
        print(tests)

        # exec("global a ;a = %s(2,3)" % funName)
        # print(a)
        for i in range(len(tests)):
            print(tests[i])
            try:
                exec('global a; a = %s(*(tests[i]))' % funName)
            except:
                print("something wrong")
            currentResult.append(a)

        return currentResult
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

