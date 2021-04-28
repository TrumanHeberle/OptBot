from utils.state import Action, BallState, CarState, State
from utils.vector import Vector

def test_init():
    """action manipulation"""
    to_list = lambda a: [a.throttle, a.steer, a.pitch, a.yaw, a.roll, a.jump, a.boost, a.handbrake]
    n_actions = 8
    # action setting
    action = Action([0,0,0,0,0,0,0,0])
    assert len(action)==n_actions
    assert to_list(action) == [0,0,0,0,0,0,0,0]
    # single parameter setting
    action.throttle = 1
    assert len(action)==n_actions
    assert to_list(action) == [1,0,0,0,0,0,0,0]
    action.steer = 2
    assert len(action)==n_actions
    assert to_list(action) == [1,2,0,0,0,0,0,0]
    action.pitch = 3
    assert len(action)==n_actions
    assert to_list(action) == [1,2,3,0,0,0,0,0]
    action.yaw = 4
    assert len(action)==n_actions
    assert to_list(action) == [1,2,3,4,0,0,0,0]
    action.roll = 5
    assert len(action)==n_actions
    assert to_list(action) == [1,2,3,4,5,0,0,0]
    action.jump = 6
    assert len(action)==n_actions
    assert to_list(action) == [1,2,3,4,5,6,0,0]
    action.boost = 7
    assert len(action)==n_actions
    assert to_list(action) == [1,2,3,4,5,6,7,0]
    action.handbrake = 8
    assert len(action)==n_actions
    assert to_list(action) == [1,2,3,4,5,6,7,8]
    # multiple parameter setting
    action.throttle = -8
    action.steer = -7
    action.pitch = -6
    action.yaw = -5
    action.roll = -4
    action.jump = -3
    action.boost = -2
    action.handbrake = -1
    assert len(action)==n_actions
    assert to_list(action) == [-8,-7,-6,-5,-4,-3,-2,-1]

def test_ball_state():
    """ball state manipulation"""
    n_bs = 9
    # ball state setting
    bs = BallState([0,1,2,3,4,5,6,7,8])
    assert len(bs)==n_bs
    assert bs.location==Vector(0,1,2)
    assert bs.velocity==Vector(3,4,5)
    assert bs.angular_velocity==Vector(6,7,8)
    # single parameter setting
    bs.location = Vector(9,10,11)
    assert len(bs)==n_bs
    assert bs.location==Vector(9,10,11)
    assert bs.velocity==Vector(3,4,5)
    assert bs.angular_velocity==Vector(6,7,8)
    bs.velocity = Vector(12,13,14)
    assert len(bs)==n_bs
    assert bs.location==Vector(9,10,11)
    assert bs.velocity==Vector(12,13,14)
    assert bs.angular_velocity==Vector(6,7,8)
    bs.angular_velocity = Vector(15,16,17)
    assert len(bs)==n_bs
    assert bs.location==Vector(9,10,11)
    assert bs.velocity==Vector(12,13,14)
    assert bs.angular_velocity==Vector(15,16,17)
    # multiple parameter setting
    bs.location = Vector(-1,-2,-3)
    bs.velocity = Vector(-4,-5,-6)
    bs.angular_velocity = Vector(-7,-8,-9)
    assert len(bs)==n_bs
    assert bs.location==Vector(-1,-2,-3)
    assert bs.velocity==Vector(-4,-5,-6)
    assert bs.angular_velocity==Vector(-7,-8,-9)
    # inplace parameter setting
    bs.location += 2
    bs.velocity += 2
    bs.angular_velocity += 2
    assert len(bs)==n_bs
    assert bs.location==Vector(1,0,-1)
    assert bs.velocity==Vector(-2,-3,-4)
    assert bs.angular_velocity==Vector(-5,-6,-7)

