# valueIterationAgents.py
# -----------------------
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


import mdp, util, random


from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.states=mdp.getStates()
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"


        for state in self.states:
            self.values[state]=0

        while self.iterations>0:
            tempValues=util.Counter()
            for state in self.states:
                if not self.mdp.isTerminal(state):
                    actions=self.mdp.getPossibleActions(state)
                    valueAction=util.Counter()
                    for action in actions:
                        valueAction[action]=self.getQValue(state,action)
                    tempValues[state]=valueAction[valueAction.argMax()]
            self.values=tempValues
            self.iterations=self.iterations-1






    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        transitionStates=self.mdp.getTransitionStatesAndProbs(state, action)
        qValue=0

        for tState in transitionStates:
            nextState=tState[0]
            prob=tState[1]
            actionValue = self.mdp.getReward(state, action, nextState)
            nextActionValue=self.getValue(nextState)*self.discount
            qValue=qValue+(actionValue+nextActionValue)*prob

        return qValue
        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        #util.raiseNotDefined()

        if self.mdp.isTerminal(state):
            return None
        else:
            actions=self.mdp.getPossibleActions(state)
            valueAction=util.Counter()
            for action in actions:
                valueAction[action]=self.getQValue(state,action)
            x= valueAction.argMax()

            return x


            #action=mdp.getPossibleActions(state)
            #transitionState=mdp.getTransitionStatesAndProbs(state, action)


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
