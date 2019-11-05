import math
import random
import numpy as np
import matplotlib.pyplot as plt

class TSP:

    def __init__(self):
        #cities represented as their coords in a tuple (x,y)
        self.cities = list()

    #returns tuple (initial distance, best distance)
    #if testing=False, will show graphs of paths and more information
    def simulatedAnnealing(self, testing=False):
        "searches for shortest path between city coordinates"
        if not testing: #for regular running, not gathering stats
            print("Enter city coords sep. by space 'X Y' (enter 'done' to finish)")
            print("For random input: enter 'done' w/out entering any coords")
            choice = input("Coords 'X Y': ")
            while choice != 'done':
                coords = choice.split()
                self.cities.append((choice[0], choice[1]))
                choice = input("Coords 'X Y': ")
            if len(self.cities) == 0: #no input => random generation
                coordsX = np.random.rand(20) * 200
                coordsY = np.random.rand(20) * 200
                for i in range(len(coordsX)):
                    self.cities.append((round(coordsX[i]), round(coordsY[i])))
                print("No input - generated 20 random city positions")
        else: #when testing => random generation
            coordsX = np.random.rand(20) * 200
            coordsY = np.random.rand(20) * 200
            for i in range(len(coordsX)):
                self.cities.append((round(coordsX[i]), round(coordsY[i])))
        temp = 10000 #temperature for annealing
        coolingRate = 0.001
        iterations = 0 #counts iterations

        #Start with greedy approach to path generation
        # - start at random city
        # - repeatedly link to closest city until path formed

        initialSolution = self.getInitial()

        if not testing:
            print("initial solution distance: " + str(self.heuristic(initialSolution)))
            self.plotPath(initialSolution)
        
        currentSolution = self.copyPath(initialSolution)

        best = self.copyPath(initialSolution) #initialize best to the same
        bestDist = self.heuristic(best) #records distance of best solution

        history = list() #records new solution distances
        currHistory = list()
        numIter = 10000 #number of times algorithm iterates

        while temp > 0.0001 or iterations < numIter:
            #create neighbor path
            newSolution = self.copyPath(currentSolution)

            #random positions in the path
            pos1 = round((len(newSolution) - 1) * random.random())
            pos2 = round((len(newSolution) - 1) * random.random())

            #swap the cities in the path order
            city1 = newSolution[pos1]
            city2 = newSolution[pos2]
            newSolution[pos2] = city1
            newSolution[pos1] = city2

            #get energy of solutions
            currEnergy = self.heuristic(currentSolution)
            newEnergy = self.heuristic(newSolution)

            if iterations in [round(numIter/4), round(numIter/2), 3 * round(numIter/4)]:
                #self.plotPath(newSolution)
                if not testing:
                    print("iteration " + str(iterations) + ": " + str(currEnergy))

            #compare energies to decide if we keep new solution
            if self.acceptProb(currEnergy, newEnergy, temp) > random.random():
                #print("curr changed!")
                currentSolution = self.copyPath(newSolution)

            #update best solution if (new) current solution is better
            if self.heuristic(currentSolution) < bestDist:
                bestDist = self.heuristic(currentSolution)
                best = self.copyPath(currentSolution)

            #history.append(newEnergy)
            currHistory.append(currEnergy)

            temp = temp * (1 - coolingRate)
            iterations = iterations + 1
        if not testing:
            print("final solution distance: " + str(bestDist))
            self.plotPath(best)
            print("plot of solution heuristic over each iteration:")
            #plt.scatter(list(range(len(history))), history)
            #plt.show()
            #print(str(max(history)) + ", " + str(min(history)))
            plt.scatter(list(range(len(currHistory))), currHistory)
            plt.show()
        return (self.heuristic(initialSolution), bestDist)
        


    def acceptProb(self, curr, new, T):
        "calculate the acceptance probability"
        if new < curr: #always accept if new is better
            return 1
        return math.exp(-abs(curr - new) / T)
        
            
    def distance(self, A, B):
        "gets euclidean distance between coordinate tuples A and B"
        xDist = abs(A[0] - B[0])
        yDist = abs(A[1] - B[1])
        return math.sqrt((xDist*xDist) + (yDist*yDist))

    def heuristic(self, path):
        "gets the distance of the given path"
        d = 0
        for i in range(len(path)):
            fromCity = path[i]
            if i + 1 < len(path):
                toCity = path[i + 1]
            else:
                toCity = path[0]
            d = d + self.distance(fromCity, toCity)
        return d

    def getInitial(self):
        "returns a greedy path (closest neighbors alg) of the cities"
        initial = list()
        path = list() #records the greedy path
        remainingCities = list(range(len(self.cities)))
        curr = 0
        nextCity = None
        while len(remainingCities) > 0:
            remainingCities.remove(curr)
            path.append(curr)
            distance = 10000 #value greater than any possible city gap
            for i in remainingCities: #finds closest neighbor
                d = self.distance(self.cities[curr],self.cities[i])
                if d < distance:
                    distance = d
                    nextCity = i
            curr = nextCity
        for i in range(len(path)):
            initial.append(self.cities[path[i]])
        return initial


    def copyPath(self, p):
        "makes copy of given list of tuples (so they aren't referenced linked)"
        copy = list()
        for coord in p:
            copy.append(coord)
        return copy

    def plotPath(self, p):
        "displays matplot graph of given path"
        listX = list()
        listY = list()
        #print(p)
        for coords in p:
            #print(coords)
            listX.append(coords[0])
            listY.append(coords[1])
        plt.scatter(listX, listY)
        plt.plot(listX, listY)
        plt.show()


#Run this to start the program
tsp = TSP()
results = tsp.simulatedAnnealing()


#the below was used for gathering stats on the algorithm
"""
import time
a = time.time()

averagePercent = 0
iters = 100
for i in range(iters):
    tsp = TSP()
    results = tsp.simulatedAnnealing(testing=True)
    print(results[0], results[1])
    change = abs(results[0] - results[1])/results[0] #percent change (decrease in dist) from initial greedy solution
    averagePercent = averagePercent + change
    print(str(((i + 1)/iters) * 100) + "%")
    print("time elapsed " + str(round(time.time() - a)) + "s")
averagePercent = round((averagePercent / iters) * 100)
print("average percent change is " + str(averagePercent) + "%")
"""
