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


from multiprocessing import set_forkserver_preload
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        # aka Score
        evalNum = 0

        # Ghost eval
        listOfGhostDist = []
        closestGhost = 0
        for ghost in range(len(newGhostStates)): # range(len()) for indexation
            ghostPos = successorGameState.getGhostPositions()[ghost] # indexation of ghosts
            listOfGhostDist.append(manhattanDistance(newPos, ghostPos))
        if listOfGhostDist != []:
            closestGhost = min(listOfGhostDist) # min distance
        
        # Food eval
        listOfFoodDist = []
        closestFood = 0
        for food in newFood.asList():
            listOfFoodDist.append(manhattanDistance(newPos, food))
        if listOfFoodDist != []:
            closestFood = min(listOfFoodDist) # min distance

        # Capsule eval
        capsules = currentGameState.getCapsules()
        listOfCapsDist = []
        closestCapsule = 0
        for capsule in capsules:
            listOfCapsDist.append(manhattanDistance(newPos, capsule))
        if listOfCapsDist != []:
            closestCapsule = min(listOfCapsDist) # min distance

        # Eval calc
        closestScaredGhostIndex = listOfGhostDist.index(closestGhost)
        foodCost = (1/(closestFood + 1)) + (1/(len(listOfFoodDist) + 1)) # min distance + count (less dots - higher score) conv to <1
        capsuleCost = (1/(closestCapsule + 1)) + (1/(len(listOfCapsDist) + 1)) # same
        ghostCost = (1/(closestGhost + 1)) # min distance conv to <1
        if closestGhost>1:
            evalNum += foodCost + capsuleCost + successorGameState.getScore()
            if newScaredTimes[closestScaredGhostIndex]>1: # if scared --> + ghost cost
                evalNum += ghostCost
            else: # else --> - ghost cost
                evalNum += -ghostCost
        else:
            evalNum = -1 # if too close -- run away
        return evalNum

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def miniMax(agentIndex, gameState, _depth):
            if _depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            # Maximise for pacman (0)
            if agentIndex == 0:
                value = float("-inf")
                actions = gameState.getLegalActions(agentIndex)
                for action in actions:
                    value = max(value, miniMax(1, gameState.generateSuccessor(0, action), _depth))
                return value
            
            # Minimise for ghosts (1)
            else:
                value = float("inf")
                actions = gameState.getLegalActions(agentIndex)
                if (agentIndex == gameState.getNumAgents() -1): # switch between pacman and ghost (0/1)
                    _depth += 1 # depth will inc to depth.self
                    for action in actions:
                        value = min(value, miniMax(0, gameState.generateSuccessor(agentIndex, action), _depth))
                else:
                    for action in actions:
                        value = min(value, miniMax(agentIndex + 1, gameState.generateSuccessor(agentIndex, action), _depth))
                return value
        
        _depth = 0 # depth will inc to depth.self
        actions = gameState.getLegalActions(0) # Pacman actions
        actionQueue = util.PriorityQueue()

        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            value = miniMax(1, successor, _depth) # 1 for ghost -> pacman
            actionQueue.push(action, value)        
        
        # Action with high priority
        while not actionQueue.isEmpty():
            step = actionQueue.pop()

        # return action
        return step

        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def alphaBetaMiniMax(agentIndex, gameState, _depth, alpha, beta):
            if _depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            # Maximise for pacman (0)
            if agentIndex == 0:
                value = float("-inf")
                actions = gameState.getLegalActions(agentIndex)
                for action in actions:
                    value = max(value, alphaBetaMiniMax(1, gameState.generateSuccessor(0, action), _depth, alpha, beta))
                    if value > beta:
                        return value
                    alpha = max(alpha, value)
                return value
            
            # Minimise for ghosts (1)
            else:
                value = float("inf")
                actions = gameState.getLegalActions(agentIndex)
                if (agentIndex == gameState.getNumAgents() -1): # switch between pacman and ghost (0/1)
                    _depth += 1 # depth will inc to depth.self
                    for action in actions:
                        value = min(value, alphaBetaMiniMax(0, gameState.generateSuccessor(agentIndex, action), _depth, alpha, beta))
                        if value < alpha:
                            return value
                        beta = min(beta, value)
                else:
                    for action in actions:
                        value = min(value, alphaBetaMiniMax(agentIndex + 1, gameState.generateSuccessor(agentIndex, action), _depth, alpha, beta))
                        if value < alpha:
                            return value
                        beta = min(beta, value)
                return value
        
        _depth = 0 # depth will inc to depth.self
        actions = gameState.getLegalActions(0) # Pacman actions
        actionQueue = util.PriorityQueue()
        alpha = float("-inf") # initial alpha
        beta = float("inf") # initial beta

        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            value = alphaBetaMiniMax(1, successor, _depth, alpha, beta) # 1 for ghost -> pacman
            if value > beta: # for next iteration (for pacman, because of agentIndex = 1)
                return action
            alpha = max(alpha, value)
            actionQueue.push(action, value)        
        
        # Action with high priority
        while not actionQueue.isEmpty():
            step = actionQueue.pop()

        # return action
        return step

        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectiMax(agentIndex, gameState, _depth):
            if _depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            # Maximise for pacman (0)
            if agentIndex == 0:
                value = float("-inf")
                actions = gameState.getLegalActions(agentIndex)
                for action in actions:
                    value = max(value, expectiMax(1, gameState.generateSuccessor(0, action), _depth))
                return value
            
            # Minimise for ghosts (1)
            else:
                value = 0
                actions = gameState.getLegalActions(agentIndex)
                if (agentIndex == gameState.getNumAgents() -1): # switch between pacman and ghost (0/1)
                    _depth += 1 # depth will inc to depth.self
                    for action in actions: # values sum
                        value += expectiMax(0, gameState.generateSuccessor(agentIndex, action), _depth)
                else:
                    for action in actions: # values sum
                        value += expectiMax(agentIndex + 1, gameState.generateSuccessor(agentIndex, action), _depth)
                return value/len(actions) # avarage value
        
        _depth = 0 # depth will inc to depth.self
        actions = gameState.getLegalActions(0) # Pacman actions
        betterAction = Directions.STOP # initial best action
        bettervalue = float("-inf") # initial better value


        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            value = expectiMax(1, successor, _depth) # 1 for ghost -> pacman
            if value > bettervalue:
                bettervalue = value
                betterAction = action

        # return action
        return betterAction

        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
