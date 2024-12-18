import numpy as np
from tqdm import tqdm

import Dynamics.dynamics as dyn
import utils.convert as convert
import utils.quaternion as quat
import utils.horizons as horizons
import Dynamics.body as body

class Simulator():

    def __init__(self, bodies, start, end, dt, horizons_dt):
        self.bodies = bodies
        t_array = np.arange(start, end, convert.convertSecToDays(dt))
        self.t_array = t_array
        self.time_since_j2000 = t_array[0]
        self.last_time = 2*t_array[0] - t_array[1]
        self.spacecrafts = []
        self.prev_true = self.time_since_j2000
        self.horizons_dt = horizons_dt
        for i, body in enumerate(self.bodies):
            if body.name == "Earth":
                self.idx_earth = i

    def init_bodies(bodies, start_time, end_time, dt):
        objs = []
        for obj in bodies:
            states, dt = horizons.get_state_from_horizons(obj, start_time, end_time, dt)
            obj = body.Body(obj, states)   
            objs.append(obj)
        return objs, dt
    
    def add_spacecrafts(self, spacecraft):
        self.spacecrafts = spacecraft

    def check_impact(self, sat, body):
        if np.linalg.norm(sat.state - body.state) < body.radius:
            print(f"{sat.get_name()} impacted {body.name}")
            if body.name == "Earth":
                sat.set_crashed(True, self.time_since_j2000)
            else:
                sat.set_crashed(False)

    def tic(self, dt):
        sigma = 5.67e-8
        T_star = 5772
        self.time_since_j2000 += dt
        next_true = self.prev_true + self.horizons_dt
        if self.time_since_j2000 == next_true:
            self.prev_true = self.time_since_j2000

        for sat in self.spacecrafts:
            new_state, new_qEci2Body, ecef_state, ll_state = np.zeros(6), np.zeros(4), np.zeros(6), np.zeros(2)
            
            if not sat.is_crashed():
                new_state, new_qEci2Body = dyn.orbit_prop(sat, dt, self.bodies)
                bci_state = convert.icrs2eci(new_state, self.bodies[0].state)
            else:
                if sat.ecef_crash is not None:
                    ecef_state = sat.ecef_crash  
                    new_state = self.bodies[self.idx_earth].state + convert.ecef2eci(ecef_state, convert.convertSecToDays(self.time_since_j2000))
                    bci_state = convert.icrs2eci(new_state, self.bodies[0].state)
                    new_qEci2Body = quat.init_quat(bci_state, "lvlh")
            
            for body in self.bodies:
                self.check_impact(sat, body)
            if self.bodies[0].name == "Earth":
                ecef_state = convert.eci2ecef(bci_state, convert.convertSecToDays(self.time_since_j2000))
                ll_state = convert.ecef2lla(ecef_state)

            illumination = dyn.total_illumination(sat.state, self.bodies)
            theta = 1
            f = (self.bodies[1].radius**2 * sigma * T_star**4) / ((np.linalg.norm(sat.state[0:3] - self.bodies[1].state[0:3])**2))
            power_avail = sat.solar_array_area * f * illumination * np.cos(theta)
            
            sat.update_state(self.time_since_j2000, new_state, new_qEci2Body, bci_state, ecef_state, ll_state, illumination, power_avail)
        
        for body in self.bodies:
            body.update_state(self.bodies, dt, self.time_since_j2000 == next_true)
            
    def run(self):
        for t in tqdm(self.t_array):
            self.tic(convert.convertDaysToSec(t-self.last_time))
            self.last_time = t
        return self.t_array, self.spacecrafts