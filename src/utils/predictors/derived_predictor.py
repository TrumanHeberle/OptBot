from copy import copy
from utils.predictors.predictor import StatePredictor
import utils.vector as vector
from utils.state import State
from utils.vector import Vector
from math import sin, cos, pi

g = 650 # gravitational acceleration
R = 91.25 # ball radius
Y = 2 # ???
CR = 0.6 # ball coefficient of restitution
mu = 0.285 # ball coefficient of friction
VB_MAX = 6000 # ball max velocity
OMEGAB_MAX = 6 # ball max angular velocity

YAW_MAX = pi
PITCH_MAX = pi/2
ROLL_MAX = pi
OMEGAC_MAX = 5.5             # maximum angular velocity
Tr = -36.07956616966136     # roll torque coefficient
Tp = -12.14599781908070     # pitch torque coefficient
Ty = 8.91962804287785       # yaw torque coefficient
Dr = -4.47166302201591      # roll drag coefficient
Dp = -2.798194258050845     # pitch drag coefficient
Dy = -1.886491900437232     # yaw drag coefficient
HITBOX_HEIGHT = 31.3
VC_MAX = 2300               # car max velocity

def update_ball(state,dt):
    # TODO: add better surface normal selection and bounce conditions
    normal = Vector(0,0,1)
    point = Vector(state.location.x,state.location.y,0)
    dist_perp = (state.location-point).scalar_project(normal)
    vel_perp = state.velocity.scalar_project(normal)
    if dist_perp <= R and vel_perp < 0:
        # bounce
        vel_perp = normal*vel_perp
        vel_tang = state.velocity-vel_perp
        vel_surf = vel_tang+copy(normal).cross(state.angular_velocity)*R
        Jperp = -vel_perp*(1+CR)
        Jtang = vel_surf if vel_surf.mag()==0 else -vel_surf*min(1,Y*vel_perp.mag()/vel_surf.mag())*mu
        state.velocity += Jperp+Jtang
        state.angular_velocity += Jtang.cross(normal)*R
    else:
        # gravity
        state.angular_velocity.z -= g*dt
    # update states
    state.velocity = state.velocity.mag_normalize(VB_MAX)
    state.angular_velocity = state.angular_velocity.mag_normalize(OMEGAB_MAX)
    state.location += state.velocity*dt

def turn_curvature(vmag):
    if vmag<=0:
        return 0
    if vmag<500:
        return 0.0069-5.84e-6*vmag
    if vmag<1000:
        return 0.00561-3.26e-6*vmag
    if vmag<1500:
        return 0.0043-1.95e-6*vmag
    if vmag<1750:
        return 0.003025-1.1e-6*vmag
    return 0.0018-4e-7*vmag

def update_car(state,action,dt):
    throttle = 1 if action.boost>0 else action.throttle
    # update velocity
    forward = Vector(1,0,0).rpy(state.rotation)
    up = Vector(0,0,1).rpy(state.rotation)
    left = Vector(0,1,0).rpy(state.rotation)
    vnorm = state.velocity.normalize()
    vm = state.velocity.mag()
    vforward = state.velocity.scalar_project(forward)
    vleft = state.velocity.scalar_project(left)
    acc = forward*991.667*action.boost # boosting
    # TODO: address determining wheel contact for all surfaces
    if state.location.z > HITBOX_HEIGHT:
        # aerial physics
        T = Vector(Tr,Tp,Ty)
        D = Vector(Dr,Dp*(1-abs(state.rotation.pitch)),Dy*(1-abs(state.rotation.yaw)))
        torque = T*state.rotation+D*state.angular_velocity.rpy(-state.rotation)
        torque = torque.rpy(state.rotation)
        state.angular_velocity += torque*dt
        state.velocity.z -= g*dt # gravity
        # jump/dodge
        if action.jump and state.last_action.jump and not state.double_jumped:
            # extend jump
            acc += up*1458.333374
        elif action.jump and not state.last_action.jump and not state.double_jumped:
            # dodge
            state.double_jumped = 1
            dir = (forward*throttle-left*action.steer).normalize()
            acc += dir*291.667/dt
    else:
        # ground physics
        # TODO: address frictional forces, normal forces, wall driving, etc...
        n = Vector(0,0,1)
        if abs(throttle)<0.01:
            # coast
            acc -= vnorm*525
        elif (throttle>0 and vforward<0) or (throttle<0 and vforward>0):
            # brake
            acc -= vnorm*3500
        elif vm<1400:
            # throttle
            acc += forward*throttle*(1600-1440*vm/1400)
        elif vm<1410:
            # throttle
            acc += forward*throttle*(160-16*(vm-1400))
        # get turn curvature
        K = turn_curvature(vm)
        state.angular_velocity = n*action.steer*vm*K
        acc -= left*action.steer*(vm**2)*K
        acc -= g*forward.z # gravity
        # jump
        state.double_jumped = 0
        if action.jump and not state.jumped and not state.last_action.jump:
            state.jumped = 1
            acc += up*291.667/dt
        else:
            state.jumped = 0
    state.angular_velocity = state.angular_velocity.mag_normalize(OMEGAC_MAX)
    # update rotation
    r = state.angular_velocity.scalar_project(forward)
    p = state.angular_velocity.scalar_project(left)
    y = state.angular_velocity.scalar_project(up)
    mx = Vector(ROLL_MAX, PITCH_MAX, YAW_MAX)
    state.rotation = (state.rotation+Vector(r,p,y)*dt+mx) % (mx*2)-mx
    # update state
    state.jumped = action.jump
    state.velocity += acc*dt
    state.velocity = state.velocity.mag_normalize(VC_MAX)
    state.location += state.velocity*dt
    state.last_action = action

class Predictor(StatePredictor):
    """Updates the state by using hand derived approximate models of the physics."""
    def predict(self, state, actions, dt):
        next_state = copy(state)
        # update cars
        for i, car in enumerate(next_state.drones):
            update_car(car,actions[0][i],dt)
        for i, car in enumerate(next_state.enemies):
            update_car(car,actions[1][i],dt)
        # predict ball location
        update_ball(next_state.ball,dt)
        return next_state
