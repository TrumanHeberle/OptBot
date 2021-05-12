from utils.decision import DecisionTree, Node

def test_node_init():
    """decision tree node initialzation"""
    # node
    n1 = Node(0,1)
    assert n1
    assert n1.value == 0
    assert n1.key == 1
    assert n1.parent is None
    assert n1.score == 0
    # node with parent
    n2 = Node(3,4,n1)
    assert n2
    assert n2.value == 3
    assert n2.key == 4
    assert n2.parent is n1
    assert n2.score == 0
    # node with parent/score
    n3 = Node(5,6,n2,7)
    assert n3
    assert n3.value == 5
    assert n3.key == 6
    assert n3.parent is n2
    assert n3.score == 7

def test_node_properties():
    """decision tree node properties"""
    n1 = Node(0,1)
    n2 = Node(3,4,n1)
    n3 = Node(5,6,n2,7)
    n4 = Node(8,9,n2,10)
    # initial branch of root nodes
    err = False
    try:
        n1.initial_branch
    except Exception as e:
        err = e
    assert err
    # initial branch of branched nodes
    assert n2.initial_branch is n2
    assert n3.initial_branch is n2
    assert n4.initial_branch is n2
    # path values of nodes
    assert n1.path == [0]
    assert n2.path == [0,3]
    assert n3.path == [0,3,5]
    assert n4.path == [0,3,8]

def test_node_str():
    """decision tree node to string"""
    n = Node(5,6,None,7)
    assert n.value == 5
    assert str(n) == "5"
    assert repr(n) == "5"

def test_init():
    """decision tree initialization"""
    branch = lambda s,d: s+d
    prune = lambda s: s
    decisions = [1,2,3]
    tree = DecisionTree(0,decisions,branch,prune)
    # test node parameters
    assert tree
    assert tree.root.value == 0
    assert tree.decisions == decisions
    assert tree.brancher == branch
    assert tree.pruner == prune

def test_properties():
    """decision tree properties"""
    branch = lambda s,d: s+d
    prune = lambda s: s
    decisions = [1,2,3]
    tree = DecisionTree(0,decisions,branch,prune)
    # initial state
    err = False
    try:
        tree.is_determined
    except Exception as e:
        err = e
    assert err
    assert tree.ideal_path == [0]
    err = False
    try:
        tree.ideal_key
    except Exception as e:
        err = e
    assert err
    # branch
    tree.branch()
    assert not tree.is_determined
    assert tree.ideal_path == [0,3]
    assert tree.ideal_key == 3
    # prune
    tree.prune(1)
    assert tree.is_determined
    assert tree.ideal_path == [0,3]
    assert tree.ideal_key == 3

def test_branch():
    """decision tree branching"""
    branch = lambda s,d: s+d
    prune = lambda s: s
    decisions = [1,2,3]
    tree = DecisionTree(0,decisions,branch,prune)
    # branch 1
    tree.branch()
    assert not tree.is_determined
    assert tree.ideal_path == [0,3]
    assert tree.ideal_key == 3
    assert sorted([n.value for n in tree.top]) == [1,2,3]
    # branch 2
    tree.branch()
    assert not tree.is_determined
    assert tree.ideal_path == [0,3,6]
    assert tree.ideal_key == 3
    assert sorted([n.value for n in tree.top]) == [2,3,3,4,4,4,5,5,6]
    # branch 3
    tree.branch()
    assert not tree.is_determined
    assert tree.ideal_path == [0,3,6,9]
    assert tree.ideal_key == 3
    assert sorted([n.value for n in tree.top]) == \
        [3,4,4,4,5,5,5,5,5,5,6,6,6,6,6,6,6,7,7,7,7,7,7,8,8,8,9]

def test_prune():
    """decision tree pruning"""
    branch = lambda s,d: s+d
    prune = lambda s: s
    decisions = [1,2,3]
    tree = DecisionTree(0,decisions,branch,prune)
    # prune 1
    tree.branch(); tree.prune(3)
    assert not tree.is_determined
    assert tree.ideal_path == [0,3]
    assert tree.ideal_key == 3
    assert sorted([n.value for n in tree.top]) == [1,2,3]
    # prune 2
    tree.branch(); tree.prune(4)
    assert not tree.is_determined
    assert tree.ideal_path == [0,3,6]
    assert tree.ideal_key == 3
    assert sorted([n.value for n in tree.top]) == [4,5,5,6]
    # prune 3
    tree.branch(); tree.prune(5)
    assert tree.is_determined
    assert tree.ideal_path == [0,3,6,9]
    assert tree.ideal_key == 3
    assert sorted([n.value for n in tree.top]) == [7,7,8,8,9]
