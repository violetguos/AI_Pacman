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
    "*** YOUR CODE HERE ***"
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    #print type(problem) = instance
    #print type(problem.getSuccessors(problem.getStartState())) = list
    #print "get cost of action:", problem.getCostOfActions()
    #print "get pacman state:", problem.getPacmanState()
    #util.raiseNotDefined()
    open_list = []#util.PriorityQueue()
    successors_list = [] #use a list at the moment
    goal_bool = problem.isGoalState(problem.getStartState())
    return dfs_helper(problem, open_list, successors_list, goal_bool)


def end_state(n):
    '''
    return the end state, the last tuple in the first tuple
    of a list
    :param n:
    :return:
    '''
    for item in n:
        last = item[-1]  # could be an int or a tuple
        if isinstance(last, tuple):
            return last
        else:
            return item

def find_succ_in_n(n, succ):
    '''
    returns ture if succ is found in n
    :param n:
    :param succ:
    :return:
    '''
    for item in n:
        for i in range
        first = item[0][0]  # could be an int or a tuple
        if isinstance(first, tuple):
            if first == succ:
                return True
            else
                return False
        else:



def dfs_helper(problem, open_list, successors_list, goal_bool):
    '''
    Helper function for DFS search
    '''
    #n = []
    open_list.append(problem.getStartState())
    #print "open_list ", open_list
    while len(open_list) != 0: #hack to check if empty
        n = []
        n.append(open_list.pop(0)) #n = [( ), ( )] or [((),())]
        n_end_state = end_state(n) #end state function
        #print "end state ", n_end_state
        if problem.isGoalState(n_end_state):
            return n
        successors_list = problem.getSuccessors(n_end_state)
        #print "successors_list ", successors_list #[(),()]
        #extract only the position info
        successor_pos = []
        for i in successors_list:
            successor_pos.append(i[0])
        print "successor_pos = ", successor_pos
        for succ in successor_pos:
            if n.count(succ) == 0: #succ is  () type
                n.append(succ)
                print "n append succ", n
                open_list.append(tuple(n)) #n.append is a list, openlist is a list
                print "openg list after ", open_list
    return False


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
