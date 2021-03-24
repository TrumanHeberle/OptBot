from abc import ABC, abstractmethod
import numpy as np

### THIS FILE CONTAINS CODE CLASSES OF DEVELOPED STATE SCORERS
# values of the state variable can be found in state.py

class StateScorer(ABC):
    """This is a base class for a state scorer. All developed state
    scorers developed should inherit from this class."""
    @abstractmethod
    def score(self, state: np.ndarray) -> np.ndarray:
        """Returns a scalar representing the score of a given game state."""
        raise NotImplementedError
