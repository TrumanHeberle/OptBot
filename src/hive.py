from typing import Dict
from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.hivemind.python_hivemind import PythonHivemind
import utils.constants as C
from utils.state import reduce_state, reduce_action, expand_action, StateStorage

class OptBotHivemind(PythonHivemind):
    def initialize_hive(self, state: GameTickPacket) -> None:
        """Initializes the collection of bots (drones)."""
        index = next(iter(self.drone_indices))
        self.team = state.game_cars[index].team
        self.enemy_indices = set([i for i in range(state.num_cars) if state.game_cars[i].team != self.team])
        # initialize history
        self.state_history = StateStorage();
        self.actions = {i:expand_action(C.NOTHING) for i in self.drone_indices}

    def choose_action(self, state, dt: float) -> Dict[int, PlayerInput]:
        """Chooses a decision for the action of each drone."""
        return {i: C.FORWARD for i in self.drone_indices}

    def get_outputs(self, state: GameTickPacket) -> Dict[int, PlayerInput]:
        """Returns a dictionary where the keys are indices of your drones and
        the values are PlayerInput objects (the controller inputs)"""
        # check if round is active
        if state.game_info.is_round_active:
            # round is active, update state and make bot decisions
            current_state = reduce_state(state, self.drone_indices, self.enemy_indices)
            self.actions = self.choose_action(current_state, C.DT)
            self.state_history.store(current_state, self.actions, state.game_info.seconds_elapsed)
            # uncondense actions for RLBot API
            self.actions = {i:expand_action(self.actions[i]) for i in self.actions}
        else:
            # round was interrupted, restart data capture
            self.state_history.conclude()
        return self.actions
