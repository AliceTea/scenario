# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 17:30:09 2017

@author: jason
"""

def fuzz_arima(timelist,statslist):
    pass

def payless(duration,timelist,statslist):
    if len(statslist) < 1:
        return duration
    if statslist[len(statslist)-1] > 5000000:
        return max(duration/3,1)
    elif statslist[len(statslist)-1] < 3000000:
        return min(duration*2,100)
    else:
        return duration

def swd(duration,timelist,statslist):
    pass

def adarate(duration,timelist,statslist):
    pass