Travelling Salesman Problem (TSP)
--------------------------------
The travelling salesman problem is a problem where one finds the optimal route (shortest route)
between a group of cities. The optimal route is obtained by minimizing the total distance of the route
between each city, where the path must go to each city once.  For more details on this problem, you can see the
wikipedia page here:  https://en.wikipedia.org/wiki/Travelling_salesman_problem

Simulated Annealing
-------------------
To solve this problem, I used an algorithm called simulated annealing.  I start the algorithm off by initializing
with a greedy closest-neighbors search solution.  This usually gives a pretty good result on its own, however there
are often several changes that can be made to further optimize the solution, which is where the simulated annealing
search comes to use. Simulated Annealing is, simply put, a way of searching where in the beginning random and
seemingly worse changes in the route are more frequent and able to occur due to a "temperature", which gradually 
decreases.  As the temperature "cools", the algorithm is restricted from taking more random and possibly incorrect
steps, and begins to only accept decisions that yield positive effect to the goal.  Allowing the algorithm to make
some incorrect changes and experiment lets it go try and find shorter paths that might not be readily detected
due to the nature of a greedy algorithm.  
Here's the wiki for more info:  https://en.wikipedia.org/wiki/Simulated_annealing

Result
------
I tested my algorithm by randomly generating 20 "cities" as coordinates on a 200 by 200 area.
Since the number of cities to connect is relatively small, the greedy search I initialize the algorithm with seems
to usually get a pretty close result, but with some changes still needed. Occasionally, the algorithm fails to find a
better solution than the greedy search, but on average it can improve the route and decrease it from the initialized
solution's length by about 8-10% (I ran tests on batches of size 100 to obtain these numbers).

How to run
----------
Just run the code of tsp.py as is and it will prompt you to input city coordinates to fill the search space
* city coordinates need to be 0 - 200
* to randomly produce 20 cities, just input 'done'
* to visualize results and algorithm performance, you need matplot python packages.
 - the code will print the plot of the initialized greedy search solution, then the final solution after simulated
   annealing, and then a plot of the algorithm's heuristic values from each iteration (10000)