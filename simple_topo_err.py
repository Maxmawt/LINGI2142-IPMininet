from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig, BGP, ebgp_session, bgp_peering
import ipmininet.router.config.bgp as _bgp


class SimpleBGPTopoErr(IPTopo):
	"""This topology is composed of two AS connected in dual homing with different local pref"""

	def build(self, *args, **kwargs):
		"""
	TODO slide 27 BGP-RR-TE
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
		as1r3 = self.addRouter('as1r3')
		as1r3.addDaemon(BGP)
		as1r5 = self.addRouter('as1r5')
		as1r5.addDaemon(BGP)
		as1r6 = self.addRouter('as1r6')
		as1r6.addDaemon(BGP)
		as6r1 = self.addRouter('as6r1')
		as6r1.addDaemon(BGP, address_families=(_bgp.AF_INET6(networks=('dead:beef::/48',)),))
		as6r2 = self.addRouter('as6r2')
		as6r2.addDaemon(BGP, address_families=(_bgp.AF_INET6(networks=('dead:beef::/48',)),))
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
		self.addLink(as6r1, h1, params1={"ipv6": "dead:beef:1::/48"}, params2={"ipv6": "dead:beef:2::/48"})
		self.addLink(as6r2, h2, params1={"ipv6": "dead:beef:3::/48"}, params2={"ipv6": "dead:beef:4::/48"})
		self.addLink(as1r5, h3)
		self.addLink(as1r6, h4)
		_bgp.set_rr(self, as1r1, peers=[as1r3, as1r5])
		_bgp.set_rr(self, as1r3, peers=[as1r1, as1r6])

		# Add full mesh
		self.addAS(6, (as6r1, as6r2))
		self.addAS(1, (as1r1, as1r3, as1r5, as1r6))
		bgp_peering(self, as1r1, as1r5)
		bgp_peering(self, as1r3, as1r6)
		bgp_peering(self, as1r1, as1r3)

		# Add eBGP session
		ebgp_session(self, as1r1, as6r1)
		ebgp_session(self, as1r3, as6r2)

		# Add test hosts ?
		# for r in self.routers():
		#     self.addLink(r, self.addHost('h%s' % r))
		super(SimpleBGPTopoErr, self).build(*args, **kwargs)

	def bgp(self, name):
		r = self.addRouter(name, config=RouterConfig)
		r.addDaemon(BGP, address_families=(
			_bgp.AF_INET(redistribute=('connected',)),
			_bgp.AF_INET6(redistribute=('connected',))))
		return r
