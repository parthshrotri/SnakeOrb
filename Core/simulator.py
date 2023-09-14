import numpy as np
import pandas as pd
from tqdm import tqdm

import Dynamics.dynamics as dyn

class Simulator():

    def __init__(self, central_body, t_array, bodies):
        self.central_body = central_body
        self.t_array = t_array
        self.bodies = bodies
        self.t_array = t_array
        self.time_since_j2000 = t_array[0]
        self.last_time = t_array[0]

    def tic(self, satlist, dt):
        self.time_since_j2000 += dt
        new_state, new_qEci2Body = np.zeros(6), np.zeros(4)
        ecef_state = np.zeros(6)
        ll_state = np.zeros(2)

        for sat in satlist:
            new_state, new_qEci2Body = dyn.orbit_prop(sat, dt, self.central_body)
            if self.central_body.name == "Earth":
                ecef_state = dyn.eci2ecef(new_state, self.time_since_j2000/(60*60*24))
                ll_state = dyn.ecef2ll(ecef_state)
            sat.update_state(self.time_since_j2000, new_state, new_qEci2Body, ecef_state, ll_state)
            
    def run(self):
        for t in tqdm(self.t_array):
            self.tic(self.bodies, t-self.last_time)
            self.last_time = t
        trajs = {}
        for sat in self.bodies:
            trajs[sat.get_name()] = sat.get_history()
        return trajs