import sys
import ast
import random
import astor
import os
sys.path.append('..')
from FaultLocalization.Tracer import Tracer
from FaultLocalization.DataReader import DataReader
from AstTree.AstHelper import AstHelper
from Data.FlagObj import Flag

class Genetic:
    def CreatePollution(self,fname):
        PolutionArr = []
        tracer = Tracer()
        dR = DataReader()
        lineArr = tracer.getLineInfor(fname,"mid","from Data.mid import mid")
        lineArrWeightPath = []
        context = dR.getContextFileWithPath(fname)
        tree = ast.parse(context)
        astHelper = AstHelper()
        node3 = astHelper.GetNodeByLineNo(3,tree)
        for i in lineArr:
            if i.weight > 0:
                lineArrWeightPath.append(i)
        for line in lineArrWeightPath:
            node = astHelper.GetNodeByLineNo(line.lineNo,tree)
            newContext = astHelper.DeleteNode(context,node)
            # print(newContext)
            PolutionArr.append(newContext)
            # print(line.lineNo)
            # print(astor.to_source(node))
        return PolutionArr,lineArrWeightPath
    def WritePollutionToFile(self):

        pop_size = 6
        dR = DataReader()
        ContextListPop = dR.getContextFileWithPath("D:\docu\KL\Variant\listPop")
        ListPop = ContextListPop.split('\n')
        # print(listPop)
        ArrPop, ArrWeightPath = self.CreatePollution("D:\docu\KL\Data\mid.py")
        ArrPop = ArrPop[1:pop_size]
        dictPathPop = dict(zip(ListPop, ArrPop))
        print(list(dictPathPop.values())[0])
        for i in range(1,pop_size):
            variantPath = "D:\docu\KL\Variant\\" + list(dictPathPop.keys())[i-1]
            dR.writeToFile(variantPath,list(dictPathPop.values())[i-1])

    def FitnessFunction(self,pop):
        unitTestPath = "D:\\docu\\KL\\Data\\unitTest.py"
        dynamicTestPath = "D:\\docu\\KL\\Data\\DynamicUnitTest.py"
        stringImportLib = "import sys" + "\n" + "sys.path.append('..')" + "\n"
        context = dR.getContextFileWithPath(unitTestPath)
        pop5 = pop + "\n"
        contextDynamicTest = stringImportLib + pop5 + context
        # dR.writeToFile("D:\\docu\\KL\\Data\\DynamicUnitTest.py",contextDynamicTest)
        # print(contextDynamicTest)
        return contextDynamicTest
    def CrossOver(self,fnameA,funNameA,fnameB,funNameB,importStringA,importStringB):
        dR = DataReader()
        cutpointA = self.GetCutOffPoint(fnameA,funNameA,importStringA)
        cutpointB = self.GetCutOffPoint(fnameB,funNameB,importStringB)
        contextA = dR.getContextFileWithPath(fnameA)
        contextB = dR.getContextFileWithPath(fnameB)
        treeA = ast.parse(contextA)
        treeB = ast.parse(contextB)
        helper = AstHelper()
        nodeCutA = helper.GetNodeByLineNo(cutpointA,treeA)
        nodeCutB = helper.GetNodeByLineNo(cutpointB,treeB)
        lineNodeCutA = helper.GetFullStatementNode(nodeCutA)
        lineNodeCutB = helper.GetFullStatementNode(nodeCutB)

        print(lineNodeCutA)
        print(lineNodeCutB)

        return cutpointA, cutpointB

    def GetCutOffPoint(self,fname,funName,importString):
        tracer = Tracer()
        arrLineWeight = tracer.getLineInfor(fname,funName,importString)
        randomWeightPoint = random.choice(list(arrLineWeight.keys()))
        while arrLineWeight[randomWeightPoint] == 0:
            randomWeightPoint = random.choice(list(arrLineWeight.keys()))
        return randomWeightPoint # tra ve dong trong weight path

if __name__ == '__main__':
    # Create pollution by mutation and write to file
    # mu = Genetic()
    # mu.WritePollutionToFile()

    pop5 = "from Variant.Pop5 import mid"
    pop4 = "from Variant.Pop4 import mid"

    mu = Genetic()
    mu.CrossOver("D:\docu\KL\Variant\Pop5.py","mid","D:\docu\KL\Variant\Pop4.py","mid",pop5,pop4)

    # mu.GetCutOffPoint("D:\docu\KL\Variant\Pop4.py","mid",pop4)
    # matingPool = []
    # mu = Genetic()
    # dR = DataReader()
    # pop_size = 6
    # listTestResult = {}
    # linkToContextMap = {}
    # popList = ["from Variant.Pop5 import mid\n",
    #            "from Variant.Pop4 import mid\n",
    #            "from Variant.Pop3 import mid\n",
    #            "from Variant.Pop2 import mid\n",
    #            "from Variant.Pop1 import mid\n"
    #            ]
    # for pop in popList:
    #     linkToContextMap[pop] = "D:\docu\KL\Variant\\" + pop[13:17] +".py"
    # for pop in popList:
    #     flag = Flag(0, 0, 0)
    #     contextDynamicTest = mu.FitnessFunction(pop)
    #     exec(contextDynamicTest)
    #     print(flag.passed)
    #     listTestResult[pop] = flag.passed/pop_size
    # for pop in popList:
    #     n = int(listTestResult[pop]*10)
    #     # print(n)
    #     for i in range(n):
    #         matingPool.append(pop)
    # for pop in popList:
    #     a = random.choice(matingPool)
    #     b = random.choice(matingPool)
    #     linkToContextA = linkToContextMap[a]
    #     linkToContextB = linkToContextMap[b]
    #     progA = dR.getContextFileWithPath(linkToContextA)
    #     progB = dR.getContextFileWithPath(linkToContextB)
    #     print(linkToContextA)
    #     print(linkToContextB)