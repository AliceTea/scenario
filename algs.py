# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 17:30:09 2017

@author: jason
"""

def fuzz_arima(timelist,statslist):
    pass

def payless(duration,timelist,statslist):
    pass

def swd(duration,timelist,statslist):
    pass

def adarate(duration,timelist,statslist):
    if statslist[len(statslist)-1] > 1000000:
        return max(duration/3,1)
    elif statslist[len(statslist)-1] < 500000:
        return min(duration*2,5)
    else:
        return duration
    pass