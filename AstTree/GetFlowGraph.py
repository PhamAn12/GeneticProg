import ast

import astor
class MyOptimizer(ast.NodeTransformer):

    def visit_generic(self, node):
        # if node.id == 'pi':
        #     return ast.Num(n=3.14159265)
        # return node
        print(node)

tree = ast.parse("y = 2 * pi")
print(astor.to_source(tree))
optimizer = MyOptimizer()
tree = optimizer.visit(tree)
print(ast.dump(tree))
print(astor.to_source(tree))