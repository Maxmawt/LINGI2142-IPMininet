from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, AccessList, AF_INET6


class MedBGPTopo(IPTopo):

    def build(self, *args, **kwargs):
        """
        Topo from slide 26 iBGP
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
        as3r1 = self.bgp('as3r1')
        as3r2 = self.bgp('as3r2')
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
        self.addLink(as1r1, as1r6, params1={"ip": ("fd00:1:1::1/48",)},
                     params2={"ip": ("fd00:1:1::2/48",)})
        self.addLink(as1r1, as1r3, params1={"ip": ("fd00:1:2::1/48",)},
                     params2={"ip": ("fd00:1:2::2/48",)})
        self.addLink(as1r3, as1r2, params1={"ip": ("fd00:1:4::1/48",)},
                     params2={"ip": ("fd00:1:4::2/48",)})
        self.addLink(as1r3, as1r6, params1={"ip": ("fd00:1:3::1/48",)},
                     params2={"ip": ("fd00:1:3::2/48",)})
        self.addLink(as1r2, as1r4, params1={"ip": ("fd00:1:5::1/48",)},
                     params2={"ip": ("fd00:1:5::2/48",)})
        self.addLink(as1r4, as1r5, params1={"ip": ("fd00:1:6::1/48",)},
                     params2={"ip": ("fd00:1:6::2/48",)})
        self.addLink(as1r5, as1r6, params1={"ip": ("fd00:1:7::1/48",)},
                     params2={"ip": ("fd00:1:7::2/48",)})
        self.addLink(as4r1, as1r5, params1={"ip": ("fd00:4:2::1/48",)},
                     params2={"ip": ("fd00:4:2::2/48",)})
        self.addLink(as4r2, as1r4, params1={"ip": ("fd00:4:1::1/48",)},
                     params2={"ip": ("fd00:4:1::2/48",)})
        self.addLink(as3r2, as1r1, params1={"ip": ("fd00:3:1::1/48",)},
                     params2={"ip": ("fd00:3:1::2/48",)})
        self.addLink(as3r1, as1r6, params1={"ip": ("fd00:3:2::1/48",)},
                     params2={"ip": ("fd00:3:2::2/48",)})
        self.addLink(as3r1, as3r2, params1={"ip": ("fd00:3:3::1/48",)},
                     params2={"ip": ("fd00:3:3::2/48",)}, igp_cost=7)
        self.addLink(as3r1, as2r1, params1={"ip": ("fd00:2:1::1/48",)},
                     params2={"ip": ("fd00:2:1::2/48",)})
        self.addLink(as2r1, as4r1, params1={"ip": ("fd00:2:2::1/48",)},
                     params2={"ip": ("fd00:2:2::2/48",)})
        self.addLink(as4r1, as4r2, params1={"ip": ("fd00:4:3::1/48",)},
                     params2={"ip": ("fd00:4:3::2/48",)}, igp_cost=2)
        self.addLink(as2r1, as2h1, params1={"ip": ("dead:beef::1/32",)},
                     params2={"ip": ("dead:beef::2/32",)})

        self.addLink(as1r1, as1h1)
        self.addLink(as1r2, as1h2)
        self.addLink(as1r3, as1h3)
        self.addLink(as1r4, as1h4)
        self.addLink(as1r5, as1h5)
        self.addLink(as1r6, as1h6)

        # Set Med
        al = AccessList(name='all', entries=('any',))
        as3r2.get_config(BGP).set_med(7, to_peer=as1r1, matching=(al,))
        as3r1.get_config(BGP).set_med(0, to_peer=as1r6, matching=(al,))
        as4r1.get_config(BGP).set_med(0, to_peer=as1r5, matching=(al,))
        as4r2.get_config(BGP).set_med(2, to_peer=as1r4, matching=(al,))

        # Add full mesh
        self.addAS(2, (as2r1,))
        self.addiBGPFullMesh(3, routers=[as3r1, as3r2])
        self.addiBGPFullMesh(4, routers=[as4r1, as4r2])
        self.addiBGPFullMesh(1, routers=[as1r1, as1r2, as1r3, as1r4, as1r5, as1r6])

        # Add eBGP session
        ebgp_session(self, as1r6, as3r1)
        ebgp_session(self, as1r1, as3r2)
        ebgp_session(self, as1r4, as4r2)
        ebgp_session(self, as1r5, as4r1)
        ebgp_session(self, as3r1, as2r1)
        ebgp_session(self, as2r1, as4r1)

        super(MedBGPTopo, self).build(*args, **kwargs)

    def bgp(self, name):
        r = self.addRouter(name)
        r.addDaemon(BGP, address_families=(
            AF_INET6(redistribute=('connected',)),))
        return r