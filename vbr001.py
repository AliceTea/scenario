import sys
import re
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import Host

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


if __name__ == '__main__':

    f = open('vbrconf001','r')
    lines = f.readlines()
    line = lines[0]
    hs = re.findall('h\d+->h\d+',line)
    m = re.findall('h\d+',hs[0])
    

    
    setLogLevel('info')
    topo = SimpleTopo()
    net = Mininet(topo)
    net.start()
    dumpNodeConnections(net.hosts)
    
    for host in net.hosts:
        if host.name == m[0]:
            client = host
            print "client = " + m[0] 
        if host.name ==  m[1]:
            server = host
            print "server = " + m[1] 
    client.cmd('vlc-wrapper udp://@:9999&')
    clientIP = client.IP()
    strs = re.findall('\S+',line)
    video = strs[1] 
    server.cmd('vlc-wrapper -vvv '+ video +' --sout udp:' + str(clientIP) + ':9999 --ttl 10')
    net.stop()
