#!/usr/bin/env python2
from deap import base, creator, tools, algorithms, gp
import numpy as np
import random
import network
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


def evalObj(weights):
    return network.evalRobot(weights),

def getNewInd():
    return creator.Individual(network.Network((400,20,4)).weights)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", getNewInd)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evalObj)
toolbox.register("mate", tools.cxSimulatedBinary, eta=0.5)
toolbox.register("mutate", gp.mutEphemeral, mode="one")
toolbox.register("select", tools.selTournament, tournsize=3)

def ret(ind1, ind2):
    return False

def main():
    pop = toolbox.population(n=30)
    hof = tools.HallOfFame(1, similar=ret)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.1, halloffame=hof, ngen=60, stats=stats,  verbose=True)
    return pop, logbook, hof


if __name__ == "__main__":
    pop, log, hof = main()
    print("Best individual is with fitness: %s" % (hof[0].fitness))
    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")
    plt.show()


