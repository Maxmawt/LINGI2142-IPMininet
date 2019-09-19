from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, AF_INET6


class SimpleBGPTopo(IPTopo):

    def build(self, *args, **kwargs):
        """
        Topo from slide 22 iBGP
        """
        # Add all routers
        as1r1 = self.bgp('as1r1')
        as1r2 = self.bgp('as1r2')
        as1r3 = self.bgp('as1r3')
        as1r4 = self.bgp('as1r4')
        as1r5 = self.bgp('as1r5')
        as1r6 = self.bgp('as1r6')
        as4r1 = self.addRouter('as4r1')
        as4r1.addDaemon(BGP, address_families=(AF_INET6(networks=('dead:beef::/32',)),))
        as4r2 = self.addRouter('as4r2')
        as4r2.addDaemon(BGP, address_families=(AF_INET6(networks=('dead:beef::/32',)),))
        h1 = self.addHost('h1')

        # Add Links
        self.addLink(as1r1, as1r6)
        self.addLink(as1r1, as1r3)
        self.addLink(as1r3, as1r2)
        self.addLink(as1r3, as1r6)
        self.addLink(as1r2, as1r4)
        self.addLink(as1r4, as1r5)
        self.addLink(as1r5, as1r6)
        self.addLink(as4r1, as1r6)
        self.addLink(as4r2, as1r5)
        self.addLink(as4r1, h1, params1={"ip": "dead:beef::/48"}, params2={"ip": "dead:beef::1/48"})
        self.addLink(as4r2, h1, params1={"ip": "dead:beef::2/48"}, params2={"ip": "dead:beef::3/48"})

        # Add full mesh
        self.addAS(4, (as4r1, as4r2))
        self.addiBGPFullMesh(1, (as1r1, as1r2, as1r3, as1r4, as1r5, as1r6))

        # Add eBGP session
        ebgp_session(self, as1r6, as4r1)
        ebgp_session(self, as1r5, as4r2)

        super(SimpleBGPTopo, self).build(*args, **kwargs)

    def bgp(self, name):
        r = self.addRouter(name)
        r.addDaemon(BGP, address_families=(
            AF_INET6(redistribute=('connected',)),))
        return r