# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 17:30:09 2017

@author: jason
"""
import arima
import math
import pandas as pd

ws_max=3
#ws=1#nodrmal
ws=0#sw-arima
ws_init=50


step=1
model_arima = None
predict = []
predict_num = 0

def sw_arima(ts,tp,source_tp):
    global model_arima
    global ws
    global ws_init
    global step
    global predict
    global predict_num
    print(predict_num)
    ret = 1
    tp.index = pd.to_datetime(tp.index,unit='ms')
    if model_arima != None:
        #assert(predict != [])
        if (abs(tp[len(tp)-1]-predict[len(predict)-1]))/tp[len(tp)-1] > 0.2:
            model_arima = None
            ws = 0
            step = 1
            predict=[]
            return step
        else:
            window=[]
            window=tp[len(tp)-ws:len(tp)]
            print("ws:"+str(ws))
            print("data length:"+str(len(window)))
            param = arima.getparam(window)
            ws = ws + step
            if param != [] :
                model_arima = arima.getmodel(window)
                if step < 3:
                    step = step + 1
                forecast = model_arima.forecast(step)[0]
                if len(forecast) > 1:
                    for i in forecast[0:len(forecast)-1]:
                        source_tp.append(i)
                        predict_num = predict_num + 1
                    predict=[]
                    predict.append(forecast[len(forecast)-1])
                else:
                    predict=forecast
                return step
            else:
                step = 1
                ws = 0
                predict=[]
                model_arima = None
                return step
        pass
    else:
        if ws > 40:
            print('go init')
            window=[]
            window=tp[len(tp)-ws:len(tp)]
            print len(tp)
            print("ws:"+str(ws))
            print("data length:"+str(len(window)))
            param = arima.getparam(window)
            if param != []:
                model_arima = arima.getmodel(window)
                forecast = model_arima.forecast(step)[0]
                predict=forecast
                ws = ws + step
                return step
            else:
                model_arima = None
                ws = 0
                step = 1
                predict = []
                return step
        else:
            print(ws)
            ws = ws + 1
            ret = 1
            step = 1
            predict = []
            return step
    print("final data length:"+str(len(tp)))
    return ret

def payless(duration,timelist,statslist):
    if len(statslist) < 1:
        return duration
    if statslist[len(statslist)-1] > 4900000:
        return max(duration/3,1)
    elif statslist[len(statslist)-1] < 950000:
        return min(duration*2,100)
    else:
        return duration

def swt(duration,timelist,statslist,duration_max):
#   duration_max=100
    duration_min=1
    ret = 0
    win=[]
    global ws
    if len(statslist)<1:
#        print 'swt init'
        ws=3
    if(len(statslist)>1):
        var=statslist[len(statslist)-1]
        i=len(statslist)-2
        while len(win)<ws and i>=0:
            win.append(statslist[i])
            i=i-1

        mean = 0
        for dat in win:
            mean = mean + dat
        mean=mean/len(win)
        stdev = 0
 
        for dat in win:
            stdev = stdev + (dat-mean)*(dat-mean)
        stdev = math.sqrt(stdev/(len(win)))

    else:
        mean = 0
        stdev = 0
        var=0
    
    if var > mean + 2*stdev:
        ret = max(duration/2,duration_min)
        ws=min(3,ws/2)
    else:
        ret = min(duration*2,duration_max)
        ws=ws+1
    if len(win)>ws:
        win.remove(win[0])
#    print 'stdev:'+str(stdev)+' mean:'+str(mean)+' var:'+str(var)+' ws:'+str(ws)
    return ret

def adarate(duration,timelist,statslist,duration_max):
#    duration_max=100
    duration_min=1
    ret = duration
    win=[]
    global ws_max
    global ws
    if len(statslist)<1:
#        print 'adarate init'
        ws_max=3
        ws=1
    if(len(statslist)>1):
        i=len(statslist)-1
        while len(win)<ws and i>=0:
            if i > 0:
                win.append(statslist[i]/(timelist[i]-timelist[i-1]))
            else:
                win.append(statslist[i]/(timelist[i]))
            i=i-1

        mean = 0
        for dat in win:
            mean = mean + dat
        mean=mean/len(win)
        stdev = 0
 
        for dat in win:
            stdev = stdev + (dat-mean)*(dat-mean)
        stdev = math.sqrt(stdev/(len(win)))

    else:
        mean = 0
        stdev = 0
   
    if stdev > 0.2*mean:
        ret = max(duration/2,duration_min)
        ws_max=min(3,ws_max/2)
#        ws=1
    else:
        ret = min(duration*2,duration_max)
        ws_max=ws_max+1
        ws=ws+1
    if len(win)>ws_max and ws>1:
        ws=ws-1
#    print 'stdev:'+str(stdev)+' mean:'+str(mean)+ ' ws:'+str(ws) + ' ws_max:'+str(ws_max)
    return ret
