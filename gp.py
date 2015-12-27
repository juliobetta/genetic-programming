from copy import deepcopy
from math import log

class fwrapper:
    def __init__(self, function, childCount, name):
        self.function = function
        self.childCount = childCount
        self.name = name


class node:
    def __init__(self, wrapper, children):
        self.function = wrapper.function
        self.name = wrapper.name
        self.children = children

    def evaluate(self, values):
        results = [n.evaluate(values) for n in self.children]
        return self.function(results)

    def display(self, indent=0):
        print (' '*indent) + self.name
        for child in self.children:
            child.display(indent+1)



class paramnode:
    def __init__(self, index):
        self.index = index

    def evaluate(self, values):
        return values[self.index]

    def display(self, indent=0):
        print '%sp%d' % (' '*indent, self.index)



class constnode:
    def __init__(self, value):
        self.value = value

    def evaluate(self, values):
        return self.value

    def display(self, indent=0):
        print '%sconst%d' % (' '*indent, self.value)
