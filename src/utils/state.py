from typing import Set, Dict, List
import numpy as np
from copy import copy
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.structures.bot_input_struct import PlayerInput
from utils.vector import Vector
import utils.constants as C

class CarState(np.ndarray):
    """Stores information about the current car state"""
    def __new__(self, inputs):
        return np.asarray(inputs).view(self)
    @property
    def location(self):
        """car location vector"""
        return Vector(*self[0:3])
    @property
    def velocity(self):
        """car velocity vector"""
        return Vector(*self[3:6])
    @property
    def angular_velocity(self):
        """car angular velocity vector"""
        return Vector(*self[6:9])
    @property
    def rotation(self):
        """car euler rotation angles"""
        return Vector(*self[9:12])
    @property
    def jumped(self):
        """car has jumped"""
        return self[12]
    @property
    def double_jumped(self):
        """car has double jumped"""
        return self[13]
    @property
    def last_action(self):
        """car last choosen action"""
        return PlayerInput(*self[14:22],0)
    @location.setter
    def location(self, value: Vector):
        self[0:3] = list(value)
        return self
    @velocity.setter
    def velocity(self, value: Vector):
        self[3:6] = list(value)
        return self
    @angular_velocity.setter
    def angular_velocity(self, value: Vector):
        self[6:9] = list(value)
        return self
    @rotation.setter
    def rotation(self, value: Vector):
        self[9:12] = list(value)
        return self
    @jumped.setter
    def jumped(self, value: bool):
        self[12] = value
        return self
    @double_jumped.setter
    def double_jumped(self, value: bool):
        self[13] = value
        return self
    @last_action.setter
    def last_action(self, value: PlayerInput):
        self[14] = value.throttle
        self[15] = value.steer
        self[16] = value.pitch
        self[17] = value.yaw
        self[18] = value.roll
        self[19] = value.jump
        self[20] = value.boost
        self[21] = value.handbrake
        return self

class BallState(np.ndarray):
    """Stores information about the current ball state"""
    def __new__(self, inputs):
        return np.asarray(inputs).view(self)
    @property
    def location(self):
        """ball location vector"""
        return Vector(*self[0:3])
    @property
    def velocity(self):
        """ball velocity vector"""
        return Vector(*self[3:6])
    @property
    def angular_velocity(self):
        """ball angular velocity vector"""
        return Vector(*self[6:9])
    @location.setter
    def location(self, value: Vector):
        self[0:3] = list(value)
        return self
    @velocity.setter
    def velocity(self, value: Vector):
        self[3:6] = list(value)
        return self
    @angular_velocity.setter
    def angular_velocity(self, value: Vector):
        self[6:9] = list(value)
        return self

class State(np.ndarray):
    def __new__(self, inputs):
        ball = inputs[0]
        drones = inputs[1]
        enemies = inputs[2]
        self.ndrones = len(drones)
        self.nenemies = len(enemies)
        return np.hstack((ball,*drones,*enemies)).view(self)
    @property
    def ball(self):
        return BallState(self[0:9])
    @property
    def drones(self):
        return [CarState(self[9+i*22:9+(i+1)*22]) for i in range(self.ndrones)]
    @property
    def enemies(self):
        start = 9+(self.ndrones+1)*22
        return [CarState(self[start+i*22:start+(i+1)*22]) for i in range(self.nenemies)]

def reduce_car(car, last_action: PlayerInput) -> CarState:
    """Returns a car state given an RLBot car packet and the previous car action"""
    phys = car.physics
    location = phys.location
    velocity = phys.velocity
    angular_velocity = phys.angular_velocity
    rotation = phys.rotation
    return [
        location.x, location.y, location.z,
        velocity.x, velocity.y, velocity.z,
        angular_velocity.x, angular_velocity.y, angular_velocity.z,
        rotation.roll, rotation.pitch, rotation.yaw,
        car.jumped, car.double_jumped,
        last_action.throttle, last_action.steer,
        last_action.pitch, last_action.yaw, last_action.roll,
        last_action.jump, last_action.boost, last_action.handbrake
    ]

def reduce_ball(ball) -> BallState:
    """Returns a ball state given an RLBot ball packet"""
    location = ball.location
    velocity = ball.velocity
    angular_velocity = ball.angular_velocity
    return [
        location.x, location.y, location.z,
        velocity.x, velocity.y, velocity.z,
        angular_velocity.x, angular_velocity.y, angular_velocity.z,
    ]

class StateStorage:
    """Stores the game state and action history"""
    def __init__(self, drone_indices: Set[int], enemy_indices: Set[int]):
        self.drone_indices = drone_indices
        self.enemy_indices = enemy_indices
        self.last_actions = {i:C.NOTHING for i in self.drone_indices | self.enemy_indices}
    def add_interupt(self):
        """Called when an abrupt change occurs in game. Ex scoring a goal..."""
        pass
    def add_actions(self, actions: Dict[int, PlayerInput]) -> Dict[int, PlayerInput]:
        """Stores a set of actions into action history and returns an action dictionary"""
        # store reduced actions
        self.last_actions = actions
        return {i:actions[i] for i in self.drone_indices}
    def add_state(self, packet: GameTickPacket) -> State:
        """Stores a state into state history and returns the condensed state"""
        # reduce state
        ball = reduce_ball(packet.game_ball.physics)
        # reduce car states
        drones = [reduce_car(packet.game_cars[i], self.last_actions[i]) for i in self.drone_indices]
        enemies = [reduce_car(packet.game_cars[i], self.last_actions[i]) for i in self.enemy_indices]
        # store reduced state
        self.last_state = State([ball,drones,enemies])
        return self.last_state
