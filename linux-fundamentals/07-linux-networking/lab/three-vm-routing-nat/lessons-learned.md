
# Lessons Learned — Linux Routing, NAT and Firewalls

## Overview

This project provided hands-on experience configuring and troubleshooting Linux networking using three CentOS Stream 10 virtual machines.

The main lessons involved IP addressing, routing, packet forwarding, NAT, firewall management, connection tracking and configuration persistence.

## 1. A Linux Server Can Function as a Router

A Linux machine can connect multiple networks when it has suitable network interfaces, routing information and IP forwarding enabled.

In this lab, the router connected:

- `192.168.10.0/24` — Server 1 network
- `192.168.20.0/24` — Server 2 network
- `10.0.5.0/24` — External VirtualBox NAT network

The router used separate interfaces to communicate with each network.

**Key takeaway:** Linux routing is not limited to dedicated networking appliances.

## 2. Routing and NAT Are Different

Routing determines the next destination for a packet.

NAT modifies packet address information.

In this lab, the router used its routing table to forward internet-bound traffic through `enp0s10`.

Masquerading translated internal source addresses to the router's external address, `10.0.5.15`.

**Key takeaway:** Routing determines where packets travel, while NAT changes their addressing.

## 3. Default Gateways Are Essential

Each internal server required a default gateway:

- Server 1: `192.168.10.1`
- Server 2: `192.168.20.1`

Without an appropriate route, a server cannot send traffic to destinations outside its directly connected networks.

**Key takeaway:** IP addressing and routing must be configured together.

## 4. IPv4 Forwarding Must Be Enabled

The router required:

```bash
net.ipv4.ip_forward = 1
```

The setting was made persistent using:

```text
/etc/sysctl.d/99-lab-router.conf
```

**Key takeaway:** A multi-interface Linux machine does not automatically forward IPv4 packets between networks.

## 5. nftables and firewalld Have Different Roles

During the lab, nftables was used directly to create and inspect NAT rules.

This helped demonstrate:

- NAT chains and hooks
- Masquerading
- Packet counters
- Rule inspection

The final configuration used firewalld to manage persistent firewall zones and forwarding policies.

Firewalld used nftables as its backend.

**Key takeaway:** Understanding low-level firewall mechanisms makes higher-level firewall management easier to troubleshoot.

## 6. Connection Tracking Explains NAT Return Traffic

The `conntrack` utility helped demonstrate how Linux tracks network flows.

For outgoing traffic, connection tracking records information that allows returning packets to be associated with the original communication.

This supports reverse NAT translation.

**Key takeaway:** Connection tracking is important for understanding stateful networking and NAT.

## 7. Firewall Zones Organize Network Trust

The router used three firewall zones:

| Zone | Interface | Purpose |
|---|---|---|
| internal | enp0s3, enp0s8 | Internal networks |
| external | enp0s10 | NAT-facing network |
| public | enp0s9 | Management network |

A firewalld policy named `lab-internet` allowed traffic to be forwarded from `internal` to `external`.

**Key takeaway:** Firewall zones and policies help separate network interfaces according to their intended purpose.

## 8. Persistence Is Part of Infrastructure Reliability

The router was rebooted after the configuration was completed.

The following settings remained functional:

- Network interface assignments
- IPv4 forwarding
- Firewall zones
- Forwarding policy
- NAT-based internet connectivity

Both internal servers successfully reached `8.8.8.8` after the reboot.

**Key takeaway:** A working configuration should be tested again after restarting the system.

## 9. Troubleshooting Should Be Systematic

The lab reinforced a structured approach:

1. Check network interfaces.
2. Verify IP addresses.
3. Inspect routes and gateways.
4. Check IPv4 forwarding.
5. Inspect firewall policies.
6. Verify NAT.
7. Test external IP connectivity.
8. Test DNS resolution.
9. Inspect connection tracking.

**Key takeaway:** Isolating each networking layer is more effective than changing multiple settings without evidence.

## 10. Relevance to DevOps Engineering

The skills developed in this project apply to:

- Linux server administration
- Cloud networking and virtual networks
- Firewall and security group troubleshooting
- Container and Kubernetes networking fundamentals
- Network connectivity troubleshooting
- Infrastructure reliability and validation

The lab provides foundational knowledge for understanding how application traffic moves between hosts and networks.

## Future Improvements

Possible extensions include:

- Configuring an internal DNS server.
- Implementing DHCP for internal networks.
- Adding restrictive firewall policies.
- Capturing packets using `tcpdump`.
- Automating configuration with Ansible.
- Rebuilding the environment using Infrastructure as Code.

## Conclusion

This project strengthened my understanding of how Linux systems route, translate, filter and track network traffic.

The most valuable experience was moving from temporary networking experiments to a persistent configuration, then validating the complete system after reboot.
