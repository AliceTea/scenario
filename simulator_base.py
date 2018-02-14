# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:53:35 2017

@author: jason
"""

import sys
import re
import algs
import matplotlib.pyplot as plt
import math
import pandas as pd
from scipy import interpolate


def predict(timelist,statslist,method,*args):
    ret = 0
    if method=='fuzz_arima':
        pass
    elif method=='fuzz_RNN':
        pass
    elif method=='RNN':
        pass
    elif method=='arima':
        pass
    return ret


def measure(duration,timelist,statslist,method,*args):
    ret=1
    if method=='default':
        ret=1
    elif method=='SWT':
        if len(args)!=1:
            ret = algs.swt(duration,timelist,statslist,10)
        else:
            ret = algs.swt(duration,timelist,statslist,args[0])
    elif method=='adarate':
        if len(args)!=1:
            ret = algs.adarate(duration,timelist,statslist,10)
        else:
            ret = algs.adarate(duration,timelist,statslist,args[0])
    elif method=='sw_arima':
        ret = algs.sw_arima(timelist,pd.Series(statslist),statslist)
    elif method=='payless':
        ret = algs.payless(duration,timelist,statslist)
        
    return ret

'''
Error Rate:
The error rate reflect the difference between measured data and real data.
The measured data need interpolation.
'''

def errorate(timelist=[],ratelist=[],realratelist=[]):
    i=0 
    while len(realratelist) > len(timelist):
        if timelist[i] > i+1:
            timelist.insert(i,i+1)
            ratelist.insert(i,ratelist[i-1])
        else:
            i=i+1

#    plt.plot(timelist[0:2645],realratelist)
    i=0
    error=0
    while i<len(realratelist):
        if realratelist[i]==0:
            error=error+0
        else:
            error=error+((realratelist[i]-ratelist[i])/float(realratelist[i]))*((realratelist[i]-ratelist[i])/float(realratelist[i]))
        i=i+1
    return math.sqrt(error/len(realratelist))
#    pass
#    print timelist
#    plt.plot(timelist,ratelist)
    
def overhead(ratelist):
    return len(ratelist)
    pass

def sort(lA,lB):
    i=0
    while i<len(lA):
        i=i+1
        j=0
        flag=0
        while j<len(lA)-1:
            if(lA[j]>lA[j+1]):
                tmp = lA[j+1]
                lA[j+1] = lA[j]
                lA[j] = tmp
                tmp = lB[j+1]
                lB[j+1] = lB[j]
                lB[j] = tmp
                flag=1
            j=j+1
        if flag==0:
            return

def method_alltest(methods):
    lA=[] #list of overhead
    lB=[] #list of error rate
    ret=tuple()
    if methods == 'payless':
        i=5
        while i<10:
            i=i*2
            ret=method_test(methods,i)
            lA.append(ret[0])
            lB.append(ret[1])
    elif methods == 'SWT':
        i=5
        while i<10:
            i=i*2
            ret=method_test(methods,i)
            lA.append(ret[0])
            lB.append(ret[1])
    elif methods == 'adarate':
        i=5
        while i<10:
            i=i*2
            ret=method_test(methods,i)
            lA.append(ret[0])
            lB.append(ret[1])
    sort(lA,lB)
    plt.plot(lA,lB,'^-')
    print lA
    print lB
    return lA,lB
            
def method_test(methods,*args):
    #E:\我的坚果云\Documents\学生生涯\学校\实验报告\实验数据
    #file = open(unicode(r'E:\我的坚果\Documents\学生生涯\学校\实验报告\实验数据\2049B.datx','utf-8'),'r+')
    file = open(unicode(r'/home/jason/Downloads/2049B.datx','utf-8'),'r+')
    #file = open(r'/media/jason/Seagate Backup Plus Drive/实验数据/2017年12月11日UTC.datx','r+')
    ts=[]
    duration=1
    statslist=[]
    timelist=[]
    ratelist=[]
    method=methods
    line=file.readline()
    loop=0
    count=0
    ts=0
    while line != "":
    #    cnt=cnt+1
    #    print cnt
        loop=duration
        while loop>0:
            loop=loop-1
            line=file.readline()
            data=re.findall('\d+',line)
            if(data==[]):
                break
#            count=count+int(data[1])#normal mode
            count=float(data[1])#sw-arima mode
        ts=ts+duration
        #ratelist.append(count/duration)#normal mode
        ratelist.append(count)#normal mode
        statslist.append(count)
        timelist.append(ts)
        count=0
        if len(args)!=1:
            duration=measure(duration,timelist,statslist,method)
        else:
            duration=measure(duration,timelist,statslist,method,args[0])
        assert duration>0,'duration is illedga'

    #plt.plot(timelist,ratelist,label=methods)
    plt.plot(statslist,'*-',label=methods)
    tp=[]
    for i in stateslist:
        tp.append(i)
#    interpolation('default',timelist,ratelist)

    #E:\我的坚果云\Documents\学生生涯\学校\实验报告\实验数据
    #file = open(unicode(r'E:\我的坚果\Documents\学生生涯\学校\实验报告\实验数据\2049B.datx','utf-8'),'r+')
    file = open(unicode(r'/home/jason/Downloads/2049B.datx','utf-8'),'r+')
    #file = open(r'/media/jason/Seagate Backup Plus Drive/实验数据/2017年12月11日UTC.datx','r+')
    ts=[]
    duration=1
    statslist=[]
    realratelist=[]
    method='default'
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
        realratelist.append(count/duration)
        statslist.append(count)
        count=0
    errorate(timelist, ratelist, realratelist)
    plt.plot(realratelist,'.-',label="real")
    plt.legend()

#    print 'overhead:'+str(overhead(ratelist))
#    print 'error:'+str(errorate(timelist,ratelist,realratelist))
    return overhead(ratelist),errorate(timelist,ratelist,realratelist)

#method_test('payless')
#method_test('SWT')
#method_test('payless')

#method_test('adarate')
method_test('sw_arima')
#method_alltest('SWT')
plt.show()
