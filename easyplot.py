import re
import sys
import matplotlib.pylab as pl
import csv
sys.path.append("~/workspace/scenario")
from entropy import *
import xml.etree.ElementTree as ET
import math

class ExpData():

    def __init__(self,match):
        self.timestamp = []
        self.speed = []
        self.flowmatch = match




class Exp():

    def __init__(self):
        self.Name = "Expdata"
        self.dataMap = {}
        self.lineMap = {'SWT':'-x','elastic':'-','myself':'-','polling':':','payless':'-','adarateR':'-','adarate':'-','ARIMA':'-o'}
        self.colorMap = {'SWT':'b','elastic':'g','myself':'r','polling':'k','payless':'k','adarateR':'r','adarate':'b','ARIMA':'r'}
        # self.colorMap = {'SWT':'b','elastic':'b','myself':'b','polling':'b','payless':'b','adarateR':'b','adarate':'b'}

    def parselog(self, filename = ''):
        if filename == '':
            pass
        else:
            file = open(filename, 'r')
            head = ""
            flag = 0
            linenum = 0
            for line in file.readlines():
                linenum = linenum + 1
                if flag == 1:
                    if len(re.findall('OFOxmList', line)) != 0:
                        if not self.dataMap.has_key(line):
                            self.dataMap[line] = ExpData(line)
                        head = line
                        continue
                    if len(re.findall('TimeStamp:', line)) != 0 and len(re.findall('Speed:', line)) != 0:
                        tmp = re.findall('\d\.\d+E\d', line)[0]
                        num = float(re.findall('\d\.\d+', tmp)[0])
                        tmp = re.findall('E\d', tmp)[0]
                        num = num * float(10 ^ (int(re.findall('\d+', tmp)[0])))
                        print num
                        self.dataMap[head].timestamp.append(num)
                        tmp = re.findall('\d+\.\d+Mbps', line)
                        if len(tmp) > 0:
                            tmp = tmp[0]
                            num = float(re.findall('\d+\.\d+', tmp)[0])
                            print num
                            self.dataMap[head].speed.append(num)
                        else:
                            self.dataMap[head].speed.append(0)
                        continue
                    else:
#                        self.dataMap[copy.deepcopy(data.flowmatch)] = copy.deepcopy(data)
                        print  self.dataMap[head]
                        print  self.dataMap[head].flowmatch
                        print  self.dataMap[head].speed
                        print  self.dataMap[head].timestamp
                        flag = 0
                if len(re.findall('Speed Table', line)) != 0:
                    print 'find Speed Table'
                    flag = 1

    def basicplot(self,TimeStamp,Speed):
        print TimeStamp
        print Speed
        if len(TimeStamp) <=0:
            return
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
        pl.plot(x,y)

    def csvplot(self,filename):
        f = open(filename,'r')
        line = f.readline()
        print line
        if len(re.findall("TimeStamp Speed",line)) == 0:
            print "file is error"
        lines = f.readlines()

        primitive = float(lines[0].split(" ",1)[0])

        ts=[]
        bps=[]
        for line in lines:
            x,y = line.split(" ",1)
            ts.append((float(x)-primitive)*(1000000000))
            ts.append((float(x)-primitive)*(1000000000))
            bps.append(float(y))
            bps.append(float(y))
        del ts[len(ts)-1]
        del bps[0]

        labelname = re.findall("\w+-",filename)[0]
        labelname = re.findall("\w+",labelname)[0]
        if labelname == 'payless':
            min = re.findall("\d+M-\d+M",filename)[0]
            max = re.findall("\d+M-\d+M", filename)[0]
            min = re.findall("\d+",min)[0]
            max = re.findall("\d+", max)[1]
            labelname = labelname+","+"min="+min+"Mbps"+","+"max="+max+"Mbps"
        agtype = re.findall("\w+", labelname)[0]
        pl.plot(ts,bps,self.lineMap[agtype]+self.colorMap[agtype],label=labelname)
