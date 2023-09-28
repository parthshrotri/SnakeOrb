import numpy as np

import Core.simulator as sim
import Dynamics.body as body
import Dynamics.satellite as satellite
import utils.OEConvert as OEConvert
import utils.display as disp
import utils.time as time

main_body = body.central_body("Earth")

start_time = time.convertCalendarToJ2000(2002, 7, 16, 0, 1, 0, 0, -7)
duration = time.convertToSeconds(years=0, months=0, days=1, hours=0, minutes=10, seconds=0)
end_time = start_time+duration # s
dt = 60 # s

# Dragon
sat1_kep = np.array([26600*1000, 0.737, 63.4, 90, 270, 3])
sat1_eciStateInit = OEConvert.keplerian_to_state_vec(sat1_kep, main_body.mu)

sat1_area = np.array([np.pi*2**2, 5*4, 5*4])
sat1_mass = 9616 # kg
sat1_omega = np.array([0, 0, 0])
sat1_cd = 2.2

sat1 = satellite.Satellite("Dragon", sat1_eciStateInit, sat1_omega, sat1_cd, sat1_area, sat1_mass)

t_array = np.arange(start_time, end_time, dt)
SnakeOrb = sim.Simulator(main_body, t_array, [sat1])

trajs = SnakeOrb.run()

colorscales = ['Purp']
names = [sat1.get_name()]

disp.BCI(t_array, trajs, names, colorscales, central_body=main_body)
disp.ECEF(t_array, trajs, names, colorscales, central_body=main_body)
disp.ground_track(t_array, trajs, names, colorscales, central_body=main_body)

disp.state_vec(sat1.get_name(), sat1.get_state())
disp.kep_elem(sat1.get_name(), OEConvert.state_vec_to_keplerian(sat1.get_state(), main_body.mu))