import sys
import ast
import astor
sys.path.append('..')
from FaultLocalization.Tracer import Tracer
from FaultLocalization.DataReader import DataReader
from AstTree.AstHelper import AstHelper
class Fitness:
    def FitnessFunction(self):
        dT = DataReader()
        ctx = dT.getContextFileWithPath("D:\\docu\\KL\\Data\\unitTest1.py")
        print(ctx)
        exec (ctx)
        # exec(ctx)

if __name__ == '__main__':
    # f = Fitness()
    # ctxx = f.FitnessFunction()
    dT = DataReader()
    ctx = dT.getContextFileWithPath("D:\\docu\\KL\\Data\\unitTest1.py")
    print(ctx)
    exec(ctx)