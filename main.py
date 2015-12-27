import utils

print "BUILDING RANDOM TREES \n\n"

hiddenSet = utils.buildHiddenSet()

random1 = utils.makeRandomTree(2)
random2 = utils.makeRandomTree(2)

print str(utils.scoreFunction(random1, hiddenSet))
print str(utils.scoreFunction(random2, hiddenSet))



# mutation

print "\n\n MUTATION"

mutatedRandom1 = utils.mutate(random1, 2)
random1.display()
mutatedRandom1.display()

print str(utils.scoreFunction(mutatedRandom1, hiddenSet))



# crossover

print "\n\n CROSSOVER"

cross = utils.crossOver(random1, random2)
random1.display()
random2.display()
cross.display()

print str(utils.scoreFunction(cross, hiddenSet))



# evolving

print "\n\n EVOLVING"

rankFunction = utils.getRankFunction(hiddenSet)

utils.evolve(2, 500, rankFunction)
