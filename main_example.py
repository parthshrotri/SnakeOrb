import numpy as np

import Core.simulator as sim
import Dynamics.dynamics as dyn
import Dynamics.body as body
import Dynamics.satellite as satellite
import utils.OEConvert as OEConvert
import utils.display as disp

main_body = body.central_body("Earth")

start_time = 2460170.5*24*60*60 # s
end_time = start_time + 24*60*60 # s
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

sat1_qEci2Body = dyn.init_quat(sat1_eciStateInit, "lvlh")
sat1_omega = np.array([0, 0, 0])
sat1_cd = [2.2, 2.2, 2.2]

sat1 = satellite.Satellite("Hubble", sat1_eciStateInit, sat1_qEci2Body, sat1_omega, sat1_cd, sat1_area, sat1_mass)
sat2 = satellite.Satellite("TDRS-C", sat2_eciStateInit, sat1_qEci2Body, sat1_omega, sat1_cd, sat1_area, sat1_mass)
sat3 = satellite.Satellite("NAVSTAR 68", sat3_eciStateInit, sat1_qEci2Body, sat1_omega, sat1_cd, sat1_area, sat1_mass)
sat4 = satellite.Satellite("IntelSat 901", sat4_eciStateInit, sat1_qEci2Body, sat1_omega, sat1_cd, sat1_area, sat1_mass)

t_array = np.arange(start_time, end_time, dt)
SnakeOrb = sim.Simulator(main_body, t_array, [sat1, sat2, sat3, sat4])

trajs = SnakeOrb.run()

colorscales = ['Purp', 'Reds', 'Magenta', 'Blues']
names = [sat1.get_name(), sat2.get_name(), sat3.get_name(), sat4.get_name()]

disp.BCI(t_array, trajs, names, colorscales, central_body=main_body)
disp.ECEF(t_array, trajs, names, colorscales, central_body=main_body)
disp.ground_track(t_array, trajs, names, colorscales, central_body=main_body)

disp.state_vec(sat1.get_name(), sat1.get_state())
disp.state_vec(sat2.get_name(), sat2.get_state())
disp.state_vec(sat3.get_name(), sat3.get_state())
disp.state_vec(sat4.get_name(), sat4.get_state())

disp.kep_elem(sat1.get_name(), OEConvert.state_vec_to_keplerian(sat1.get_state(), main_body.mu))
disp.kep_elem(sat2.get_name(), OEConvert.state_vec_to_keplerian(sat2.get_state(), main_body.mu))
disp.kep_elem(sat3.get_name(), OEConvert.state_vec_to_keplerian(sat3.get_state(), main_body.mu))
disp.kep_elem(sat4.get_name(), OEConvert.state_vec_to_keplerian(sat4.get_state(), main_body.mu))