import gp
from random import random,randint,choice
from copy import deepcopy

################################################################################
# WRAPPERS #####################################################################
################################################################################

addw = gp.fwrapper(lambda params:params[0] + params[1], 2, 'add')
subw = gp.fwrapper(lambda params:params[0] - params[1], 2, 'subtract')
mulw = gp.fwrapper(lambda params:params[0] * params[1], 2, 'multiply')


def ifFunc(params):
    if params[0] > params[1]: return params[1]
    else: return params[2]
ifw = gp.fwrapper(ifFunc, 3, 'if')


def isGreater(params):
    if params[0] > params[1]: return 1
    else: return 0
gtw = gp.fwrapper(isGreater, 2, 'isGreater')



################################################################################
# TREES ########################################################################
################################################################################

def exampleTree():
    return gp.node(ifw, [
        gp.node(gtw, [gp.paramnode(0), gp.constnode(3)]),
        gp.node(addw, [gp.paramnode(1), gp.constnode(5)]),
        gp.node(subw, [gp.paramnode(1), gp.constnode(2)])
    ])


def makeRandomTree(nParams, maxDepth=4, fpr=0.5, ppr=0.6):
    """ Make a random tree

    Arguments:
    nParams  -- Number of parameters that the tree will take
    maxDepth -- Max depth of the tree (default 4)
    fpr      -- Probability that the node created is a function (default 0.5)
    ppr      -- Probability that the node created is a paramnode (default 0.6)
    """

    flist = [addw, mulw, ifw, gtw, subw]

    if random() < fpr and maxDepth > 0:
        wrapper = choice(flist)
        children = [makeRandomTree(nParams, maxDepth-1, fpr, ppr)
                    for i in range(wrapper.childCount)]
        return gp.node(wrapper, children)

    elif random() < ppr:
        return gp.paramnode(randint(0, nParams-1))

    else:
        return gp.constnode(randint(0, 10))



################################################################################
# MEASURING SUCCESS ############################################################
################################################################################

def hiddenFunction(x, y):
    return x**2+2*y+3*x+5


def buildHiddenSet():
    rows = []

    for i in range(200):
        x = randint(0, 40)
        y = randint(0, 40)
        rows.append([x, y, hiddenFunction(x, y)])

    return rows


def scoreFunction(tree, rows):
    diff = 0

    for data in rows:
        val = tree.evaluate([data[0], data[1]])
        diff += abs(val - data[2])

    return diff



################################################################################
# EVOLUTION ####################################################################
################################################################################

def mutate(tree, nParams, probChange=0.1):
    if random() < probChange:
        return makeRandomTree(nParams)
    else:
        result = deepcopy(tree)
        if isinstance(tree, gp.node):
            result.children = [mutate(child, nParams, probChange)
                               for child in tree.children]
        return result


def crossOver(tree1, tree2, probSwap=0.7, top=1):
    if random() < probSwap and not top:
        return deepcopy(tree2)
    else:
        result = deepcopy(tree1)
        if isinstance(tree1, gp.node) and isinstance(tree2, gp.node):
            result.children = [
                crossOver(child, choice(tree2.children), probSwap, 0)
                for child in tree1.children
            ]
        return result
