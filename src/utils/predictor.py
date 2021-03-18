from abc import ABC, abstractmethod
from typing import List
import numpy as np
from math import sin, cos, pi

### THIS FILE CONTAINS CODE CLASSES OF DEVELOPED STATE PREDICTORS
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

class DerivedStatePredictor(StatePredictor):
    """Updates the state by using hand derived approximate models of the physics."""
    def predict(self, state: np.ndarray, actions: List[np.ndarray], dt: float) -> np.ndarray:
        next_state = state.copy()
        # TODO: derive physics model and add code here to predict state update
        # note the following implementation may be very wrong,
        # I simply tried random things until it worked
        # iterate through each bot and enemy
        for i, action in enumerate(actions):
            # get current values
            pitch = next_state[18+3*i]
            yaw = next_state[19+3*i]
            roll = next_state[20+3*i]
            pos = next_state[6+3*i:9+3*i]
            vel = next_state[12+3*i:15+3*i]
            # update rotation
            yaw += action[3] * (1 + 0.025 * action[6]) * np.linalg.norm(vel) / 1000 * dt
            pitch += action[2] * (1 + 0.025 * action[6]) * np.linalg.norm(vel) / 1000 * dt
            roll += action[4] * (1 + 0.025 * action[6]) * np.linalg.norm(vel) / 1000 * dt
            yaw = (yaw + pi) % (2 * pi) - pi
            pitch = (pitch + pi) % (2 * pi) - pi
            roll = (roll + pi) % (2 * pi) - pi
            next_state[18+3*i] = pitch
            next_state[19+3*i] = yaw
            next_state[20+3*i] = roll
            # update velocity
            cp = cos(pitch)
            cy = cos(yaw)
            cr = cos(roll)
            sp = sin(pitch)
            sy = sin(yaw)
            sr = sin(roll)
            rmat = np.matrix([[cp*cy, cy*sp*sr-cr*sy, -cr*cy*sp-sr*sy],
                [cp*sy, cr*cy+sp*sr*sy, cy*sr-cr*sp*sy],[sp, -cp*sr, cp*cr]])
            forward = np.squeeze(np.asarray(np.matmul(rmat,np.array([1,0,0]))))
            dir = np.squeeze(np.asarray(np.matmul(rmat,np.array([0,0,1]))))
            dir += np.squeeze(np.asarray(np.matmul(rmat,np.array([0,1,0])))) * action[1]
            dir += forward * action[0]
            m = np.linalg.norm(dir)
            if m > 0:
                dir /= m
            vel += (action[0] + action[6]/100) * forward * 1000 + action[5] * dir * 100
            m = np.linalg.norm(vel)
            if m >= 2350:
                vel *= 2350 / m
            # update position
            pos += vel * dt
        # predict ball location
        next_state[:3] += next_state[3:6] * dt
        return next_state
