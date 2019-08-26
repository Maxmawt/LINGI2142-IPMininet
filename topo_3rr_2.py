from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig, BGP, ebgp_session, bgp_peering, set_rr


class BGPTopo3RR(IPTopo):
	"""This topology is composed of two AS connected in dual homing with different local pref"""

	def build(self, *args, **kwargs):
		"""
	TODO slide 44 iBGP RED config
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
		# Add routers
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
		as1r7 = self.addRouter('as1r7')
		as1r7.addDaemon(BGP)
		as1r8 = self.addRouter('as1r8')
		as1r8.addDaemon(BGP)
		as1r9 = self.addRouter('as1r9')
		as1r9.addDaemon(BGP)
		as1ra = self.addRouter('as1ra')
		as1ra.addDaemon(BGP)
		as1rb = self.addRouter('as1rb')
		as1rb.addDaemon(BGP)
		as5r1 = self.addRouter('as5r1')
		as5r1.addDaemon(BGP)
		as3r1 = self.addRouter('as3r1')
		as3r1.addDaemon(BGP)
		as2r1 = self.addRouter('as2r1')
		as2r1.addDaemon(BGP, address_families=(_bgp.AF_INET6(networks=('dead:beef::/48',)),))

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
		set_rr(self, as1r5, peers=[as1r1, as1r2, as1r3, as1r4, as1r6, as1r7, as1r8, as1r9, as1ra, as1rb])
		set_rr(self, as1r6, peers=[as1r1, as1r2, as1r3, as1r4, as1r5, as1r7, as1r8, as1r9, as1ra, as1rb])
		set_rr(self, as1r7, peers=[as1r1, as1r2, as1r3, as1r4, as1r5, as1r6, as1r8, as1r9, as1ra, as1rb])

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

		# Add test hosts ?
		# for r in self.routers():
		#     self.addLink(r, self.addHost('h%s' % r))
		super(BGPTopo3RR, self).build(*args, **kwargs)

	def bgp(self, name):
		r = self.addRouter(name, config=RouterConfig)
		r.addDaemon(BGP, address_families=(
			_bgp.AF_INET(redistribute=('connected',)),
			_bgp.AF_INET6(redistribute=('connected',))))
		return r
