# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class Actions:
    """
    A collection of static methods for manipulating move actions.
    """
    # Directions
    _directions = {Directions.NORTH: (0, 1),
                   Directions.SOUTH: (0, -1),
                   Directions.EAST:  (1, 0),
                   Directions.WEST:  (-1, 0),
                   Directions.STOP:  (0, 0)}

    _directionsAsList = _directions.items()

    def directionToVector(direction, speed = 1.0):
        #print "Actions in vector, ", direction
        dx, dy =  Actions._directions[direction]
        return (dx * speed, dy * speed)
    directionToVector = staticmethod(directionToVector)



class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]


    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newScore = successorGameState.getScore()

        #active ghosts
        active_ghosts = []
        for ghost in newGhostStates:
            if ghost.scaredTimer == 0:
                active_ghosts.append(ghost.getPosition())
        active_ghosts_dist = []
        if len(active_ghosts)>0:
            for i in range(len(active_ghosts)):
                active_ghosts_dist.append(util.manhattanDistance(active_ghosts[i], newPos))
            ghost_score = min(active_ghosts_dist)
        else:
            ghost_score = 0

        dist_food = []
        food_list = newFood.asList()
        food_num = successorGameState.getNumFood()
        if len(food_list) > 0:
            for i in range(len(food_list)):
                dist_food.append(util.manhattanDistance(food_list[i], newPos))
            food_score = min(dist_food)
        else:
            food_score = 0
        food_score +=(10*food_num)




        return (newScore + ghost_score - food_score)

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """


    def getValue(self, state, curr_depth, agent):
        if agent ==0:
            value = float("-inf")
        else:
            value = float("inf")

        if curr_depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        else:
            for move in state.getLegalActions(agent):
                next_pos = state.generateSuccessor(agent, move)
                if agent==0:
                    value = max(value, self.getValue(next_pos, curr_depth, 1))
                elif agent !=0: #min
                    if agent == (state.getNumAgents() - 1):
                        value = min(value, self.getValue(next_pos, curr_depth + 1, 0))
                    else:
                        value = min(value, self.getValue(next_pos, curr_depth, agent + 1))
        return value

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        maxValue = float("-inf")
        maxAction = None
        for move in gameState.getLegalActions(0):
            next_pos = gameState.generateSuccessor(0, move)
            next_val = self.getValue(next_pos, 0, 1)
            if next_val > maxValue:
                maxValue = next_val
                maxAction =move
        return maxAction



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getValue(self, state, curr_depth, agent, alpha, beta):
        if agent == 0:
            value = float("-inf")
        else:
            value = float("inf")

        if curr_depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        else:
            for move in state.getLegalActions(agent):
                next_pos = state.generateSuccessor(agent, move)
                if agent == 0:
                    value = max(value, self.getValue(next_pos, curr_depth, 1, alpha, beta))

                    if value >= beta:
                        return value
                    alpha = max(alpha, value)
                elif agent != 0:  # min
                    if agent == (state.getNumAgents() - 1):
                        value = min(value, self.getValue(next_pos, curr_depth + 1, 0, alpha, beta))

                        if value <= alpha:
                            return value
                        beta = min(beta, value)

                    else:
                        value = min(value, self.getValue(next_pos, curr_depth, agent + 1, alpha, beta))


                        if value <=alpha:
                            return value
                        beta = min(beta, value)
        return value



    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        maxValue = float("-inf")
        maxAction = None
        alpha = float("-inf")
        beta = float("inf")
        for move in gameState.getLegalActions(0):
            next_pos = gameState.generateSuccessor(0, move)
            next_val = self.getValue(next_pos, 0, 1, alpha,beta)
            if next_val > maxValue:
                maxValue = next_val
                maxAction =move
            if maxValue >= beta:
                return maxValue
            alpha = max(alpha, maxValue)


        return maxAction



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectNode(self, state, curr_depth, agent, value, next_pos):
        cnt = 0
        if agent == (state.getNumAgents() - 1):
            value +=(self.getValue(next_pos, curr_depth + 1, 0))
            cnt +=1

        else:
            value +=(self.getValue(next_pos, curr_depth, agent + 1))
            cnt += 1
        return  value/cnt

    def getValue(self, state, curr_depth, agent):
        if agent ==0:
            value = float("-inf")
        else:
            value = 0

        if curr_depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        else:
            for move in state.getLegalActions(agent):
                next_pos = state.generateSuccessor(agent, move)
                if agent==0:
                    value = max(value, self.getValue(next_pos, curr_depth, 1))
                elif agent !=0: #min
                    value = self.expectNode(state, curr_depth, agent, value, next_pos)

        return value

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        maxValue = float("-inf")
        maxAction = None
        for move in gameState.getLegalActions(0):
            next_pos = gameState.generateSuccessor(0, move)
            next_val = self.getValue(next_pos, 0, 1)
            if next_val > maxValue:
                maxValue = next_val
                maxAction =move
        return maxAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"


    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newScore = currentGameState.getScore()
    num_cap = len(currentGameState.getCapsules())


    if currentGameState.isLose():
        return float("-inf")
    elif currentGameState.isWin():
        return float("inf")

    dist_food = []
    food_list = newFood.asList()
    food_num = currentGameState.getNumFood()


    if len(food_list) > 0:
        for i in range(len(food_list)):
            dist_food.append(util.manhattanDistance(food_list[i], newPos))
        sorted(dist_food)


        food_score = min(dist_food)
    else:
        food_score = 0

    #if len(food_list) == 1:
    #    food_score = -1000
    #if len(dist_food) > 1:
    #    if dist_food[0] == dist_food[1]:
    #        food_score =1000
    ###ghost
    active_ghosts = []
    scared_ghosts = []
    for ghost in newGhostStates:
        if ghost.scaredTimer == 0:
            active_ghosts.append(ghost.getPosition())
        else:
            scared_ghosts.append(ghost.getPosition())

    active_ghosts_dist = []
    scared_ghosts_dist = []
    closet_active = float("inf")

    closet_scared = 0
    if len(active_ghosts) > 0:
        for i in range(len(active_ghosts)):
            active_ghosts_dist.append(util.manhattanDistance(active_ghosts[i], newPos))
        closet_active = min(active_ghosts_dist)
    else:
        closet_active = float("inf")

    if len(scared_ghosts) >0:
        for i in range(len(scared_ghosts)):
            scared_ghosts_dist.append(util.manhattanDistance(scared_ghosts[i], newPos))
        closet_scared = min(scared_ghosts_dist)

    return (- 1.5*food_score - 2*(1.0/closet_active) - 2*closet_scared + 2*newScore- 20*num_cap -5*food_num)
# Abbreviation
better = betterEvaluationFunction

