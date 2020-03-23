import sys
import ast
import random
import astor
import os
sys.path.append('..')
from FaultLocalization.Tracer import Tracer
from FaultLocalization.DataReader import DataReader
from AstTree.AstHelper import AstHelper
from Genetic.Fitness import Fitness
from Data.FlagObj import Flag

class Genetic:
    def CreatePollution(self,fname):
        PolutionArr = []
        tracer = Tracer()
        dR = DataReader()
        weightpathMap,lineArr = tracer.getLineInfor(fname,"mid","from Data.mid import mid")
        lineArrWeightPath = []
        context = dR.getContextFileWithPath(fname)
        tree = ast.parse(context)
        astHelper = AstHelper()
        node3 = astHelper.GetNodeByLineNo(3,tree)
        for i in weightpathMap:
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
        # cutpointA = self.GetCutOffPoint(fnameA,funNameA,importStringA)
        # cutpointB = self.GetCutOffPoint(fnameB,funNameB,importStringB)
        cutpointA = 5
        cutpointB = 4
        contextA = dR.getContextFileWithPath(fnameA)
        contextB = dR.getContextFileWithPath(fnameB)
        treeA = ast.parse(contextA)
        treeB = ast.parse(contextB)
        helper = AstHelper()
        nodeCutA = helper.GetNodeByLineNo(cutpointA,treeA)
        nodeCutB = helper.GetNodeByLineNo(cutpointB,treeB)
        lineNodeCutA = helper.GetFullStatementNode(nodeCutA)
        lineNodeCutB = helper.GetFullStatementNode(nodeCutB)

        # print(lineNodeCutA)
        # print(lineNodeCutB)
        indexA = contextA.find(lineNodeCutA)
        indexB = contextB.find(lineNodeCutB)
        print(indexA)
        print(contextA[:indexA])
        print(contextB[indexA:])
        # print(contextA[:indexA] + contextB[indexA:])
        # print(contextB[:indexA] + contextA[indexA:])
        # elif indexB > indexA:
        #     print(contextB[:indexA] + contextA[indexA:indexB] + contextB[indexB:])

        # print("dòng lệnh bị cắt trong A : " + str(cutpointA))
        # print("full nội dung dòng lệnh trong A : " + str(lineNodeCutA))
        # print(contextA[indexA:])
        # print(contextA[:indexA])
        # print("dòng lệnh bị cắt trong B : " + str(cutpointB))
        # print("full nội dung dòng lệnh trong B : " + str(lineNodeCutB))
        # print(contextB[indexB:])
        # print(contextB[:indexB])
        # print("Đoạn giữa : ")
        print(contextA[indexA:indexB])
        # print(indexA)
        # print(indexB)
        # if indexA <= indexB:
        #     print(contextA[indexA:indexB])
        # else:
        #     print(contextA[indexB:indexA])


        return cutpointA, cutpointB
    def CrossOverOp(self,fAname,funAname,importStringA,fBname,funBname,importStringB):
        tracer = Tracer()
        weightpathMapA,lineArrA = tracer.getLineInfor(fAname,funAname,importStringA)
        weightpathMapB, lineArrB = tracer.getLineInfor(fBname, funBname, importStringB)
        lineArrC = lineArrA # copy children C and D by parent A and B
        lineArrD = lineArrB

        for i in range(len(lineArrC)):
            print(lineArrC[i].text)
        cutoff = self.GetCutOffPoint(fAname,funAname,importStringA)
        print(cutoff)
        print(weightpathMapA[cutoff])
        for i in range(len(lineArrA)):
             if i > cutoff:
                 prob = random.random()
                 # print(prob)
                 if prob < weightpathMapA[cutoff]:
                     # print(lineArrB[i].text)
                     lineArrC[i].text = lineArrB[i].text
                     lineArrD[i].text = lineArrA[i].text
        for i in range(len(lineArrC)):
            print(lineArrC[i].text)
        for i in range(len(lineArrD)):
            print(lineArrD[i].text)
    def GetCutOffPoint(self,fname,funName,importString):
        tracer = Tracer()
        arrLineWeight,arrLineInfor = tracer.getLineInfor(fname,funName,importString)
        randomWeightPoint = random.choice(list(arrLineWeight.keys()))
        while arrLineWeight[randomWeightPoint] == 0 or randomWeightPoint == 1:
            randomWeightPoint = random.choice(list(arrLineWeight.keys()))
        print(randomWeightPoint)
        print(arrLineInfor[randomWeightPoint].text)
        return randomWeightPoint # tra ve dong trong weight path
    def GetProbLine(self,fname,funName,importString):
        tracer = Tracer()
        mapLineProp = {}
        weightpathMapA, lineArrA = tracer.getLineInfor(fname, funName, importString)
        print(weightpathMapA)
        # for i in range(len(weightpathMapA)):
        #     print(weightpathMapA[i])

if __name__ == '__main__':
    # Create pollution by mutation and write to file
    # mu = Genetic()
    # mu.WritePollutionToFile()

    pop5 = "from Variant.Pop5 import mid"
    # Create mating pool and pick up variant to crossover and mutation
    # fitnesspoint = Fitness()
    # print(fitnesspoint.FitnessFunction("mid",pop5))
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
    #     listTestResult[pop] = fitnesspoint.FitnessFunction("mid",pop) # add fitness point to list
    # for pop in popList:
    #     n = int(listTestResult[pop]*10)
    #     print(n)
    #     for i in range(n):
    #         matingPool.append(pop)
    # print(matingPool)
    # for pop in popList:
    #     a = random.choice(matingPool)
    #     b = random.choice(matingPool)
    #     linkToContextA = linkToContextMap[a]
    #     linkToContextB = linkToContextMap[b]
    #     progA = dR.getContextFileWithPath(linkToContextA)
    #     progB = dR.getContextFileWithPath(linkToContextB)
    #     print(linkToContextA)
    #     print(linkToContextB)

    mu = Genetic()
    mu.CrossOverOp("D:\docu\KL\Variant\Pop5.py","mid","from Variant.Pop5 import mid","D:\docu\KL\Variant\Pop2.py","mid","from Variant.Pop2 import mid")
    # mu.GetProbLine("D:\docu\KL\Variant\Pop2.py","mid","from Variant.Pop2 import mid")
    # tracer = Tracer()
    # weightpathMapA, lineArrA = tracer.getLineInfor("D:\docu\KL\Variant\Pop5.py","mid","from Variant.Pop5 import mid")
    # lineArrC = lineArrA
    # print("Len : " + str(len(lineArrC)))
    # print("text 8 : " + lineArrC[8].text)
    # lineArrC[8].text = "ldldld"
    # for i in range(len(lineArrC)):
    #     print(lineArrC[i].text)