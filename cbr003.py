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
from xml.dom.minidom import parse
import xml.dom.minidom

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


    def parseconf(self,filename):
        DOMTree = parse(filename)
        collection = DOMTree.documentElement
        switches = collection.getElementsByTagName("switch")
        hosts = collection.getElementsByTagName("host")
        controller = collection.getElementsByTagName("controller")
        links = collection.getElementsByTagName("link")

        print switches[0].getAttribute("title")
        print hosts
        print controller



if __name__ == '__main__':

    tmp = ComplexTopo()
    tmp.parseconf('/home/jason/workspace/scenario/xml-demo.xml')