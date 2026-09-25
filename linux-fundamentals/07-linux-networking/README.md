# Linux Networking

This section documents my practical learning of Linux networking as part of my DevOps journey.

My goal was not only to learn networking commands, but to understand how applications communicate over a network and how to troubleshoot connectivity problems systematically.

## What I Learned

Through this section, I explored:

- Network interfaces and IP addresses
- Loopback and localhost
- Routing and default gateways
- DNS and hostname resolution
- `/etc/hosts`
- `/etc/resolv.conf`
- `/etc/nsswitch.conf`
- DNS record types
- Ports and TCP listeners
- Application binding
- Network troubleshooting with Linux tools

## Practical Lab

To apply these concepts, I created a small Flask application and deliberately introduced different networking and application failures.

The application was accessed using:

```text
http://app1.local:5000

I configured app1.local locally and used it to practise troubleshooting the path between a hostname and an application.

The lab helped me understand the relationship between:

Hostname
   ↓
Name Resolution
   ↓
IP Address
   ↓
Routing / Reachability
   ↓
Port
   ↓
Application Binding
   ↓
Application Process

Troubleshooting Scenarios

I practised troubleshooting several failures:

Incorrect hostname-to-IP mapping
app1.local resolved to the wrong IP address.
I used getent, ip addr, and ip route to investigate.
Application listening on the wrong port
The application was expected on port 5000 but was listening on 8080.
I used ss -lntp to identify the listening port.
Incorrect application binding
The application was bound to 127.0.0.1:5000 instead of 0.0.0.0:5000.
This helped me understand the difference between localhost-only access and listening across IPv4 interfaces.
Application process stopped
Nothing was listening on port 5000.
I used ss, pgrep, and ps to determine whether the application process was running.

Commands Practised

| Command                   | Purpose                                             |
| ------------------------- | --------------------------------------------------- |
| `ip addr`                 | View network interfaces and assigned IP addresses   |
| `ip route`                | View the system routing table                       |
| `getent hosts <hostname>` | Check hostname resolution                           |
| `ping <host>`             | Test IP reachability                                |
| `ss -lntp`                | Inspect listening TCP ports and processes           |
| `curl <URL>`              | Test application connectivity                       |
| `pgrep -af <name>`        | Search for a running process using its command line |
| `ps -fp <PID>`            | Inspect a specific process                          |
| `nslookup <hostname>`     | Query DNS information                               |
| `dig <hostname>`          | Inspect DNS resolution in more detail               |


Key Lesson

One of the most important lessons from this lab was to avoid making assumptions when troubleshooting.

Instead, I learned to:

Inspect first, identify the failing layer, make a change, and then verify the fix.

For example, an application being "unavailable" does not automatically mean that the network is down. The problem could be hostname resolution, the destination IP, routing, the listening port, application binding, or the application process itself.

Lab Application

The Flask application used for these exercises is available here:

lab/app1.py

Notes

The detailed notes and exercises in this section are organised into:

Networking Fundamentals
IP Addresses and Interfaces
Routing and Gateways
DNS and Name Resolution
Ports and Application Binding
Network Troubleshooting

This repository documents my continued hands-on learning as I build practical Linux and DevOps skills.
