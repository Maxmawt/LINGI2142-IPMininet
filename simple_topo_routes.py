from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, AF_INET6


class SimpleBGPTopoRoutes(IPTopo):

    def build(self, *args, **kwargs):
        """
        Topo from slide 30 iBGP
        """
        # Add all routers
        as1r1 = self.addRouter('as1r1')
        as1r1.addDaemon(BGP, address_families=(AF_INET6(networks=('1:1::/48',)),))
        as1r2 = self.addRouter('as1r2')
        as1r2.addDaemon(BGP, address_families=(AF_INET6(networks=('1:1::/48',)),))
        as1r3 = self.addRouter('as1r3')
        as1r3.addDaemon(BGP, address_families=(AF_INET6(networks=('1:1::/48',)),))
        as1r4 = self.addRouter('as1r4')
        as1r4.addDaemon(BGP, address_families=(AF_INET6(networks=('1:1::/48',)),))
        as2r1 = self.addRouter('as2r1')
        as2r1.addDaemon(BGP, address_families=(AF_INET6(networks=('dead:beef::/48',)),))
        h1 = self.addHost('h1')
        as3r1 = self.addRouter('as3r1')
        as3r1.addDaemon(BGP, address_families=(AF_INET6(networks=('beef:dead::/48',)),))
        as3r2 = self.addRouter('as3r2')
        as3r2.addDaemon(BGP, address_families=(AF_INET6(networks=('beef:dead::/48',)),))
        h2 = self.addHost('h2')

        # Add links
        self.addLink(as1r1, as1r2)
        self.addLink(as1r1, as1r3)
        self.addLink(as1r3, as1r4)
        self.addLink(as1r2, as1r4)
        self.addLink(as1r3, as2r1)
        self.addLink(as1r2, as3r1)
        self.addLink(as3r1, as3r2)
        self.addLink(as3r2, as2r1)
        self.addLink(as2r1, h1, params1={"ip": "dead:beef::/48"}, params2={"ip": "dead:beef::1/48"})
        self.addLink(as3r1, h2, params1={"ip": "dead:beef::4/48"}, params2={"ip": "dead:beef::5/48"})
        self.addLink(as3r2, h2, params1={"ip": "dead:beef::2/48"}, params2={"ip": "dead:beef::3/48"})

        # Add AS and fullmeshes
        self.addAS(2, (as2r1,))
        self.addiBGPFullMesh(1, routers=[as1r1, as1r2, as1r3, as1r4])
        self.addiBGPFullMesh(3, routers=[as3r1, as3r2])

        # Add eBGP sessions
        ebgp_session(self, as1r2, as3r1)
        ebgp_session(self, as3r2, as2r1)
        ebgp_session(self, as2r1, as1r3)

        super(SimpleBGPTopoRoutes, self).build(*args, **kwargs)

    def bgp(self, name):
        r = self.addRouter(name)
        r.addDaemon(BGP, address_families=(
            AF_INET6(redistribute=('connected',)),))
        return r       

