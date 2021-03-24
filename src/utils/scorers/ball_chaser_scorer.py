from utils.scorers.scorer import StateScorer
from numpy.linalg import norm

class Scorer(StateScorer):
    """Scores the state such that bots are rewarded for being closer to the ball
    while punishing bots the closer enemies get to the ball."""
    def score(self, state):
        # get ball location
        b = state[:3]
        # score enemies and drones (distance from ball)
        return  norm(b - state[9:12]) - norm(b - state[6:9])
