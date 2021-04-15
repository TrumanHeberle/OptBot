from typing import Dict, List
from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.hivemind.python_hivemind import PythonHivemind
import utils.constants as C
from utils.state import StateStorage, State
from utils.scorers.ball_chaser_scorer import Scorer
from utils.predictors.derived_predictor import Predictor
from utils.decision import DecisionTree
from utils.vector import Vector
from time import time

### THIS FILE CONTAINS CODE TO CONTROL A NETWORK OF BOTS

class OptBotHivemind(PythonHivemind):
    def initialize_hive(self, state: GameTickPacket) -> None:
        """Initializes the collection of bots (drones)."""
        self.enemy_indices = set([i for i in range(state.num_cars) if state.game_cars[i].team != self.team])
        self.history = StateStorage(self.drone_indices, self.enemy_indices)
        self.scorer = Scorer()
        self.predictor = Predictor()
        self.hive_actions = {i:self.history.last_actions[i] for i in self.drone_indices}

    def choose_action(self, state: State) -> Dict[int, PlayerInput]:
        """Returns a dictionary of predicted enemy and bot actions."""
        actions = {}
        # select worst possible action per enemy
        for i in self.enemy_indices:
            actions[i] = C.NOTHING
        # select best possible action per drone
        for i in self.drone_indices:
            # instantiate decision tree
            def brancher(state, action):
                # predict next state for a drone assuming remaining drone inputs remain constant
                dactions = [action if i==j else self.drone_actions[j] for j in self.drone_indices]
                eactions = [C.NOTHING for _ in self.enemy_indices]
                return self.predictor.predict(state, [dactions, eactions], C.DT)
            dtree = DecisionTree(state, C.ACTIONS, brancher, self.scorer.score)
            # determine best case action
            dtree.branch()
            for _ in range(C.TIMESTEPS-1):
                dtree.prune(C.NUM_RETAIN)
                if dtree.is_determined():
                    # break from loop if all the best paths stem from a single action
                    # (saves computation time)
                    dtree.prune(1)
                dtree.branch()
            # set best case action
            actions[i] = dtree.ideal_key()
        # render prediction
        self.renderer.begin_rendering()
        last = state
        for s in dtree.ideal_path():
            bll = list(last.ball.location-2)
            bls = list(s.ball.location-2)
            cll = list(last.drones[0].location-2)
            cls = list(s.drones[0].location-2)
            dir = list((s.drones[0].location-2)+Vector(1,0,0).rpy(s.drones[0].rotation)*50)
            self.renderer.draw_line_3d(bll,bls,self.renderer.white())
            self.renderer.draw_rect_3d(bls,4,4,True,self.renderer.white())
            self.renderer.draw_line_3d(cll,cls,self.renderer.white())
            self.renderer.draw_rect_3d(cls,4,4,True,self.renderer.white())
            self.renderer.draw_line_3d(cls,dir,self.renderer.red())
            last = s
        self.renderer.end_rendering()
        return actions

    def get_outputs(self, state: GameTickPacket) -> Dict[int, PlayerInput]:
        """Returns a dictionary where the keys are indices of your drones and
        the values are PlayerInput objects (the controller inputs)"""
        # check if round is active
        if state.game_info.is_round_active:
            # round is active, update state and make bot decisions
            current_state = self.history.add_state(state)
            self.hive_actions = self.history.add_actions(self.choose_action(current_state))
        else:
            # round was interrupted, restart data capture
            self.history.add_interupt()
        return self.hive_actions
