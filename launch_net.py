import importlib
import ipmininet
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

importlib.import_module('simple_bgp_network')
from topo_med import MedBGPTopo

net = IPNet(topo=MedBGPTopo())
ipmininet.DEBUG_FLAG = True
try:
	net.start()
	IPCLI(net)
finally:
	net.stop()