#        print ts
#        pl.hold()
#        pl.show()

    def multiplot(self):
        num = int(sys.argv[1])
        print range(1,num+1)
        for i in range(1,num+1):
            self.csvplot(sys.argv[i+1])

        #plot configuration
        pl.xlabel("time(seconds)")
        pl.ylabel("traffic rate(Mbps)")
        pl.axis([0,60,0,40])
        pl.legend(loc="left upper",fancybox='false',fontsize=10)
        pl.show()

    def ent(self,filename):
        f = open(filename,'r')
        line = f.readline()
        print line
        if len(re.findall("TimeStamp Speed",line)) == 0:
            print "file is error"
        lines = f.readlines()

        primitive = float(lines[0].split(" ",1)[0])

        ts=[]
        bps=[]
        for line in lines:
            x,y = line.split(" ",1)
            ts.append((float(x)-primitive)*(1000000000))
            bps.append(float(y))
        
        ent_x = []
        ts.append(65535)
        bps.append(0)
        r = [0.1*i for i in range(600)]
        for i in r: 
            ent_x.append(bps[0])
            if(ts[0] < i):
                del ts[0]
                del bps[0]
        ent = entropy()
        return ent.calc_ent(ent_x)

    def entgrap(self,sourcefile,filename):
        f = open(filename,'r')
        line = f.readline()
        print line
        if len(re.findall("TimeStamp Speed",line)) == 0:
            print "file is error"
        lines = f.readlines()

        primitive = float(lines[0].split(" ",1)[0])

        ts=[]
        bps=[]
        for line in lines:
            x,y = line.split(" ",1)
            ts.append((float(x)-primitive)*(1000000000))
            bps.append(float(y))
        
        ent_x = []
        ts.append(65535)
        bps.append(0)
        r = [0.1*i for i in range(600)]
        for i in r: 
            ent_x.append(bps[0])
            if(ts[0] < i):
                del ts[0]
                del bps[0]

        f = open(sourcefile,'r')
        line = f.readline()
        print line
        if len(re.findall("TimeStamp Speed",line)) == 0:
            print "file is error"
        lines = f.readlines()

        primitive = float(lines[0].split(" ",1)[0])

        ts=[]
        bps=[]
        for line in lines:
            x,y = line.split(" ",1)
            ts.append((float(x)-primitive)*(1000000000))
            bps.append(float(y))
        
        ent_y = []
        ts.append(65535)
        bps.append(0)
        r = [0.1*i for i in range(600)]
        for i in r: 
            ent_y.append(bps[0])
            if(ts[0] < i):
                del ts[0]
                del bps[0]
        ent = entropy()
        return ent.calc_ent_grap(ent_x,ent_y)

    def error(self,sourcefile,filename):
        f = open(filename,'r')
        line = f.readline()
        print line
        if len(re.findall("TimeStamp Speed",line)) == 0:
            print "file is error"
        lines = f.readlines()

        primitive = float(lines[0].split(" ",1)[0])

        ts=[]
        bps=[]
        for line in lines:
            x,y = line.split(" ",1)
            ts.append((float(x)-primitive)*(1000000000))
            bps.append(float(y))
        
        ent_x = []
        ts.append(65535)
        bps.append(0)
        r = [0.1*i for i in range(600)]
        for i in r: 
            ent_x.append(bps[0])
            if(ts[0] < i):
                del ts[0]
                del bps[0]

        f = open(sourcefile,'r')
        line = f.readline()
        print line
        if len(re.findall("TimeStamp Speed",line)) == 0:
            print "file is error"
        lines = f.readlines()

        primitive = float(lines[0].split(" ",1)[0])

        ts=[]
        bps=[]
        for line in lines:
            x,y = line.split(" ",1)
            ts.append((float(x)-primitive)*(1000000000))
            bps.append(float(y))
        
        ent_y = []
        ts.append(65535)
        bps.append(0)
        r = [0.1*i for i in range(600)]
        for i in r: 
            ent_y.append(bps[0])
            if(ts[0] < i):
                del ts[0]
                del bps[0]

        R = 0
        N = len(ent_y)
        S = 0
        for i in range(N):
            if ent_x[i] == 0 and ent_y[i] == 0:
                continue
            if ent_x[i] == 0 or ent_y[i] == 0:
                S = S +1
                continue
            S = S + math.fabs((ent_x[i]-ent_y[i])/ent_y[i])
        R = math.sqrt(S)/N
        return R

    def entplot(self,filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        

        width = 3
        gap = 3
        start = 0
        color = {'payless':'b','myself':'r','elastic':'g','SWT':'y','polling':'k'}
        entropy = root.find('entropy')
        flag = True
        for group in entropy.findall('group'):
            for sample in group.findall('sample'):
                filepath = sample.find('filepath').text
                ag = sample.find('algorithm').text
                start = start + width
                if flag:
                    pl.bar(start,self.ent(filepath),width,color=color[ag],label=ag)
                else:
                    pl.bar(start,self.ent(filepath),width,color=color[ag])
            flag = False
            start = start + gap


        pl.xlabel("experiments")
        pl.ylabel("bit")
        pl.axis([0,33,0,10])
        pl.title('entropy')
        pl.legend(loc="left upper",fancybox='false',fontsize=10)
        pl.grid(True)
        pl.show()
        pass

    def entgraplot(self,filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        

        width = 3
        gap = 3
        start = 0
        color = {'payless':'b','myself':'r','elastic':'g','SWT':'y','polling':'k'}
        entropy = root.find('mutual')
        flag = True
        for group in entropy.findall('group'):
            for sample in group.findall('sample'):
                filepath = sample.find('filepath').text
                ag = sample.find('algorithm').text
                start = start + width + 3
                if flag:
                    pl.bar(start,self.entgrap(filepath,group.find('compare_sample').find('filepath').text),width,color=color[ag],label=ag)
                else:
                    pl.bar(start,self.entgrap(filepath,group.find('compare_sample').find('filepath').text),width,color=color[ag])
            flag = False
            start = start + gap


        pl.xlabel("experiments")
        pl.ylabel("bit")
        pl.axis([0,30,0,10])
        pl.title('mutual information')
        pl.legend(loc="left upper",fancybox='false',fontsize=10)
        pl.grid(True)
        pl.show()
        pass

    def balancedentplot(self,filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        

        width = 1
        gap = 3
        start = 0
        color = {'payless':'b','myself':'r','elastic':'g','SWT':'y','polling':'k'}
        entropy = root.find('mutual')
        flag = True
        for group in entropy.findall('group'):
            for sample in group.findall('sample'):
                filepath = sample.find('filepath').text
                ag = sample.find('algorithm').text
                start = start + width
                if flag:
                    pl.bar(start,(1-self.error(filepath,group.find('compare_sample').find('filepath').text))*(self.ent(filepath)),width,color=color[ag],label=ag)
                else:
                    pl.bar(start,(1-self.error(filepath,group.find('compare_sample').find('filepath').text))*(self.ent(filepath)),width,color=color[ag])
            flag = False
            start = start + gap


        pl.xlabel("experiments")
        pl.ylabel("bit")
        pl.axis([0,30,0,10])
        pl.title('Balanced Information  Entropy')
        pl.legend(loc="left upper",fancybox='false',fontsize=10)
        pl.grid(True)
        pl.show()
        pass

    def errorplot(self,filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        

        width = 3
        gap = 3
        start = 0
        entropy = root.find('mutual')
        flag = True
        for group in entropy.findall('group'):
            for sample in group.findall('sample'):
                filepath = sample.find('filepath').text
                ag = sample.find('algorithm').text
                start = start + width + 3
                if flag:
                    pl.bar(start,self.error(filepath,group.find('compare_sample').find('filepath').text),width,color=self.colorMap[ag],label=ag)
                    print self.error(filepath,group.find('compare_sample').find('filepath').text)
                else:
                    pl.bar(start,self.error(filepath,group.find('compare_sample').find('filepath').text),width,color=self.colorMap[ag])
                    print self.error(filepath,group.find('compare_sample').find('filepath').text)
            flag = False
            start = start + gap


        pl.xlabel("experiments")
        pl.ylabel("error")
        pl.axis([0,30,0,0.05])
        pl.title('Error')
        # pl.legend(loc="left upper",fancybox='false',fontsize=10)
        pl.grid(True)
        pl.show()
        pass

    def overheadplot(self,filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        

        width = 2.5
        gap = 3
        start = 0
        entropy = root.find('entropy')
        flag = True
        ymax = 0
        for group in entropy.findall('group'):
            for sample in group.findall('sample'):
                filepath = sample.find('filepath').text
                ag = sample.find('algorithm').text
                start = start + width + 2
                f = open(filepath,'r')
                lines = f.readlines()
                if len(lines) >= ymax:
                    ymax = len(lines)
                if flag:
                    pl.bar(start,len(lines),width,color=self.colorMap[ag],label=ag)
                    print len(lines) 
                else:
                    pl.bar(start,len(lines),width,color=self.colorMap[ag])
                    print len(lines)
                f.close()


        # ents = []
        # ents.append(self.ent(sys.argv[1]))
        # ents.append(self.ent(sys.argv[2]))
        # ents.append(self.ent(sys.argv[3]))
        #plot configuration
        pl.xlabel("experiments")
        pl.ylabel("polling times")
        pl.axis([0,35,0,ymax+10])
        pl.title('overhead')
        # pl.legend(loc="left upper",fancybox='false',fontsize=10)
        pl.grid(True)
        pl.show()
        pass

    def xmlplot(self):
        pass

    def basicshow(self):
        for i in self.dataMap:
            assert (isinstance(self.dataMap[i], ExpData))
            self.basicplot(self.dataMap[i].timestamp,self.dataMap[i].speed)
        pl.show()

    def dataGetByProtocol(self,protocol='UDP'):
        dellist = []
        for i in self.dataMap.iterkeys():
            if len(re.findall('ETH_TYPE=OFOxmEthTypeVer13\(value=0x800\)',i)) == 0:
                dellist.append(i)
        for i in dellist:
            del self.dataMap[i]

    def dataGetByInport(self,Inport=1):
        dellist = []
        for i in self.dataMap.iterkeys():
            assert (isinstance(i,str))
            if len(re.findall('IN_PORT=OFOxmInPortVer13\(value='+str(Inport)+'\)',i)) == 0:
                dellist.append(i)
        for i in dellist:
            assert (isinstance(self.dataMap[i],ExpData))
            del self.dataMap[i]

    def dataGetBySrc(self):
        pass

    def dataGetByDst(self):
        pass


if __name__ == '__main__':
    exp = Exp()
#    exp.parselog(sys.argv[1])
#    exp.basicshow()
#    exp.csvplot(sys.argv[1])
    exp.multiplot()
    # exp.entgraplot(sys.argv[1])
    # exp.entplot(sys.argv[1])
    # exp.overheadplot(sys.argv[1])
    # exp.errorplot(sys.argv[1])
    # exp.balancedentplot(sys.argv[1])

