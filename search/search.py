# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    #"*** YOUR CODE HERE ***"
    #dfs
    #bfs full cycle check
    open_list = util.Stack()
    node = [problem.getStartState()]
    start = (node, 0, [])
    open_list.push(start)
    #visited = set()
    # visited.add(start[0])
    # print "open_list ", open_list
    while not open_list.isEmpty():  # hack to check if empty
        (node, cost, path) = open_list.pop()  # node cost path
        #visited.add(node)


        state = node[-1]
        # print "path = ", path
        if (problem.isGoalState(state)):
            return path
        successor = problem.getSuccessors(state)
        for succ_node, succ_action, succ_cost in successor:
            old_node = list(node)
            if not succ_node in node:  # not visited yet
                # print "succ node, ", succ_node
                # print "path = ", path
                new_cost = cost + succ_cost
                old_node.append(succ_node)
                new_path = path + [succ_action]
                new_state = (old_node, new_cost, new_path)
                open_list.push(new_state)
    return []  # no solution case


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    open_list = util.Queue()
    start = (problem.getStartState(), 0, [])
    open_list.push(start)
    visited = set()
    visited.add(problem.getStartState())
    # print "open_list ", open_list
    while not open_list.isEmpty():  # hack to check if empty
        (node, cost, path) = open_list.pop()  # node cost path
        state = node
        #visited.add(state)

        # print "path = ", path
        if (problem.isGoalState(state)):
            return path
        successor = problem.getSuccessors(state)

        for succ_node, succ_action, succ_cost in successor:
            if not succ_node in visited:  # not visited yet
                #print "succ node, ", succ_node
                #print "path = ", path
                new_cost = cost + succ_cost
                new_node = succ_node
                new_path = path + [succ_action]
                new_state = (new_node, new_cost, new_path)
                open_list.push(new_state)
                visited.add(succ_node)
    return []  # no solution case



def ucs_helper(problem, open_list):
    start = (problem.getStartState(),0,[])
    open_list.push(start , 0)
    visited = {}
    visited.update({problem.getStartState():0})

    while not open_list.isEmpty():
        state = open_list.pop() #state = node, cost, path
        node = state[0]
        cost = state[1]
        path = state[2]
        if cost <= visited[node]:
            if problem.isGoalState(node):
                return path
            successor = problem.getSuccessors(node)

            for succ_node, succ_action, succ_cost in successor:
                new_cost = cost + succ_cost
                if not succ_node in visited or new_cost < visited[succ_node]:  # not visited yet
                    #print "succ node, ", succ_node
                    #print "path = ", path
                    new_node = succ_node
                    new_path = path + [succ_action]
                    new_state = (new_node, new_cost, new_path)
                    open_list.push(new_state, new_cost)
                    visited.update({succ_node:new_cost})

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    open_list = util.PriorityQueue()
    return ucs_helper(problem, open_list)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0



def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    open_list = util.PriorityQueue()
    start = (problem.getStartState(), [], 0)
    start_h = heuristic(start[0], problem=problem)
    open_list.push(start, start_h)

    visited = {}
    visited.update({problem.getStartState():0})
    while not open_list.isEmpty():
        state = open_list.pop()
        node = state[0]
        path = state[1]

        cost = state[2] #problem.getCostOfActions(path)
        if cost <= visited[node]:
            if problem.isGoalState(node):
                return path
            successor = problem.getSuccessors(node)
            for succ_node, succ_action, succ_cost in successor:
                #s_cost = problem.getCostOfActions(path + [succ_action])  + heuristic(node, problem=problem)  # succ_cost + problem.getCostOfActions(path)\

                g_cost = cost + succ_cost #problem.getCostOfActions(path + [succ_action]) #path to succ node
                if not succ_node in visited or g_cost < visited[succ_node]:  # not visited yet
                    # print "succ node, ", succ_node
                    # print "path = ", path
                    new_cost = cost + succ_cost
                    new_fcost = g_cost + heuristic(succ_node, problem=problem)  # succ_cost + problem.getCostOfActions(path)\
                    new_node = succ_node
                    new_path = path + [succ_action]
                    new_state = (new_node, new_path, new_cost)  # (new_node, new_cost, new_path)
                    open_list.push(new_state, new_fcost)
                    visited.update({succ_node:g_cost})
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
