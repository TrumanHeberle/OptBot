from typing import Dict, List
from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.hivemind.python_hivemind import PythonHivemind
import numpy as np
import utils.constants as C
from utils.state import reduce_state, expand_action, StateStorage
from utils.scorers.ball_chaser_scorer import Scorer
from utils.predictors.derived_predictor import Predictor
from utils.decision import DecisionTree
from time import time

### THIS FILE CONTAINS CODE TO CONTROL A NETWORK OF BOTS

class OptBotHivemind(PythonHivemind):
    def initialize_hive(self, state: GameTickPacket) -> None:
        """Initializes the collection of bots (drones)."""
        index = next(iter(self.drone_indices))
        #self.team = state.game_cars[index].team
        self.enemy_indices = set([i for i in range(state.num_cars) if state.game_cars[i].team != self.team])
        # initialize history
        self.state_history = StateStorage();
        self.actions = {i:expand_action(C.NOTHING) for i in self.drone_indices}
        self.scorer = Scorer()
        self.predictor = Predictor()

    def choose_action(self, state: np.ndarray, dt: float) -> List[np.ndarray]:
        """Chooses a decision for the action of each drone. Returns a list of
        bot actions in order of drone indices."""
        actions = []
        # select best possible action per bot
        for i in self.drone_indices:
            # instantiate decision tree
            def brancher(state, action):
                # predict next state for a drone assuming remaining drone inputs remain constant
                action_list = [action if i==j else self.actions[j] for j in self.drone_indices]
                return self.predictor.predict(state, action_list, dt)
            dtree = DecisionTree(state, C.ACTIONS, brancher, self.scorer.score)
            # determine best case action
            dtree.branch()
            for _ in range(C.TIMESTEPS):
                dtree.prune(C.NUM_RETAIN)
                if dtree.is_determined():
                    # break from loop if all the best paths stem from a single action
                    # (saves computation time)
                    break
                dtree.branch()
            # set best case action
            actions.append(dtree.ideal_key())
        return actions

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
            self.actions = {dindex:expand_action(self.actions[i]) for dindex, i in enumerate(self.drone_indices)}
        else:
            # round was interrupted, restart data capture
            self.state_history.conclude()
        return self.actions
