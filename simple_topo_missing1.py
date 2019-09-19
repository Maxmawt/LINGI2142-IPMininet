from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, bgp_peering, AF_INET6


class SimpleBGPTopoMissing1(IPTopo):

    def build(self, *args, **kwargs):
        """
        Topo from slide 33 iBGP
        """
        # Add all routers
        as1r1 = self.bgp('as1r1')

        as1r4 = self.bgp('as1r4')
        as1r5 = self.bgp('as1r5')
        as1r6 = self.bgp('as1r6')
        as4r1 = self.bgp('as4r1')
        as4r2 = self.bgp('as4r2')
        as5r1 = self.bgp('as5r1')
        as3r1 = self.bgp('as3r1')
        as2r1 = self.addRouter('as2r1')
        as2r1.addDaemon(BGP, address_families=(AF_INET6(networks=('dead:beef::/48',)),))
        h1 = self.addHost('h1')

        # Add Links
        self.addLink(as1r1, as1r6)
        self.addLink(as1r1, as1r4, igp_cost=7)
        self.addLink(as1r4, as1r5)
        self.addLink(as1r5, as1r6)
        self.addLink(as4r1, as1r5)
        self.addLink(as4r2, as1r4)
        self.addLink(as3r1, as1r1)
        self.addLink(as5r1, as1r6)
        self.addLink(as3r1, as5r1)
        self.addLink(as5r1, as2r1)
        self.addLink(as2r1, as4r1)
        self.addLink(as4r1, as4r2)
        self.addLink(as2r1, h1, params1={"ip": "dead:beef::/48"}, params2={"ip": "dead:beef::1/48"})

        # Add full mesh
        self.addAS(2, (as2r1,))
        self.addAS(3, (as3r1,))
        self.addAS(5, (as5r1,))
        self.addiBGPFullMesh(4, routers=[as4r1, as4r2])
        self.addAS(1, (as1r1, as1r4, as1r5, as1r6))
        bgp_peering(self, as1r1, as1r5)
        bgp_peering(self, as1r1, as1r4)
        bgp_peering(self, as1r4, as1r5)

        # Add eBGP session
        ebgp_session(self, as1r1, as3r1)
        ebgp_session(self, as1r4, as4r2)
        ebgp_session(self, as1r5, as4r1)
        ebgp_session(self, as3r1, as5r1)
        ebgp_session(self, as5r1, as2r1)
        ebgp_session(self, as2r1, as4r1)

        super(SimpleBGPTopoMissing1, self).build(*args, **kwargs)

