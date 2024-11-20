import utils.convert as convert
import utils.quaternion as quat
class Satellite:
    def __init__(self, name, state, omega, area, mass, solar_array_area ,colorscale, cd=2.2):
        self.name = name
        self.state = state
        self.ecef_crash = None
        self.qEci2Body = quat.init_quat(state, "lvlh")
        self.omega = omega
        self.area = area
        self.mass = mass
        self.solar_array_area = solar_array_area
        self.colorscale = colorscale
        self.cd = cd
        self.crashed = False
        self.history = {"time":[],
                        "state_x":[],
                        "state_y":[],
                        "state_z":[],
                        "state_vx":[],
                        "state_vy":[],
                        "state_vz":[],
                        "qEciToBody_q1":[],
                        "qEciToBody_q2":[],
                        "qEciToBody_q3":[],
                        "qEciToBody_q4":[],
                        "omega_x":[],
                        "omega_y":[],
                        "omega_z":[],
                        "state_x_bci":[],
                        "state_y_bci":[],
                        "state_z_bci":[],
                        "state_vx_bci":[],
                        "state_vy_bci":[],
                        "state_vz_bci":[],
                        "state_x_ecef":[],
                        "state_y_ecef":[],
                        "state_z_ecef":[],
                        "state_vx_ecef":[],
                        "state_vy_ecef":[],
                        "state_vz_ecef":[],
                        "state_lat":[],
                        "state_lon":[],
                        "illumination":[],
                        "power_avail":[]}

    def update_state(self, time, new_state, new_qEci2Body, new_state_bci, new_state_ecef, new_state_ll, new_state_illumination, new_power):
        self.state = new_state
        self.qEci2Body = new_qEci2Body
        self.history["time"].append(time)
        self.history["state_x"].append(self.state[0]/1000)
        self.history["state_y"].append(self.state[1]/1000)
        self.history["state_z"].append(self.state[2]/1000)
        self.history["state_vx"].append(self.state[3]/1000)
        self.history["state_vy"].append(self.state[4]/1000)
        self.history["state_vz"].append(self.state[5]/1000)
        self.history["qEciToBody_q1"].append(self.qEci2Body[0])
        self.history["qEciToBody_q2"].append(self.qEci2Body[1])
        self.history["qEciToBody_q3"].append(self.qEci2Body[2])
        self.history["qEciToBody_q4"].append(self.qEci2Body[3])
        self.history["omega_x"].append(self.omega[0])
        self.history["omega_y"].append(self.omega[1])
        self.history["omega_z"].append(self.omega[2])
        self.history["state_x_bci"].append(new_state_bci[0]/1000)
        self.history["state_y_bci"].append(new_state_bci[1]/1000)
        self.history["state_z_bci"].append(new_state_bci[2]/1000)
        self.history["state_vx_bci"].append(new_state_bci[3]/1000)
        self.history["state_vy_bci"].append(new_state_bci[4]/1000)
        self.history["state_vz_bci"].append(new_state_bci[5]/1000)
        self.history["state_x_ecef"].append(new_state_ecef[0]/1000)
        self.history["state_y_ecef"].append(new_state_ecef[1]/1000)
        self.history["state_z_ecef"].append(new_state_ecef[2]/1000)
        self.history["state_vx_ecef"].append(new_state_ecef[3]/1000)
        self.history["state_vy_ecef"].append(new_state_ecef[4]/1000)
        self.history["state_vz_ecef"].append(new_state_ecef[5]/1000)
        self.history["state_lat"].append(new_state_ll[0])
        self.history["state_lon"].append(new_state_ll[1])
        self.history["illumination"].append(new_state_illumination)
        self.history["power_avail"].append(new_power)

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
    
    def set_ecef_static(self, state, time):
        self.ecef_crash = convert.eci2ecef(state, time)
    
    def set_crashed(self, earth, time=0):
        self.crashed = True
        if earth:
            self.set_ecef_static(self.state, time)
    
    def is_crashed(self):
        return self.crashed
    
        