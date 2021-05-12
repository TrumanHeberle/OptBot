from utils.scorers.scorer import StateScorer
from utils.vector import Vector
from math import sin, pi

X = 0
Y = 5120
Z = 321
ENEMY_NET = Vector(X,Y,Z)
DRONE_NET = Vector(X,-Y,Z)
OMEGAC_MAX = 5.5

class Scorer(StateScorer):
    """Scores the state such that bots are rewarded for being closer to the ball
    while punishing bots the closer enemies get to the ball. Also rewards the
    ball being closer to the enemies' net while punishing the ball being closer
    to the drones' net."""
    def score(self, state):
        s = 0
        # reward for drones being closer
        for i in state.drones:
            car = state.drones[i]
            d1 = state.ball.location-car.location
            d2 = DRONE_NET-state.ball.location
            f = Vector(1,0,0).rpy(car.rotation)
            a = f.angle(d1)
            s -= (d1.mag()+d2.mag())*a/sin(a)
        # reward for enemies being farther
        for i in state.enemies:
            car = state.enemies[i]
            d1 = state.ball.location-car.location
            d2 = ENEMY_NET-state.ball.location
            f = Vector(1,0,0).rpy(car.rotation)
            a = f.angle(d1)
            s += (d1.mag()+d2.mag())*a/sin(a)
        # reward ball being farther from drone net
        s += (state.ball.location-ENEMY_NET).mag()
        # reward ball being closer to enemy net
        s -= (state.ball.location-DRONE_NET).mag()
        return  s
