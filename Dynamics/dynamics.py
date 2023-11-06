import numpy as np
import scipy.integrate as int
import utils.quaternion as quat

def get_rho(rel_state, body):
    r_mag = np.linalg.norm(rel_state)
    rho = body.rho0*np.exp(-(r_mag - body.radius)/body.scaleHeight)
    return rho

def get_drag_accel(sat, body):
    rel_state = sat.state - body.state
    rho = get_rho(rel_state[0:3], body)
    vel_body = quat.qov(sat.qEci2Body, rel_state[3:6])
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

def orbit_prop(sat, dt, bodies):
    omega = get_omega(sat, dt)
    state = int.odeint(orbit_ode, sat.state, [0,dt], args = (sat, bodies),rtol=1e-13, atol=1e-13)
    qEci2Body = quat.qprop(sat.qEci2Body, omega, dt)
    qEci2Body = quat.init_quat(state[1], "lvlh")
    return state[1], qEci2Body

def J2_accel(rel_state, body):
    J2 = body.J2 # m^3/s^2
    r = np.linalg.norm(rel_state[0:3])
    Jx = J2*rel_state[0]/r**7 * (6*rel_state[2]**2 - 3/2*(rel_state[0]**2 + rel_state[1]**2))
    Jy = J2*rel_state[1]/r**7 * (6*rel_state[2]**2 - 3/2*(rel_state[0]**2 + rel_state[1]**2))
    Jz = J2*rel_state[2]/r**7 * (3*rel_state[2]**2 - 9/2*(rel_state[0]**2 + rel_state[1]**2))
    return np.array([Jx, Jy, Jz])

def orbit_ode(state, t, sat, bodies):
    ax, ay, az = 0, 0, 0
    for body in bodies:
        rel_state = state - body.state
        J2_effect = J2_accel(rel_state, body)
        r = np.linalg.norm(rel_state[0:3])
        if body.name == "Earth" or body.name == "Mars" or body.name == "Venus" or body.name == "Pluto":
            drag = quat.qov(quat.qinv(sat.qEci2Body), get_drag_accel(sat, body))
        else:
            drag = np.array([0,0,0])
        ax += -body.mu*rel_state[0]/r**3 + J2_effect[0] + drag[0]*np.sign(-rel_state[3])
        ay += -body.mu*rel_state[1]/r**3 + J2_effect[1] + drag[1]*np.sign(-rel_state[4])
        az += -body.mu*rel_state[2]/r**3 + J2_effect[2] + drag[2]*np.sign(-rel_state[5])
    return np.array([state[3], state[4], state[5], ax, ay, az])