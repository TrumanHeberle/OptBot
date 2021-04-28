from utils.scorers.scorer import StateScorer

class Scorer(StateScorer):
    """Scores the state such that bots are rewarded for being closer to the ball
    while punishing bots the closer enemies get to the ball."""
    def score(self, state):
        s = 0
        # reward for drones being closer
        for i in state.drones:
            car = state.drones[i]
            s -= (state.ball.location-car.location).mag()
        # reward for enemies being farther
        for i in state.enemies:
            car = state.enemies[i]
            s += (state.ball.location-car.location).mag()
        return  s
