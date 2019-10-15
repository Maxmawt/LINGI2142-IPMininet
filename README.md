# LINGI2142-IPMininet

## Launch the CLI

To launch the CLI and test the topologies, run
```bash
python3 launch_net.py --topo=TOPO
```

where TOPO is one the following topologies (from the slides in the courses folder):
- simple_bgp_network (from the examples of ipmininet)
- simple_topo_2rr (from slide 39 iBGP)
- simple_topo_as (from slide 23 iBGP)
- simple_topo_err (from slide 27 BGP-RR-TE)
- simple_topo_local_pref (from the examples of ipmininet)
- simple_topo_med (from slide 25 iBGP)
- simple_topo_missing1 (from slide 33 iBGP)
- simple_topo_missing2 (from slide 33 iBGP)
- simple_topo_missing3 (from slide 33 iBGP)
- simple_topo (from slide 22 iBGP)
- simple_topo_rr (from slide 38 iBGP)
- topo_2rr_1 (from slide 40 iBGP)
- topo_2rr_2 (from slide 42 iBGP RED config)
- topo_2rr_3 (from slide 42 iBGP GREEN config)
- topo_2rr_4 (from slide 42 iBGP YELLOW config)
- topo_2rr_5 (from slide 42 iBGP BLUE config)
- topo_3rr_1 (from slide 43 iBGP)
- topo_3rr_2 (from slide 44 iBGP RED config)
- topo_3rr_3 (from slide 44 iBGP BLUE config)
- topo_med (slide 26 iBGP)
- topo_te_1 (from slide 30 BGP_RR_TE with R3 and R6 as RRs)
- topo_te_2 (from slide 30 BGP_RR_TE with R3 and R4 as RRs)

## Useful Commands

* To get the routes in `ipv6` of a node NODE
```bash
mininet> NODE route -6
```
* To get all the prefixes received by a node NODE using bgpd.
Enter first:
```bash
mininet> noecho NODE telnet localhost bgpd
```
Enter the password zebra and enter the following command:
```bash
NODE> show show bgp ipv6
```
* To get informations about the different links and interfaces
```bash
mininet> links
```

## Contribute

If you find errors, do not hesitate to raise an issue. 
If you want to add topologies, feel free to open a pull request.
