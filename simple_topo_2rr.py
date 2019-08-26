from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig, BGP, ebgp_session, bgp_peering, set_rr


class SimpleBGPTopo2RR(IPTopo):
	"""This topology is composed of two AS connected in dual homing with different local pref"""

	def build(self, *args, **kwargs):
		"""
	TODO slide 39 iBGP
           +----------+                                   +--------+
                      |                                   |
         AS1          |                  AS2              |        AS3
                      |                                   |
                      |                                   |
    +-------+   eBGP  |  +-------+     iBGP    +-------+  |  eBGP   +-------+
    | as1r1 +------------+ as2r1 +-------------+ as2r2 +------------+ as3r1 |
    +-------+         |  +-------+             +-------+  |         +-------+
                      |                                   |
                      |                                   |
                      |                                   |
         +------------+                                   +--------+
        """
		# Add all routers
		as1r1 = self.addRouter('as1r1')
		as1r1.addDaemon(BGP)
		as1r2 = self.addRouter('as1r2')
		as1r2.addDaemon(BGP)
		as1r3 = self.addRouter('as1r3')
		as1r3.addDaemon(BGP)
		as1r4 = self.addRouter('as1r4')
		as1r4.addDaemon(BGP)
		as1r5 = self.addRouter('as1r5')
		as1r5.addDaemon(BGP)
		as1r6 = self.addRouter('as1r6')
		as1r6.addDaemon(BGP)
		as4r1 = self.addRouter('as4r1')
		as4r1.addDaemon(BGP, address_families=(_bgp.AF_INET6(networks=('dead:beef::/32',)),))
		as4r2 = self.addRouter('as4r2')
		as4r2.addDaemon(BGP, address_families=(_bgp.AF_INET6(networks=('dead:beef::/32',)),))

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
		set_rr(self, as1r3, peers=[as1r1, as1r2, as1r4, as1r5, as1r6])
		set_rr(self, as1r5, peers=[as1r1, as1r2, as1r4, as1r3, as1r6])

		# Add full mesh
		self.addAS(4, (as4r1, as4r2))
		self.addAS(1, (as1r1, as1r2, as1r3, as1r4, as1r5, as1r6))
		
		# Add eBGP session
		ebgp_session(self, as1r6, as4r1)
		ebgp_session(self, as1r5, as4r2)

		# Add test hosts ?
		# for r in self.routers():
		#     self.addLink(r, self.addHost('h%s' % r))
		super(SimpleBGPTopo2RR, self).build(*args, **kwargs)

	def bgp(self, name):
		r = self.addRouter(name, config=RouterConfig)
		r.addDaemon(BGP, address_families=(
			_bgp.AF_INET(redistribute=('connected',)),
			_bgp.AF_INET6(redistribute=('connected',))))
		return r
