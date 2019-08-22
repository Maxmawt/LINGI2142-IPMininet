import importlib
import ipmininet
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

importlib.import_module('simple_bgp_network')
from simple_topo_missing3 import SimpleBGPTopoMissing

net = IPNet(topo=SimpleBGPTopoMissing())
ipmininet.DEBUG_FLAG = True
try:
	net.start()
	IPCLI(net)
finally:
	net.stop()
