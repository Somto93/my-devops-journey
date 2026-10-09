
# Linux Routing, NAT & Firewall Lab

## Project Overview

This project demonstrates how to build and configure a Linux router connecting two isolated networks using three CentOS Stream 10 virtual machines in VirtualBox.

The router provides communication between the internal networks and internet access through Network Address Translation (NAT).

The lab also explores Linux packet forwarding, nftables, firewalld, connection tracking, and persistent network configuration.

## Project Objectives

- Configure multiple network interfaces using NetworkManager.
- Connect two isolated subnets using a Linux router.
- Configure default gateways and IPv4 forwarding.
- Implement source NAT using masquerading.
- Explore nftables rules, counters and connection tracking.
- Configure persistent firewall zones and forwarding policies using firewalld.
- Troubleshoot network connectivity using Linux networking tools.
- Verify that the configuration survives a router reboot.

## Technologies Used

| Technology | Purpose |
|---|---|
| CentOS Stream 10 | Linux operating system |
| Oracle VirtualBox | Virtualization platform |
| NetworkManager | Network interface configuration |
| nftables | Linux packet filtering and NAT |
| firewalld | Persistent firewall management |
| conntrack | Connection tracking inspection |
| MobaXterm | Remote SSH administration |
| Linux CLI | Network configuration and troubleshooting |

## Network Architecture

Three virtual machines were configured:

| VM | Internal IP | Default Gateway |
|---|---|---|
| lab-server-1 | 192.168.10.10/24 | 192.168.10.1 |
| lab-server-2 | 192.168.20.10/24 | 192.168.20.1 |
| lab-router | 192.168.10.1/24 and 192.168.20.1/24 | 10.0.5.2 |

The router also uses:

- `enp0s9` — Host-only management interface (`192.168.56.30/24`)
- `enp0s10` — VirtualBox NAT interface (`10.0.5.15/24`)

See [Network Topology](topology.md) for the complete architecture.

## Implementation Summary

### 1. Network Configuration

Configured static internal IP addresses and default gateways using NetworkManager.

### 2. Linux Routing

Enabled IPv4 forwarding to allow packets to travel between network interfaces.

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Configured persistent forwarding using:

```text
/etc/sysctl.d/99-lab-router.conf
```

### 3. NAT with nftables

Initially implemented masquerading using nftables to allow internal servers to access external networks.

Used nftables counters and conntrack to observe packet translation.

### 4. Persistent Firewall Configuration

Migrated from manually configured nftables NAT rules to firewalld-managed NAT.

Configured:

- `internal` zone for the two internal interfaces.
- `external` zone for the NAT-facing interface.
- `public` zone for the host-only management interface.
- `lab-internet` policy permitting forwarding from internal to external.

### 5. Connectivity Testing

Verified connectivity using:

```bash
ping -c 4 8.8.8.8
ping -c 4 www.google.com
ip route
sudo firewall-cmd --get-active-zones
sudo conntrack -L -f ipv4
```

Both internal servers successfully accessed the internet.

### 6. Persistence Verification

Rebooted the router and verified that:

- IPv4 forwarding remained enabled.
- Firewall zone assignments were restored.
- The `lab-internet` policy remained active.
- Both internal servers retained internet connectivity.

## Project Results

- Successfully connected two isolated Linux networks.
- Configured internet access using NAT masquerading.
- Implemented persistent routing and firewall configuration.
- Verified network traffic using nftables and conntrack.
- Confirmed functionality after a router reboot.

## Documentation

- [Network Topology](topology.md)
- [Network Configuration](configuration.md)
- [Testing and Verification](testing-and-verification.md)
- [Troubleshooting](troubleshooting.md)
- [Lessons Learned](lessons-learned.md)

## Skills Demonstrated

Linux administration, TCP/IP networking, routing, NAT, firewall configuration, connection tracking, troubleshooting, virtualization and technical documentation.
