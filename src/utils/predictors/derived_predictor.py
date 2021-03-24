from utils.predictors.predictor import StatePredictor
from math import sin, cos, pi
import numpy as np

class Predictor(StatePredictor):
    """Updates the state by using hand derived approximate models of the physics."""
    def predict(self, state, actions, dt):
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
            yaw += action[3] * (1 + 0.025 * action[6] + 0.25 * action[7] * action[1] * action[0]) * np.linalg.norm(vel) / 1000 * dt
            pitch += action[2] * (1 + 0.025 * action[6]) * np.linalg.norm(vel) / 1000 * dt
            roll += action[4] * (1 + 0.025 * action[6]) * np.linalg.norm(vel) / 1000 * dt
            yaw = (yaw + pi) % (2 * pi) - pi
            pitch = (pitch + pi) % pi - pi/2
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
            forward[2] = 0;
            up = np.squeeze(np.asarray(np.matmul(rmat,np.array([0,0,1]))))
            right = np.squeeze(np.asarray(np.matmul(rmat,np.array([0,1,0]))))
            vel += (action[0] - action[7] + action[6]) * (forward + 0.25 * action[1] * right) * dt * 500
            m = np.linalg.norm(vel)
            if m >= 2350:
                vel *= 2350 / m
            # update position
            pos += vel * dt
        # predict ball location
        next_state[:3] += next_state[3:6] * dt
        return next_state
