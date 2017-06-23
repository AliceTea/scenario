import re
import sys
import matplotlib.pylab as pl
import copy

class ExpData():

    def __init__(self,match):
        self.timestamp = []
        self.speed = []
        self.flowmatch = match


class Exp():

    def __init__(self):
        self.Name = "Expdata"
        self.dataMap = {}


    def parselog(self, filename = ''):
        if filename == '':
            pass
        else:
            file = open(filename, 'r')

            flag = 0
            linenum = 0
            for line in file.readlines():
                linenum = linenum + 1
                if flag == 1:
                    if len(re.findall('OFOxmList', line)) != 0:
                        data = ExpData(line)
                        continue
                    if len(re.findall('TimeStamp:', line)) != 0 and len(re.findall('Speed:', line)) != 0:
                        tmp = re.findall('\d\.\d+E\d', line)[0]
                        num = float(re.findall('\d\.\d+', tmp)[0])
                        tmp = re.findall('E\d', tmp)[0]
                        num = num * float(10 ^ (int(re.findall('\d+', tmp)[0])))
                        print num
                        data.timestamp.append(num)
                        tmp = re.findall('\d+\.\d+Mbps', line)
                        if len(tmp) > 0:
                            tmp = tmp[0]
                            num = float(re.findall('\d+\.\d+', tmp)[0])
                            print num
                            data.speed.append(num)
                        else:
                            data.speed.append(0)
                        continue

                    self.dataMap[copy.deepcopy(data.flowmatch)] = copy.deepcopy(data)
                    print data.speed
                    print data.timestamp
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

    def basicshow(self):
        for i in self.dataMap:
            assert (isinstance(self.dataMap[i], ExpData))
            self.basicplot(self.dataMap[i].timestamp,self.dataMap[i].speed)
        pl.show()

    def dataGetByProtocol(self,protocol='UDP'):
        dellist = []
        for i in self.dataMap.iterkeys():
            if len(re.findall('ETH_TYPE=OFOxmEthTypeVer13\(value=0x806\)',i)) == 0:
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
    exp.parselog(sys.argv[1])
#    exp.dataGetByProtocol()
    exp.basicshow()

