from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, bgp_peering, set_rr, AF_INET6


class BGPTopo3RR3(IPTopo):

    def build(self, *args, **kwargs):
        """
        Topo from slide 44 iBGP BLUE config
        """
        # Add routers
        as1r1 = self.bgp('as1r1')
        as1r2 = self.bgp('as1r2')
        as1r3 = self.bgp('as1r3')
        as1r4 = self.bgp('as1r4')
        as1r5 = self.bgp('as1r5')
        as1r6 = self.bgp('as1r6')
        as1r7 = self.bgp('as1r7')
        as1r8 = self.bgp('as1r8')
        as1r9 = self.bgp('as1r9')
        as1ra = self.bgp('as1ra')
        as1rb = self.bgp('as1rb')
        as5r1 = self.bgp('as5r1')
        as3r1 = self.bgp('as3r1')
        as2r1 = self.addRouter('as2r1')
        as2r1.addDaemon(BGP, address_families=(AF_INET6(networks=('dead:beef::/48',)),))

        # Add Links
        self.addLink(as1r1, as1r6)
        self.addLink(as1r1, as1r3)
        self.addLink(as1r3, as1r2)
        self.addLink(as1r3, as1r6)
        self.addLink(as1r2, as1r4)
        self.addLink(as1r4, as1r5)
        self.addLink(as1r5, as1r6)
        self.addLink(as1r5, as1r7)
        self.addLink(as1r5, as1r9)
        self.addLink(as1r6, as1r7)
        self.addLink(as1r6, as1r8)
        self.addLink(as1r8, as1ra)
        self.addLink(as1r8, as1r9)
        self.addLink(as1r9, as1rb)
        self.addLink(as1ra, as2r1)
        self.addLink(as1ra, as1rb)
        self.addLink(as1rb, as2r1)
        self.addLink(as3r1, as1r1)
        self.addLink(as5r1, as1r6)
        self.addLink(as3r1, as5r1)
        self.addLink(as5r1, as2r1)
        set_rr(self, rr=as1r2, peers=[as1r1, as1r3, as1r4, as1r5, as1r6, as1r7, as1r8, as1r9, as1ra, as1rb])
        set_rr(self, rr=as1r3, peers=[as1r1, as1r2, as1r4, as1r5, as1r6, as1r7, as1r8, as1r9, as1ra, as1rb])
        set_rr(self, rr=as1r8, peers=[as1r1, as1r2, as1r3, as1r4, as1r5, as1r6, as1r7, as1r9, as1ra, as1rb])
        set_rr(self, rr=as1r9, peers=[as1r1, as1r2, as1r3, as1r4, as1r5, as1r6, as1r7, as1r8, as1ra, as1rb])

        # Add full mesh
        self.addAS(2, (as2r1,))
        self.addAS(3, (as3r1,))
        self.addAS(5, (as5r1,))
        self.addAS(1, (as1r1, as1r2, as1r3, as1r4, as1r5, as1r6, as1r7, as1r8, as1r9, as1ra, as1rb))

        # Add eBGP session
        ebgp_session(self, as1r6, as5r1)
        ebgp_session(self, as1r1, as3r1)
        ebgp_session(self, as3r1, as5r1)
        ebgp_session(self, as5r1, as2r1)
        ebgp_session(self, as1ra, as2r1)
        ebgp_session(self, as1rb, as2r1)

        super(BGPTopo3RR3, self).build(*args, **kwargs)

