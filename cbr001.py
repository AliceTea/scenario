from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

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

    setLogLevel('info')
    topo = SimpleTopo()
    net = Mininet(topo)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll();
    net.stop();
