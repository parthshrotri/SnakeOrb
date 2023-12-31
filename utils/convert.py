import numpy as np

def eci2ecef(eciState, days_since_j2000):
    gamma = np.radians(360.9856123035484*days_since_j2000 + 280.46)
    dcm = np.array([[np.cos(gamma), np.sin(gamma), 0],
                    [-np.sin(gamma), np.cos(gamma), 0],
                    [0, 0, 1]])
    ecefState = np.zeros(eciState.shape)
    ecefState[0:3] = np.matmul(dcm, eciState[0:3].T).T
    ecefState[3:6] = np.matmul(dcm, eciState[3:6].T).T

    return ecefState

def ecef2eci(ecefState, days_since_j2000):
    gamma = -np.radians(360.9856123035484*days_since_j2000 + 280.46)
    dcm = np.array([[np.cos(gamma), -np.sin(gamma), 0],
                    [np.sin(gamma), np.cos(gamma), 0],
                    [0, 0, 1]])
    eciState = np.zeros(ecefState.shape)
    eciState[0:3] = np.matmul(dcm, ecefState[0:3].T).T
    eciState[3:6] = np.matmul(dcm, ecefState[3:6].T).T

    return eciState

def ecef2lla(ecefState):
    if np.linalg.norm(ecefState) == 0:
        return np.array([np.nan, np.nan, np.nan])
    r_delta = np.linalg.norm(ecefState[0:1])
    sinA = ecefState[1]/r_delta
    cosA = ecefState[0]/r_delta

    Lon = np.arctan2(sinA,cosA)

    if Lon < -np.pi:
        Lon = Lon + 2*np.pi

    Lat = np.arcsin(ecefState[2]/np.linalg.norm(ecefState))
    return np.array([np.degrees(Lat), np.degrees(Lon), np.linalg.norm(ecefState[0:2])])

def AU_to_meters(AU):
    return AU*149597870700

def meters_to_AU(meters):
    return meters/149597870700

def km_to_AU(km):
    return km/149597870.700

def AU_to_km(au):
    return au*149597870.700

def convertToSeconds(years, months, days, hours, minutes, seconds, milliseconds=0):
    return milliseconds/1000 + seconds + minutes*60 + hours*60*60 + days*24*60*60 + months*30*24*60*60 + years*365*24*60*60

def convertSecToDays(seconds):
    return seconds/(24*60*60)

def convertDaysToSec(days):
    return days*24*60*60

def convertCalendarToJ2000(years, months, days, hours, minutes, seconds, milliseconds=0, timezone=0):
    return convertToSeconds(years, months, days, hours, minutes, seconds, milliseconds) - convertToSeconds(2000, 1, 1, 12, 0, 0, 0) + timezone*60*60
