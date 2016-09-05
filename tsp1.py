# Copyright 2010-2014 Google
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Traveling Salesman Sample.

   This is a sample using the routing library python wrapper to solve a
   Traveling Salesman Problem.
   The description of the problem can be found here:
   http://en.wikipedia.org/wiki/Travelling_salesman_problem.
   The optimization engine uses local search to improve solutions, first
   solutions being generated using a cheapest addition heuristic.
   Optionally one can randomly forbid a set of random connections between nodes
   (forbidden arcs).
"""



import random
import argparse
from ortools.constraint_solver import pywrapcp
# You need to import routing_enums_pb2 after pywrapcp!
from ortools.constraint_solver import routing_enums_pb2

def createAjtable(): 
# read nodes information and store these info in a dictionary 
    with open('test.txt','r') as infile:
        d = [d.replace('\n','').split(' ') for d in infile.readlines()] 
    ajtable = {}
    size = len(d)
    distance_max = 1000 # based on data, distance of my data is from 0 to 100, using 1000 to make sure the unconnect nodes is not selected
    for from_node in range(size): # nested  to initialize the dictionary
      ajtable[from_node] = {}
      for to_node in range(size):
        if from_node == to_node:
          ajtable[from_node][to_node] = 0
        else:
          ajtable[from_node][to_node] = distance_max
    for node in d: # rewrite the relationship of nodes
        i = int(node[0])
        for k in node[1:]:
            j, value = k.split(':')
            ajtable[i][int(j)] = float(value)
    return len(d), ajtable

class AdjacentMatrix(object): #using class to follow the or-tool instruction
  """AdjacentMatrix"""
  def __init__(self, size, ajtable):
    """Initialize adjacent matrix."""
    self.matrix = ajtable
  def Distance(self, from_node, to_node):
    return self.matrix[from_node][to_node]


def main():
  # Create routing model
  size, ajtable = createAjtable()
  if size > 0:
    # TSP of size args.tsp_size
    # Second argument = 1 to build a single tour (it's a TSP).
    # Nodes are indexed from 0 to parser_tsp_size - 1, by default the start of
    # the route is node 0.
    routing = pywrapcp.RoutingModel(size, 1)
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    # Setting first solution heuristic (cheapest addition).
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Setting the cost function.
    # Put a callback to the distance accessor here. The callback takes two
    # arguments (the from and to node inidices) and returns the distance between
    # these nodes.

    matrix = AdjacentMatrix(size, ajtable) # if we don't use full size adjacent matrix, it will select some nodes which don't connect at all
    print 'matrix', matrix.matrix #visualize the dictionary for debug
    
    matrix_callback = matrix.Distance
    if matrix_callback :
      routing.SetArcCostEvaluatorOfAllVehicles(matrix_callback)
    else:
      routing.SetArcCostEvaluatorOfAllVehicles(Distance)

    # Solve, returns a solution if any.
    assignment = routing.Solve()
    if assignment:
      # Solution cost.
      print 'travel cost: ', assignment.ObjectiveValue()
      # Inspect solution.
      route_number = 0
      node = routing.Start(route_number)
      route = ''
      while not routing.IsEnd(node):
        route += str(node) + ' '
        node = assignment.Value(routing.NextVar(node))
      route += '0'
      print 'travel route: ', route
    else:
      print 'No solution found.'
  else:
    print 'Specify an instance greater than 0.'

if __name__ == '__main__':
    main()
