import numpy as np
import scipy.integrate as int
import utils.quaternion as quat

def get_rho(state, central_body):
    r_mag = np.linalg.norm(state[0:3])
    rho = central_body.rho0*np.exp(-(r_mag - central_body.radius)/central_body.scaleHeight)
    return rho

def get_drag_accel(sat, central_body):
    rho = get_rho(sat.state, central_body)
    vel_body = quat.qov(sat.qEci2Body, sat.state[3:6])
    dragx = -1/2*sat.cd*sat.area[0]*rho*vel_body[0]**2 / sat.mass
    dragy = -1/2*sat.cd*sat.area[1]*rho*vel_body[1]**2 / sat.mass
    dragz = -1/2*sat.cd*sat.area[2]*rho*vel_body[2]**2 / sat.mass
    drag_vec = np.array([dragx, dragy, dragz])
    return drag_vec

def get_omega(sat, dt):
    omega = int.odeint(angular_acceleration, sat.omega, [0,dt], args = (sat, ), rtol=1e-13, atol=1e-13)
    return omega[1]

def angular_acceleration(sat, omega, dt):
    return np.array([0,0,0])

def orbit_prop(sat, dt, central_body):
    omega = get_omega(sat, dt)
    state = int.odeint(orbit_ode, sat.state, [0,dt], args = (sat, central_body),rtol=1e-13, atol=1e-13)
    qEci2Body = quat.qprop(sat.qEci2Body, omega, dt)
    qEci2Body = quat.init_quat(state[1], "lvlh")
    return state[1], qEci2Body

def J2_accel(state, central_body):
    J2 = central_body.J2 # m^3/s^2
    r = np.sqrt(state[0]**2 + state[1]**2 + state[2]**2)
    Jx = J2*state[0]/r**7 * (6*state[2]**2 - 3/2*(state[0]**2 + state[1]**2))
    Jy = J2*state[1]/r**7 * (6*state[2]**2 - 3/2*(state[0]**2 + state[1]**2))
    Jz = J2*state[2]/r**7 * (3*state[2]**2 - 9/2*(state[0]**2 + state[1]**2))
    return np.array([Jx, Jy, Jz])

def orbit_ode(state, t, sat, central_body):
    grav_param = central_body.mu # m^3/s^2
    J2_effect = J2_accel(state, central_body)
    r = np.sqrt(state[0]**2 + state[1]**2 + state[2]**2)
    if central_body.name == "Earth" or central_body.name == "Mars" or central_body.name == "Venus" or central_body.name == "Pluto":
        drag = quat.qov(quat.qinv(sat.qEci2Body), get_drag_accel(sat, central_body))
    else:
        drag = np.array([0,0,0])
    ax = -grav_param*state[0]/r**3 + J2_effect[0] + drag[0]*np.sign(-state[3])
    ay = -grav_param*state[1]/r**3 + J2_effect[1] + drag[1]*np.sign(-state[4])
    az = -grav_param*state[2]/r**3 + J2_effect[2] + drag[2]*np.sign(-state[5])
    return np.array([state[3], state[4], state[5], ax, ay, az])