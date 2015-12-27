import gp

addw = gp.fwrapper(lambda l:l[0]+l[1],2,'add')
subw = gp.fwrapper(lambda l:l[0]-l[1],2,'subtract')
mulw = gp.fwrapper(lambda l:l[0]*l[1],2,'multiply')


def iffunc(l):
    if l[0]>l[1]: return l[1]
    else: return l[2]
ifw = gp.fwrapper(iffunc,3,'if')


def isgreater(l):
    if l[0]>l[1]: return 1
    else: return 0
gtw = gp.fwrapper(isgreater,2,'isgreater')


flist = [addw,mulw,ifw,gtw,subw]


def exampletree():
    return gp.node(ifw, [
        gp.node(gtw, [gp.paramnode(0), gp.constnode(3)]),
        gp.node(addw, [gp.paramnode(1), gp.constnode(5)]),
        gp.node(subw, [gp.paramnode(1), gp.constnode(2)])
    ])
