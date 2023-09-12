import numpy as np
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import Dynamics.dynamics as dyn
import Dynamics.body as body
import Dynamics.satellite as satellite
import utils.OEConvert as OEConvert
import utils.display as disp

from tqdm import tqdm

main_body = body.central_body("Earth")

time_since_j2000 = 2460170.5*24*60*60 # s
tf = time_since_j2000 + 24*60*60 # s
dt = 60 # s

# Hubble
sat1_eciStateInit = 1000 * np.array([ 3.082461354447172E+03, -2.886974162019587E+03, -5.328634038549732E+03,  5.517292527064879E+00,  5.292343106730224E+00,  3.261779963465199E-01]) 
sat1_area = [13.2,4.2, 4.2]
sat1_mass = 12246 # kg

# TDRS-C
sat2_eciStateInit = 1000 * np.array([1.834972617364065E+03, -4.094912584403288E+04, -9.447814899874296E+03,  3.075240221002479E+00,  1.063463080156267E-01,  1.717410482773772E-01])
sat1_area = [17.3, 14.2, 14.2]
sat1_mass = 2224.9  # kg

# NAVSTAR 68
sat3_eciStateInit = 1000 * np.array([-1.470747376099415E+04, -5.876519871435620E+03, -2.162638997372999E+04,  2.154795554948612E+00, -3.122108078672046E+00, -5.839907110615412E-01])
sat1_area = [2.49, 2.03, 2.24]
sat1_mass = 1633 # kg

# IntelSat 901
sat4_eciStateInit = 1000 * np.array([1.721649642391115E+04, -3.849194159448530E+04, -2.941039527884672E+01,  2.806682181074147E+00,  1.255084892346541E+00, -4.767689185029973E-03])
sat1_area = [5.6, 3.5, 3.0]
sat1_mass = 4725 # kg

sat1_qEci2Body = dyn.init_quat(sat1_eciStateInit, "ram")
sat1_omega = np.array([0, 0, 0])
sat1_cd = [2.2, 2.2, 2.2]

sat1 = satellite.Satellite("Hubble", sat1_eciStateInit, sat1_qEci2Body, sat1_omega, sat1_cd, sat1_area, sat1_mass)
sat2 = satellite.Satellite("TDRS-C", sat2_eciStateInit, sat1_qEci2Body, sat1_omega, sat1_cd, sat1_area, sat1_mass)
sat3 = satellite.Satellite("NAVSTAR 68", sat3_eciStateInit, sat1_qEci2Body, sat1_omega, sat1_cd, sat1_area, sat1_mass)
sat4 = satellite.Satellite("IntelSat 901", sat4_eciStateInit, sat1_qEci2Body, sat1_omega, sat1_cd, sat1_area, sat1_mass)
sat1_ecef_state = dyn.eci2ecef(sat1_eciStateInit, time_since_j2000/(60*60*24))
sat1_ll_state = dyn.ecef2ll(sat1_ecef_state)
sat1.update_state(0, sat1_eciStateInit, sat1_qEci2Body, sat1_ecef_state, sat1_ll_state)
sat2_ecef_state = dyn.eci2ecef(sat2_eciStateInit, time_since_j2000/(60*60*24))
sat2_ll_state = dyn.ecef2ll(sat2_ecef_state)
sat2.update_state(0, sat2_eciStateInit, sat1_qEci2Body, sat2_ecef_state, sat2_ll_state)
sat3_ecef_state = dyn.eci2ecef(sat3_eciStateInit, time_since_j2000/(60*60*24))
sat3_ll_state = dyn.ecef2ll(sat3_ecef_state)
sat3.update_state(0, sat3_eciStateInit, sat1_qEci2Body, sat3_ecef_state, sat3_ll_state)
sat4_ecef_state = dyn.eci2ecef(sat4_eciStateInit, time_since_j2000/(60*60*24))
sat4_ll_state = dyn.ecef2ll(sat4_ecef_state)
sat4.update_state(0, sat4_eciStateInit, sat1_qEci2Body, sat4_ecef_state, sat4_ll_state)

t_array = np.arange(time_since_j2000, tf, dt)

for t in tqdm(t_array):
    time_since_j2000 += dt
    new_state, new_qEci2Body = dyn.orbit_prop(sat1, dt, main_body)
    ecef_state = dyn.eci2ecef(new_state, time_since_j2000/(60*60*24))
    ll_state = dyn.ecef2ll(ecef_state)
    sat1.update_state(t, new_state, new_qEci2Body, ecef_state, ll_state)

    new_state, new_qEci2Body = dyn.orbit_prop(sat2, dt, main_body)
    ecef_state = dyn.eci2ecef(new_state, time_since_j2000/(60*60*24))
    ll_state = dyn.ecef2ll(ecef_state)
    sat2.update_state(t, new_state, new_qEci2Body, ecef_state, ll_state)

    new_state, new_qEci2Body = dyn.orbit_prop(sat3, dt, main_body)
    ecef_state = dyn.eci2ecef(new_state, time_since_j2000/(60*60*24))
    ll_state = dyn.ecef2ll(ecef_state)
    sat3.update_state(t, new_state, new_qEci2Body, ecef_state, ll_state)

    new_state, new_qEci2Body = dyn.orbit_prop(sat4, dt, main_body)
    ecef_state = dyn.eci2ecef(new_state, time_since_j2000/(60*60*24))
    ll_state = dyn.ecef2ll(ecef_state)
    sat4.update_state(t, new_state, new_qEci2Body, ecef_state, ll_state)
sat1_traj = pd.DataFrame(sat1.history)
sat2_traj = pd.DataFrame(sat2.history)
sat3_traj = pd.DataFrame(sat3.history)
sat4_traj = pd.DataFrame(sat4.history)

trajs = [sat1_traj, sat2_traj, sat3_traj, sat4_traj]
colorscales = ['Purp', 'Reds', 'Magenta', 'Blues']
names = [sat1.get_name(), sat2.get_name(), sat3.get_name(), sat4.get_name()]

disp.BCI(t_array, trajs, names, colorscales, central_body=main_body)
disp.BCBF(t_array, trajs, names, colorscales, central_body=main_body)
disp.ground_track(t_array, trajs, names, colorscales, central_body=main_body)

disp.state_vec(sat1.get_name(), sat1.get_state())
disp.state_vec(sat2.get_name(), sat2.get_state())
disp.state_vec(sat3.get_name(), sat3.get_state())
disp.state_vec(sat4.get_name(), sat4.get_state())

disp.kep_elem(sat1.get_name(), OEConvert.state_vec_to_keplerian(sat1.get_state(), main_body.mu))
disp.kep_elem(sat2.get_name(), OEConvert.state_vec_to_keplerian(sat2.get_state(), main_body.mu))
disp.kep_elem(sat3.get_name(), OEConvert.state_vec_to_keplerian(sat3.get_state(), main_body.mu))
disp.kep_elem(sat4.get_name(), OEConvert.state_vec_to_keplerian(sat4.get_state(), main_body.mu))