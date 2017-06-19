import os
import sys
import re
import time
from functools import partial
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

class SimpleTopo(Topo):

    def __init__(
            self,
            **opts
            ):

        super(SimpleTopo,self).__init__(**opts)

        h1 = self.addHost('h1');
        h2 = self.addHost('h2');
        sw = self.addSwitch('s1');
        link = self.addLink(h1,sw);
        link = self.addLink(h2,sw);

class ComplexTopo(SimpleTopo):

    def __init__(
            self,
            filename='',
            **opts
            ):
        if filename == '':
            super(ComplexTopo,self).__init__()
        else:


    def parseconf(self,filename):
        conf = open(filename,'r')
        lines = conf.readlines()
        topoflag = 0
        for line in lines:
            if topoflag == 1:
                #parse configuration
                nodes = re.findall(r'h\d+->s\d+',line)
                hosts = re.findall(r'h\d+',nodes[0])
                switches = re.findall(r's\d+',nodes[0])
                if nodes.__len__() == 1 and switches.__len__() == 1:
                    host = self.addHost(str(hosts[0]))
                    sw = self.addSwitch(str(switches[0]))
                    self.addLink(host,sw)
                    

            if line == 'topo:':
                topoflag = 1
                


if __name__ == '__main__':

    f = open(str(sys.argv[1]),'r')
    
    setLogLevel('info')
    topo = SimpleTopo()
    net = Mininet(topo,controller=partial(RemoteController,ip='127.0.0.1',port=6653))
    net.start()
    dumpNodeConnections(net.hosts)
    time.sleep(10)
    for sw in net.switches:
        os.system('sudo ovs-vsctl set bridge s1 protocols=OpenFlow13')
        
    lines = f.readlines()
    for line in lines:
        m = re.findall(r'\w+',line)
        print str(m[0])
        print int(m[1])
        net.iperf(net.hosts,'UDP',str(m[0]),None,int(m[1]),8080)
         
    time.sleep(10)
    net.stop()
