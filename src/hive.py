from typing import Dict, List
from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.hivemind.python_hivemind import PythonHivemind
import utils.constants as C
from utils.state import State, Action
from utils.scorers.goal_scorer import Scorer
from utils.predictors.derived_predictor import Predictor
from utils.decision import DecisionTree
from utils.vector import Vector

### THIS FILE CONTAINS CODE TO CONTROL A NETWORK OF BOTS

class OptBotHivemind(PythonHivemind):
    def initialize_hive(self, state: GameTickPacket) -> None:
        """Initializes the collection of bots (drones)."""
        self.enemy_indices = set(i for i in range(state.num_cars) if state.game_cars[i].team != self.team)
        self.drone_actions = {i:C.NOTHING for i in self.drone_indices}
        self.enemy_actions = {i:C.NOTHING for i in self.enemy_indices}
        self.controls = {i:PlayerInput(*self.drone_actions[i]) for i in self.drone_indices}
        self.scorer = Scorer()
        self.predictor = Predictor()
        self.stopped = False
        self.initial_states = [None]
        self.final_states = []
        self.time = 0

    def choose_action(self, state: State) -> List[Dict[int, Action]]:
        """Returns a dictionary of predicted enemy and bot actions."""
        # select worst possible action per enemy
        enemy_actions = {}
        for i in self.enemy_indices:
            enemy_actions[i] = C.NOTHING
        # select best possible action per drone
        drone_actions = {}
        for i in self.drone_indices:
            # instantiate decision tree
            def brancher(state, action):
                # predict next state for a drone assuming remaining drone inputs remain constant
                for j in self.drone_indices:
                    state.drones[j].current_action = action if i==j else state.drones[j].last_action
                for j in self.enemy_indices:
                    state.enemies[j].current_action = state.enemies[j].last_action
                return self.predictor.predict(state)
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
            drone_actions[i] = dtree.ideal_key()
        # render prediction
        self.renderer.begin_rendering()
        last = state
        for s in dtree.ideal_path():
            bll = last.ball.location-2
            bls = s.ball.location-2
            cll = last.drones[0].location-2
            cls = s.drones[0].location-2
            dir = (s.drones[0].location-2)+Vector(1,0,0).rpy(s.drones[0].rotation)*50
            self.renderer.draw_line_3d(tuple(bll),tuple(bls),self.renderer.white())
            self.renderer.draw_rect_3d(tuple(bls),4,4,True,self.renderer.white())
            self.renderer.draw_line_3d(tuple(cll),tuple(cls),self.renderer.white())
            self.renderer.draw_rect_3d(tuple(cls),4,4,True,self.renderer.white())
            self.renderer.draw_line_3d(tuple(cls),tuple(dir),self.renderer.red())
            last = s
        self.renderer.end_rendering()
        return drone_actions, enemy_actions

    def get_outputs(self, state: GameTickPacket) -> Dict[int, Action]:
        """Returns a dictionary where the keys are indices of your drones and
        the values are PlayerInput objects (the controller inputs)"""
        # check if round is active
        if state.game_info.is_round_active:
            # round is active, update state and make bot decisions
            self.stopped = False
            current_state = State.from_packet(state, self.drone_actions, self.enemy_actions)
            current_state.dt = C.DT
            self.drone_actions, self.enemy_actions = self.choose_action(current_state)
            # finalize stored packets
            for i in self.drone_actions:
                current_state.drones[i].current_action = self.drone_actions[i]
            for i in self.enemy_actions:
                current_state.enemies[i].current_action = self.enemy_actions[i]
            last_state = self.initial_states[-1]
            if last_state is not None:
                last_state.dt = state.game_info.seconds_elapsed - self.time
                self.final_states.append(current_state)
                self.initial_states.append(current_state)
            else:
                self.initial_states[-1] = current_state
            self.time = state.game_info.seconds_elapsed
            # transform into RLBot compatible inputs
            self.controls = {i:PlayerInput(*self.drone_actions[i]) for i in self.drone_indices}
        elif not self.stopped:
            # first interrupted frame, restart data capture
            self.stopped = True
            self.initial_states[-1] = None
            # train predictor if possible
            if self.final_states:
                self.predictor.train(self.initial_states[:-1], self.final_states)
            # set controls to nothing
            self.controls = {i:PlayerInput(*C.NOTHING) for i in self.drone_indices}
        return self.controls
