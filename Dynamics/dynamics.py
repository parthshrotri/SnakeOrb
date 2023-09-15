import numpy as np
import scipy.integrate as int

# Quaternion defined as: q1 = real, q2 = i, q3 = j, q4 = k
def init_quat(eciState, attitude):
    if attitude == "lvlh":
        vel = eciState[3:6]
        imag = np.cross(vel, np.array([1,0,0]))
        real = np.linalg.norm(vel) + np.dot(vel, np.array([1,0,0]))
        return qnorm(np.array([real, imag[0], imag[1], imag[2]]))
    
def qinv(quat):
    return np.array([quat[0], -quat[1], -quat[2], -quat[3]]) / np.linalg.norm(quat)

def qnorm(quat):
    return quat / np.linalg.norm(quat)

def qov(quat, vec):
    quat = qnorm(quat)
    dcm = np.array([[1-2*(quat[2]**2 + quat[3]**2), 2*(quat[1]*quat[2] - quat[3]*quat[2]), 2*(quat[1]*quat[3] + quat[2]*quat[0])],
                    [2*(quat[1]*quat[2] + quat[3]*quat[0]), 1-2*(quat[1]**2 + quat[3]**2), 2*(quat[2]*quat[3] - quat[1]*quat[0])],
                    [2*(quat[1]*quat[3] - quat[2]*quat[0]), 2*(quat[2]*quat[3] + quat[1]*quat[0]), 1-2*(quat[1]**2 + quat[2]**2)]])
    return np.matmul(dcm, vec) 

def get_rho(state, central_body):
    r_mag = np.linalg.norm(state[0:3])
    rho = central_body.rho0*np.exp(-(r_mag - central_body.radius)/central_body.scaleHeight)
    return rho

def get_drag_accel(sat, central_body):
    rho = get_rho(sat.state, central_body)
    dragx = -1/2*sat.cd_x*sat.area_x*rho*sat.state[3]**2 / sat.mass
    dragy = -1/2*sat.cd_y*sat.area_y*rho*sat.state[4]**2 / sat.mass
    dragz = -1/2*sat.cd_z*sat.area_z*rho*sat.state[5]**2 / sat.mass
    drag_vec = np.array([dragx, dragy, dragz])
    return qov(sat.qEci2Body, drag_vec)

def qprop(q, dt, sat):
    q = qnorm(q)
    omega = int.odeint(angular_acceleration, sat.omega, [0,dt], args = (sat, ), rtol=1e-13, atol=1e-13)[1]
    if(np.linalg.norm(omega) != 0):
        omega = omega / np.linalg.norm(omega)
    qdot = 1/2 * np.array([0, omega[0], omega[1], omega[2]]) * q
    q = q + qdot*dt
    return qnorm(q)

def angular_acceleration(sat, omega, dt):
    return np.array([0,0,0])

def orbit_prop(sat, dt, central_body):
    mu = central_body.mu
    state = int.odeint(orbit_ode, sat.state, [0,dt], args = (sat, central_body),rtol=1e-13, atol=1e-13)
    qEci2Body = int.odeint(qprop, sat.qEci2Body, [0,dt], args = (sat, ), rtol=1e-13, atol=1e-13)
    # qEci2Body = init_quat(state[1], "ram")
    return state[1], qEci2Body[1]
    # return state[1], qEci2Body

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
        drag = get_drag_accel(sat, central_body)
    else:
        drag = np.array([0,0,0])
    ax = -grav_param*state[0]/r**3 + J2_effect[0] + drag[0]
    ay = -grav_param*state[1]/r**3 + J2_effect[1] + drag[1]
    az = -grav_param*state[2]/r**3 + J2_effect[2] + drag[2]
    return np.array([state[3], state[4], state[5], ax, ay, az])