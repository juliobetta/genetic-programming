from math import log
from random import random,randint,choice
from copy import deepcopy
import gp

################################################################################
# WRAPPERS #####################################################################
################################################################################

addw = gp.Wrapper(lambda params:params[0] + params[1], 2, 'add')
subw = gp.Wrapper(lambda params:params[0] - params[1], 2, 'subtract')
mulw = gp.Wrapper(lambda params:params[0] * params[1], 2, 'multiply')


def if_func(params):
    if params[0] > params[1]: return params[1]
    else: return params[2]
ifw = gp.Wrapper(if_func, 3, 'if')


def is_greater(params):
    if params[0] > params[1]: return 1
    else: return 0
gtw = gp.Wrapper(is_greater, 2, 'is_greater')



################################################################################
# TREES ########################################################################
################################################################################

def example_tree():
    return gp.Node(ifw, [
        gp.Node(gtw, [gp.ParamNode(0), gp.ConstNode(3)]),
        gp.Node(addw, [gp.ParamNode(1), gp.ConstNode(5)]),
        gp.Node(subw, [gp.ParamNode(1), gp.ConstNode(2)])
    ])


def make_random_tree(n_params, max_depth=4, fpr=0.5, ppr=0.6):
    """ Make a random tree

    Arguments:
    n_params  -- Number of parameters that the tree will take
    max_depth -- Max depth of the tree (default 4)
    fpr       -- Probability that the node created is a function (default 0.5)
    ppr       -- Probability that the node created is a ParamNode (default 0.6)
    """

    flist = [addw, mulw, ifw, gtw, subw]

    if random() < fpr and max_depth > 0:
        wrapper = choice(flist)
        children = [make_random_tree(n_params, max_depth-1, fpr, ppr)
                    for i in range(wrapper.child_count)]
        return gp.Node(wrapper, children)

    elif random() < ppr:
        return gp.ParamNode(randint(0, n_params-1))

    else:
        return gp.ConstNode(randint(0, 10))



################################################################################
# MEASURING SUCCESS ############################################################
################################################################################

def hidden_function(x, y):
    return x**2+2*y+3*x+5


def build_hidden_set():
    rows = []

    for i in range(200):
        x = randint(0, 40)
        y = randint(0, 40)
        rows.append([x, y, hidden_function(x, y)])

    return rows


def score_function(tree, rows):
    diff = 0

    for data in rows:
        val = tree.evaluate([data[0], data[1]])
        diff += abs(val - data[2])

    return diff


def get_rank_function(dataset):
    def rank_function(population):
        scores = [(score_function(tree, dataset), tree) for tree in population]
        scores.sort()
        return scores

    return rank_function



################################################################################
# EVOLUTION ####################################################################
################################################################################

def mutate(tree, n_params, prob_change=0.1):
    if random() < prob_change:
        return make_random_tree(n_params)
    else:
        result = deepcopy(tree)
        if isinstance(tree, gp.Node):
            result.children = [mutate(child, n_params, prob_change)
                               for child in tree.children]
        return result


def cross_over(tree1, tree2, prob_swap=0.7, top=1):
    if random() < prob_swap and not top:
        return deepcopy(tree2)
    else:
        result = deepcopy(tree1)
        if isinstance(tree1, gp.Node) and isinstance(tree2, gp.Node):
            result.children = [
                cross_over(child, choice(tree2.children), prob_swap, 0)
                for child in tree1.children
            ]
        return result


def evolve(n_params, pop_size, rank_function, max_gen = 500,
           mutation_rate = 0.1, breeding_rate = 0.4, pexp = 0.7, pnew = 0.05):

    # Returns a random number, tending towards lower numbers. The lower pexp is,
    # more lower number will get.
    def select_index():
        return int(log(random()) / log(pexp))

    # Create a random initial population
    population = [make_random_tree(n_params) for i in range(pop_size)]

    for i in range(max_gen):
        scores = rank_function(population)
        print scores[0][0]
        if(scores[0][0] == 0): break

        # The two best always make it
        new_pop = [scores[0][1], scores[1][1]]

        # Build the next generation
        while len(new_pop) < pop_size:
            if random() > pnew:
                new_pop.append(
                    mutate(
                        cross_over(
                            scores[select_index()][1],
                            scores[select_index()][1],
                            prob_swap = breeding_rate
                        ),
                        n_params,
                        prob_change = mutation_rate
                    )
                )
            else:
                # Add a random node to mix things up
                new_pop.append(make_random_tree(n_params))

        population = new_pop

    scores[0][1].display()
    return scores[0][1]
