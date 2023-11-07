import numpy as np
from astropy.time import Time
from astroquery.jplhorizons import Horizons

import utils.convert as convert

def get_state_from_horizons(body, start_time, end_time, dt):
    start_time = Time(start_time, format="jd", scale='utc').isot
    end_time = Time(end_time, format="jd", scale='utc').isot
    horizons_dt_str = ""
    horizons_dt = dt
    if dt <= 60:
        horizons_dt_str = "1m"
        horizons_dt = 60
    if body == "Earth":
        body = "399"
    elif body == "Moon":
        body = "301"
    elif body == "Sun":
        body = "10"
    elif body == "Mercury":
        body = "199"
    elif body == "Venus":
        body = "299"
    elif body == "Mars":
        body = "499"
    elif body == "Jupiter":
        body = "599"
    elif body == "Saturn":
        body == "699"
    elif body == "Uranus":
        body == "799"
    elif body == "Neptune":
        body == "899"
    elif body == "Pluto":
        body = "999"
    
    obj = Horizons(id=body, location='@0', epochs={'start':start_time, 'stop':end_time, 'step':horizons_dt_str})
    vecs = obj.vectors()
    x = convert.AU_to_meters(vecs["x"])
    y = convert.AU_to_meters(vecs["y"])
    z = convert.AU_to_meters(vecs["z"])
    vx = convert.AU_to_meters(vecs["vx"])/convert.convertDaysToSec(1)
    vy = convert.AU_to_meters(vecs["vy"])/convert.convertDaysToSec(1)
    vz = convert.AU_to_meters(vecs["vz"])/convert.convertDaysToSec(1)
    state = np.array([x, y, z, vx, vy, vz])
    return state, horizons_dt