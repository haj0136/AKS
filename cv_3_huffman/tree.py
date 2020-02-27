import heapq


class Tree:
    def __init__(self, root, symbol_limit):
        def build_code_dict(node, prefix):
            if isinstance(node, InternalNode):
                build_code_dict(node.leftchild, prefix + (0,))
                build_code_dict(node.rightchild, prefix + (1,))
            elif isinstance(node, Leaf):
                if node.symbol in self.codes:
                    raise ValueError("Symbol has more than one code")
                self.codes[node.symbol] = prefix
            else:
                raise AssertionError("Illegal node type")

        if symbol_limit < 2:
            raise ValueError("At least 2 symbols needed")

        self.root = root
        self.codes = {}
        build_code_dict(root, ())

        def __str__():
            def to_str(prefix, node):
                if isinstance(node, InternalNode):
                    return to_str(prefix + "0", node.leftchild) + to_str(prefix + "0", node.rightchild)
                elif isinstance(node, Leaf):
                    return "Code {}: Symbol {}\n".format(prefix, node.symbol)
                else:
                    raise AssertionError("Illegal node type")

            return to_str("", self.root)


def build_tree(frequencies: dict):
    pqueue = []

    for symbol, freq in frequencies.items():
        if freq > 0:
            heapq.heappush(pqueue, (freq, symbol, Leaf(symbol)))

    while len(pqueue) > 1:
        x = heapq.heappop(pqueue)  # Tuple of (frequency, symbol, node object)
        y = heapq.heappop(pqueue)  # Tuple of (frequency, symbol, node object)
        z = (x[0] + y[0], x[1] + y[1], InternalNode(x[2], y[2]))  # Construct new tuple
        heapq.heappush(pqueue, z)

    return Tree(pqueue[0][2], len(frequencies))


class Node(object):
    pass


class InternalNode(Node):
    def __init__(self, left, right):
        if not isinstance(left, Node) or not isinstance(right, Node):
            raise TypeError()
        self.leftchild = left
        self.rightchild = right


class Leaf(Node):
    def __init__(self, sym):
        self.symbol = sym
