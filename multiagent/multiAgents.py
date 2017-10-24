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
    def countFood(self, food, newPos):
        cnt = 0
        pi = newPos[0]
        pj = newPos[1]
        if pi<len(food[0]) and pj < len(food[1]):
            if food[pi + 1][pj+1]:
                cnt+=1
        if pi >=1 and pj >=1:
            if food[pi-1][pj-1]:
                cnt+=1
        if pi<len(food[0])-1 and pj >=1:
            if food[pi+1][pj-1]:
                cnt +=1
        if pi >= 1 and pj < len(food[0]) - 1:
            if food[pi- 1][pj+1]:
                cnt+=1

        return cnt
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
        numFood = self.countFood(newFood, newPos)
        #print "NEW FOOD",newFood
        #print "type",newFood[0][0]
        "*** YOUR CODE HERE ***"
        return (successorGameState.getScore() + numFood)

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
    #
    # def getValue(self, state, curr_depth, agent, alpha, beta):
    #
    #     if curr_depth == self.depth or state.isWin() or state.isLose():
    #         return self.evaluationFunction(state)
    #     elif agent == 0:
    #         value = self.max_agent(state, curr_depth, agent, alpha, beta)
    #         return value
    #     else:
    #         value = self.min_agent(state, curr_depth, agent, alpha, beta)
    #         return value

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
                elif agent != 0:  # min
                    if agent == (state.getNumAgents() - 1):
                        value = min(value, self.getValue(next_pos, curr_depth + 1, 0, alpha, beta))
                        if value >= beta:
                            return value
                        alpha = max(alpha, value)
                    else:
                        value = min(value, self.getValue(next_pos, curr_depth, agent + 1, alpha, beta))
                        if value <=alpha:
                            return value
                        beta = min(beta, value)
        return value

    def max_agent(self, state,  curr_depth, agent, alpha, beta):
        maxvalue = float("-inf")
        for move in state.getLegalActions(agent):
            next_pos = state.generateSuccessor(agent, move)
            maxvalue = max(maxvalue, self.getValue(next_pos, curr_depth, 1, alpha, beta))
            if maxvalue > alpha:
                alpha = maxvalue
            if alpha > beta:
                #print "prune alpha bete", alpha, beta
                return alpha
            #print "no prune alpha bete", alpha, beta



        return maxvalue

    def min_agent(self, state, curr_depth, agent, alpha, beta):
        minvalue = float("inf")
        for move in state.getLegalActions(agent):
            if agent == (state.getNumAgents() - 1):
                next_pos = state.generateSuccessor(agent, move)
                minvalue = min(minvalue, self.getValue(next_pos, curr_depth + 1, 0, alpha, beta))

            else:
                next_pos = state.generateSuccessor(agent, move)
                minvalue = min(minvalue, self.getValue(next_pos, curr_depth, agent + 1, alpha, beta))
            if minvalue < beta:
                beta = minvalue

            if beta < alpha:
                #print "prune alpha bete", alpha, beta

                return beta
            #print "no prune alpha bete", alpha, beta

        return minvalue

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
        return maxAction



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectNode(self, state, curr_depth, agent, value, next_pos):
        if agent == (state.getNumAgents() - 1):
            value += self.getValue(next_pos, curr_depth + 1, 0)

        else:
            value += self.getValue(next_pos, curr_depth, agent + 1)

        return value

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
    """ 
    def getValue(self, state, curr_depth, agent):
        maxvalue = float("-inf")
        minvalue = 0

        if curr_depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        elif agent == 0:#max

            for move in state.getLegalActions(agent):
                next_pos = state.generateSuccessor(agent, move)
                maxvalue = max(maxvalue, self.getValue(next_pos, curr_depth, 1))

            return maxvalue

        else:

            for move in state.getLegalActions(agent):
                if agent == (state.getNumAgents() - 1):
                    next_pos = state.generateSuccessor(agent, move)
                    minvalue += self.getValue(next_pos, curr_depth +1 , 0)
                else:
                    next_pos = state.generateSuccessor(agent, move)
                    minvalue +=self.getValue(next_pos, curr_depth, agent + 1)
            return float(minvalue/(agent))
    """
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
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

