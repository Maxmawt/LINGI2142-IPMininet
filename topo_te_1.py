from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig, BGP, ebgp_session, bgp_peering, set_rr


class BGPTopoTE(IPTopo):
	"""This topology is composed of two AS connected in dual homing with different local pref"""

	def build(self, *args, **kwargs):
		"""
	TODO slide ? BGP_RR_TE with R3 and R6 as RRs
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
		as8r1 = self.addRouter('as8r1')
		as8r1.addDaemon(BGP, address_families=(_bgp.AF_INET6(networks=('dead:beef::/32',)),))
		as8r2 = self.addRouter('as8r2')
		as8r2.addDaemon(BGP, address_families=(_bgp.AF_INET6(networks=('dead:beef::/32',)),))
		as7r1 = self.addRouter('as7r1')
		as7r1.addDaemon(BGP, address_families=(_bgp.AF_INET6(networks=('feeb:daed::/32',)),))
		as7r2 = self.addRouter('as7r2')
		as7r2.addDaemon(BGP, address_families=(_bgp.AF_INET6(networks=('feeb:daed::/32',)),))
		as7r3 = self.addRouter('as7r3')
		as7r3.addDaemon(BGP, address_families=(_bgp.AF_INET6(networks=('feeb:daed::/32',)),))

		# Add Links
		self.addLink(as1r1, as1r6)
		self.addLink(as1r1, as1r3)
		self.addLink(as1r3, as1r2)
		self.addLink(as1r3, as1r6)
		self.addLink(as1r2, as1r4)
		self.addLink(as1r4, as1r5)
		self.addLink(as1r5, as1r6)
		self.addLink(as1r2, as8r1)
		self.addLink(as1r4, as8r2)
		self.addLink(as1r1, as7r1)
		self.addLink(as1r3, as7r2)
		self.addLink(as1r5, as7r3)
		self.addLink(as1r6, as7r3)
		set_rr(self, as1r3, peers=[as1r1, as1r2, as1r4, as1r5, as1r6])
		set_rr(self, as1r6, peers=[as1r1, as1r2, as1r3, as1r4, as1r5])

		# Add full mesh
		self.addiBGPFullMesh(1, (as1r1, as1r2, as1r3, as1r4, as1r5, as1r6))
		self.addAS(7, (as7r1, as7r2, as7r3))
		self.addAS(8, (as8r1, as8r2))

		# Add eBGP session
		ebgp_session(self, as1r2, as8r1)
		ebgp_session(self, as1r4, as8r2)
		ebgp_session(self, as1r1, as7r1)
		ebgp_session(self, as1r3, as7r2)
		ebgp_session(self, as1r5, as7r3)
		ebgp_session(self, as1r6, as7r3)


		# Add test hosts ?
		# for r in self.routers():
		#     self.addLink(r, self.addHost('h%s' % r))
		super(BGPTopoTE, self).build(*args, **kwargs)

	def bgp(self, name):
		r = self.addRouter(name, config=RouterConfig)
		r.addDaemon(BGP, address_families=(
			_bgp.AF_INET(redistribute=('connected',)),
			_bgp.AF_INET6(redistribute=('connected',))))
		return r
