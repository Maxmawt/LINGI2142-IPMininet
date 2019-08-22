# LINGI2142-IPMininet

## Useful Commands

* To get the route in `ipv6` of a node NODE
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