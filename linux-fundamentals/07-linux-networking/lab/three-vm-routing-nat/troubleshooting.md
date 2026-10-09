
# Linux Network Troubleshooting

## Overview

This document describes the troubleshooting techniques explored during the three-VM Linux routing and NAT lab.

The main objective was to understand how to identify problems involving network interfaces, routing, IP forwarding, NAT, firewall rules and DNS resolution.

## 1. Troubleshooting Methodology

When a Linux server cannot reach another network, investigate the problem in layers:

1. Check whether the network interface is active.
2. Verify the IP address and subnet.
3. Inspect the routing table and default gateway.
4. Test connectivity to the local gateway.
5. Check whether the router has IPv4 forwarding enabled.
6. Inspect firewall policies and NAT rules.
7. Test connectivity to an external IP address.
8. Test DNS resolution separately.
9. Inspect packet counters and connection tracking.

This approach helps identify where connectivity is failing.

## 2. Checking Network Interfaces

Commands:

```bash
ip -br addr
ip link show
nmcli device status
```

These commands help identify:

- Missing IP addresses.
- Interfaces that are down.
- Incorrect network assignments.
- Interfaces not managed by NetworkManager.

### Key lesson

A server cannot communicate correctly if its interface is down or configured with an incorrect IP address.

## 3. Troubleshooting Routing

Commands:

```bash
ip route
ip route get 8.8.8.8
```

The first command displays the routing table.

The second shows which route Linux would select for a specific destination.

For example, Server 1 should route external traffic through:

```text
default via 192.168.10.1
```

Server 2 should use:

```text
default via 192.168.20.1
```

### Key lesson

A correctly configured IP address is not enough. A server also needs a valid route to destinations outside its local subnet.

## 4. Checking IPv4 Forwarding

On the router:

```bash
sysctl net.ipv4.ip_forward
```

Expected:

```text
net.ipv4.ip_forward = 1
```

If forwarding is disabled, the router will not forward IPv4 packets between interfaces.

The persistent configuration used in this lab was:

```text
/etc/sysctl.d/99-lab-router.conf
```

Containing:

```ini
net.ipv4.ip_forward = 1
```

### Key lesson

A Linux machine with multiple network interfaces does not automatically function as a router.

## 5. Troubleshooting NAT

During the initial lab, nftables was used to configure and inspect NAT rules.

Useful command:

```bash
sudo nft list ruleset
```

NAT packet counters were used to check whether packets matched masquerading rules.

The final configuration used firewalld:

```bash
sudo firewall-cmd --zone=external --query-masquerade
```

Expected:

```text
yes
```

### Key lesson

Routing and NAT perform different functions.

Routing determines where packets should go.

NAT changes packet address information so internal hosts can communicate through an external interface.

## 6. Troubleshooting Firewall Zones

Command:

```bash
sudo firewall-cmd --get-active-zones
```

Expected:

```text
external
  interfaces: enp0s10
internal
  interfaces: enp0s8 enp0s3
public (default)
  interfaces: enp0s9
```

To inspect the forwarding policy:

```bash
sudo firewall-cmd --info-policy=lab-internet
```

The policy permits traffic from the internal zone to the external zone.

### Key lesson

An interface assigned to the wrong firewall zone can cause traffic to be processed under an unintended security policy.

## 7. Connection Tracking

Command:

```bash
sudo conntrack -L -f ipv4
```

Connection tracking helped us understand how Linux associates outgoing packets with returning traffic.

During NAT, the original packet source and translated address can be observed through the connection tracking entries.

### Key lesson

Connection tracking provides useful evidence when investigating whether traffic is reaching the router and how NAT is being applied.

## 8. Distinguishing DNS Problems from Routing Problems

Test external IP connectivity:

```bash
ping -c 4 8.8.8.8
```

Test hostname resolution and connectivity:

```bash
ping -c 4 www.google.com
```

If the first test succeeds but the second fails, DNS resolution should be investigated.

