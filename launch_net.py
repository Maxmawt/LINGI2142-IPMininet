import importlib
import ipmininet
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

importlib.import_module('simple_bgp_network')
from simple_topo_err import SimpleBGPTopoErr

net = IPNet(topo=SimpleBGPTopoErr())
ipmininet.DEBUG_FLAG = True
try:
	net.start()
	IPCLI(net)
finally:
	net.stop()
