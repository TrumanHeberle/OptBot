from typing import Set, Dict, List
from copy import copy
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.structures.bot_input_struct import PlayerInput
from utils.vector import Vector
import utils.constants as C

### THIS FILE CONTAINS FUNCTIONS AND CLASSES TO HELP MANAGE PACKETS

class CarState:
    """Stores information about the current car state"""
    def __init__(self, location: Vector, velocity: Vector, \
        angular_velocity: Vector, rotation: Vector, \
        jumped: bool, double_jumped: bool, last_action: PlayerInput):
        self.location = location
        self.velocity = velocity
        self.angular_velocity = angular_velocity
        self.rotation = rotation
        self.jumped = jumped
        self.double_jumped = double_jumped
        self.last_action = last_action
    def __copy__(self):
        return CarState(
            location=copy(self.location),\
            velocity=copy(self.velocity),\
            angular_velocity=copy(self.angular_velocity),\
            rotation=copy(self.rotation),\
            jumped=copy(self.jumped), double_jumped=copy(self.double_jumped),
            last_action=copy(self.last_action))

class BallState:
    """Stores information about the current ball state"""
    def __init__(self, location: Vector, velocity: Vector, angular_velocity: Vector):
        self.location = location
        self.velocity = velocity
        self.angular_velocity = angular_velocity
    def __copy__(self):
        return BallState(
            location=copy(self.location),\
            velocity=copy(self.velocity),\
            angular_velocity=copy(self.angular_velocity))

class State:
    """Stores information about the current state"""
    def __init__(self, ball: BallState, drones: List[CarState], enemies: List[CarState]):
        self.ball = ball
        self.drones = drones
        self.enemies = enemies
    def __copy__(self):
        return State(
            ball=copy(self.ball),\
            drones=[copy(car) for car in self.drones],\
            enemies=[copy(car) for car in self.enemies])

def reduce_car(car, last_action: PlayerInput) -> CarState:
    """Returns a car state given an RLBot car packet and the previous car action"""
    phys = car.physics
    return CarState(
        location=Vector(phys.location.x, phys.location.y, phys.location.z),\
        velocity=Vector(phys.velocity.x, phys.velocity.y, phys.velocity.z),\
        angular_velocity=Vector(phys.angular_velocity.x, phys.angular_velocity.y, phys.angular_velocity.z),\
        rotation=Vector(phys.rotation.roll, phys.rotation.pitch, phys.rotation.yaw),\
        jumped=car.jumped, double_jumped=car.double_jumped,\
        last_action=last_action)

def reduce_ball(ball) -> BallState:
    """Returns a ball state given an RLBot ball packet"""
    return BallState(
        location=Vector(ball.location.x, ball.location.y, ball.location.z),\
        velocity=Vector(ball.velocity.x, ball.velocity.y, ball.velocity.z),\
        angular_velocity=Vector(ball.angular_velocity.x, ball.angular_velocity.y, ball.angular_velocity.z))

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
        self.last_state = State(ball, drones, enemies)
        return self.last_state
