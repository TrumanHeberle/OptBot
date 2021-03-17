from typing import Dict
from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.hivemind.python_hivemind import PythonHivemind

class OptBotHivemind(PythonHivemind):
    def initialize_hive(self, packet: GameTickPacket) -> None:
        index = next(iter(self.drone_indices))
        self.team = packet.game_cars[index].team

    def get_outputs(self, packet: GameTickPacket) -> Dict[int, PlayerInput]:
        return {index: PlayerInput(throttle=1.0) for index in self.drone_indices}
