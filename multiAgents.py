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
import math

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

        # helps prevent looping
        if Directions.STOP in [legalMoves[index] for index in bestIndices]:
            return random.choice(legalMoves)
        else:
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

        newFood = newFood.asList() + successorGameState.getCapsules()
        oldPos = currentGameState.getPacmanPosition()
        oldFood = currentGameState.getFood().asList() + currentGameState.getCapsules()
        oldGhostStates = currentGameState.getGhostStates()

        if successorGameState.isLose():
            return -10

        # gets distance of closest ghost in old state
        oldGhost = None
        oldGhostDist = None
        for ghost in oldGhostStates:
            ghostDist = manhattanDistance(ghost.getPosition(), oldPos)
            if oldGhostDist is None or ghostDist < oldGhostDist:
                oldGhost = ghost
                oldGhostDist = ghostDist
        # if closest ghost is 'scared', distance is inverted so Pacman is attracted
        if oldGhost is not None and oldGhost.scaredTimer != 0:
            oldGhostDist = oldGhostDist * -1

        # gets distance of closest ghost in new state
        newGhost = None
        newGhostDist = None
        for ghost in newGhostStates:
            ghostDist = manhattanDistance(ghost.getPosition(), newPos)
            if newGhostDist is None or ghostDist < newGhostDist:
                newGhost = ghost
                newGhostDist = ghostDist
        # if closest ghost is 'scared', distance is inverted so Pacman is attracted to ghost
        if newGhost is not None and newGhost.scaredTimer != 0:
            newGhostDist = newGhostDist * -1

        # gScore is score based on distance from ghost, higher is better
        gScore = 0
        if newGhostDist and oldGhostDist:
            gScore = newGhostDist - oldGhostDist

        # gScorePriority weights gScore depending on distance from nearest ghost
        # if nearest ghost is not 'scared'
        if newGhostDist and newGhostDist > 0:
            # non-linear for extreme avoidance if ghost is closer, and less if ghost is far away
            # numerator is distance when ghost avoidance is more important than food, must be > 2
            gScorePriority = 4 / newGhostDist
        else:
            # attraction to 'scared' ghost equal to food attraction
            gScorePriority = 1

        # fScore is score based on distance from food, higher is better
        # if Pacman has not reached food
        if not len(oldFood) > len(newFood):
            # closest food distance in old state
            oldFoodDist = None
            for food in oldFood:
                foodDist = manhattanDistance(food, oldPos)
                if oldFoodDist is None or foodDist < oldFoodDist:
                    oldFoodDist = foodDist
            # closest food distance in new state
            newFoodDist = None
            for food in newFood:
                foodDist = manhattanDistance(food, newPos)
                if newFoodDist is None or foodDist < newFoodDist:
                    newFoodDist = foodDist
            fScore = oldFoodDist - newFoodDist
        # if pacman has reached food
        else:
            # value of 2 is greater than any fScore if food had not been reached
            fScore = 2

        return fScore + gScore * gScorePriority

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # returns the action selected by the minimax algorithm
        return self.minimax(gameState, 0)[1]

    def minimax(self, gameState, depth):
        """ Minimax recursive algorithm for getAction """

        numAgents = gameState.getNumAgents()

        # 0 specifies Pacman, non-0 represents a ghost
        agent = depth % numAgents

        # termination condition if game ends or depth limit is reached
        if gameState.isWin() or gameState.isLose() or depth == self.depth * numAgents:
            return self.evaluationFunction(gameState), None

        # recursive call gets score for each legal action
        successors = []
        actions = gameState.getLegalActions(agent)
        for action in actions:
            score = self.minimax(gameState.generateSuccessor(agent, action), depth + 1)[0]
            successors.append((score, action))

        # for Pacman (maximizing player)
        if agent == 0:
            successor = max(successors)

        # for ghosts (minimizing player)
        else:
            successor = min(successors)

        return successor


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # returns the action selected by the minimax algorithm
        return self.alphaBeta(gameState, 0, math.inf * -1, math.inf)[1]

    def alphaBeta(self, gameState, depth, alpha, beta):
        """ Minimax recursive algorithm with alpha-beta pruning for getAction """

        numAgents = gameState.getNumAgents()

        # 0 specifies Pacman, non-0 represents a ghost
        agent = depth % numAgents

        # termination condition if game ends or depth limit is reached
        if gameState.isWin() or gameState.isLose() or depth == self.depth * numAgents:
            return self.evaluationFunction(gameState), None

        actions = gameState.getLegalActions(agent)
        successor = None

        # for Pacman (maximizing player)
        if agent == 0:
            for action in actions:
                score = self.alphaBeta(gameState.generateSuccessor(agent, action), depth + 1, alpha, beta)[0]
                current = score, action
                if successor:
                    successor = max(successor, current)
                else:
                    successor = current
                # beta cut-off
                alpha = max(alpha, successor[0])
                if beta < alpha:
                    break

        # for ghosts (minimizing player)
        else:
            for action in actions:
                score = self.alphaBeta(gameState.generateSuccessor(agent, action), depth + 1, alpha, beta)[0]
                current = score, action
                if successor:
                    successor = min(successor, current)
                else:
                    successor = current
                # alpha cut-off
                beta = min(successor[0], beta)
                if beta < alpha:
                    break

        return successor


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        # returns the action selected by the expectimax algorithm
        return self.expectimax(gameState, 0)[1]

    def expectimax(self, gameState, depth):
        """ Expectimax recursive algorithm for getAction """

        numAgents = gameState.getNumAgents()

        # 0 specifies Pacman, non-0 represents a ghost
        agent = depth % numAgents

        # termination condition if game ends or depth limit is reached
        if gameState.isWin() or gameState.isLose() or depth == self.depth * numAgents:
            return self.evaluationFunction(gameState), None

        actions = gameState.getLegalActions(agent)

        # for Pacman (maximizing player)
        if agent == 0:
            successor = None
            for action in actions:
                score = self.expectimax(gameState.generateSuccessor(agent, action), depth + 1)[0]
                current = score, action
                if successor:
                    successor = max(successor, current)
                else:
                    successor = current
            return successor

        # for ghosts (chance player)
        else:
            netScore = 0
            for action in actions:
                netScore += self.expectimax(gameState.generateSuccessor(agent, action), depth + 1)[0]
            # gets average score, assuming ghosts select action randomly
            score = netScore / len(actions)
            return score, None

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: State evaluated on distance to closest food,
                 number of remaining foods (priority 2x food dist),
                 and average distance from ghost (priority grows exponentially:
                 far ghost < food dist, close ghost > remaining foods)
    """
    "*** YOUR CODE HERE ***"

    position = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList() + currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()

    # addition of game score prevents Pacman stagnation
    if currentGameState.isLose():
        return -100000 + currentGameState.getScore()
    elif currentGameState.isWin():
        return 100000 + currentGameState.getScore()

    # gScore is score based on distance from ghosts, higher is better
    gScore = 0
    for ghost in ghostStates:
        ghostDist = manhattanDistance(ghost.getPosition(), position)
        # non-linear for extreme avoidance if ghost is closer, and less if ghost is far away
        # numerator is distance when ghost avoidance is more important than food, must be > 2
        if ghost.scaredTimer == 0:
            gScore -= 4 / ghostDist
        # attraction to 'scared' ghost equal to food attraction
        else:
            foods += [ghost.getPosition()]
    gScore = gScore / len(ghostStates)

    # fScore is score based on distance from closest food and remaining food
    fScore = -len(foods)
    fScore += 1/min([manhattanDistance(position, food) for food in foods])

    return gScore + fScore + currentGameState.getScore()


# Abbreviation
better = betterEvaluationFunction