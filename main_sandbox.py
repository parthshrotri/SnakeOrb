import numpy as np
from astropy.time import Time

import Core.simulator as sim
import Dynamics.satellite as satellite
import utils.OEConvert as OEConvert
import utils.display as disp
import utils.convert as convert

start_time = Time("2020-01-01T00:00:00", format='isot', scale='utc').jd # s
duration = convert.convertToSeconds(years=0, months=0, days=1, hours=0, minutes=0, seconds=0)
end_time = start_time+convert.convertSecToDays(duration) # s
dt = 1 # s 

def_bodies = ["Earth", "Sun"]
bodies, horizons_dt = sim.Simulator.init_bodies(def_bodies, start_time, end_time, dt)
SnakeOrb = sim.Simulator(bodies, start_time, end_time, dt, horizons_dt)

# Dragon
sat1_kep = np.array([26600*1000, 0.737, 63.4, 90, 270, 3])
sat1_stateInit = OEConvert.keplerian_to_state_vec(sat1_kep, bodies[0].mu)
sat1_area = np.array([np.pi*2**2, 5*4, 5*4])
sat1_mass = 9616 # kg
sat1_omega = np.array([0, 0, 0])
sat1_cd = 2.2

sat1 = satellite.Satellite("Dragon", sat1_stateInit+bodies[0].state, sat1_omega, sat1_cd, sat1_area, sat1_mass)
SnakeOrb.add_spacecrafts([sat1])

trajs = SnakeOrb.run()

colorscales = ['Purp']
names = [sat1.get_name()]

disp.solar_system(SnakeOrb.t_array, trajs, names, colorscales, bodies, show_sun=False)
disp.BCI(SnakeOrb.t_array, trajs, names, colorscales, bodies)
disp.ECEF(SnakeOrb.t_array, trajs, names, colorscales, bodies)
disp.ground_track(SnakeOrb.t_array, trajs, names, colorscales, bodies)

disp.state_vec(sat1.get_name(), sat1.get_state()-bodies[0].state)
disp.kep_elem(sat1.get_name(), OEConvert.state_vec_to_keplerian(sat1.get_state()-bodies[0].state, bodies[0].mu))