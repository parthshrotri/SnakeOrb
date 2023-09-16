import numpy as np

# Quaternion defined as: q1 = real, q2 = i, q3 = j, q4 = k
def init_quat(eciState, attitude):
    if attitude == "lvlh":
        body_vec_in_eci = eciState[3:6]
        eci_x = np.array([0,1,0])

        axis = np.cross(body_vec_in_eci, eci_x)
        if np.linalg.norm(axis) == 0:
            q = np.array([1,0,0,0])
            return q
        angle = np.arccos(np.dot(body_vec_in_eci, eci_x) / (np.linalg.norm(body_vec_in_eci)))
        q = np.array([np.cos(angle/2), axis[0]*np.sin(angle/2), axis[1]*np.sin(angle/2), axis[2]*np.sin(angle/2)])
        return qnorm(q)
    
def qinv(quat):
    return np.array([quat[0], -quat[1], -quat[2], -quat[3]]) / np.linalg.norm(quat)

def qnorm(quat):
    return quat / np.linalg.norm(quat)

def qov(quat, vec):
    quat = qnorm(quat)
    vec = np.array([0, vec[0], vec[1], vec[2]])
    q_inv = qinv(quat)
    return (q_inv * vec * quat)[1:4]

def qoq(quat1, quat2):
    quat1 = qnorm(quat1)
    quat2 = qnorm(quat2)
    return quat1*quat2

def qprop(q, omega, dt):
    q = qnorm(q)
    if(np.linalg.norm(omega) != 0):
        omega = omega / np.linalg.norm(omega)
    qdot = 1/2 * np.array([0, omega[0], omega[1], omega[2]]) * q
    q = q + qdot*dt
    return qnorm(q)
