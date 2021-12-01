import random
import numpy as np


def setupCombination(populationNumber, geneSize, possibleValues):
    population = {}
    for i in range(1, populationNumber + 1):
        gene = []
        for m in range(geneSize):
            randomValue = random.randint(possibleValues[0], possibleValues[1])
            gene.append([randomValue])
        population[i] = gene

    return population


def setupPermutation(populationNumber, possibleValues):
    population = {}
    for i in range(1, populationNumber + 1):
        dummyList = []
        for m in possibleValues:
            dummyList.append(m)
        gene = []
        for m in range(len(possibleValues)):
            randomIndex = random.randint(0, len(dummyList) - 1)
            gene.append(dummyList[randomIndex])
            dummyList.pop(randomIndex)
        population[i] = gene

    return population


def mateRoutesCombination(population):
    updatedPopulation = population.copy()
    childIndex = int(len(population)) + 1

    for j in range(1, int(len(population)), 2):
        parent1 = population[j]
        parent2 = population[j + 1]

        mateIndex = random.randint(1, len(population[1]) - 1)
        for k in range(1, mateIndex + 1):
            child1 = parent1[:mateIndex] + parent2[mateIndex:]
            child2 = parent2[:mateIndex] + parent1[mateIndex:]

        updatedPopulation[childIndex] = child1
        updatedPopulation[childIndex + 1] = child2
        childIndex += 2

    return updatedPopulation


def mateRoutesPermutation(population):
    updatedPopulation = population.copy()
    childIndex = int(len(population)) + 1

    for j in range(1, int(len(population)), 2):
        parent1 = population[j]
        parent2 = population[j + 1]
        child1 = parent1.copy()
        child2 = parent2.copy()

        mateIndex = random.randint(1, len(population[1]) - 1)
        for k in range(1, mateIndex + 1):
            if child1[k] != child2[k]:
                swapIndex = child2.index(child1[k])
                temp = child2[k]
                child2[k] = child1[k]
                child2[swapIndex] = temp

        updatedPopulation[childIndex] = child2
        childIndex += 1

        child1 = parent1.copy()
        child2 = parent2.copy()

        mateIndex = random.randint(1, len(population[1]) - 1)
        for k in range(1, mateIndex + 1):
            if child2[k] != child1[k]:
                swapIndex = child1.index(child2[k])
                temp = child1[k]
                child1[k] = child2[k]
                child1[swapIndex] = temp

        updatedPopulation[childIndex] = child1
        childIndex += 1

    return updatedPopulation


def cullGenesElitism(population, amount):
    updatedPopulation = {}

    for j in range(1, amount + 1):
        updatedPopulation[j] = population[j]

    return updatedPopulation


def cullGenesTournament(population, startProbability):
    updatedPopulation = {}
    probabilityDict = {}
    contestantList = []
    possibleGenes = range(1, len(population) + 1)
    for i in range(1, len(population) + 1):
        probabilityDict[i] = startProbability * (1 - startProbability) ** i

    for i in range(len(possibleGenes)):
        availableGenes = list(set(possibleGenes).difference(contestantList))
        contestant = random.randint(0, len(availableGenes) - 1)
        contestantList.append(contestant)
    for i, j in enumerate(range(0, len(population), 2), 1):
        contestant1Probability = probabilityDict[contestantList[j]]
        contestant2Probability = probabilityDict[contestantList[j + 1]]
        contestant1Win = contestant1Probability / (contestant1Probability + contestant2Probability)

        if random.randint(1, 100) <= contestant1Win:
            updatedPopulation[i] = population[contestantList[j]]
        else:
            updatedPopulation[i] = population[contestantList[j + 1]]

    return updatedPopulation

def mutateRoutesCombination(population, mutationRate, possibleValues):
    updatedPopulation = population.copy()
    for i in updatedPopulation:
        if random.randint(1, 100) <= mutationRate:
            swapValue = possibleValues[random.randint(0, len(possibleValues[i]) - 1)]
            swapIndex = random.randint(1, len(updatedPopulation[i]))
            updatedPopulation[i][swapIndex] = swapValue

    return updatedPopulation

def mutateRoutesPermutation(population, mutationRate):
    updatedPopulation = population.copy()
    for i in updatedPopulation:
        for j in range(updatedPopulation[i]):
            if random.randint(1, 100) <= mutationRate:
                swapIndex = random.randint(0, len(updatedPopulation[i]) - 1)
                temp = updatedPopulation[j][swapIndex]
                updatedPopulation[swapIndex] = updatedPopulation[i][j]
                updatedPopulation[i][j] = temp

    return updatedPopulation


def randomSwapRoute(route, swapRate):
    updatedRoute = route.copy()

    for k in range(len(updatedRoute)):
        if random.randint(1, 100) <= swapRate:
            swapIndex = random.randint(0, len(route) - 1)
            tempLock = updatedRoute[swapIndex]
            updatedRoute[swapIndex] = updatedRoute[k]
            updatedRoute[k] = tempLock

    return updatedRoute


def calculateCost(population, cities):
    populationCostList = []
    for i in range(1, int(len(population) + 1)):
        distance = 0
        for k, j in enumerate(population[i], 1):
            if k < len(population[i]):
                distance += ((cities[j][1] - cities[population[i][k]][1]) ** 2 +
                             (cities[j][2] - cities[population[i][k]][2]) ** 2) ** (1 / 2)
        distance += ((cities[population[i][0]][1] - cities[population[i][-1]][1]) ** 2 +
                     (cities[population[i][0]][2] - cities[population[i][-1]][2]) ** 2) ** (1 / 2)
        populationCostList.append(distance)
    return populationCostList


def sortRoutes(population, populationCostList):
    updatedPopulation = {}
    updatedPopulationCostList = []

    for i in range(1, len(population) + 1):
        minIndex = np.argmin(populationCostList)
        updatedPopulation[i] = population[minIndex + 1]
        updatedPopulationCostList.append(populationCostList[minIndex])
        populationCostList[minIndex] = 9999999
        i += 1

    return updatedPopulation, updatedPopulationCostList
