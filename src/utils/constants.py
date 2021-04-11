from rlbot.utils.structures.bot_input_struct import PlayerInput

### THIS FILE CONTAINS USEFUL CONSTANTS

# SETTINGS
DT = 0.032;      # elapsed time between state predictor updates
TIMESTEPS = 5;  # number of timesteps in advance for decision tree
NUM_RETAIN = 2; # number of paths to retain when pruning the decision tree

# ACTIONS
# throttle, steer, pitch, yaw, roll (-1,0,1) jump, boost, handbrake (0,1)
# see https://github.com/RLBot/RLBotPythonExample/wiki/Input-and-Output-Data
NOTHING                     = PlayerInput(0,0,0,0,0,0,0,0)
JUMP                        = PlayerInput(0,0,0,0,0,1,0,0)
RIGHT_ROLL                  = PlayerInput(0,0,0,0,1,0,0,0)
LEFT_ROLL                   = PlayerInput(0,0,0,0,-1,0,0,0)
RIGHT_JUMP                  = PlayerInput(0,1,0,1,0,1,0,0)
LEFT_JUMP                   = PlayerInput(0,-1,0,-1,0,1,0,0)
FORWARD                     = PlayerInput(1,0,-1,0,0,0,0,0)
FORWARD_BOOST               = PlayerInput(1,0,-1,0,0,0,1,0)
FORWARD_JUMP                = PlayerInput(1,0,-1,0,0,1,0,0)
FORWARD_RIGHT               = PlayerInput(1,1,-1,1,0,0,0,0)
FORWARD_RIGHT_BRAKE         = PlayerInput(1,1,-1,1,0,0,0,1)
FORWARD_RIGHT_BOOST         = PlayerInput(1,1,-1,1,0,0,1,0)
FORWARD_RIGHT_BOOST_BRAKE   = PlayerInput(1,1,-1,1,0,0,1,1)
FORWARD_LEFT                = PlayerInput(1,-1,-1,-1,0,0,0,0)
FORWARD_LEFT_BRAKE          = PlayerInput(1,-1,-1,-1,0,0,0,1)
FORWARD_LEFT_BOOST          = PlayerInput(1,-1,-1,-1,0,0,1,0)
FORWARD_LEFT_BOOST_BRAKE    = PlayerInput(1,-1,-1,-1,0,0,1,1)
BACKWARD                    = PlayerInput(-1,0,1,0,0,0,0,0)
BACKWARD_JUMP               = PlayerInput(-1,0,1,0,0,1,0,0)
BACKWARD_RIGHT              = PlayerInput(-1,1,1,1,0,0,0,0)
BACKWARD_RIGHT_BRAKE        = PlayerInput(-1,1,1,1,0,0,0,1)
BACKWARD_LEFT               = PlayerInput(-1,-1,1,-1,0,0,0,0)
BACKWARD_LEFT_BRAKE         = PlayerInput(-1,-1,1,-1,0,0,0,1)

# ACTION SET
# limits the bot to choose from this subset of actions
ACTIONS = [
    NOTHING, FORWARD, FORWARD_RIGHT, FORWARD_LEFT, BACKWARD, BACKWARD_RIGHT,
    BACKWARD_LEFT, FORWARD_BOOST, FORWARD_RIGHT_BOOST, FORWARD_LEFT_BOOST,
    FORWARD_RIGHT_BRAKE, FORWARD_LEFT_BRAKE, FORWARD_JUMP
]
