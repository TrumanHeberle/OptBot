from abc import ABC, abstractmethod
from typing import List
import numpy as np

### THIS FILE CONTAINS A TEMPLATE CLASS FOR DEVELOPING STATE PREDICTORS
# values of the state variable can be found in state.py

class StatePredictor(ABC):
    """This is a base class for a state predictor. All developed state
    predictors developed should inherit from this class."""
    @abstractmethod
    def predict(self, state: np.ndarray, actions: List[np.ndarray], dt: float) -> np.ndarray:
        """Takes an input state, a list of the actions of each drone, and a
        timestep and returns a prediction of the output state after the
        timestep has elapsed."""
        raise NotImplementedError
