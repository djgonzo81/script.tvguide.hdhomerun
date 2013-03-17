import datetime as dt
import xbmc
import xbmcaddon

__addon_id__= 'service.tvguide.hdhomerun'
__Addon = xbmcaddon.Addon(__addon_id__)

def convertDateToString(value):
    return str(value.year).zfill(4) + str(value.month).zfill(2) + str(value.day).zfill(2) + str(value.hour).zfill(2) + str(value.minute).zfill(2) + str(value.second).zfill(2)

def convertStringToDate(value):
    return dt.datetime(int(value[:4]), int(value[4:][:2]), int(value[6:][:2]), int(value[8:][:2]), int(value[10:][:2]), int(value[12:]))

def encode(string):
    return string.encode('UTF-8','replace')

def getSetting(name):
    return __Addon.getSetting(name)

def isNullOrEmpty(value):
    return value is None or len(value) == 0

def log(message,loglevel=xbmc.LOGNOTICE):
    xbmc.log(encode("[" + __addon_id__ + "]: " + message),level=loglevel)

def setSetting(name,value):
    __Addon.setSetting(name,value)
