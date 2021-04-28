from utils.state import Action

### THIS FILE CONTAINS USEFUL CONSTANTS

# SETTINGS
DT = 0.008          # elapsed time between state predictor updates
TIMESTEPS = 3       # number of timesteps in advance for decision tree
NUM_RETAIN = 4      # number of paths to retain when pruning the decision tree

# ACTIONS
# throttle, steer, pitch, yaw, roll ([-1,0,1]) jump, boost, handbrake ([0,1])
# see https://github.com/RLBot/RLBotPythonExample/wiki/Input-and-Output-Data
NOTHING                     = Action([0,0,0,0,0,0,0,0])
JUMP                        = Action([0,0,0,0,0,1,0,0])
RIGHT_ROLL                  = Action([0,0,0,0,1,0,0,0])
LEFT_ROLL                   = Action([0,0,0,0,-1,0,0,0])
RIGHT_JUMP                  = Action([0,1,0,1,0,1,0,0])
LEFT_JUMP                   = Action([0,-1,0,-1,0,1,0,0])
FORWARD                     = Action([1,0,-1,0,0,0,0,0])
FORWARD_BOOST               = Action([1,0,-1,0,0,0,1,0])
FORWARD_JUMP                = Action([1,0,-1,0,0,1,0,0])
FORWARD_RIGHT               = Action([1,1,-1,1,0,0,0,0])
FORWARD_RIGHT_BRAKE         = Action([1,1,-1,1,0,0,0,1])
FORWARD_RIGHT_BOOST         = Action([1,1,-1,1,0,0,1,0])
FORWARD_RIGHT_BOOST_BRAKE   = Action([1,1,-1,1,0,0,1,1])
FORWARD_LEFT                = Action([1,-1,-1,-1,0,0,0,0])
FORWARD_LEFT_BRAKE          = Action([1,-1,-1,-1,0,0,0,1])
FORWARD_LEFT_BOOST          = Action([1,-1,-1,-1,0,0,1,0])
FORWARD_LEFT_BOOST_BRAKE    = Action([1,-1,-1,-1,0,0,1,1])
BACKWARD_JUMP               = Action([-1,0,1,0,0,1,0,0])
BACKWARD                    = Action([-1,0,1,0,0,0,0,0])
BACKWARD_RIGHT              = Action([-1,1,1,1,0,0,0,0])
BACKWARD_RIGHT_BRAKE        = Action([-1,1,1,1,0,0,0,1])
BACKWARD_LEFT               = Action([-1,-1,1,-1,0,0,0,0])
BACKWARD_LEFT_BRAKE         = Action([-1,-1,1,-1,0,0,0,1])
ROLL_LEFT                   = Action([0,0,0,0,-1,0,0,0])
ROLL_RIGHT                  = Action([0,0,0,0,1,0,0,0])
PITCH_UP                    = Action([0,0,1,0,0,0,0,0])
PITCH_DOWN                  = Action([0,0,-1,0,0,0,0,0])
YAW_RIGHT                   = Action([0,1,0,1,0,0,0,0])
YAW_LEFT                    = Action([0,-1,0,-1,0,0,0,0])

# ACTION SET
# limits the bot to choose from this subset of actions
ACTIONS = [
    NOTHING, FORWARD, FORWARD_RIGHT, FORWARD_LEFT, BACKWARD, BACKWARD_RIGHT,
    BACKWARD_LEFT, FORWARD_BOOST, FORWARD_RIGHT_BOOST, FORWARD_LEFT_BOOST,
    FORWARD_RIGHT_BRAKE, FORWARD_LEFT_BRAKE, FORWARD_JUMP, BACKWARD_JUMP,
    YAW_LEFT, YAW_RIGHT, PITCH_UP, PITCH_DOWN, ROLL_LEFT, ROLL_RIGHT
]
