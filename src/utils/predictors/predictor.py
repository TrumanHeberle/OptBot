from abc import ABC, abstractmethod
from typing import List
from rlbot.utils.structures.bot_input_struct import PlayerInput
from utils.state import State

### THIS FILE CONTAINS A TEMPLATE CLASS FOR DEVELOPING STATE PREDICTORS
# values of the state variable can be found in state.py

class StatePredictor(ABC):
    """This is a base class for a state predictor. All developed state
    predictors developed should inherit from this class."""
    @abstractmethod
    def predict(self, state: State, actions: List[List[PlayerInput]], dt: float) -> State:
        """Takes an input state, a 2 lists of the actions for each bot
        (drones, enemies), and a timestep and returns a prediction of the output
        state after the timestep has elapsed."""
        raise NotImplementedError
