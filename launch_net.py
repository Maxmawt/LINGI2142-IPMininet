import importlib
import ipmininet
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.clean import cleanup
from mininet.log import lg, LEVELS

from simple_bgp_network import SimpleBGPTopo
from simple_topo_2rr import SimpleBGPTopo2RR
from simple_topo_as import SimpleBGPTopoAS
from simple_topo_err import SimpleBGPTopoErr
from simple_topo_local_pref import SimpleBGPTopoLocalPref
from simple_topo_med import SimpleBGPTopoMed
from simple_topo_missing1 import SimpleBGPTopoMissing1
from simple_topo_missing2 import SimpleBGPTopoMissing2
from simple_topo_missing3 import SimpleBGPTopoMissing3
from simple_topo import SimpleBGPTopo
from simple_topo_routes import SimpleBGPTopoRoutes
from simple_topo_rr import SimpleBGPTopoRR
from topo_2rr_1 import BGPTopo2RR1
from topo_2rr_2 import BGPTopo2RR2
from topo_2rr_3 import BGPTopo2RR3
from topo_2rr_4 import BGPTopo2RR4
from topo_2rr_5 import BGPTopo2RR5
from topo_3rr_1 import BGPTopo3RR1
from topo_3rr_2 import BGPTopo3RR2
from topo_3rr_3 import BGPTopo3RR3
from topo_med import MedBGPTopo
from topo_te_1 import BGPTopoTE1
from topo_te_2 import BGPTopoTE2

import argparse

TOPOS = {'simple_bgp_network': SimpleBGPTopo,
         'simple_topo_2rr': SimpleBGPTopo2RR,
         'simple_topo_as': SimpleBGPTopoAS,
         'simple_topo_err': SimpleBGPTopoErr,
         'simple_topo_local_pref': SimpleBGPTopoLocalPref,
         'simple_topo_med': SimpleBGPTopoMed,
         'simple_topo_missing1': SimpleBGPTopoMissing1,
         'simple_topo_missing2': SimpleBGPTopoMissing2,
         'simple_topo_missing3': SimpleBGPTopoMissing3,
         'simple_topo': SimpleBGPTopo,
         'simple_topo_rr': SimpleBGPTopoRR,
         'topo_2rr_1': BGPTopo2RR1,
         'topo_2rr_2': BGPTopo2RR2,
         'topo_2rr_3': BGPTopo2RR3,
         'topo_2rr_4': BGPTopo2RR4,
         'topo_2rr_5': BGPTopo2RR5,
         'topo_med': MedBGPTopo,
         'topo_te_1': BGPTopoTE1,
         'simple_topo_routes': SimpleBGPTopoRoutes,
         'topo_3rr_1': BGPTopo3RR1,
         'topo_3rr_2': BGPTopo3RR2,
         'topo_3rr_3': BGPTopo3RR3,
         'topo_te_2': BGPTopoTE2
         }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topo', choices=TOPOS.keys(), default='simple_bgp_network',
                        help='the topology that you want to start')
    parser.add_argument('--log', choices=LEVELS.keys(), default='info',
                        help='The level of details in the logs')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    lg.setLogLevel(args.log)
    if args.log == 'debug':
        ipmininet.DEBUG_FLAG = True
    kwargs = {}
    net = IPNet(topo=TOPOS[args.topo](**kwargs))
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
        cleanup()
