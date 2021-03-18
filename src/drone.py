from pathlib import Path
from rlbot.agents.hivemind.drone_agent import DroneAgent

### THIS IS A DUMMY CLASS REQUIRED TO START RLBOT

class Drone(DroneAgent):
    hive_path = str(Path(__file__).parent / "hive.py")
    hive_key = "-7083110645583806601"
    hive_name = "OptBot Hivemind"
