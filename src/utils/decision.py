import heapq

### THIS FILE CONTAINS CLASSES FOR AN ARBITRARY DECISION TREE

class DecisionTree:
    def __init__(self, root, decision_list, brancher, pruner):
        """Creates a decision tree. Root is the initial packet. Decision list is
        a list of decisions initially available. Brancher is a function that
        takes a packet (1st arg) and a decision (2nd arg) and returns an updated
        packet. Pruner is a function that takes a packet and returns a score value."""
        self.root = Node(root)
        self.top = [self.root]
        self.decisions = decision_list
        self.brancher = brancher
        self.pruner = pruner
        self.npruner = lambda node: node.score
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
    def is_determined(self):
        """Returns if there is only one viable decision from the root."""
        return len(set([node.initial_branch() for node in self.top])) <= 1
    def branch(self):
        """Branches the topmost nodes."""
        self.top = [(self.brancher(n.value, d), d, n) \
            for n in self.top for d in self.decisions]
        self.top = [Node(s,d,n,self.pruner(s)+n.score) for s,d,n in self.top]
    def prune(self,n):
        """Prunes the topmost nodes to have a maximum count of n."""
        if len(self.top) > n:
            self.top = heapq.nlargest(n, self.top, key=self.npruner)
    def reduce(self):
        """Reduces the decision list available during branching."""
        self.decisions = [n.initial_branch().key for n in self.top]
    def ideal_path(self):
        """Returns the ideal traversal path."""
        return max(self.top, key=self.npruner).path()
    def ideal_key(self):
        """Returns the first key of the ideal traversal path."""
        return max(self.top, key=self.npruner).initial_branch().key

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
    def initial_branch(self):
        """Returns the first node from the root to get to the current node."""
        if self.parent.parent == None:
            # parent is the root node
            return self
        # parent is not the root node
        return self.parent.initial_branch()
    def path(self):
        """Returns a list of the values leading up to this node."""
        if self.parent == None:
            # return root path
            return [self.value]
        # return node path
        return self.parent.path() + [self.value]
