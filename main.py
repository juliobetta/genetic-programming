import gp
from random import random,randint,choice


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
