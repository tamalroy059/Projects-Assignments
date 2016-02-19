# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.qValueTable=util.Counter()


    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        return self.qValueTable[state,action]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        valueAction=util.Counter()

        actions=self.getLegalActions(state)
        for action in actions:
            valueAction[action]=self.getQValue(state,action)
        return valueAction[valueAction.argMax()]

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        """
        valueAction=util.Counter()

        actions=self.getLegalActions(state)
        for action in actions:
            valueAction[action]=self.getQValue(state,action)
        return valueAction.argMax()
        """
        legalActions=self.getLegalActions(state)
        valueAction=util.Counter()
        unexplored=[]
        explored=[]

        for action in legalActions:
            valueAction[action]=self.getQValue(state,action)
            if self.qValueTable[state,action]==0:
                unexplored.append(action)
            else:
                explored.append(action)


        if len(explored)==0:
            action=random.choice(unexplored)
            return action
        if len(unexplored)>0:
            action=random.choice(unexplored)
            return action
        i=0

        negativeQvalue=0

        while i<len(explored):
            temp=self.getQValue(state,explored[i])
            valueAction[explored[i]]=temp
            if temp<0:
                negativeQvalue+=1
            i=i+1

        if negativeQvalue==len(explored) & len(unexplored)>0:
            action=random.choice(unexplored)
            return action

        action=valueAction.argMax()

        return action
        #util.raiseNotDefined()

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)


        action = None
        chance=util.flipCoin(self.epsilon)

        if chance:
            action=random.choice(legalActions)
        else:
            valueActions=util.Counter()
            for nAction in legalActions:
                valueActions[nAction]=self.getQValue(state,nAction)
            action=valueActions.argMax()

        return action

        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        """
        self.setEpsilon(self.epsilon*.9)

        unexplored=[]
        explored=[]
        for action in legalActions:
            if self.qValueTable[state,action]==0:
                unexplored.append(action)
            else:
                explored.append(action)

        ep=self.epsilon

        chance=util.flipCoin(self.epsilon)

        if len(explored)==0:
            action=random.choice(unexplored)
            return action
        if len(unexplored)>0 & chance:
            action=random.choice(unexplored)
            return action


        i=0

        valueAction=util.Counter()

        negativeQvalue=0

        while i<len(explored):
            temp=self.getQValue(state,explored[i])
            valueAction[explored[i]]=temp
            if temp<0:
                negativeQvalue+=1
            i=i+1

        if negativeQvalue==len(explored) & len(unexplored)>0:
            action=random.choice(unexplored)
            return action

        action=valueAction.argMax()
        """


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        sampleNew=reward+ (self.discount*self.computeValueFromQValues(nextState))
        self.qValueTable[state,action]=((1-self.alpha)*self.qValueTable[state,action])+(self.alpha*sampleNew)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)

        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()



    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        featureVector=self.featExtractor.getFeatures(state,action)
        items=featureVector.items()
        total=0
        for feature in items:
            val=self.weights[feature[0]]*feature[1]
            total=total+val
        return total
        #util.raiseNotDefined()


    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        actualVal=reward+ (self.discount*self.computeValueFromQValues(nextState))
        assumedVal=self.getQValue(state,action)
        difference=actualVal-assumedVal

        featureVector=self.featExtractor.getFeatures(state,action)
        items=featureVector.items()
        total=0
        for feature in items:
            weight=self.weights[feature[0]]
            weight=weight+self.alpha*difference*feature[1]
            self.weights[feature[0]]=weight

        #util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
