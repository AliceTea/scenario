import re
import sys
import matplotlib.pylab as pl
import csv

class ExpData():

    def __init__(self,match):
        self.timestamp = []
        self.speed = []
        self.flowmatch = match




class Exp():

    def __init__(self):
        self.Name = "Expdata"
        self.dataMap = {}
        self.lineMap = {'myself':'-','polling':':','payless':'--'}


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
        pl.plot(ts,bps,self.lineMap[agtype]+"k",label=labelname)
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

