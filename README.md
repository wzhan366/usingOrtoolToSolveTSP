# Using Ortool To Solve TSP

In this repo, I use the or-tool to solve the TSP problem.
The node relationship is stored in a txt file and the output has the travle cost and route.

## Travel sale problem
> The travelling salesman problem (TSP) asks the following question: Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city? It is an NP-hard problem in combinatorial optimization, important in operations research and theoretical computer science.

Normally we can find some dynamic solution but they are triky to implement and it is not efficient. 
Google has a toolbox called or-tool which provider sovler of this problem. After modified it a little bit, I sovled a TSP problem which posts at codeabbay.com

## Step-to-step

First, install or-tool 
- follows the standard python library installation pip step

Second, prepare the test data
- put test data in the tsp.py direction
- here I provide the test data follows structure node lind_node:cost

Third, modify code and run          
- modify the or-tool code to fit our data and run it

Installation instruction is https://developers.google.com/optimization/installing
