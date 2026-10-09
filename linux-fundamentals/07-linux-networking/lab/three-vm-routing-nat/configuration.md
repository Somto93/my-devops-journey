
# Linux Router Configuration

## Overview

This document explains how the three-VM networking lab was configured using NetworkManager, Linux IP forwarding, nftables and firewalld.

The lab was implemented on CentOS Stream 10 virtual machines running in Oracle VirtualBox.

The final configuration uses NetworkManager for interface management and firewalld for persistent NAT and forwarding policies.

## 1. Network Interface Configuration

The Linux router has four network interfaces.

| Interface | Network | IP Address | NetworkManager Profile |
|---|---|---|---|
| enp0s3 | lab-net-a | 192.168.10.1/24 | router-net-a |
| enp0s8 | lab-net-b | 192.168.20.1/24 | router-net-b |
| enp0s9 | Host-only | 192.168.56.30/24 | hostonly-mgmt |
| enp0s10 | VirtualBox NAT | 10.0.5.15/24 | router-nat |

### Inspect network interfaces

```bash
ip -br addr
```

### Inspect NetworkManager connections

```bash
nmcli connection show
```

### Inspect routing

```bash
ip route
```

The router's default gateway is `10.0.5.2`, reachable through `enp0s10`.

The external interface uses DHCP provided by VirtualBox NAT.

### Inspect the external interface

```bash
nmcli -f GENERAL.CONNECTION,GENERAL.DEVICE,IP4.ADDRESS,IP4.GATEWAY device show enp0s10
```

Verified output:

```text
GENERAL.CONNECTION: router-nat
GENERAL.DEVICE: enp0s10
IP4.ADDRESS[1]: 10.0.5.15/24
IP4.GATEWAY: 10.0.5.2
```

## 2. Internal Server Configuration

### Server 1

- Internal IP: `192.168.10.10/24`
- Default gateway: `192.168.10.1`
- Internal network: `lab-net-a`

### Server 2

- Internal IP: `192.168.20.10/24`
- Default gateway: `192.168.20.1`
- Internal network: `lab-net-b`

Both servers also have host-only management interfaces for SSH access.

## 3. Enable IPv4 Forwarding

Linux does not automatically forward IPv4 traffic between interfaces unless forwarding is enabled.

Enable forwarding at runtime:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

To make the setting persistent, create:

```text
/etc/sysctl.d/99-lab-router.conf
```

With the following content:

```ini
net.ipv4.ip_forward = 1
```

Verify:

```bash
sysctl net.ipv4.ip_forward
```

Expected output:

```text
net.ipv4.ip_forward = 1
```

This setting was verified again after rebooting the router.

## 4. Initial NAT Experiment Using nftables

Before implementing firewalld-managed NAT, the lab used nftables to explore source NAT and packet translation.

A temporary NAT table was created:

```bash
sudo nft add table ip lab_nat
```

A postrouting NAT chain was configured:

```bash
sudo nft 'add chain ip lab_nat postrouting { type nat hook postrouting priority srcnat; policy accept; }'
```

Masquerading rules were used for traffic leaving through `enp0s10` from:

- `192.168.10.0/24`
- `192.168.20.0/24`

An example rule:

```bash
sudo nft add rule ip lab_nat postrouting ip saddr 192.168.10.0/24 oifname "enp0s10" masquerade
```

A corresponding rule was used for `192.168.20.0/24`.

Packet counters were also explored to verify whether traffic matched NAT rules.

### Inspect nftables

```bash
sudo nft list ruleset
```

### Inspect NAT table

```bash
sudo nft list table ip lab_nat
```

These rules were part of the learning exercise and were not retained in the final configuration.

## 5. Connection Tracking

The `conntrack` utility was used to inspect network connections and NAT translations.

```bash
sudo conntrack -L -f ipv4
```

Connection tracking demonstrated how outgoing packets from an internal server could have their source address translated to the router's external address.

For example:

```text
Original source: 192.168.10.10
Translated source: 10.0.5.15
```

The connection tracking system also supports reverse translation of response packets.

## 6. Persistent Firewall Configuration Using firewalld

The final setup uses firewalld, which manages nftables rules through its own configuration system.

### Check firewalld

```bash
sudo systemctl status firewalld
```

### Inspect active zones

```bash
sudo firewall-cmd --get-active-zones
```

Verified configuration:

```text
external
  interfaces: enp0s10
internal
  interfaces: enp0s8 enp0s3
public (default)
  interfaces: enp0s9
```

### NetworkManager zone assignments

The connection profiles were assigned to zones:

```bash
sudo nmcli connection modify router-net-a connection.zone internal
sudo nmcli connection modify router-net-b connection.zone internal
sudo nmcli connection modify router-nat connection.zone external
```

The host-only management connection uses the default public zone.

### External zone masquerading

Verify:

```bash
sudo firewall-cmd --zone=external --query-masquerade
```

Result:

```text
yes
```

The external zone also has forwarding enabled.

## 7. Firewalld Forwarding Policy

A permanent policy named `lab-internet` permits forwarding from the internal zone to the external zone.

The policy was configured using:

```bash
sudo firewall-cmd --permanent --new-policy=lab-internet
sudo firewall-cmd --permanent --policy=lab-internet --add-ingress-zone=internal
sudo firewall-cmd --permanent --policy=lab-internet --add-egress-zone=external
sudo firewall-cmd --permanent --policy=lab-internet --set-target=ACCEPT
sudo firewall-cmd --permanent --policy=lab-internet --set-priority=-1
sudo firewall-cmd --reload
```

Inspect the policy:

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

Masquerading is managed by the external zone rather than the forwarding policy.

## 8. Remove Temporary nftables NAT Rules

After confirming that firewalld NAT and forwarding worked, the temporary nftables table was removed:

```bash
sudo nft delete table ip lab_nat
```

Verify:

```bash
sudo nft list tables
```

The final ruleset is managed by firewalld:

```text
table inet firewalld
```

This avoids maintaining overlapping NAT configurations.

## 9. Reboot Persistence

The router was rebooted:

```bash
sudo reboot
```

After reconnecting through SSH, the following were verified:

```bash
sysctl net.ipv4.ip_forward
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --info-policy=lab-internet
```

Both internal servers successfully pinged `8.8.8.8` after the reboot.

This confirmed that IPv4 forwarding, interface zone assignments, the forwarding policy and internet connectivity were restored.

## Conclusion

The final configuration provides:

- Routing between two isolated internal networks.
- Internet access through source NAT masquerading.
- Persistent IPv4 forwarding.
- NetworkManager-managed interfaces.
- Firewalld-managed zones and forwarding policies.
- SSH access through a separate host-only management network.
- Successful connectivity after a router reboot.
