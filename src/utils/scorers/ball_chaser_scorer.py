from utils.scorers.scorer import StateScorer
import utils.vector as vector

class Scorer(StateScorer):
    """Scores the state such that bots are rewarded for being closer to the ball
    while punishing bots the closer enemies get to the ball."""
    def score(self, state):
        s = 0
        # reward for drones being closer
        for car in state.drones:
            s -= (state.ball.location-car.location).mag()
        # reward for enemies being farther
        for car in state.enemies:
            s += (state.ball.location-car.location).mag()
        return  s
