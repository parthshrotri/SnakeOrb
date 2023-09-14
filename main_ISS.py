import numpy as np

import Core.simulator as sim
import Dynamics.dynamics as dyn
import Dynamics.body as body
import Dynamics.satellite as satellite
import utils.OEConvert as OEConvert
import utils.display as disp

main_body = body.central_body("Earth")

start_time = 0
end_time = start_time+365*60*60 # ss
dt = 60 # s

# International Space Station
alt = 423*1000 # km
sat1_kep = np.array([main_body.radius+alt, 0.0005466, 51.6410, 0.0, 0.0, 0.0])
sat1_eciStateInit = OEConvert.keplerian_to_state_vec(sat1_kep, main_body.mu)
sat1_area = [94, 73, 45]
sat1_mass = 420000 # kg
sat1_qEci2Body = dyn.init_quat(sat1_eciStateInit, "lvlh")
sat1_omega = np.array([0, 0, 0])
sat1_cd = [2.2, 2.2, 2.2]

sat1 = satellite.Satellite("International Space Station", sat1_eciStateInit, sat1_qEci2Body, sat1_omega, sat1_cd, sat1_area, sat1_mass)

t_array = np.arange(start_time, end_time, dt)
SnakeOrb = sim.Simulator(main_body, t_array, [sat1])

trajs = SnakeOrb.run()

colorscales = ['Purp']
names = [sat1.get_name()]

disp.BCI(t_array, trajs, names, colorscales, central_body=main_body)
disp.ECEF(t_array, trajs, names, colorscales, central_body=main_body)
disp.ground_track(t_array, trajs, names, colorscales, central_body=main_body)

disp.kep_elem(sat1.get_name(), OEConvert.state_vec_to_keplerian(sat1.get_state(), main_body.mu))