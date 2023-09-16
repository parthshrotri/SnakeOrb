import utils.convert as convert
import utils.quaternion as quat
class Satellite:
    def __init__(self, name, state, omega, cd, area, mass):
        self.name = name
        self.state = state
        self.qEci2Body = quat.init_quat(state, "lvlh")
        self.omega = omega
        self.cd = cd
        self.area = area
        self.mass = mass
        self.crashed = False
        self.history = {"time":[],
                        "state_x_eci":[],
                        "state_y_eci":[],
                        "state_z_eci":[],
                        "state_vx_eci":[],
                        "state_vy_eci":[],
                        "state_vz_eci":[],
                        "qEciToBody_q1":[],
                        "qEciToBody_q2":[],
                        "qEciToBody_q3":[],
                        "qEciToBody_q4":[],
                        "omega_x":[],
                        "omega_y":[],
                        "omega_z":[],
                        "state_x_ecef":[],
                        "state_y_ecef":[],
                        "state_z_ecef":[],
                        "state_vx_ecef":[],
                        "state_vy_ecef":[],
                        "state_vz_ecef":[],
                        "state_lat":[],
                        "state_lon":[]}

    def update_state(self, time, new_state, new_qEci2Body, new_state_ecef, new_state_ll):
        self.state = new_state
        self.qEci2Body = new_qEci2Body
        self.history["time"].append(time)
        self.history["state_x_eci"].append(new_state[0])
        self.history["state_y_eci"].append(new_state[1])
        self.history["state_z_eci"].append(new_state[2])
        self.history["state_vx_eci"].append(new_state[3])
        self.history["state_vy_eci"].append(new_state[4])
        self.history["state_vz_eci"].append(new_state[5])
        self.history["qEciToBody_q1"].append(self.qEci2Body[0])
        self.history["qEciToBody_q2"].append(self.qEci2Body[1])
        self.history["qEciToBody_q3"].append(self.qEci2Body[2])
        self.history["qEciToBody_q4"].append(self.qEci2Body[3])
        self.history["omega_x"].append(self.omega[0])
        self.history["omega_y"].append(self.omega[1])
        self.history["omega_z"].append(self.omega[2])
        self.history["state_x_ecef"].append(new_state_ecef[0])
        self.history["state_y_ecef"].append(new_state_ecef[1])
        self.history["state_z_ecef"].append(new_state_ecef[2])
        self.history["state_vx_ecef"].append(new_state_ecef[3])
        self.history["state_vy_ecef"].append(new_state_ecef[4])
        self.history["state_vz_ecef"].append(new_state_ecef[5])
        self.history["state_lat"].append(new_state_ll[0])
        self.history["state_lon"].append(new_state_ll[1])

    def get_state(self):
        return self.state
    
    def get_ecef_state(self, time):
        return convert.eci2ecef(self.state, time)
    
    def get_qEci2Body(self):
        return self.qEci2Body

    def get_name(self):
        return self.name
    
    def get_history(self):
        return self.history
    
    def set_crashed(self):
        self.crashed = True
    
    def is_crashed(self):
        return self.crashed
    
        