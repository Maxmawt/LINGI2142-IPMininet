from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig, BGP, ebgp_session
import ipmininet.router.config.bgp as _bgp


class SimpleBGPAS(IPTopo):
	"""This topology is composed of two AS connected in dual homing with different local pref"""

	def build(self, *args, **kwargs):
		"""
	TODO slide 23 iBGP
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
		as4r1.addDaemon(BGP)
		as4r2 = self.addRouter('as4r2')
		as4r2.addDaemon(BGP)
		as5r1 = self.addRouter('as5r1')
		as5r1.addDaemon(BGP)
		as3r1 = self.addRouter('as3r1')
		as3r1.addDaemon(BGP)
		as2r1 = self.addRouter('as2r1')
		as2r1.addDaemon(BGP, address_families=(_bgp.AF_INET(networks=('dead:beef::/48',)),))

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

		# Add full mesh
		self.addAS(2, (as2r1,))
		self.addAS(3, (as3r1,))
		self.addAS(5, (as5r1,))
		self.addiBGPFullMesh(4, routers=[as4r1, as4r2])
		self.addiBGPFullMesh(1, routers=[as1r1, as1r2, as1r3, as1r4, as1r5, as1r6])

		# Add eBGP session
		ebgp_session(self, as1r6, as5r1)
		ebgp_session(self, as1r1, as1r1)
		ebgp_session(self, as1r4, as4r2)
		ebgp_session(self, as1r5, as4r1)
		ebgp_session(self, as3r1, as5r1)
		ebgp_session(self, as5r1, as2r1)
		ebgp_session(self, as2r1, as4r1)

		# Add test hosts ?
		# for r in self.routers():
		#     self.addLink(r, self.addHost('h%s' % r))
		super(SimpleBGPAS, self).build(*args, **kwargs)

	def bgp(self, name):
		r = self.addRouter(name, config=RouterConfig)
		r.addDaemon(BGP, address_families=(
			_bgp.AF_INET(redistribute=('connected',)),
			_bgp.AF_INET6(redistribute=('connected',))))
		return r
