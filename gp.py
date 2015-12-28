class Wrapper:
    def __init__(self, function, child_count, name):
        self.function = function
        self.child_count = child_count
        self.name = name


class Node:
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



class ParamNode:
    def __init__(self, index):
        self.index = index

    def evaluate(self, values):
        return values[self.index]

    def display(self, indent=0):
        print '%sp%d' % (' '*indent, self.index)



class ConstNode:
    def __init__(self, value):
        self.value = value

    def evaluate(self, values):
        return self.value

    def display(self, indent=0):
        print '%sconst%d' % (' '*indent, self.value)
