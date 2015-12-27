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

def isequal(l):
    if l[0]==l[1]: return 1
    else: return 0
eqw = gp.fwrapper(isequal,2,'isequal')

flist = [addw,mulw,ifw,gtw,eqw,subw]


def exampletree():
    return gp.node(ifw, [
        gp.node(eqw, [paramnode(0), paramnode(1)]),
        gp.node(mulw, [paramnode(0), paramnode(1)]),
        gp.node(ifw, [
            gp.node(gtw, [paramnode(0), constnode(3)]),
            gp.node(addw, [paramnode(1), constnode(5)]),
            gp.node(subw, [paramnode(1), constnode(2)])
        ])
    ])
