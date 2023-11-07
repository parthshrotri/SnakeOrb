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

# International Space Station
alt = 423*1000 # km
sat1_kep = np.array([bodies[0].radius+alt, 0.0005466, 51.6410, 30, 270, 0])
sat1_stateInit = OEConvert.keplerian_to_state_vec(sat1_kep, bodies[0].mu)+bodies[0].state
sat1_area = np.array([94, 73, 45])
sat1_mass = 420000 # kg
sat1_omega = np.array([0, 0, 0])

sat1 = satellite.Satellite("International Space Station", sat1_stateInit, sat1_omega, sat1_area, sat1_mass, 'Purp')
SnakeOrb.add_spacecrafts([sat1])

times, spacecraft = SnakeOrb.run()

disp.solar_system(times, spacecraft, bodies, show_sun=False)
disp.BCI(times, spacecraft, bodies)
disp.ECEF(times, spacecraft, bodies)
disp.ground_track(times, spacecraft, bodies)

disp.state_vec(sat1.get_name(), sat1.get_state()-bodies[0].state)
disp.kep_elem(sat1.get_name(), OEConvert.state_vec_to_keplerian(sat1.get_state()-bodies[0].state, bodies[0].mu))