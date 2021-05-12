from heapq import nlargest

### THIS FILE CONTAINS CLASSES FOR AN ARBITRARY DECISION TREE

class DecisionTree:
    def __init__(self, root, decision_list, brancher, pruner):
        """Creates a decision tree. Root is the initial packet. Decision list is
        a list of decisions initially available. Brancher is a function that
        takes a packet (1st arg) and a decision (2nd arg) and returns an updated
        packet. Pruner is a function that takes a packet and returns a score value."""
        # public properties
        self.root = Node(root)
        self.top = (self.root,)
        self.decisions = decision_list
        self.brancher = brancher
        self.pruner = pruner
        # private nodewise methods
        def nbrancher(node, key):
            value = self.brancher(node.value, key)
            return Node(value, key, node, self.pruner(value) + node.score)
        def npruner(node):
            return node.score
        self.nbrancher = nbrancher
        self.npruner = npruner
    def __str__(self):
        # recreate pruned tree
        current = {node: {} for node in self.top}
        upper = {}
        while self.root not in current:
            for node in current:
                if not node.parent in upper:
                    upper[node.parent] = {}
                upper[node.parent][node] = current[node]
            current = upper
            upper = {}
        # return tree representation
        return str(current)
    @property
    def is_determined(self):
        """Returns if there is only one viable decision from the root."""
        return len(set([node.initial_branch for node in self.top])) <= 1
    @property
    def ideal_path(self):
        """Returns the ideal traversal path."""
        return max(self.top, key=self.npruner).path
    @property
    def ideal_key(self):
        """Returns the first key of the ideal traversal path."""
        return max(self.top, key=self.npruner).initial_branch.key
    def branch(self):
        """Branches the topmost nodes."""
        self.top = tuple(self.nbrancher(n,d) for n in self.top for d in self.decisions)
    def prune(self,n):
        """Prunes the topmost nodes to have a maximum count of n."""
        if len(self.top) > n:
            self.top = tuple(nlargest(n, self.top, key=self.npruner))
    def reduce(self):
        """Reduces the decision list available during branching."""
        self.decisions = [n.initial_branch.key for n in self.top]

class Node:
    def __init__(self, value, key=None, parent=None, score=0):
        """Stores relevant node information for a decision tree. The value is
        the node's packet. The key is the decision which caused the branch to
        this node. The parent is this node's parent node."""
        self.value = value
        self.key = key
        self.parent = parent
        self.score = score
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self)
    @property
    def initial_branch(self):
        """Returns the first node from the root to get to the current node."""
        return self if self.parent.parent is None else self.parent.initial_branch
    @property
    def path(self):
        """Returns a list of the values leading up to this node."""
        return [self.value] if self.parent is None else self.parent.path+[self.value]
