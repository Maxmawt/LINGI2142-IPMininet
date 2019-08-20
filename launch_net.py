import importlib
import ipmininet
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

importlib.import_module('simple_bgp_network')
from simple_topo import SimpleBGPTopo

net = IPNet(topo=SimpleBGPTopo())
ipmininet.DEBUG_FLAG = True
try:
	net.start()
	IPCLI(net)
finally:
	net.stop()
