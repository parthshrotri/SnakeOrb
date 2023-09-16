import numpy as np

def convertToSeconds(years, months, days, hours, minutes, seconds, milliseconds=0):
    return milliseconds/1000 + seconds + minutes*60 + hours*60*60 + days*24*60*60 + months*30*24*60*60 + years*365*24*60*60

def convertSecToDays(seconds):
    return seconds/(24*60*60)

def convertDaysToSec(days):
    return days*24*60*60

def convertCalendarToJ2000(years, months, days, hours, minutes, seconds, milliseconds=0, timezone=0):
    return convertToSeconds(years, months, days, hours, minutes, seconds, milliseconds) - convertToSeconds(2000, 1, 1, 12, 0, 0, 0) + timezone*60*60