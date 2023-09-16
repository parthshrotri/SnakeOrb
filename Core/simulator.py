import numpy as np
import pandas as pd
from tqdm import tqdm

import Dynamics.dynamics as dyn
import utils.time as time
import utils.convert as convert

class Simulator():

    def __init__(self, central_body, t_array, bodies):
        self.central_body = central_body
        self.t_array = t_array
        self.bodies = bodies
        self.t_array = t_array
        self.time_since_j2000 = t_array[0]
        self.last_time = 2*t_array[0] - t_array[1]

    def tic(self, satlist, dt):
        self.time_since_j2000 += dt
        new_state, new_qEci2Body = np.zeros(6), np.zeros(4)
        ecef_state = np.zeros(6)
        ll_state = np.zeros(2)
        timeDays = time.convertSecToDays(self.time_since_j2000)
        for sat in satlist:
            if not sat.is_crashed():
                new_state, new_qEci2Body = dyn.orbit_prop(sat, dt, self.central_body)

            newStateMag = np.linalg.norm(new_state[0:3])
            if newStateMag <= self.central_body.radius:
                if not sat.is_crashed():
                    print(f"{sat.get_name()} reentered {self.central_body.name}'s atmosphere")
                sat.set_crashed()
            if self.central_body.name == "Earth":
                ecef_state = convert.eci2ecef(new_state, time.convertSecToDays(self.time_since_j2000))
                ll_state = convert.ecef2lla(ecef_state)
            sat.update_state(self.time_since_j2000, new_state, new_qEci2Body, ecef_state, ll_state)
            
    def run(self):
        for t in tqdm(self.t_array):
            self.tic(self.bodies, t-self.last_time)
            self.last_time = t
        trajs = {}
        for sat in self.bodies:
            trajs[sat.get_name()] = sat.get_history()
        return trajs