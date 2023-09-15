import numpy as np
# import display as disp

def state_vec_to_keplerian(state, mu):
    a = semimajor_axis(state, mu)
    e = np.linalg.norm(eccentricity(state, mu))
    i = inclination(state)
    raan = RAAN(state)
    omega = argument_of_periapse(state, mu)
    f = true_anomaly(state, mu)
    return np.array([a, e, i, raan, omega, f])

def keplerian_to_state_vec(kep, mu):
    pos = position(kep, mu)
    vel = velocity(kep, mu)

    return np.array([pos[0], pos[1], pos[2], vel[0], vel[1], vel[2]])

def semimajor_axis(state, mu):
    r = np.linalg.norm(state[0:3])
    v = np.linalg.norm(state[3:6])
    a = 1/(2/r - v**2/mu)
    return a

def eccentricity(state, mu):
    r = state[0:3]
    v = state[3:6]
    r_mag = np.sqrt(np.dot(r, r))
    v_mag = np.sqrt(np.dot(v, v))
    e = (v_mag**2/mu - 1/r_mag)*r - 1/mu*np.dot(r, v)*v
    return e

def inclination(state):
    r = state[0:3]
    v = state[3:6]
    h = np.cross(r, v)
    h_mag = np.sqrt(np.dot(h, h))
    incl = np.arccos(np.dot(h/h_mag, np.array([0, 0, 1])))
    return incl

def node_vector(state):
    r = state[0:3]
    v = state[3:6]
    h = np.cross(r, v)
    n = np.cross(np.array([0, 0, 1]), h)
    return n


def RAAN(state):
    node = node_vector(state)
    node_mag = np.sqrt(np.dot(node, node))
    omega = np.arccos(np.dot(node, np.array([1, 0, 0])) / node_mag)
    if np.dot(node, np.array([0, 1, 0])) < 0:
        omega = 2*np.pi - omega
    return omega

def argument_of_periapse(state, mu):
    node = node_vector(state)
    node_mag = np.sqrt(np.dot(node, node))
    e = eccentricity(state, mu)
    e_mag = np.sqrt(np.dot(e, e))
    omega = np.arccos(np.dot(node, e)/(node_mag*e_mag))
    if (np.dot(e, np.array([0, 0, 1])) < 0):
        omega = 2*np.pi - omega
    return omega

def true_anomaly(state, mu):
    r = state[0:3]
    v = state[3:6]
    e = eccentricity(state, mu)
    r_mag = np.sqrt(np.dot(r, r))
    e_mag = np.sqrt(np.dot(e, e))
    f = np.arccos(np.dot(e, r)/(e_mag*r_mag))
    if (np.dot(r, v) < 0):
        f = 2*np.pi - f
    return f

def position(kep, mu):
    a = kep[0]
    e = kep[1]
    i = np.radians(kep[2])
    raan = np.radians(kep[3])
    omega = np.radians(kep[4])
    f = np.radians(kep[5])

    r = a*(1-e**2)/(1+e*np.cos(f))
    theta = omega + f
    pos = r * np.array([np.cos(theta)*np.cos(raan) - np.cos(i)*np.sin(raan)*np.sin(theta),
                        np.cos(theta)*np.sin(raan) + np.cos(i)*np.cos(raan)*np.sin(theta),
                        np.sin(i)*np.sin(theta)])
    return pos

def velocity(kep, mu):
    a = kep[0]
    e = kep[1]
    i = np.radians(kep[2])
    raan = np.radians(kep[3])
    omega = np.radians(kep[4])
    f = np.radians(kep[5])

    theta = omega + f

    h = np.sqrt(mu*a*(1-e**2))
    vel = -mu/h*np.array([-(np.cos(raan)*(np.sin(theta) + e*np.sin(omega)) + np.sin(raan)*(np.cos(theta) + e*np.cos(omega))*np.cos(i)),
                          -(np.sin(raan)*(np.sin(theta) + e*np.sin(omega)) + np.cos(raan)*(np.cos(theta) + e*np.cos(omega))*np.cos(i)),
                          (np.cos(theta) + e*np.cos(omega))*np.sin(i)])
                         
    return vel

# kep_elem_print = np.array([8000*1000, 0.125, np.radians(45), np.radians(90), np.radians(270), np.radians(5)])
# kep_elem = np.array([8000*1000, 0.125, 45, 90, 270, 5])
# state_vec = keplerian_to_state_vec(kep_elem, 3.986004418*10**14)
# kep_elem_check = state_vec_to_keplerian(state_vec, 3.986004418*10**14)
# disp.kep_elem("Initial",kep_elem_print)
# disp.state_vec("State Vec",state_vec/1000)
# disp.kep_elem("Check",kep_elem_check)