def test_car_state():
    """car state manipulation"""
    n_cs = 30
    n_actions = 8
    # car state setting
    car_params = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    last_action_params = [14,15,16,17,18,19,20,21]
    current_action_params = [22,23,24,25,26,27,28,29]
    cs = CarState(car_params+last_action_params+current_action_params)
    assert len(cs)==30
    assert len(cs.last_action)==n_actions
    assert len(cs.current_action)==n_actions
    assert cs.location==Vector(0,1,2)
    assert cs.velocity==Vector(3,4,5)
    assert cs.rotation==Vector(6,7,8)
    assert cs.angular_velocity==Vector(9,10,11)
    assert cs.jumped==12 and cs.double_jumped==13
    assert all(cs.last_action==Action(last_action_params))
    assert all(cs.current_action==Action(current_action_params))
    # single parameter setting
    cs.location = Vector(-1,-2,-3)
    assert len(cs)==30
    assert len(cs.last_action)==n_actions
    assert len(cs.current_action)==n_actions
    assert cs.location==Vector(-1,-2,-3)
    assert cs.velocity==Vector(3,4,5)
    assert cs.rotation==Vector(6,7,8)
    assert cs.angular_velocity==Vector(9,10,11)
    assert cs.jumped==12 and cs.double_jumped==13
    assert all(cs.last_action==Action(last_action_params))
    assert all(cs.current_action==Action(current_action_params))
    cs.velocity = Vector(-4,-5,-6)
    assert len(cs)==30
    assert len(cs.last_action)==n_actions
    assert len(cs.current_action)==n_actions
    assert cs.location==Vector(-1,-2,-3)
    assert cs.velocity==Vector(-4,-5,-6)
    assert cs.rotation==Vector(6,7,8)
    assert cs.angular_velocity==Vector(9,10,11)
    assert cs.jumped==12 and cs.double_jumped==13
    assert all(cs.last_action==Action(last_action_params))
    assert all(cs.current_action==Action(current_action_params))
    cs.rotation = Vector(-7,-8,-9)
    assert len(cs)==30
    assert len(cs.last_action)==n_actions
    assert len(cs.current_action)==n_actions
    assert cs.location==Vector(-1,-2,-3)
    assert cs.velocity==Vector(-4,-5,-6)
    assert cs.rotation==Vector(-7,-8,-9)
    assert cs.angular_velocity==Vector(9,10,11)
    assert cs.jumped==12 and cs.double_jumped==13
    assert all(cs.last_action==Action(last_action_params))
    assert all(cs.current_action==Action(current_action_params))
    cs.angular_velocity = Vector(-10,-11,-12)
    assert len(cs)==30
    assert len(cs.last_action)==n_actions
    assert len(cs.current_action)==n_actions
    assert cs.location==Vector(-1,-2,-3)
    assert cs.velocity==Vector(-4,-5,-6)
    assert cs.rotation==Vector(-7,-8,-9)
    assert cs.angular_velocity==Vector(-10,-11,-12)
    assert cs.jumped==12 and cs.double_jumped==13
    assert all(cs.last_action==Action(last_action_params))
    assert all(cs.current_action==Action(current_action_params))
    cs.jumped = -13
    assert len(cs)==30
    assert len(cs.last_action)==n_actions
    assert len(cs.current_action)==n_actions
    assert cs.location==Vector(-1,-2,-3)
    assert cs.velocity==Vector(-4,-5,-6)
    assert cs.rotation==Vector(-7,-8,-9)
    assert cs.angular_velocity==Vector(-10,-11,-12)
    assert cs.jumped==-13 and cs.double_jumped==13
    assert all(cs.last_action==Action(last_action_params))
    assert all(cs.current_action==Action(current_action_params))
    cs.double_jumped = -14
    assert len(cs)==30
    assert len(cs.last_action)==n_actions
    assert len(cs.current_action)==n_actions
    assert cs.location==Vector(-1,-2,-3)
    assert cs.velocity==Vector(-4,-5,-6)
    assert cs.rotation==Vector(-7,-8,-9)
    assert cs.angular_velocity==Vector(-10,-11,-12)
    assert cs.jumped==-13 and cs.double_jumped==-14
    assert all(cs.last_action==Action(last_action_params))
    assert all(cs.current_action==Action(current_action_params))
    last_action_params = [-15,-16,-17,-18,-19,-20,-21,-22]
    cs.last_action = Action(last_action_params)
    assert len(cs)==30
    assert len(cs.last_action)==n_actions
    assert len(cs.current_action)==n_actions
    assert cs.location==Vector(-1,-2,-3)
    assert cs.velocity==Vector(-4,-5,-6)
    assert cs.rotation==Vector(-7,-8,-9)
    assert cs.angular_velocity==Vector(-10,-11,-12)
    assert cs.jumped==-13 and cs.double_jumped==-14
    assert all(cs.last_action==Action(last_action_params))
    assert all(cs.current_action==Action(current_action_params))
    current_action_params = [-23,-24,-25,-26,-27,-28,-29,-30]
    cs.current_action = Action(current_action_params)
    assert len(cs)==30
    assert len(cs.last_action)==n_actions
    assert len(cs.current_action)==n_actions
    assert cs.location==Vector(-1,-2,-3)
    assert cs.velocity==Vector(-4,-5,-6)
    assert cs.rotation==Vector(-7,-8,-9)
    assert cs.angular_velocity==Vector(-10,-11,-12)
    assert cs.jumped==-13 and cs.double_jumped==-14
    assert all(cs.last_action==Action(last_action_params))
    assert all(cs.current_action==Action(current_action_params))
    # multiple parameter setting
    last_action_params = [15,16,17,18,19,20,21,22]
    current_action_params = [23,24,25,26,27,28,29,30]
    cs.location = Vector(1,2,3)
    cs.velocity = Vector(4,5,6)
    cs.rotation = Vector(7,8,9)
    cs.angular_velocity = Vector(10,11,12)
    cs.jumped = 13
    cs.double_jumped = 14
    cs.last_action = Action(last_action_params)
    cs.current_action = Action(current_action_params)
    assert len(cs)==30
    assert len(cs.last_action)==n_actions
    assert len(cs.current_action)==n_actions
    assert cs.location==Vector(1,2,3)
    assert cs.velocity==Vector(4,5,6)
    assert cs.rotation==Vector(7,8,9)
    assert cs.angular_velocity==Vector(10,11,12)
    assert cs.jumped==13 and cs.double_jumped==14
    assert all(cs.last_action==Action(last_action_params))
    assert all(cs.current_action==Action(current_action_params))

def test_state():
    """state manipulation"""
    pass
