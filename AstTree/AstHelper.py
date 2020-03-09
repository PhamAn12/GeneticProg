import ast
import re
import sys
import libcst as cst
import array as arr
import pycfg
import astor
sys.path.append('..')
from FaultLocalization.Tracer import Tracer

sys.path.append('..')
from FaultLocalization.DataReader import DataReader
from Data.FlagObj import Flag
from Data.unitTest import GetResult
class AstHelper():
    def GetNodeByLineNo(self,lineNode,tree):
        for node in ast.walk(tree):
            res = not node.__dict__ # check map is empty or not
            if ('lineno' in node.__dict__.keys()):
                if res == False and node.__dict__['lineno'] == lineNode:
                    return node
    def GetFullStatementNode(self,node):
        stringNode = astor.to_source(node)
        colOffset = node.col_offset
        arrNode = stringNode.split("\n")
        stringNodeWithOffset = ""
        del arrNode[-1]
        # print(arrNode)
        for line in arrNode:
            stringNodeWithOffset += colOffset*" " + line + "\n"
        return stringNodeWithOffset
    def GetNumberStsmOfNode(self, statementNode):
        arr = re.split('\n',statementNode)
        del arr[-1]
        return len(arr)
    def SwapNode(self,nodeSource, nodeDestination):
        ast.copy_location(nodeSource,nodeDestination)
    def DeleteNode(self,context,node):
        stringNode = astor.to_source(node)
        arrNode = stringNode.split("\n")
        print(arrNode)
        for i in arrNode:
            if i.strip() in context:
                context = context.replace(i, "")
        return context
    def InsertAfter(self, context, nodeInsert , nodeIndex):
        fullIndexNode = self.GetFullStatementNode(nodeIndex)
        fullInsertNode = self.GetFullStatementNode(nodeInsert)
        index = context.find(fullIndexNode)
        return context[:index] + fullInsertNode + context[index:]


class Tranformer:
    def DeleteStmt(self, lineNo, arr):
        return arr.remove(arr[lineNo])
    def ModifyProgByDeleteStmt(self, tracer,fname):
        # delete stmt with rank no 1
        arrLine = tracer.getLineInfor(fname)
        arrRankLine = []
        for iline in range(len(arrLine)):
            arrRankLine.append(arrLine[iline].rank)
        mostRank = arrRankLine.index(min(arrRankLine))
        self.DeleteStmt(mostRank, arrLine)
        return arrLine

class Helper:
    def CodeToTree(self, contextCode):
        return cst.parse_module(contextCode)
    def UpdateVariant(self,arrLine):
        context = ""
        for iline in range(len(arrLine)):
            context += arrLine[iline].text
        return context
    def WriteToFile(self,context):
        f = open("D:\docu\KL\Variant\dvariant.py","w+")
        f.write(context)
        f.close()
class ModifyValueVisitor(cst.CSTTransformer):
    def leave_Assign(self, node, updated_node):
        return updated_node.with_changes(value=cst.Integer(value='2'))


class AstTree:
    def getProg(self):
        dataReader = DataReader()
        context = dataReader.getContextFile()
        return context

    def dumpTree(self, tree):
        return ast.dump(tree)


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": [], "assign": []}

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(alias.name)
        self.generic_visit(node)

    def report(self):
        print(self.stats)


class AnalysisNodeVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Name(self, node):
        print('Name :', node.id)

    def visit_Num(self, node):
        print('Num :', node.__dict__['n'])

    def visit_Str(self, node):
        print("Str :", node.s)

    def visit_Print(self, node):
        print("Print :")
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        print("Assign :")
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Expr(self, node):
        print("Expr :")
        ast.NodeVisitor.generic_visit(self, node)
        return None

class Assignment(ast.NodeTransformer):
    def visit_Assign(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        print(astor.to_source(node))
if __name__ == '__main__':

    # tracedr = Tracer()
    # helper = Helper()
    #
    # h = Tranformer()
    # arr = h.ModifyProgByDeleteStmt(tracedr,"D:\docu\KL\Data\mid.py")
    # for iline in range(len(arr)):
    #     print(arr[iline].rank)
    # ct = helper.UpdateVariant(arr)
    # print(ct)
    # helper.WriteToFile(ct)
    # flag = Flag(0)
    dR = DataReader()

    context = dR.getContextFileWithPath("D:\docu\KL\Variant\Pop3.py")
    tree = ast.parse(context)

    helper = AstHelper()
    node9 = helper.GetNodeByLineNo(9,tree)
    # print(astor.to_source(node9))

    node4 = helper.GetNodeByLineNo(4,tree)
    # print(astor.to_source(node4))
    stringNode4 = helper.GetFullStatementNode(node4)
    stringNode9 = helper.GetFullStatementNode(node9)
    # print(stringNode4)
    # newContext = helper.InsertAfter(context,node8,node4)
    print(stringNode9)
    helper.GetNumberStsmOfNode(stringNode9)