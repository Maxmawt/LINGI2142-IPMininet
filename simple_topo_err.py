from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, set_rr, AF_INET6 


class SimpleBGPTopoErr(IPTopo):

    def build(self, *args, **kwargs):
        """
        Topo from slide 27 BGP-RR-TE
        """
        # Add all routers
        as1r1 = self.bgp('as1r1')
        as1r3 = self.bgp('as1r3')
        as1r5 = self.bgp('as1r5')
        as1r6 = self.bgp('as1r6')
        as6r1 = self.addRouter('as6r1')
        as6r1.addDaemon(BGP, address_families=(AF_INET6(networks=('dead:beef::/32',)),))
        as6r2 = self.addRouter('as6r2')
        as6r2.addDaemon(BGP, address_families=(AF_INET6(networks=('dead:beef::/32',)),))
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # Add Links
        self.addLink(as1r1, as1r6, ipg_cost=1)
        self.addLink(as1r5, as1r6, igp_cost=1)
        self.addLink(as1r3, as1r5, igp_cost=1)
        self.addLink(as1r1, as1r3, igp_cost=5)
        self.addLink(as6r1, as1r1)
        self.addLink(as6r2, as1r3)
        self.addLink(as6r1, h1, params1={"ip": "dead:beef::/48"}, params2={"ip": "dead:beef::1/48"})
        self.addLink(as6r2, h2, params1={"ip": "dead:beef::2/48"}, params2={"ip": "dead:beef::3/48"})
        self.addLink(as1r5, h3)
        self.addLink(as1r6, h4)
        set_rr(self, rr=as1r1, peers=[as1r3, as1r5])
        set_rr(self, rr=as1r3, peers=[as1r1, as1r6])

        # Add full mesh
        self.addAS(6, (as6r1, as6r2))
        self.addAS(1, (as1r1, as1r3, as1r5, as1r6))

        # Add eBGP session
        ebgp_session(self, as1r1, as6r1)
        ebgp_session(self, as1r3, as6r2)

        super(SimpleBGPTopoErr, self).build(*args, **kwargs)

    def bgp(self, name):
        r = self.addRouter(name)
        r.addDaemon(BGP, address_families=(
            AF_INET6(redistribute=('connected',)),))
        return r
