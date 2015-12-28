import utils

print "####### BUILDING RANDOM TREES ####### \n\n"

hidden_set = utils.build_hidden_set()

random1 = utils.make_random_tree(2)
random2 = utils.make_random_tree(2)

print str(utils.score_function(random1, hidden_set))
print str(utils.score_function(random2, hidden_set))



# mutation

print "\n\n ####### MUTATION ########"

mutated_random_1 = utils.mutate(random1, 2)
random1.display()
mutated_random_1.display()

print str(utils.score_function(mutated_random_1, hidden_set))



# crossover

print "\n\n ####### CROSSOVER #######"

cross = utils.cross_over(random1, random2)
random1.display()
random2.display()
cross.display()

print str(utils.score_function(cross, hidden_set))



# evolving

print "\n\n ####### EVOLVING #######"

rank_function = utils.get_rank_function(hidden_set)

utils.evolve(2, 500, rank_function)
