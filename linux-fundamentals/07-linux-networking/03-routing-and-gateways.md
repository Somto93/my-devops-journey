# Routing and Gateways

This section documents what I learned about Linux routing, directly connected networks, default routes, gateways, and IP forwarding.

## 1. What Is Routing?

Once a hostname has been resolved to an IP address, Linux needs to determine how packets should reach that destination.

This is the job of routing.

I can inspect the Linux routing table using:

```bash
ip route
```

During my networking lab, my routing table included:

```text
default via 172.23.208.1 dev eth0
172.23.208.0/20 dev eth0 scope link src 172.23.210.163
```

These two routes helped me understand the difference between:

- a directly connected network
- a default route

---

## 2. Reading a Route

Consider:

```text
172.23.208.0/20 dev eth0 scope link src 172.23.210.163
```

I can break this down as:

```text
172.23.208.0/20
        ↓
Destination network

dev eth0
        ↓
Use the eth0 interface

scope link
        ↓
The network is directly reachable through this interface

src 172.23.210.163
        ↓
Source IP associated with this route
```

This tells Linux that the `172.23.208.0/20` network is directly connected through `eth0`.

---

## 3. Directly Connected Networks

A directly connected network does not require the default gateway to reach destinations on that network.

For example, my machine had:

```text
eth0 → 172.23.210.163/20
```

and the routing table contained:

```text
172.23.208.0/20 dev eth0
```

During one troubleshooting exercise, I deliberately changed:

```text
app1.local → 172.23.210.163
```

to:

```text
app1.local → 172.23.210.200
```

Initially, I considered whether this was a routing problem.

However, `172.23.210.200` was still covered by the directly connected:

```text
172.23.208.0/20
```

route.

Linux therefore had a route towards that destination.

The real problem was that `app1.local` had been mapped to the wrong IP address.

This taught me:

> A connection failure does not automatically mean that routing is broken.

---

## 4. The Default Route

My routing table also contained:

```text
default via 172.23.208.1 dev eth0
```

The word:

```text
default
```

means this route can be used when Linux does not have a more specific matching route for the destination.

I can think about it as:

```text
Destination IP
      ↓
Check routing table
      ↓
Is there a more specific route?
     / \
   Yes  No
    |    |
    |    ↓
    |  Default route
    |    |
    ↓    ↓
Send according to selected route
```

---

## 5. Default Gateway

In:

```text
default via 172.23.208.1 dev eth0
```

the address:

```text
172.23.208.1
```

is the next-hop gateway for the default route.

The route tells Linux:

```text
For destinations without a more specific route:

Send the packet
      ↓
towards 172.23.208.1
      ↓
through eth0
```

This gateway can then forward traffic towards other networks.

---

## 6. Example — Reaching `8.8.8.8`

During the lab, I considered what would happen if my machine needed to send traffic to:

```text
8.8.8.8
```

Linux checks the routing table:

```text
default via 172.23.208.1 dev eth0
172.23.208.0/20 dev eth0 scope link src 172.23.210.163
```

`8.8.8.8` does not belong to my directly connected:

```text
172.23.208.0/20
```

network.

Therefore, Linux uses:

```text
default via 172.23.208.1 dev eth0
```

The path begins like this:

```text
My machine
172.23.210.163
      ↓
eth0
      ↓
Default gateway
172.23.208.1
      ↓
Other networks
      ↓
Destination
8.8.8.8
```

This helped me understand the purpose of a default gateway.

---

## 7. Reaching My Own IP

Another important lesson was that the default gateway is not involved in every connection.

For example:

```bash
curl http://172.23.210.163:5000
```

targets an IP address assigned to my own machine.

I originally associated successful communication with the default gateway, but learned that the gateway is not what makes this connection work.

The destination is local to my own system.

This distinction helped me avoid treating the default gateway as something that every packet must pass through.

---

## 8. More Specific Routes Take Priority

A useful routing principle is:

> Linux chooses the most specific matching route for a destination.

The default route is effectively the fallback when there is no more specific route.

For example:

```text
Destination: 172.23.210.200
```

matches:

```text
172.23.208.0/20 dev eth0
```

so Linux uses the directly connected route.

But:

```text
Destination: 8.8.8.8
```

does not match that network.

Linux therefore falls back to:

```text
default via 172.23.208.1 dev eth0
```

---

## 9. Static Routes

I also learned that routes can be added manually.

A route can tell Linux how to reach another network through a particular gateway.

The general idea is:

```text
Network A
   ↓
Router / Gateway
   ↓
Network B
```

