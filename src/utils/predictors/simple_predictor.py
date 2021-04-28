import numpy as np
from utils.predictors.predictor import StatePredictor
from utils.optimizers.simple import solve
from random import random
from utils.state import State

class Predictor(StatePredictor):
    def __init__(self):
        self.A = None
        self.b = None
    def predict(self, state):
        print(state.shape)
        if self.A is None or self.b is None:
            return state+np.random.uniform(-100,100,state.shape)
        return state+self.A@state+self.b
    def train(self, input_states, output_states):
        S1 = np.array(input_states).transpose()
        S2 = np.array(output_states).transpose()
        try:
            B = solve(S1,S2-S1)
            self.A = B[:,:-1]
            self.b = B[:,-1]
            print("adjusted")
        except:
            print("failed")
