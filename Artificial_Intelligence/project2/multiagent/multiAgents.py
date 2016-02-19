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
import math
import math

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
        capsuleLocation=successorGameState.getCapsules()

        "*** YOUR CODE HERE ***"

        score=0
        for x in newGhostStates:
            temp=abs(newPos[0]- x.getPosition()[0])+abs(newPos[1]- x.getPosition()[1])
            if temp!=0:
                score+=1/float(temp)


        if len(capsuleLocation)>0:
            capScore=abs(newPos[0]-capsuleLocation[0][0])+abs(newPos[1]-capsuleLocation[0][1])

            for x in capsuleLocation:
                temp=x
                tempScore=abs(newPos[0]-temp[0])+abs(newPos[1]-temp[1])
                if capScore>tempScore:
                    capScore=tempScore
        else:
            capScore=0



        if capScore!=0:
            capScore=1/float(capScore)

        foodDistance=0
        xPosition=0
        yPosition=0
        for x in newFood:
            yPosition=0
            for y in x:
                if y==True:
                    foodDist=abs(newPos[0]-xPosition)+abs(newPos[1]-yPosition)
                    if foodDist!=0:
                        foodDist=1/float(foodDist)
                    foodDistance=foodDistance+foodDist
                    #foodDistance.add(foodDist)
                yPosition=yPosition+1
            xPosition=xPosition+1

        if foodDistance==0:
            reciFood=0
        else:
            reciFood=(foodDistance)


        capState=True
        for x in newScaredTimes:
            if x==0:
                capState=False
                break

        if capState:
            score=score-capScore



        return (successorGameState.getScore()+reciFood-score)

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()
    #return betterEvaluationFunction(currentGameState)

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
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState)


    def minimax(self,gameState):
        moves=gameState.getLegalActions()
        agent=0
        best_move=None
        best_score=float('-inf')
        depth=self.depth
        for move in moves:
            clone = gameState.generateSuccessor(agent,move)
            score=self.min_play(clone,depth,agent)

            if score>best_score:
                best_move=move
                best_score=score
        return best_move

    def min_play(self,gameState,depth,agent):

        if gameState.isLose():
            return scoreEvaluationFunction(gameState)

        if gameState.isWin():
            return scoreEvaluationFunction(gameState)

        if depth==0:
            return scoreEvaluationFunction(gameState)

        if agent<gameState.getNumAgents()-1:
            agent=agent+1
        else:
            agent=0

        moves=gameState.getLegalActions(agent)
        best_score=float('inf')
        for move in moves:
            clone=gameState.generateSuccessor(agent,move)
            ghostCount=gameState.getNumAgents()-1
            if (agent<ghostCount):
                score=self.min_play(clone,depth,agent)
            else:
                score=self.max_play(clone,depth-1,agent)

            if score<best_score:
                best_move = move
                best_score = score
        return best_score

    def max_play(self,gameState,depth,agent):

        if gameState.isLose():
            return scoreEvaluationFunction(gameState)

        if gameState.isWin():
            return scoreEvaluationFunction(gameState)

        if depth==0:
            return scoreEvaluationFunction(gameState)
        if agent<gameState.getNumAgents()-1:
            agent=agent+1
        else:
            agent=0
        moves=gameState.getLegalActions(agent)
        best_score=float('-inf')
        for move in moves:
            clone=gameState.generateSuccessor(agent,move)
            score=self.min_play(clone,depth,agent)
            if score>best_score:
                best_move=move
                best_score=score
        return best_score

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        return self.alphaBetaMinimax(gameState)




    def alphaBetaMinimax(self,gameState):
        moves=gameState.getLegalActions()
        agent=0
        best_move=None
        best_score=float('-inf')
        depth=self.depth
        alpha=float('-inf')
        beta=float('inf')
        for move in moves:
            clone = gameState.generateSuccessor(agent,move)
            score=self.min_play(clone,depth,agent,alpha,beta)

            if score>best_score:
                best_move=move
                best_score=score

            if best_score>beta:
                return best_score
            alpha=max(alpha,best_score)
        return best_move

    def min_play(self,gameState,depth,agent,alpha,beta):

        if gameState.isLose():
            return scoreEvaluationFunction(gameState)
        if gameState.isWin():
            return scoreEvaluationFunction(gameState)
        if depth==0:
            return scoreEvaluationFunction(gameState)

        if agent<gameState.getNumAgents()-1:
            agent=agent+1
        else:
            agent=0

        moves=gameState.getLegalActions(agent)
        best_score=float('inf')
        for move in moves:
            clone=gameState.generateSuccessor(agent,move)
            ghostCount=gameState.getNumAgents()-1
            if (agent<ghostCount):
                score=self.min_play(clone,depth,agent,alpha,beta)
            else:
                score=self.max_play(clone,depth-1,agent,alpha,beta)

            if score<best_score:
                best_move = move
                best_score = score
            if best_score<alpha:
                return best_score
            beta=min(beta,best_score)
        return best_score

    def max_play(self,gameState,depth,agent,alpha,beta):

        if gameState.isLose():
            return scoreEvaluationFunction(gameState)

        if gameState.isWin():
            return scoreEvaluationFunction(gameState)

        if depth==0:
            return scoreEvaluationFunction(gameState)
        if agent<gameState.getNumAgents()-1:
            agent=agent+1
        else:
            agent=0
        moves=gameState.getLegalActions(agent)
        best_score=float('-inf')
        for move in moves:
            clone=gameState.generateSuccessor(agent,move)
            score=self.min_play(clone,depth,agent,alpha,beta)
            if score>best_score:
                best_move=move
                best_score=score
            if best_score>beta:
                return best_score
            alpha=max(alpha,best_score)
        return best_score

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
        return self.expectimax(gameState)

    def expectimax(self,gameState):
        moves=gameState.getLegalActions()
        agent=0
        best_move=None
        best_score=float('-inf')
        depth=self.depth
        for move in moves:
            clone = gameState.generateSuccessor(agent,move)
            score=self.min_play(clone,depth,agent)

            if score>best_score:
                best_move=move
                best_score=score
        return best_move

    def min_play(self,gameState,depth,agent):

        if gameState.isLose():
            return scoreEvaluationFunction(gameState)

        if gameState.isWin():
            return scoreEvaluationFunction(gameState)

        if depth==0:
            return scoreEvaluationFunction(gameState)

        if agent<gameState.getNumAgents()-1:
            agent=agent+1
        else:
            agent=0

        moves=gameState.getLegalActions(agent)
        totalScore=0
        availableMoves=len(moves)
        for move in moves:
            clone=gameState.generateSuccessor(agent,move)
            ghostCount=gameState.getNumAgents()-1
            if (agent<ghostCount):
                score=self.min_play(clone,depth,agent)
            else:
                score=self.max_play(clone,depth-1,agent)

            totalScore=totalScore+score

        return float(totalScore)/float(availableMoves)

    def max_play(self,gameState,depth,agent):

        if gameState.isLose():
            return scoreEvaluationFunction(gameState)

        if gameState.isWin():
            return scoreEvaluationFunction(gameState)

        if depth==0:
            return scoreEvaluationFunction(gameState)
        if agent<gameState.getNumAgents()-1:
            agent=agent+1
        else:
            agent=0
        moves=gameState.getLegalActions(agent)
        best_score=float('-inf')
        for move in moves:
            clone=gameState.generateSuccessor(agent,move)
            score=self.min_play(clone,depth,agent)
            if score>best_score:
                best_move=move
                best_score=score
        return best_score

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    capsuleLocation=successorGameState.getCapsules()

    "*** YOUR CODE HERE ***"

    score=0
    for x in newGhostStates:
        temp=abs(newPos[0]- x.getPosition()[0])+abs(newPos[1]- x.getPosition()[1])
        if temp!=0:
            score+=1/float(temp)


    if len(capsuleLocation)>0:
        capScore=abs(newPos[0]-capsuleLocation[0][0])+abs(newPos[1]-capsuleLocation[0][1])

        for x in capsuleLocation:
            temp=x
            tempScore=abs(newPos[0]-temp[0])+abs(newPos[1]-temp[1])
            if capScore>tempScore:
                capScore=tempScore
    else:
        capScore=0



    if capScore!=0:
        capScore=1/float(capScore)

    foodDistance=0
    xPosition=0
    yPosition=0
    for x in newFood:
        yPosition=0
        for y in x:
            if y==True:
                foodDist=abs(newPos[0]-xPosition)+abs(newPos[1]-yPosition)
                if foodDist!=0:
                    foodDist=1/float(foodDist)
                foodDistance=foodDistance+foodDist
                #foodDistance.add(foodDist)
            yPosition=yPosition+1
        xPosition=xPosition+1

    if foodDistance==0:
        reciFood=0
    else:
        reciFood=(foodDistance)


    capState=True
    for x in newScaredTimes:
        if x==0:
            capState=False
            break

    if capState:
        score=score-capScore



    return (successorGameState.getScore()+reciFood-score)

# Abbreviation
better = betterEvaluationFunction

