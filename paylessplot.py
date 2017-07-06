import re
import sys
import matplotlib.pyplot as pl
from math import *

tmp = 0
x = []
y = []

log = open(sys.argv[1],'r')
lines = log.readlines()

for line in lines:
    tmp = re.findall('Timestamp\s+=\s+\d+,',line)
    if tmp.__len__() != 0:
        tmp = re.findall('\d+',tmp[0])
        x.append(int(tmp[0]))
        tmp = re.findall('Utilization\s+=\s+\d+\.\d+',line)
        if tmp.__len__() != 0:
            tmp = re.findall('\d+\.\d+',tmp[0])
            y.append(float(tmp[0]))
        else:
            del x[x.__len__()-1] 

X=[]
Y=[]
for i in x:
    X.append(i)
    X.append(i)
for i in y:
    Y.append(i)
    Y.append(i)
del X[X.__len__()-1] 
del Y[0] 

pl.plot(X,Y)

pl.show()

