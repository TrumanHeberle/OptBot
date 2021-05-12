from typing import List, Dict
from numpy import ndarray, asarray
from utils.vector import Vector

class Action(ndarray):
    """Stores information about an action"""
    @staticmethod
    def params_from_input(input):
        """Returns an action list given an RLBot player input"""
        return (input.throttle, input.steer, input.pitch, input.yaw, \
            input.roll, input.jump, input.boost, input.handbrake)
    @staticmethod
    def from_input(input):
        """Returns an action given an RLBot player input"""
        return Action(Action.params_from_input(input))
    def __new__(self, values):
        return asarray(values).view(self)
    @property
    def throttle(self):
        return self[0]
    @throttle.setter
    def throttle(self, val):
        self[0] = val
    @property
    def steer(self):
        return self[1]
    @steer.setter
    def steer(self, val):
        self[1] = val
    @property
    def pitch(self):
        return self[2]
    @pitch.setter
    def pitch(self, val):
        self[2] = val
    @property
    def yaw(self):
        return self[3]
    @yaw.setter
    def yaw(self, val):
        self[3] = val
    @property
    def roll(self):
        return self[4]
    @roll.setter
    def roll(self, val):
        self[4] = val
    @property
    def jump(self):
        return self[5]
    @jump.setter
    def jump(self, val):
        self[5] = val
    @property
    def boost(self):
        return self[6]
    @boost.setter
    def boost(self, val):
        self[6] = val
    @property
    def handbrake(self):
        return self[7]
    @handbrake.setter
    def handbrake(self, val):
        self[7] = val

class BallState(ndarray):
    """Stores information about the current ball state"""
    @staticmethod
    def params_from_packet(ball):
        """Returns a ball state list given an RLBot ball packet"""
        location = ball.location
        velocity = ball.velocity
        angular_velocity = ball.angular_velocity
        return (location.x, location.y, location.z, velocity.x,
            velocity.y, velocity.z, angular_velocity.x, angular_velocity.y,
            angular_velocity.z)
    @staticmethod
    def from_packet(ball):
        """Returns a ball state given an RLBot ball packet"""
        return BallState(BallState.params_from_packet(ball))
    def __new__(self, values):
        return asarray(values).view(self)
    @property
    def location(self):
        return Vector(self[0:3])
    @location.setter
    def location(self, val):
        self[0] = val[0]; self[1] = val[1]; self[2] = val[2]
    @property
    def velocity(self):
        return Vector(self[3:6])
    @velocity.setter
    def velocity(self, val):
        self[3] = val[0]; self[4] = val[1]; self[5] = val[2]
    @property
    def angular_velocity(self):
        return Vector(self[6:9])
    @angular_velocity.setter
    def angular_velocity(self, val):
        self[6] = val[0]; self[7] = val[1]; self[8] = val[2]

class CarState(ndarray):
    """Stores information about the current car state"""
    @staticmethod
    def params_from_packet(car, last_action):
        """Returns a car state list given an RLBot car packet and the last car action"""
        phys = car.physics
        location = phys.location
        velocity = phys.velocity
        rotation = phys.rotation
        angular_velocity = phys.angular_velocity
        return (location.x, location.y, location.z, velocity.x,
            velocity.y, velocity.z, rotation.roll, rotation.pitch, rotation.yaw,
            angular_velocity.x, angular_velocity.y, angular_velocity.z,
            car.jumped, car.double_jumped, *last_action, *last_action)
    @staticmethod
    def from_packet(car, last_action):
        """Returns a car state given an RLBot car packet and the last car action"""
        return CarState(CarState.params_from_packet(car, last_action))
    def __new__(self, values):
        return asarray(values).view(self)
    @property
    def location(self):
        return Vector(self[0:3])
    @location.setter
    def location(self, val):
        self[0] = val[0]; self[1] = val[1]; self[2] = val[2]
    @property
    def velocity(self):
        return Vector(self[3:6])
    @velocity.setter
    def velocity(self, val):
        self[3] = val[0]; self[4] = val[1]; self[5] = val[2]
    @property
    def rotation(self):
        return Vector(self[6:9])
    @rotation.setter
    def rotation(self, val):
        self[6] = val[0]; self[7] = val[1]; self[8] = val[2]
    @property
    def angular_velocity(self):
        return Vector(self[9:12])
    @angular_velocity.setter
    def angular_velocity(self, val):
        self[9] = val[0]; self[10] = val[1]; self[11] = val[2]
    @property
    def jumped(self):
        return self[12]
    @jumped.setter
    def jumped(self, val):
        self[12] = val
    @property
    def double_jumped(self):
        return self[13]
    @double_jumped.setter
    def double_jumped(self, val):
        self[13] = val
    @property
    def last_action(self):
        return Action(self[14:22])
    @last_action.setter
    def last_action(self, val):
        self[14:22] = val
    @property
    def current_action(self):
        return Action(self[22:30])
    @current_action.setter
    def current_action(self, val):
        self[22:30] = val

class State(ndarray):
    """Stores information about the current game state"""
    @staticmethod
    def params_from_packet(packet, drone_actions, enemy_actions):
        ball = BallState.params_from_packet(packet.game_ball.physics)
        drone_indices = [i for i in drone_actions]
        enemy_indices = [i for i in enemy_actions]
        vals = (0,)+ball
        for i in drone_indices:
            vals += CarState.params_from_packet(packet.game_cars[i], drone_actions[i])
        for i in enemy_indices:
            vals += CarState.params_from_packet(packet.game_cars[i], enemy_actions[i])
        return vals, drone_indices, enemy_indices
    @staticmethod
    def from_packet(packet, drone_actions, enemy_actions):
        """Returns a game state given an RLBot packet and previous actions of all players"""
        return State(*State.params_from_packet(packet, drone_actions, enemy_actions))
    def __new__(self, values, drone_indices, enemy_indices):
        self.drone_indices = drone_indices
        self.enemy_indices = enemy_indices
        return asarray(values).view(self)
    @property
    def dt(self):
        return self[0]
    @dt.setter
    def dt(self, val):
        self[0] = val
    @property
    def ball(self):
        return BallState(self[1:10])
    @property
    def drones(self):
        return {i:CarState(self[10+n*30:10+(n+1)*30]) for n,i in enumerate(self.drone_indices)}
    @property
    def enemies(self):
        s = 10+len(self.drone_indices)*30
        return {i:CarState(self[s+n*30:s+(n+1)*30]) for n,i in enumerate(self.enemy_indices)}
