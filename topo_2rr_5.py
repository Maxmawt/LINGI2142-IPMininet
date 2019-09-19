from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, bgp_peering, set_rr, AF_INET6



class BGPTopo2RR5(IPTopo):

    def build(self, *args, **kwargs):
        """
        Topo from slide 42 iBGP BLUE config
		"""
        # Add all routers
        as1r1 = self.bgp('as1r1')
        as1r2 = self.bgp('as1r2')
        as1r3 = self.bgp('as1r3')
        as1r4 = self.bgp('as1r4')
        as1r5 = self.bgp('as1r5')
        as1r6 = self.bgp('as1r6')
        as4r1 = self.bgp('as4r1')
        as4r2 = self.bgp('as4r2')
        as5r1 = self.bgp('as5r1')
        as3r1 = self.bgp('as3r1')
        as2r1 = self.addRouter('as2r1')
        as2r1.addDaemon(BGP, address_families=(AF_INET6(networks=('dead:beef::/32',)),))
        as2h1 = self.addHost("as2h1")
        as1h1 = self.addHost("as1h1")
        as1h2 = self.addHost("as1h2")
        as1h3 = self.addHost("as1h3")
        as1h4 = self.addHost("as1h4")
        as1h5 = self.addHost("as1h5")
        as1h6 = self.addHost("as1h6")

        # Add Links
        self.addLink(as1r1, as1r6)
        self.addLink(as1r1, as1r3)
        self.addLink(as1r3, as1r2)
        self.addLink(as1r3, as1r6)
        self.addLink(as1r2, as1r4)
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
        self.addLink(as2r1, as2h1)
        self.addSubnet((as2r1, as2h1), subnets=('dead:beef::/32',))

        self.addLink(as1r1, as1h1)
        self.addLink(as1r2, as1h2)
        self.addLink(as1r3, as1h3)
        self.addLink(as1r4, as1h4)
        self.addLink(as1r5, as1h5)
        self.addLink(as1r6, as1h6)

        set_rr(self, rr=as1r2, peers=[as1r1, as1r3, as1r4, as1r5, as1r6])
        set_rr(self, rr=as1r4, peers=[as1r1, as1r2, as1r5, as1r3, as1r6])

        # Add full mesh
        self.addAS(2, (as2r1,))
        self.addAS(3, (as3r1,))
        self.addAS(5, (as5r1,))
        self.addiBGPFullMesh(4, routers=[as4r1, as4r2])
        self.addAS(1, (as1r1, as1r2, as1r3, as1r4, as1r5, as1r6))

        # Add eBGP session
        ebgp_session(self, as1r6, as5r1)
        ebgp_session(self, as1r1, as3r1)
        ebgp_session(self, as1r4, as4r2)
        ebgp_session(self, as1r5, as4r1)
        ebgp_session(self, as3r1, as5r1)
        ebgp_session(self, as5r1, as2r1)
        ebgp_session(self, as2r1, as4r1)

        super(BGPTopo2RR5, self).build(*args, **kwargs)

    def bgp(self, name):
        r = self.addRouter(name)
        r.addDaemon(BGP, address_families=(
            AF_INET6(redistribute=('connected',)),))
        return r