from __future__ import print_function
import pandas as pd
import numpy as np
from scipy import  stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.arima_model import ARIMA
import math

def getparam(tp=[]):
    #ARIMA(p,d,q)
    p=0
    d=0
    q=0
    #d recognize
    adf = ts.adfuller(np.array(tp.diff(d).dropna().get_values()),regression=None)
    if adf[0] < adf[4]['1%'] and adf[1] < 0.01:
        pass
    else:
        d = d + 1
        adf = ts.adfuller(np.array(tp.diff(d).dropna().get_values()),regression=None)
        if adf[0] < adf[4]['1%'] and adf[1] < 0.01:
            pass
        else:
            d = -1
            return []
    
    p=0
    q=0
    T = len(np.array(tp.diff(d)))
    Tsqrt = int(math.sqrt(T))
    acf = ts.acf(np.array(tp.diff(d).dropna()),nlags=40)
    pacf = ts.pacf(np.array(tp.diff(d).dropna()),nlags=40)
    for i in range(1,len(acf)-1):
        sum = 0
        for j in range(i+1,len(acf)):
            if abs(acf[j]) > 2*np.std(acf):
                pass
            else:
                sum = sum + 1
        if sum/(len(acf)-i-1) > 0.985:
            q = i
            break
    for i in range(1,len(pacf)-1):
        sum = 0
        for j in range(i+1,len(pacf)):
            if abs(pacf[j]) > 2*np.std(acf):
                pass
            else:
                sum = sum + 1
#        print(sum)
#        print(2*np.std(acf))
        if sum/(len(pacf)-i-1) > 0.985:
            p = i
            break
    params = []
    for i in range(p+1):
        for j in range(q+1):
            params.append([i,d,j])
            if j>=6:
                break
        if i>=6:
            break

    return params

def getmodel(tp=[]):
    params = getparam(tp)
    aicmin = np.Inf
    bestmodel = None
    for param in params:
        model = ARIMA(tp, param)
        try:
            result_arima = model.fit( disp=-1, method='css')
        except ValueError:
            continue
        print(param)
        if aicmin > result_arima.aic:
            aicmin = result_arima.aic
            bestmodel = result_arima
    return bestmodel

def plotpredict(tp=[]):
    predict = []
    for i in range(50,len(tp)-1):
        model = getmodel(tp[0:i])
        if model != None :
#            predict.append(abs((model.forecast(1)[0][0]-tp[i+1])/tp[i+1]))
            predict.append(model.forecast(1)[0][0])
        else:
            predict.append(-0.1)
#    plt.plot(predict)
    return predict

def getARIMA(tp=[]):
    tp = pd.Series(tp)
    diff1 = tp.diff(1)
    diff1 = diff1.dropna(inplace=True)
    diff2 = tp.diff(2)
    diff2 = diff1.dropna(inplace=True)
    
    d=0
    while d<=2:
        tmp = tp.diff(d)
        tmp = tmp.dropna()
        result = ts.adfuller(np.array(tmp.get_values()),regression='c')
        adf = result[0]
        pvalue = result[1]
        confidence = result[4]
        if adf < confidence['1%'] and pvalue < 0.01:
             break
        d = d + 1
        if d > 2:
            return
        
    p=0
    q=0
    T = len(np.array(tp.diff(d)))
    Tsqrt = int(math.sqrt(T))
    acf = ts.acf(np.array(tp.diff(d)),nlags=Tsqrt)
    pacf = ts.pacf(np.array(tp.diff(d)),nlags=Tsqrt)
    for i in range(1,len(acf)+1):
        if acf(i) < 1/Tsqrt:
            q = 'error'
            break
        sum = 0
        for j in range(i+1,len(acf)+1):
            if math.abs(acf[j]) > 1/Tsqrt:
                pass
            else:
                sum = sum + 1
        if sum/(len(acf)-i-1) > 0.683:
            q = i
            break
    for i in range(1,len(pacf)+1):
        if pacf(i) < 1/Tsqrt:
            p = 'error'
            break
        sum = 0
        for j in range(i+1,len(pacf)+1):
            if math.abs(pacf[j]) > 1/Tsqrt:
                pass
            else:
                sum = sum + 1
        if sum/(len(pacf)-i-1) > 0.683:
            p = i
            break
    
    model = ARIMA(tp, order=(p,d,q)) 
    result_arima = model.fit( disp=-1, method='css')
    params = result_arima.params
    return params
