import os
import sys
import re
import time
import threading
from functools import partial
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController
import xml.etree.ElementTree as ET
from graphviz import Digraph


class vlcthread(threading.Thread):
    def __init__(self,hosts=None,dst_port=None,source_add=None):
        threading.Thread.__init__(self)
        self.hosts = hosts
        self.dst_port = dst_port
        self.source_add = source_add

    def run(self):
        self.hosts[1].cmd('vlc-wrapper udp://@:' + self.dst_port + "&")
        self.hosts[0].cmd('vlc-wrapper ' \
                     + "-vvv " + " " \
                     + self.source_add + " " \
                     + "--sout " + "udp://" + str(self.hosts[1].IP()) + ":" + self.dst_port + " " \
                     #  +"&")
                     )


class SimpleTopo(Topo):

    def __init__(
            self,
            **opts
            ):

        super(SimpleTopo,self).__init__(**opts)

        h1 = self.addHost('h1');
        h2 = self.addHost('h2');
        sw = self.addSwitch('s1');
        link = self.addLink(h1, sw);
        link = self.addLink(h2, sw);

class ComplexTopo(SimpleTopo):
    allhosts = {}

    def __init__(
            self,
            filename='',
            **opts
            ):
        if filename == '':
            super(ComplexTopo,self).__init__()
        else:
            # self.drawtopo(filename)
            self.parseconf(filename)

    def parseconf(self,filename):
        tree = ET.parse(filename)
        root = tree.getroot()

        super(SimpleTopo, self).__init__()

        for host in root.findall('host'):
            hostname = host.find('name').text
            host = self.addHost(hostname)
            self.allhosts[hostname] = host

        for switch in root.findall('switch'):
            self.addSwitch(switch.find('name').text)

        for link in root.findall('link'):
            peers = link.findall('peer')
            self.addLink(peers[0].text,peers[1].text)

        controller = root.find('controller')
        if controller == None:
            net = Mininet(self)
        else:
            port = int(controller.find('listen_port').text)
            net = Mininet(self, \
                          controller=partial(RemoteController, \
                                             ip='127.0.0.1', \
                                             port=6653))
        net.start()
        dumpNodeConnections(net.hosts)
        time.sleep(10)

        traffics = {'0':[]}
        for traffic in root.findall('traffic'):
            start_time = traffic.find('start_time').text
            if not traffics.has_key(start_time):
                traffics[start_time] = []
            traffics[start_time].append(traffic)
            print start_time

        tick = 0;
        threadlist = []
        while 1:
            if traffics.has_key(str(tick)):
                l = traffics[str(tick)]
                for traffic in l:
                    if traffic.find('type').text == 'cbr':
                        hosts = []
                        hosts.append(net.get(traffic.find('src').text))
                        hosts.append(net.get(traffic.find('dst').text))
                        baudwidth = traffic.find('baudwidth').text
                        period = traffic.find('period').text
                        print 'ok'
    #                    net.iperf(hosts, protocol, baudwidth, None, period, port)
                        hosts[1].cmd('iperf -u -s&')
                        hosts[0].cmd("iperf -u -c " + str(hosts[1].IP()) + " " \
                                     + "-b "+ baudwidth + " "\
                                     + "-t "+ period + " "\
                                     + "&")
                    elif traffic.find('type').text == 'vbr':
                        hosts = []
                        hosts.append(net.get(traffic.find('src').text))
                        hosts.append(net.get(traffic.find('dst').text))
                        source_add = traffic.find('source_add').text
                        dst_port = traffic.find('dst_port').text
                        source_type = traffic.find('source_type').text
                        if source_type == 'file':
                            # hosts[1].cmd('vlc-wrapper udp://@:' + dst_port + "&")
                            # hosts[0].cmd('vlc-wrapper '\
                            #              + "-vvv " + " "\
                            #              + source_add + " "\
                            #              + "--sout " + "udp://" + str(hosts[1].IP()) + ":" + dst_port + " "\
                            #            #  +"&")
                            #              )
                            threadlist.append(vlcthread(hosts,dst_port,source_add))
                            threadlist[len(threadlist)-1].start()
                            print 'ok'

                    elif traffic.find('type').text == 'web':
                        pass
            time.sleep(1)
            tick = tick + 1


    def drawtopo(self,filename):
        tree = ET.parse(filename)
        root = tree.getroot()

        dot = Digraph(comment='topo overview')

        for host in root.findall('host'):
            hostname = host.find('name').text
            dot.node(hostname,hostname)


        for switch in root.findall('switch'):
            swname = switch.find('name').text
            dot.node(swname,swname,shape='box')

        for link in root.findall('link'):
            peers = link.findall('peer')
            dot.edge(peers[0].text,peers[1].text,None,dir='none')

        dot.render('topo.gv',view=True)


if __name__ == '__main__':

    tmp = ComplexTopo(sys.argv[1])
    tmp.drawtopo(sys.argv[1])
