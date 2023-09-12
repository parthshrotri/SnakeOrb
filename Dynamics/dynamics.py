import numpy as np
import scipy.integrate as int

def eci2ecef(eciState, days_since_j2000):
    gamma = np.radians(360.9856123035484*days_since_j2000 + 280.46)
    dcm = np.array([[np.cos(gamma), np.sin(gamma), 0],
                    [-np.sin(gamma), np.cos(gamma), 0],
                    [0, 0, 1]])
    ecefState = np.zeros(eciState.shape)
    ecefState[0:3] = np.matmul(dcm, eciState[0:3].T).T
    ecefState[3:6] = np.matmul(dcm, eciState[3:6].T).T

    return ecefState

def ecef2ll(ecefState):
    r_delta = np.linalg.norm(ecefState[0:1])
    sinA = ecefState[1]/r_delta
    cosA = ecefState[0]/r_delta

    Lon = np.arctan2(sinA,cosA)

    if Lon < -np.pi:
        Lon = Lon + 2*np.pi

    Lat = np.arcsin(ecefState[2]/np.linalg.norm(ecefState))
    return np.array([np.degrees(Lat), np.degrees(Lon), np.linalg.norm(ecefState[0:2])])

# Quaternion defined as: q1 = real, q2 = i, q3 = j, q4 = k
def init_quat(eciState, attitude):
    if attitude == "ram":
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

def get_rho(state):
    alt = np.linalg.norm(state[0:3]) - 6378.1e3 # m
    return 3.019e-15*np.exp(-alt/1000e3) # kg/m^3

def get_drag_accel(sat):
    rho = get_rho(sat.state)
    dragx = -1/2*sat.cd_x*sat.area_x*rho*sat.state[3]**2 / sat.mass
    dragy = -1/2*sat.cd_y*sat.area_y*rho*sat.state[4]**2 / sat.mass
    dragz = -1/2*sat.cd_z*sat.area_z*rho*sat.state[5]**2 / sat.mass
    return np.array([dragx, dragy, dragz])

def qprop(q, dt, sat):
    q = qnorm(q)
    omega = int.odeint(angular_acceleration, sat.omega, [0,dt], args = (sat, ), rtol=1e-13, atol=1e-13)[1]
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

def orbit_ode(state, t, sat, central_body):
    grav_param = central_body.mu # m^3/s^2
    J2 = central_body.J2 # m^3/s^2
    r = np.sqrt(state[0]**2 + state[1]**2 + state[2]**2)
    drag = get_drag_accel(sat)
    ax = -grav_param*state[0]/r**3 + J2*state[0]/r**7 * (6*state[2]**2 - 3/2*(state[0]**2 + state[1]**2)) - drag[0]
    ay = -grav_param*state[1]/r**3 + J2*state[1]/r**7 * (6*state[2]**2 - 3/2*(state[0]**2 + state[1]**2)) - drag[1]
    az = -grav_param*state[2]/r**3 + J2*state[2]/r**7 * (3*state[2]**2 - 9/2*(state[0]**2 + state[1]**2)) - drag[2]
    return np.array([state[3], state[4], state[5], ax, ay, az])