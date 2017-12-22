# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:53:35 2017

@author: jason
"""

import sys
import re
import algs
import matplotlib.pyplot as plt


def measure(duration,timelist,statslist,method):
    ret=1
    if method=='default':
        ret=1
    elif method=='SWD':
        pass
    elif method=='adarate':
        pass
    elif method=='fuzz_arima':
        ret = algs.fuzz_arima(timelist,statslist)
    elif method=='payless':
        ret = algs.payless(duration,timelist,statslist)
        
    return ret

'''
Error Rate:
The error rate reflect the difference between measured data and real data.
The measured data need interpolation.
'''

def errorate(timelist=[],ratelist=[],realratelist=[]):
    error = 0
    i=0
    tmp=0
    while i<len(timelist):
        pass
    pass
    
def overhead(ratelist):
    pass



file = open(r'/media/jason/Seagate Backup Plus Drive/实验数据/2017年12月11日UTC.datx','r+')
ts=[]
cnt=0
duration=1
statslist=[]
timelist=[]
ratelist=[]
method='payless'
line=file.readline()
loop=0
count=0
ts=0
while line != "":
#    cnt=cnt+1
#    print cnt
    duration=measure(duration,timelist,statslist,method)
    assert duration>0,'duration is illedga'
    loop=duration
    while loop>0:
        loop=loop-1
        line=file.readline()
        data=re.findall('\d+',line)
        if(data==[]):
            break
        count=count+int(data[1])
    ts=ts+duration
    ratelist.append(count/duration)
    statslist.append(count)
    timelist.append(ts)
    count=0

plt.plot(timelist,ratelist)