import numpy as np
from astropy.time import Time

import Core.simulator as sim
import Dynamics.satellite as satellite
import utils.OEConvert as OEConvert
import utils.display as disp
import utils.convert as convert
import utils.horizons as horizons

start_time = Time("2020-01-01T00:00:00", format='isot', scale='utc').jd # s
duration = convert.convertToSeconds(years=0, months=0, days=1, hours=0, minutes=0, seconds=0)
end_time = start_time+convert.convertSecToDays(duration) # s
dt = 1 # s 

def_bodies = ["Earth", "Sun"]
bodies, horizons_dt = sim.Simulator.init_bodies(def_bodies, start_time, end_time, dt)
SnakeOrb = sim.Simulator(bodies, start_time, end_time, dt, horizons_dt)

# Hubble
sat1_stateInit = horizons.get_state_from_horizons("Hubble", start_time, start_time+convert.convertSecToDays(horizons_dt), dt)[0][:,0]
disp.state_vec("Hubble", sat1_stateInit)
sat1_area = np.array([13.2,4.2, 4.2])
sat1_mass = 12246 # kg

# TDRS-C
sat2_stateInit = horizons.get_state_from_horizons("TDRS-3", start_time, start_time+convert.convertSecToDays(horizons_dt), dt)[0][:,0]
sat2_area = np.array([17.3, 14.2, 14.2])
sat2_mass = 2224.9  # kg

# NAVSTAR 68
sat3_stateInit = horizons.get_state_from_horizons("NAVSTAR-68", start_time, start_time+convert.convertSecToDays(horizons_dt), dt)[0][:,0]
sat3_area = np.array([2.49, 2.03, 2.24])
sat3_mass = 1633 # kg

# IntelSat 901
sat4_stateInit = horizons.get_state_from_horizons("INTELSAT-901", start_time, start_time+convert.convertSecToDays(horizons_dt), dt)[0][:,0]
sat4_area = np.array([5.6, 3.5, 3.0])
sat4_mass = 4725 # kg

sat1_omega = np.array([0, 0, 0])

sat1 = satellite.Satellite("Hubble", sat1_stateInit, sat1_omega, sat1_area, sat1_mass, 'Purp')
sat2 = satellite.Satellite("TDRS-3", sat2_stateInit, sat1_omega, sat2_area, sat2_mass, 'Reds')
sat3 = satellite.Satellite("NAVSTAR-68", sat3_stateInit, sat1_omega, sat3_area, sat3_mass, 'Magenta')
sat4 = satellite.Satellite("INTELSAT-901", sat4_stateInit, sat1_omega, sat4_area, sat4_mass, 'Blues')
SnakeOrb.add_spacecrafts([sat1, sat2, sat3, sat4])

times, spacecraft = SnakeOrb.run()

disp.solar_system(times, spacecraft, bodies, show_sun=False)
disp.BCI(times, spacecraft, bodies)
disp.ECEF(times, spacecraft, bodies)
disp.ground_track(times, spacecraft, bodies)

for sat in spacecraft:
    disp.state_vec(sat.get_name(), sat.get_state()-bodies[0].state)
    disp.kep_elem(sat.get_name(), OEConvert.state_vec_to_keplerian(sat.get_state()-bodies[0].state, bodies[0].mu))