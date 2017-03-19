from mininet.topo import Topo

class FatTree(Topo):
    def __init__(self):
        super(self.__class__, self).__init__()

        coreSWs = list(self.createCoreSW())
        agrgSWs = list(self.createAgrgSW())
        edgeSWs = list(self.createEdgeSW())
        hosts = list(self.createHosts())

        self.connCA(coreSWs, agrgSWs)
        self.connAE(agrgSWs, edgeSWs)
        self.connEH(edgeSWs, hosts)

    def createCoreSW(self):
        for i in range(1001, 1001 + 4):
            yield self.addSwitch("s{}".format(i))

    def createAgrgSW(self):
        for i in range(2001, 2001 + 8):
            yield self.addSwitch("s{}".format(i))

    def createEdgeSW(self):
        for i in range(3001, 3001 + 8):
            yield self.addSwitch("s{}".format(i))

    def createHosts(self):
        for i in range(4001, 4001 + 16):
            yield self.addHost("h{}".format(i))

    def connCA(self, coreSWs, agrgSWs):
        for i, a_sw in enumerate(agrgSWs):
            if i % 2 == 0:
                self.addLink(coreSWs[0], a_sw)
                self.addLink(coreSWs[1], a_sw)
            else:
                self.addLink(coreSWs[2], a_sw)
                self.addLink(coreSWs[3], a_sw)

    def connAE(self, agrgSWs, edgeSWs):
        for i, e_sw in enumerate(edgeSWs):
            if i % 2 == 0:
                group = i
            else:
                group = i - 1

            toConnAgrg_sws = agrgSWs[group : group+2]

            for a_sw in toConnAgrg_sws:
                self.addLink(a_sw, e_sw)

    def connEH(self, edgeSWs, hosts):
        for i, host in enumerate(hosts):
            self.addLink(edgeSWs[i/2], host)

topos = { 'fatTree' : ( lambda: FatTree() ) }