Useful commands:

```bash
cat /etc/resolv.conf
getent hosts www.google.com
```

### Key lesson

DNS resolution and IP connectivity are separate functions.

A server can have working routing and NAT but still fail to resolve domain names.

## 9. Verifying Changes After Reboot

After configuring persistent routing and firewall policies, the router was rebooted.

The following were checked:

```bash
sysctl net.ipv4.ip_forward
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --info-policy=lab-internet
```

Both internal servers were also tested:

```bash
ping -c 4 8.8.8.8
```

All checks succeeded.

### Key lesson

A configuration that works before reboot is not necessarily persistent.

Reboot testing is an important part of validating Linux infrastructure.

## 10. Troubleshooting Checklist

| Symptom | First checks |
|---|---|
| Interface has no IP | `ip -br addr`, `nmcli device status` |
| Cannot reach gateway | IP address, subnet, interface state |
| Cannot reach external IP | Default route, forwarding, firewall, NAT |
| External IP works but hostname fails | DNS resolver configuration |
| NAT does not appear to work | Firewall masquerading, nftables, conntrack |
| Network fails after reboot | Persistent NetworkManager, sysctl and firewalld configuration |
| SSH access fails | Interface address, routing, SSH service, firewall zone |


## 11. Practical Troubleshooting and Validation Exercises

### Exercise 1: Inspecting NAT Packet Counters

**Objective:** Determine whether traffic from the internal servers matched the configured nftables NAT rules.

**Actions:**

1. Configured NAT masquerading rules for the two internal subnets.
2. Used nftables counters to inspect matching traffic.
3. Generated traffic from the internal servers.
4. Observed the counters registering matching packets.

**Outcome:** Confirmed that traffic was reaching the NAT rules.

**Lesson:** Packet counters provide evidence of rule matching, rather than relying solely on connectivity tests.

### Exercise 2: Inspecting NAT with conntrack

**Objective:** Understand how Linux tracks connections when source NAT is applied.

**Command:**

```bash
sudo conntrack -L -f ipv4
```

**Observation:**

Connection tracking entries showed traffic originating from internal addresses, including `192.168.10.10`, with reply-side information reflecting translation to the router's external address, `10.0.5.15`.

**Outcome:** Observed how connection tracking supports NAT and return traffic.

**Lesson:** Connection tracking helps explain packet translation beyond what a successful ping can demonstrate.

### Exercise 3: Verifying firewalld Without Manual NAT Rules

**Objective:** Confirm that firewalld-managed masquerading worked independently of the temporary nftables NAT table.

**Actions:**

1. Configured firewalld zones and the `lab-internet` forwarding policy.
2. Enabled masquerading through the external zone.
3. Removed the temporary nftables table:

```bash
sudo nft delete table ip lab_nat
```

4. Verified the remaining tables:

```bash
sudo nft list tables
```

**Observed output:**

```text
table inet firewalld
```

5. Tested internet connectivity from both internal servers.

**Outcome:** Both servers successfully accessed the internet without the temporary NAT table.

**Lesson:** Testing after removing the experimental rules confirmed that the final configuration did not depend on them.

### Exercise 4: Verifying Configuration Persistence

**Objective:** Determine whether routing and firewall configuration survived a reboot.

**Actions:**

1. Rebooted the router.
2. Reconnected through SSH.
3. Verified IPv4 forwarding.
4. Inspected active firewall zones.
5. Verified the permanent forwarding policy.
6. Tested external connectivity from both internal servers.

**Outcome:** All checks succeeded.

**Lesson:** Reboot testing is essential for distinguishing temporary changes from persistent infrastructure configuration.


## Conclusion

This lab reinforced the importance of systematic network troubleshooting.

Rather than changing several settings simultaneously, each networking layer should be tested independently.

The combination of `ip`, `nmcli`, `sysctl`, `nft`, `firewall-cmd`, `ping` and `conntrack` provides a practical toolkit for diagnosing Linux networking problems.
