from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig, BGP, ebgp_session
import ipmininet.router.config.bgp as _bgp


class MedBGPTopo(IPTopo):
	"""This topology is composed of two AS connected in dual homing with different local pref"""

	def build(self, *args, **kwargs):
		"""
	TODO slide 26 iBGP
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
		as3r1 = self.addRouter('as3r1')
		as3r1.addDaemon(BGP)
		as3r2 = self.addRouter('as3r2')
		as3r2.addDaemon(BGP)
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
		self.addLink(as4r1, as1r5)
		self.addLink(as4r2, as1r4)
		self.addLink(as3r2, as1r1)
		self.addLink(as3r1, as1r6)
		self.addLink(as3r1, as3r2, igp_cost=7)
		self.addLink(as3r1, as2r1)
		self.addLink(as2r1, as4r1)
		self.addLink(as4r1, as4r2, igp_cost=2)

		# Set Med
		_bgp.set_med(self, as3r2, as1r1, 7)
		_bgp.set_med(self, as3r1, as1r6, 0)
		_bgp.set_med(self, as4r1, as1r5, 0)
		_bgp.set_med(self, as4r2, as1r4, 2)
		
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

		# Add test hosts ?
		# for r in self.routers():
		#     self.addLink(r, self.addHost('h%s' % r))
		super(MedBGPTopo, self).build(*args, **kwargs)

	def bgp(self, name):
		r = self.addRouter(name, config=RouterConfig)
		r.addDaemon(BGP, address_families=(
			_bgp.AF_INET(redistribute=('connected',)),
			_bgp.AF_INET6(redistribute=('connected',))))
		return r
