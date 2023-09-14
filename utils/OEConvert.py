import numpy as np

def state_vec_to_keplerian(state, mu):
    a = semimajor_axis(state, mu)
    e = np.linalg.norm(eccentricity(state, mu))
    i = inclination(state)
    raan = RAAN(state)
    omega = argument_of_periapse(state, mu)
    v = true_anomaly(state, mu)
    return np.array([a, e, i, raan, omega, v])

def keplerian_to_state_vec(kep, mu):
    kep[2] = np.radians(kep[2])
    kep[3] = np.radians(kep[3])
    kep[4] = np.radians(kep[4])
    kep[5] = np.radians(kep[5])
    pos = r(kep)
    vel = v(kep, mu)
    return np.array([pos[0], pos[1], pos[2], vel[0], vel[1], vel[2]])

def r(kep):
    a = kep[0]
    e = kep[1]
    i = kep[2]
    raan = kep[3]
    omega = kep[4]
    f = kep[5]
    
    r_mag = a*(1-e**2)/(1+e*np.cos(f))
    theta = omega + f
    pos = r_mag*np.array([np.cos(theta)*np.cos(raan)-np.cos(i)*np.sin(theta)*np.sin(raan),
                  np.cos(theta)*np.sin(raan)+np.cos(i)*np.cos(raan)*np.sin(theta),
                  np.sin(i)*np.sin(theta)])
    return pos

def v(kep, mu):
    a = kep[0]
    e = kep[1]
    i = kep[2]
    raan = kep[3]
    omega = kep[4]
    f = kep[5]

    h_mag = np.sqrt(mu*a*(1-e**2))
    theta = omega + f
    vel = (mu/h_mag)*np.array([-np.cos(raan)*(np.sin(theta) + e*np.sin(omega)) - np.sin(raan)*(np.cos(theta) + e*np.cos(omega))*np.cos(i),
                             -np.sin(raan)*(np.sin(theta) + e*np.sin(omega)) - np.cos(raan)*(np.cos(theta) + e*np.cos(omega))*np.cos(i),
                             (np.cos(theta) + e*np.cos(omega))*np.sin(i)])
    
    return vel

def semimajor_axis(state, mu):
    r_mag = np.linalg.norm(state[0:3])
    v_mag = np.linalg.norm(state[3:6])
    a = 1/((2/r_mag - v_mag**2/mu))
    return a

def eccentricity(state, mu):
    r = state[0:3]
    v = state[3:6]
    r_mag = np.linalg.norm(r)
    v_mag = np.linalg.norm(v)
    e_vec = (v_mag**2/mu - 1/r_mag)*r - np.dot(r,v)*v/mu
    return e_vec

def node_line(state):
    r = state[0:3]
    v = state[3:6]
    h_vec = np.cross(r,v)
    n_vec = np.cross(np.array([0,0,1]), h_vec)
    return n_vec

def inclination(state):
    r = state[0:3]
    v = state[3:6]
    h_vec = np.cross(r,v)
    h_mag = np.linalg.norm(h_vec)
    i = np.arccos(h_vec[2]/h_mag)
    return i

def RAAN(state):
    n_vec = node_line(state)
    n_mag = np.linalg.norm(n_vec)
    raan = np.arccos(np.dot([1, 0, 0], n_vec)/n_mag)
    return raan

def argument_of_periapse(state, mu):
    e_vec = eccentricity(state, mu)
    n_vec = node_line(state)
    n_mag = np.linalg.norm(n_vec)
    e_mag = np.linalg.norm(e_vec)
    omega = np.arccos(np.dot(n_vec, e_vec)/(n_mag*e_mag))
    if e_vec[2] < 0:
        omega = 2*np.pi - omega
    return omega

def true_anomaly(state, mu):
    r = state[0:3]
    e = eccentricity(state, mu)
    r_mag = np.linalg.norm(r)
    e_mag = np.linalg.norm(e)
    v = np.arccos(np.dot(e,r)/(e_mag*r_mag))
    if np.linalg.norm(np.dot(r,v)) < 0:
        v = 2*np.pi - v
    return v
