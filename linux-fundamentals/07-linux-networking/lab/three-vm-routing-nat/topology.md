
# Network Topology

## Overview

This lab uses three CentOS Stream 10 virtual machines running in Oracle VirtualBox.

Two servers are placed in separate internal networks. A third VM acts as a Linux router, connecting both networks and providing internet access through NAT.

## Network Diagram

```text
                       INTERNET
                          |
                 VirtualBox NAT
                    10.0.5.2
                          |
                   enp0s10
                   10.0.5.15
                          |
                  +----------------+
                  |   lab-router   |
                  |                |
                  | IP Forwarding  |
                  | firewalld NAT  |
                  +----------------+
                    |            |
              enp0s3|            |enp0s8
          192.168.10.1        192.168.20.1
                    |            |
               lab-net-a     lab-net-b
                    |            |
          192.168.10.10      192.168.20.10
                    |            |
             lab-server-1    lab-server-2

Management network (Host-only: 192.168.56.0/24)
  Windows host: 192.168.56.1
  Server 1:     192.168.56.10
  Server 2:     192.168.56.20
  Router:       192.168.56.30
```

## Virtual Machine Interfaces

| VM | Interface | VirtualBox Network | IP Address |
|---|---|---|---|
| lab-server-1 | enp0s3 | Internal: lab-net-a | 192.168.10.10/24 |
| lab-server-1 | enp0s9 | Host-only | 192.168.56.10/24 |
| lab-server-2 | enp0s3 | Internal: lab-net-b | 192.168.20.10/24 |
| lab-server-2 | enp0s9 | Host-only | 192.168.56.20/24 |
| lab-router | enp0s3 | Internal: lab-net-a | 192.168.10.1/24 |
| lab-router | enp0s8 | Internal: lab-net-b | 192.168.20.1/24 |
| lab-router | enp0s9 | Host-only | 192.168.56.30/24 |
| lab-router | enp0s10 | NAT | 10.0.5.15/24 |

## Default Gateways

| Machine | Default Gateway |
|---|---|
| lab-server-1 | 192.168.10.1 |
| lab-server-2 | 192.168.20.1 |
| lab-router | 10.0.5.2 |

The internal servers send traffic for destinations outside their local subnet to the Linux router.

The router forwards internet-bound packets through its NAT-facing interface.

## How Traffic Flows

Example: lab-server-1 accesses 8.8.8.8.

1. Server 1 generates an ICMP echo request.
2. The destination is outside 192.168.10.0/24.
3. Server 1 forwards the packet to its default gateway, 192.168.10.1.
4. The router receives the packet on enp0s3.
5. The firewall policy permits forwarding from the internal zone to the external zone.
6. NAT masquerading translates the source address from 192.168.10.10 to 10.0.5.15.
7. The packet exits through enp0s10 towards the VirtualBox NAT gateway.
8. The response returns through the router.
9. Connection tracking allows the reverse NAT translation.
10. The router forwards the response to Server 1.

Server 2 follows the same process through enp0s8.

## Firewall Zones

| Zone | Interfaces | Purpose |
|---|---|---|
| internal | enp0s3, enp0s8 | Internal lab networks |
| external | enp0s10 | Internet-facing NAT network |
| public | enp0s9 | Host-only management network |

The `lab-internet` firewalld policy permits forwarding from the internal zone to the external zone.

Masquerading is enabled on the external zone.

## Network Design Decisions

### Separate internal networks

The two servers are intentionally placed in different VirtualBox internal networks to practise Layer 3 routing.

### Dedicated Linux router

A separate VM handles routing, firewall rules and NAT, providing practical experience with Linux networking administration.

### Host-only management network

The management network allows SSH access from the Windows host without relying on the internal routing configuration.

### VirtualBox NAT adapter

The router uses a separate NAT-facing adapter for internet connectivity, allowing the internal servers to reach external networks through the Linux router.
