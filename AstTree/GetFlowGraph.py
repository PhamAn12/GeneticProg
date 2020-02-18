import astor
REGISTRY_IDX = 0
REGISTRY = {}
def get_registry_idx():
    global REGISTRY_IDX
    v = REGISTRY_IDX
    REGISTRY_IDX += 1
    return v
def reset_registry():
    global REGISTRY_IDX
    global REGISTRY
    REGISTRY_IDX = 0
    REGISTRY = {}
def register_node(node):
    node.rid = get_registry_idx()
    REGISTRY[node.rid] = node
def get_registry():
    return dict(REGISTRY)
class CFGNode(dict):
    def __init__(self, parents=[], ast=None):
        super().__init__()
        self.rid = None
        assert type(parents) is list
        register_node(self)
        self.parents = parents
        self.ast_node = ast
        self.update_children(parents)  # requires self.rid
        self.children = []
        self.calls = []

    def i(self):
        return str(self.rid)

    def update_children(self, parents):
        for p in parents:
            p.add_child(self)

    def add_child(self, c):
        if c not in self.children:
            self.children.append(c)

    def lineno(self):
        return self.ast_node.lineno if hasattr(self.ast_node, 'lineno') else 0

    def __str__(self):
        return "id:%d line[%d] parents: %s : %s" % (
            self.rid, self.lineno(), str([p.rid for p in self.parents]),
            self.source())

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.rid == other.rid

    def __neq__(self, other):
        return self.rid != other.rid

    def set_parents(self, p):
        self.parents = p

    def add_parent(self, p):
        if p not in self.parents:
            self.parents.append(p)

    def add_parents(self, ps):
        for p in ps:
            self.add_parent(p)

    def add_calls(self, func):
        self.calls.append(func)

    def source(self):
        return astor.to_source(self.ast_node).strip()

    def to_json(self):
        return {
            'id': self.rid,
            'parents': [p.rid for p in self.parents],
            'children': [c.rid for c in self.children],
            'calls': self.calls,
            'at': self.lineno(),
            'ast': self.source()
        }
if __name__ == '__main__':
    cff = CFGNode()
    cff.to_json()
