import re
import sys
import numpy as np
import matplotlib.pylab as pl

file = open(sys.argv[1],'r')

flag = 0
TimeStamp = []
Speed = []
fignum = 0
linenum = 0
for line in file.readlines():
    linenum = linenum +1
    sys.stdout.write('\b'*len(str(linenum))+str(linenum))
    if flag == 1:
        if len(re.findall('OFOxmList',line)) != 0:
            continue
        if len(re.findall('TimeStamp:',line)) != 0 and len(re.findall('Speed:',line)) != 0:
            tmp = re.findall('\d\.\d+E\d',line)[0]
            num = float(re.findall('\d\.\d+',tmp)[0])
            tmp = re.findall('E\d',tmp)[0]
            num = num*float(10^(int(re.findall('\d+',tmp)[0])))
            print num
            TimeStamp.append(num)
            tmp = re.findall('\d+\.\d+Mbps',line)
            if len(tmp) > 0:
                tmp = tmp[0]
                num = float(re.findall('\d+\.\d+',tmp)[0])
                print num
                Speed.append(num)
            else:
                Speed.append(0)
            continue
        
        x=[]
        y=[]
        for i in TimeStamp:
            x.append(i)
            x.append(i)
        for i in Speed:
            y.append(i)
            y.append(i)
        x=x[0:len(x)]
        y=y[1:len(y)]
        y.append(0)
        print x
        print y 
        pl.plot(x,y)
        pl.show()
        pl.savefig("./figs/"+str(fignum))
        flag = 0
        fignum = fignum + 1
        TimeStamp = []
        Speed = []

    if len(re.findall('Speed Table',line)) != 0:
        print 'find Speed Table'
        flag = 1
