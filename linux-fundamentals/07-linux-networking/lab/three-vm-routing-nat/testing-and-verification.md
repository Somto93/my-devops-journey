
# Testing and Verification

## Overview

This document describes the tests performed to verify routing, NAT, DNS resolution, firewall configuration, connection tracking and persistence in the three-VM Linux networking lab.

## 1. Network Connectivity

### Server 1

Internal address: `192.168.10.10/24`

Default gateway: `192.168.10.1`

Test command:

```bash
ping -c 4 8.8.8.8
```

**Result:** Successful.

Server 1 reached the external IP address through the Linux router.

### Server 2

Internal address: `192.168.20.10/24`

Default gateway: `192.168.20.1`

Test command:

```bash
ping -c 4 8.8.8.8
```

**Result:** Successful.

Server 2 also reached the external IP address through the Linux router.

These tests confirmed that both internal networks could reach an external destination.

## 2. DNS Resolution

The following command was tested from both servers:

```bash
ping -c 4 www.google.com
```

**Result:** Successful.

The hostname resolved to an IP address, and ICMP connectivity succeeded.

This demonstrated that the servers had functioning DNS resolution in addition to IP connectivity.

## 3. IPv4 Forwarding

On the router:

```bash
sysctl net.ipv4.ip_forward
```

Verified output:

```text
net.ipv4.ip_forward = 1
```

**Result:** Successful.

The Linux kernel was configured to forward IPv4 packets between interfaces.

## 4. NAT Verification with nftables

During the initial nftables experiment, NAT masquerading rules were configured for both internal subnets.

Packet counters were used to observe whether traffic matched the configured rules.

The counters registered matching packets while the servers generated traffic.

**Result:** Successful.

This provided evidence that packets were traversing the NAT rules.

## 5. Connection Tracking

The router's connection tracking table was inspected using:

```bash
sudo conntrack -L -f ipv4
```

The observations included ICMP connections originating from internal servers.

Example addresses observed during the lab:

```text
Original source:   192.168.10.10
Translated source: 10.0.5.15
```

The original and reply tuples helped demonstrate how NAT translation was tracked.

**Result:** Successful.

## 6. Firewalld Zone Verification

On the router:

```bash
sudo firewall-cmd --get-active-zones
```

Verified output:

```text
external
  interfaces: enp0s10
internal
  interfaces: enp0s8 enp0s3
public (default)
  interfaces: enp0s9
```

**Result:** Successful.

Each router interface was assigned to the intended firewall zone.

## 7. External Zone Masquerading

Command:

```bash
sudo firewall-cmd --zone=external --list-all
```

Relevant verified output:

```text
external (active)
  interfaces: enp0s10
  forward: yes
  masquerade: yes
```

**Result:** Successful.

The external zone had masquerading enabled.

## 8. Forwarding Policy Verification

Command:

```bash
sudo firewall-cmd --info-policy=lab-internet
```

Verified output:

```text
lab-internet (active)
  priority: -1
  target: ACCEPT
  ingress-zones: internal
  egress-zones: external
  masquerade: no
```

**Result:** Successful.

The firewall policy allowed traffic to be forwarded from the internal zone to the external zone.

NAT masquerading was handled separately by the external zone.

## 9. Firewalld-Only NAT Test

The temporary nftables NAT table was deleted:

```bash
sudo nft delete table ip lab_nat
```

The remaining nftables tables were inspected:

```bash
sudo nft list tables
```

Verified output:

```text
table inet firewalld
```

Both servers were then tested again for external IP and DNS connectivity.

**Result:** Successful.

This confirmed that the servers could access the internet without the temporary manually configured nftables NAT table.

## 10. Reboot Persistence Test

The router was restarted:

```bash
sudo reboot
```

After rebooting, the following checks were performed:

| Component | Result |
|---|---|
| SSH access to router | Passed |
| IPv4 forwarding | Passed |
| Firewall zone assignments | Passed |
| `lab-internet` policy | Passed |
| Server 1 internet connectivity | Passed |
| Server 2 internet connectivity | Passed |

Both servers successfully pinged `8.8.8.8` after the reboot.

**Result:** Successful.

This demonstrated that the final configuration was persistent.

## 11. Test Summary

| Test | Status |
|---|---|
| Server 1 external IP connectivity | PASS |
| Server 2 external IP connectivity | PASS |
| DNS resolution | PASS |
| IPv4 forwarding | PASS |
| nftables NAT counters | PASS |
| conntrack inspection | PASS |
| Firewalld zone configuration | PASS |
| External zone masquerading | PASS |
| Forwarding policy | PASS |
| Firewalld-only NAT | PASS |
| Reboot persistence | PASS |

## Conclusion

The testing confirmed that the Linux router could forward traffic from two isolated internal networks to an external network using NAT masquerading.

The final firewalld configuration remained functional after rebooting the router.

The lab also demonstrated the importance of validating networking changes through connectivity tests, firewall inspection and connection tracking.
