from typing import Set
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.structures.bot_input_struct import PlayerInput
import numpy as np

### THIS FILE CONTAINS FUNCTIONS AND CLASSES TO HELP MANAGE PACKETS

def reduce_state(state: GameTickPacket, drone_indices: Set[int], enemy_indices: Set[int]) -> np.ndarray:
    """Returns a condensed version of an RLBot packet."""
    # get game state for cars and ball
    drones = [state.game_cars[i] for i in drone_indices]
    enemies = [state.game_cars[i] for i in enemy_indices]
    ball = state.game_ball.physics
    # condense game state into a list
    return np.array([
        # game ball location [0:3]
        ball.location.x, ball.location.y, ball.location.z,
        # game ball velocity [3:6]
        ball.velocity.x, ball.velocity.y, ball.velocity.z,
        # drone locations (in order) [6:9]
        drones[0].physics.location.x, drones[0].physics.location.y, drones[0].physics.location.z,
        # enemy locations (in order) [9:12]
        enemies[0].physics.location.x, enemies[0].physics.location.y, enemies[0].physics.location.z,
        # drone velocities (in order) [12:15]
        drones[0].physics.velocity.x, drones[0].physics.velocity.y, drones[0].physics.velocity.z,
        # enemy velocity (in order) [15:18]
        enemies[0].physics.velocity.x, enemies[0].physics.velocity.y, enemies[0].physics.velocity.z,
        # drone rotations (in order) [18:21]
        drones[0].physics.rotation.pitch, drones[0].physics.rotation.yaw, drones[0].physics.rotation.roll,
        # enemy rotations (in order) [21:24]
        enemies[0].physics.rotation.pitch, enemies[0].physics.rotation.yaw, enemies[0].physics.rotation.roll,
    ])

def reduce_action(action: PlayerInput) -> np.ndarray:
    """Returns a condensed version of the provided action"""
    return np.array([
        # directional controls [0:2]
        action.throttle, action.steer,
        # rotational controls [2:5]
        action.pitch, action.yaw, action.roll,
        # boolean controls [5:8]
        action.jump, action.boost, action.handbrake
    ])

def expand_action(action: np.ndarray) -> PlayerInput:
    """Returns an uncondensed version of the provided action"""
    return PlayerInput(*action)

class StateStorage:
    """Stores lists of (state, action, timestamp) pairs. A chain is a series of
    states which directly follow each other."""
    def __init__(self):
        # concluded state chain list
        self.state_chains = []
        self.action_chains = []
        self.timestamp_chains = []
        self.total_states = 0
        # the immediate state chain
        self.states = []
        self.actions = []
        self.timestamps = []
    def __len__(self):
        return self.total_states
    def store(self, state, action, timestamp: float) -> None:
        """Stores a frame into the immediate state chain"""
        self.states.append(state)
        self.actions.append(action)
        self.timestamps.append(timestamp)
        self.total_states += 1
    def conclude(self):
        """Concludes and stores the immediate state chain into history before
        restarting the immediate state chain"""
        # check if immediate state chain is empty
        if len(self.states) > 0:
            # immediate state chain is not empty, conclude chain
            self.state_chains.append(self.states)
            self.action_chains.append(self.actions)
            self.timestamp_chains.append(self.timestamps)
            # restart immediate state chain
            self.states = []
            self.actions = []
            self.timestamps = []
