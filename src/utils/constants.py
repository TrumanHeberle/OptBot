from rlbot.utils.structures.bot_input_struct import PlayerInput
from utils.state import reduce_action

### THIS FILE CONTAINS USEFUL CONSTANTS

# SETTINGS
DT = 0.08;      # elapsed time between state predictor updates
TIMESTEPS = 1;  # number of timesteps in advance for decision tree
NUM_RETAIN = 5; # number of paths to retain when pruning the decision tree

# ACTIONS
# throttle, steer, pitch, yaw, roll (-1,0,1) jump, boost, handbrake (0,1)
# see https://github.com/RLBot/RLBotPythonExample/wiki/Input-and-Output-Data
NOTHING                     = reduce_action(PlayerInput(0,0,0,0,0,0,0,0))
JUMP                        = reduce_action(PlayerInput(0,0,0,0,0,1,0,0))
RIGHT_ROLL                  = reduce_action(PlayerInput(0,0,0,0,1,0,0,0))
LEFT_ROLL                   = reduce_action(PlayerInput(0,0,0,0,-1,0,0,0))
RIGHT_JUMP                  = reduce_action(PlayerInput(0,1,0,1,0,1,0,0))
LEFT_JUMP                   = reduce_action(PlayerInput(0,-1,0,-1,0,1,0,0))
FORWARD                     = reduce_action(PlayerInput(1,0,-1,0,0,0,0,0))
FORWARD_BOOST               = reduce_action(PlayerInput(1,0,-1,0,0,0,1,0))
FORWARD_JUMP                = reduce_action(PlayerInput(1,0,-1,0,0,1,0,0))
FORWARD_RIGHT               = reduce_action(PlayerInput(1,1,-1,1,0,0,0,0))
FORWARD_RIGHT_BRAKE         = reduce_action(PlayerInput(1,1,-1,1,0,0,0,1))
FORWARD_RIGHT_BOOST         = reduce_action(PlayerInput(1,1,-1,1,0,0,1,0))
FORWARD_RIGHT_BOOST_BRAKE   = reduce_action(PlayerInput(1,1,-1,1,0,0,1,1))
FORWARD_LEFT                = reduce_action(PlayerInput(1,-1,-1,-1,0,0,0,0))
FORWARD_LEFT_BRAKE          = reduce_action(PlayerInput(1,-1,-1,-1,0,0,0,1))
FORWARD_LEFT_BOOST          = reduce_action(PlayerInput(1,-1,-1,-1,0,0,1,0))
FORWARD_LEFT_BOOST_BRAKE    = reduce_action(PlayerInput(1,-1,-1,-1,0,0,1,1))
BACKWARD                    = reduce_action(PlayerInput(-1,0,1,0,0,0,0,0))
BACKWARD_JUMP               = reduce_action(PlayerInput(-1,0,1,0,0,1,0,0))
BACKWARD_RIGHT              = reduce_action(PlayerInput(-1,1,1,-1,0,0,0,0))
BACKWARD_RIGHT_BRAKE        = reduce_action(PlayerInput(-1,1,1,-1,0,0,0,1))
BACKWARD_LEFT               = reduce_action(PlayerInput(-1,-1,1,1,0,0,0,0))
BACKWARD_LEFT_BRAKE         = reduce_action(PlayerInput(-1,-1,1,1,0,0,0,1))

# ACTION SET
# limits the bot to choose from this subset of actions
ACTIONS = [
    FORWARD, FORWARD_RIGHT, FORWARD_LEFT, BACKWARD, BACKWARD_RIGHT, BACKWARD_LEFT,
    FORWARD_BOOST, FORWARD_RIGHT_BOOST, FORWARD_LEFT_BOOST, FORWARD_RIGHT_BRAKE,
    FORWARD_LEFT_BRAKE
]