A static route provides an explicit path towards a destination network.

A common Linux command format is:

```bash
ip route add <destination-network> via <gateway>
```

For example:

```bash
ip route add 192.168.2.0/24 via 192.168.1.1
```

This tells Linux that traffic destined for:

```text
192.168.2.0/24
```

should be sent through:

```text
192.168.1.1
```

---

## 10. IP Forwarding

Routing traffic from one network to another requires more than simply having multiple network interfaces.

Linux also has an IP forwarding setting.

I can inspect it using:

```bash
cat /proc/sys/net/ipv4/ip_forward
```

A value of:

```text
0
```

means IPv4 forwarding is disabled.

A value of:

```text
1
```

means IPv4 forwarding is enabled.

This becomes important when a Linux machine is being used to forward packets between networks.

A simple model is:

```text
Machine A
192.168.1.x
      ↓
Linux Router
      ↓
Machine C
192.168.2.x
```

For the Linux machine in the middle to act as a router, packet forwarding must be enabled in addition to having the appropriate routes.

---

## 11. Routing vs IP Forwarding

I learned to separate these concepts.

### Routing

Routing determines:

> Where should a packet go?

I inspect routes with:

```bash
ip route
```

### IP Forwarding

IP forwarding determines whether the Linux machine can forward packets arriving on one interface towards another network/interface.

I inspect it with:

```bash
cat /proc/sys/net/ipv4/ip_forward
```

So:

```text
Routing
   ↓
Determine the path

IP Forwarding
   ↓
Allow the machine to forward traffic between networks
```

---

## 12. `ip addr` vs `ip route`

These commands answer different questions.

### `ip addr`

```bash
ip addr
```

asks:

> What interfaces and IP addresses does my machine have?

### `ip route`

```bash
ip route
```

asks:

> How will Linux reach a destination?

For example:

```text
ip addr
   ↓
eth0 = 172.23.210.163

ip route
   ↓
172.23.208.0/20 → eth0
default → 172.23.208.1 via eth0
```

---

## 13. Routing During Troubleshooting

When an application is unavailable, I should not run `ip route` simply because there is a networking problem.

I should use it when I need to answer a routing question.

For example:

```text
Can the hostname be resolved?
        ↓
getent hosts

What IPs are configured locally?
        ↓
ip addr

How would Linux reach the destination?
        ↓
ip route

Is the application listening?
        ↓
ss -lntp

Can I connect to the application?
        ↓
curl
```

Each command provides evidence about a different part of the communication path.

---

## 14. Routing Troubleshooting Example

During my lab:

```bash
curl --connect-timeout 3 http://app1.local:5000
```

timed out after I deliberately changed the `/etc/hosts` entry.

I investigated using:

```bash
getent hosts app1.local
```

and found:

```text
172.23.210.200 app1.local
```

I compared this with:

```bash
ip addr
```

which showed:

```text
eth0 → 172.23.210.163
```

I also considered the routing table:

```bash
ip route
```

which showed:

```text
172.23.208.0/20 dev eth0
```

This meant Linux still had a route towards `172.23.210.200`.

Therefore, the main issue was not the absence of a route.

The hostname was pointing to the wrong destination.

I corrected `/etc/hosts` so that:

```text
app1.local → 172.23.210.163
```

and verified the application again.

---

## Commands I Practised

| Command | Purpose |
|---|---|
| `ip route` | Display the Linux routing table |
| `ip addr` | Display interfaces and IP addresses |
| `ip link` | Inspect network interfaces |
| `ping <destination>` | Test IP reachability |
| `ip route add ...` | Add a route |
| `cat /proc/sys/net/ipv4/ip_forward` | Check whether IPv4 forwarding is enabled |
| `getent hosts <hostname>` | Check what IP a hostname resolves to |
| `curl <URL>` | Test application connectivity |

---

## Key Lessons

From learning about routing and gateways, I learned that:

- Routing determines how packets should reach a destination.
- `ip route` displays the Linux routing table.
- Directly connected networks have routes associated with local interfaces.
- The default route is used when there is no more specific matching route.
- A default gateway is the next hop used by the default route.
- Not every connection uses the default gateway.
- Traffic to my own local interface does not need to travel through the default gateway.
- A machine can have a valid route to the wrong destination IP.
- Therefore, having a route does not prove that name resolution returned the correct destination.
- IP forwarding is important when a Linux system needs to forward packets between networks.

The troubleshooting lesson I took from this is:

> Do not assume that a connection failure is a routing problem. First determine the destination IP, then use the routing table to understand how Linux intends to reach that destination.
