import sys
sys.path.append('..')
from FaultLocalization.Line import Line


class DataReader:

    def file_len(self,fname):
        lines = []
        testCode = []
        # fname = "D:\docu\KL\Data\mid.py"
        with open(fname) as f:
            for i, l in enumerate(f):
                line = Line(0.0, 0, l, i + 1, 0)
                testCode.append(l)
                lines.append(line)
        return i + 1, lines


    def getContextFile(self):
        fname = "D:\docu\KL\Data\mid.py"
        with open(fname) as f :
            content = f.read()
        return content
    def getContextFileWithPath(self, path):
        contents = ""
        with open(path) as f:
            for line in f.readlines():
                contents += line
        return contents
    def writeToFile(self,fname,context):
        # ContextListPop = self.getContextFileWithPath("D:\docu\KL\Variant\listPop")
        # ListPop = ContextListPop.split('\n')
        # # print(listPop)
        # for path in ListPop:
        #     variantPath = "D:\docu\KL\Variant\\"+ path
        #     f = open(variantPath,"w+")
        #     context = "abc"
        #     f.write(context)
        #     f.close()
        #     print(variantPath)
        
        f = open(fname, "w+")
        f.write(context)
        f.close()
if __name__ == '__main__':
    dR = DataReader()
    length = dR.file_len("D:\docu\KL\Variant\Pop4.py")
    print(length)
    # print(dR.getContextFile())
