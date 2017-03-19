from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

class FatTree(Topo):
    def __init__(self):
        super(self.__class__, self).__init__()

        coreSWs = list(self.createCoreSW())
        agrgSWs = list(self.createAgrgSW())
        edgeSWs = list(self.createEdgeSW())
        hosts = list(self.createHosts())

        ###
        # C : Core Switch
        # A : Aggregation Swtich
        # E : Edge Switch
        # H : Hosts
        self.connCA(coreSWs, agrgSWs)
        self.connAE(agrgSWs, edgeSWs)
        self.connEH(edgeSWs, hosts)

    ###
    # Create Switch: s1001 ~ s1004
    #
    def createCoreSW(self):
        for i in range(1001, 1001 + 4):
            yield self.addSwitch("s{}".format(i))

    ###
    # Create Switch: s2001 ~ s2008
    #
    def createAgrgSW(self):
        for i in range(2001, 2001 + 8):
            yield self.addSwitch("s{}".format(i))

    ###
    # Create Switch: s3001 ~ s3008
    #
    def createEdgeSW(self):
        for i in range(3001, 3001 + 8):
            yield self.addSwitch("s{}".format(i))
    ###
    # Create Host: h4001 ~ h4016
    #
    def createHosts(self):
        for i in range(4001, 4001 + 16):
            yield self.addHost("h{}".format(i))

    ###
    # Connecting between Core Switch and Aggregation Switch
    #
    def connCA(self, coreSWs, agrgSWs):
        for i, a_sw in enumerate(agrgSWs):
            if i % 2 == 0:
                self.addLink(coreSWs[0], a_sw, bw=100, loss=2)
                self.addLink(coreSWs[1], a_sw, bw=100, loss=2)
            else:
                self.addLink(coreSWs[2], a_sw, bw=100, loss=2)
                self.addLink(coreSWs[3], a_sw, bw=100, loss=2)

    ###
    # Connecting between Aggregation Switch  and Edge Switch
    #
    def connAE(self, agrgSWs, edgeSWs):
        for i, e_sw in enumerate(edgeSWs):
            if i % 2 == 0:
                group = i
            else:
                group = i - 1

            toConnAgrg_sws = agrgSWs[group : group+2]

            for a_sw in toConnAgrg_sws:
                self.addLink(a_sw, e_sw, bw=100)

    ###
    # Connecting between Edge Switch and Hosts
    #
    def connEH(self, edgeSWs, hosts):
        for i, host in enumerate(hosts):
            self.addLink(edgeSWs[i/2], host)

topos = { 'fatTree' : ( lambda: FatTree() ) }

# Testing
def perfTest():
    topo = FatTree()
    net = Mininet(topo=topo, link=TCLink, controller=None)

    ###
    # Lab1:
    #   The net connects to controller
    #       name = floodlight
    #       ip = 127.0.0.1
    #       port = 5563
    ctrl_ip = '127.0.0.1'
    ctrl_port = 6653
    Lab1(net, ctrl_ip, ctrl_port)

    ###
    # Starting the network
    #
    net.start()

    ###
    # Lab2:
    #   Dumping host connections
    #
    Lab2(net)

    ###
    # Lab3:
    #   Ping Full
    Lab3(net)

    ###
    # Lab4:
    #   Iperf Testing
    #       Server: h4001, h4009
    #       Client: h4003
    #   The log file of the host name by [name].log
    #
    h4001 = 'h4001'
    h4009 = 'h4009'
    h4003 = 'h4003'
    Lab4(net, h4001, h4009, h4003)

    net.stop()

def Lab1(net, ctrl_ip, ctrl_port):
    print ("\t@@@ [Lab 1/4] [Start] Connect to floodlight ip={} port={} @@@".format(ctrl_ip, ctrl_port))
    net.addController(
        'floodlight',
        controller=RemoteController,
        ip=ctrl_ip,
        port=ctrl_port
    )
    print ("\t@@@ [Lab 1/4] [Done] @@@")
    return

def Lab2(net):
    print ("\t@@@ [Lab 2/4] [Start] Dumping host connections @@@")
    dumpNodeConnections(net.hosts)
    print ("\t@@@ [Lab 2/4] [End] @@@")
    return

def Lab3(net):
    print ("\t@@@ [Lab 3/4] [Start] Ping Full @@@")
    net.pingAll()
    print ("\t@@@ [Lab 3/4] [Done] @@@")
    return

def Lab4(net, h4001, h4009, h4003):
    print ("\t@@@ [Lab 4/4] [Start] Iperf Server: {} and {}, client: {} @@@".format(h4001, h4009, h4003))
    h4001, h4009, h4003 = net.get(h4001, h4009, h4003)
    p_h4001_iperf = h4001.popen('iperf -s -u -i 1 > h4001.log', shell=True)
    p_h4009_iperf =h4009.popen('iperf -s -u -i 1 > h4009.log', shell=True)

    iperfClientCmd = 'iperf -c {} -u -t 10 -i 1 -b 100m | tee -a h4003.log'
    h4003.cmdPrint(iperfClientCmd.format(h4001.IP()))
    h4003.cmdPrint(iperfClientCmd.format(h4009.IP()))

    p_h4001_iperf.kill()
    p_h4009_iperf.kill()
    print ("\t@@@ [Lab 4/4] [Done] @@@")
    return

if __name__ == "__main__":
    setLogLevel('info')
    perfTest()
