from copy import copy
from utils.predictors.predictor import StatePredictor
import utils.vector as vector
from utils.state import State
from utils.vector import Vector
from math import sin, cos, acos, pi

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

def car_ball_scale(vmag: float) -> float:
    if vmag<=667:
        return 0.65
    if vmag<=2200:
        return 0.65-(vmag-667)/22000
    return 0.55-(vmag-2200)*(0.25)/(4667-2200);

def car_ball_collision(ball,car):
    # TODO: make collision condition better
    if (car.location-ball.location).mag() > R: return
    f = Vector(1,0,0).rpy(car.rotation)
    n = ball.location-car.location
    n.z *= 0.35
    n = (n-f*0.35*(n).dot(f)).normalize()
    vmag = (ball.velocity-car.velocity).mag()
    Jcol = n*vmag*car_ball_scale(vmag)
    ball.velocity += Jcol

def update_ball(state,dt):
    # TODO: add better surface normal selection and bounce conditions
    normal = Vector(0,0,1)
    point = Vector(state.ball.location.x,state.ball.location.y,0)
    dist_perp = (state.ball.location-point).scalar_project(normal)
    vel_perp = state.ball.velocity.scalar_project(normal)
    if dist_perp <= R and vel_perp < 0:
        # wall bounce
        vel_perp = normal*vel_perp
        vel_tang = state.ball.velocity-vel_perp
        vel_surf = vel_tang+copy(normal).cross(state.ball.angular_velocity)*R
        Jperp = -vel_perp*(1+CR)
        Jtang = vel_surf if vel_surf.mag()==0 else -vel_surf*min(1,Y*vel_perp.mag()/vel_surf.mag())*mu
        state.ball.velocity += Jperp+Jtang
        state.ball.angular_velocity += Jtang.cross(normal)*R
    else:
        # gravity
        state.ball.velocity.z -= g*dt
    # get car collisions
    for i in state.drones:
        car_ball_collision(state.ball,state.drones[i])
    for i in state.enemies:
        car_ball_collision(state.ball,state.enemies[i])
    # update states
    state.ball.velocity = state.ball.velocity.mag_normalize(VB_MAX)
    state.ball.angular_velocity = state.ball.angular_velocity.mag_normalize(OMEGAB_MAX)
    state.ball.location += state.ball.velocity*dt

def turn_curvature(vmag: float) -> float:
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

def update_car(state,dt):
    action = state.current_action
    throttle = 1 if action.boost>0 else action.throttle
    # update velocity
    forward = Vector(1,0,0).rpy(state.rotation)
    up = Vector(0,0,1).rpy(state.rotation)
    left = Vector(0,-1,0).rpy(state.rotation)
    vnorm = state.velocity.normalize()
    vm = state.velocity.mag()
    vforward = state.velocity.scalar_project(forward)
    vleft = state.velocity.scalar_project(left)
    acc = forward*991.667*action.boost # boosting
    # TODO: address determining wheel contact for all surfaces
    if state.location.z > HITBOX_HEIGHT:
        # aerial physics
        u = Vector(action.roll,action.pitch,action.yaw)
        T = Vector(Tr,Tp,Ty)
        D = Vector(Dr,Dp*(1-abs(u.pitch)),Dy*(1-abs(u.yaw)))
        torque = T*u+D*state.angular_velocity.rpy(-state.rotation)
        torque = torque.rpy(state.rotation)
        state.angular_velocity += torque*dt
        state.velocity.z -= g*dt # gravity
        # jump/dodge
        # TODO: address jump time limits
        # TODO: address dodge momentum effects
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
        # TODO: address braking forces
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
    # update rotation
    state.angular_velocity = state.angular_velocity.mag_normalize(OMEGAC_MAX)
    dr = state.angular_velocity.scalar_project(forward)*dt
    dp = state.angular_velocity.scalar_project(left)*dt
    dy = state.angular_velocity.scalar_project(up)*dt
    state.rotation = state.rotation+Vector(dr,dp,dy)
    state.rotation.pitch = acos(-Vector(1,0,0).rpy(state.rotation).z)-pi/2
    state.rotation.roll = (state.rotation.roll+ROLL_MAX) % (ROLL_MAX*2)-ROLL_MAX
    state.rotation.yaw = (state.rotation.yaw+YAW_MAX) % (YAW_MAX*2)-YAW_MAX
    # update state
    state.jumped = action.jump
    state.velocity += acc*dt
    state.velocity = state.velocity.mag_normalize(VC_MAX)
    state.location += state.velocity*dt
    state.last_action = action

class Predictor(StatePredictor):
    """Updates the state by using hand derived approximate models of the physics."""
    def predict(self, state):
        next_state = copy(state)
        # update cars
        for i in next_state.drones:
            update_car(next_state.drones[i],next_state.dt)
        for i in next_state.enemies:
            update_car(next_state.enemies[i],next_state.dt)
        # predict ball location
        update_ball(next_state,next_state.dt)
        return next_state
