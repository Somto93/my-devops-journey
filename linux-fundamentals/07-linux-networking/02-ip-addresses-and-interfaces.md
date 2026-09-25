# IP Addresses and Network Interfaces

This section documents what I learned about Linux network interfaces, IP addresses, loopback addresses, and how they relate to application connectivity.

## 1. What Is a Network Interface?

A network interface is a point through which a system communicates with a network.

I can view the network interfaces configured on my Linux system using:

```bash
ip addr
```

During my networking lab, two important interfaces were:

```text
lo
eth0
```

They serve different purposes.

---

## 2. The Loopback Interface — `lo`

My `ip addr` output included the loopback interface:

```text
lo
```

with the IPv4 address:

```text
127.0.0.1
```

The loopback interface allows the machine to communicate with itself.

The address:

```text
127.0.0.1
```

is commonly associated with:

```text
localhost
```

So when I ran:

```bash
curl http://127.0.0.1:5000
```

I was connecting to a service on my own machine through the loopback interface.

A useful mental model is:

```text
127.0.0.1
    ↓
Loopback interface (lo)
    ↓
My own machine
```

---

## 3. The `eth0` Interface

My WSL environment also had an interface called:

```text
eth0
```

During the lab, `eth0` had the IPv4 address:

```text
172.23.210.163
```

I found this using:

```bash
ip addr
```

The output showed an address similar to:

```text
inet 172.23.210.163/20
```

This told me that `172.23.210.163` was assigned to the `eth0` interface.

I could therefore test my Flask application directly using:

```bash
curl http://172.23.210.163:5000
```

when the application was listening on the appropriate interface.

---

## 4. `lo` vs `eth0`

One of the most useful things I learned was the difference between the loopback interface and a network-facing interface.

```text
lo
└── 127.0.0.1
    └── Communication with my own machine through loopback

eth0
└── 172.23.210.163
    └── Network interface used for network communication
```

This distinction became very important when troubleshooting application binding.

---

## 5. IP Address vs Network Interface

I learned not to treat an IP address and a network interface as exactly the same thing.

For example:

```text
eth0
```

is the interface.

While:

```text
172.23.210.163
```

is an IP address assigned to that interface.

So I can think about it as:

```text
Interface
    ↓
eth0
    ↓
Assigned IP
    ↓
172.23.210.163
```

A network interface can have one or more addresses associated with it.

---

## 6. Understanding `ip addr`

The command:

```bash
ip addr
```

provides information about the network interfaces configured on a Linux machine.

During my lab, I used it to answer:

> What IP address is actually assigned to this machine?

This was especially useful when troubleshooting `app1.local`.

For example, if:

```bash
getent hosts app1.local
```

returned:

```text
172.23.210.200 app1.local
```

but:

```bash
ip addr
```

showed:

```text
eth0 → 172.23.210.163
```

I could compare the two pieces of evidence and see that the hostname was resolving to a different IP.

This helped me identify an incorrect `/etc/hosts` mapping during one of my troubleshooting exercises.

---

## 7. Interface State

The output of `ip addr` also provides information about the state of an interface.

For example, I saw `eth0` marked as:

```text
UP
```

This indicates that the interface is enabled.

However, an interface being `UP` does not automatically prove that an application is reachable.

There could still be problems involving:

```text
Name resolution
Routing
Port
Application binding
Application process
```

This is why I should combine `ip addr` with other troubleshooting commands instead of relying on one command alone.

---

## 8. Understanding CIDR Notation

My `eth0` address appeared as:

```text
172.23.210.163/20
```

The `/20` is CIDR notation.

It represents the network prefix length.

In my routing table, I saw the directly connected network represented as:

```text
172.23.208.0/20
```

with my source address:

```text
172.23.210.163
```

This helped me understand why an address such as:

```text
172.23.210.200
```

could still fall within the directly connected network even though it was not the IP address assigned to my machine.

That became important during my wrong-IP troubleshooting exercise.

The problem was not necessarily that Linux had no route to `172.23.210.200`.

The problem was that:

```text
app1.local
```

had been mapped to the wrong destination IP.

---

## 9. Testing My Own Interface Address

When my Flask application was configured with:

```python
app.run(host="0.0.0.0", port=5000)
```

I could access it using:

```bash
curl http://127.0.0.1:5000
```

and:

```bash
curl http://172.23.210.163:5000
```

This helped me understand what:

```text
0.0.0.0:5000
```

means when shown as a listening socket.

It means the application is listening on port `5000` across the machine's IPv4 interfaces.

---

## 10. Application Binding and Interfaces

One of my troubleshooting exercises demonstrated why network interfaces matter to applications.

I deliberately configured Flask as:

```python
app.run(host="127.0.0.1", port=5000)
```

Then I checked:

```bash
ss -lntp | grep 5000
```

and saw:

```text
127.0.0.1:5000
```

The application worked when I used:

```bash
curl http://127.0.0.1:5000
```

but it did not work through:

```text
app1.local
```

because `app1.local` resolved to my `eth0` address:

```text
172.23.210.163
```

The application was not listening there.

I fixed the issue by changing:

```python
app.run(host="127.0.0.1", port=5000)
```

to:

```python
app.run(host="0.0.0.0", port=5000)
```

This taught me that:

> Having the correct IP and the correct port does not guarantee connectivity. The application must also be listening on an appropriate local address/interface.

---

## 11. `ip addr` vs `ip route`

I initially needed to separate these two commands because they answer different questions.

### `ip addr`

```bash
ip addr
```

answers:

> What network interfaces and IP addresses does this machine have?

For example:

```text
eth0 → 172.23.210.163
```

### `ip route`

```bash
ip route
```

answers:

> How will Linux send traffic towards a destination?

For example:

```text
default via 172.23.208.1 dev eth0
```

These commands are related, but they do not provide the same information.

---

## 12. `ip addr` vs Name Resolution

Another distinction I learned was between:

```bash
ip addr
```

and:

```bash
getent hosts app1.local
```

`ip addr` tells me about addresses configured on my own machine.

`getent hosts` tells me what address a hostname resolves to.

For troubleshooting, I can compare them:

```text
getent hosts app1.local
            ↓
What IP does the name resolve to?

ip addr
            ↓
What IP is actually assigned to my machine?
```

For example:

```text
app1.local → 172.23.210.163
eth0       → 172.23.210.163
```

means the hostname is pointing to the expected interface address.

But:

```text
app1.local → 172.23.210.200
eth0       → 172.23.210.163
```

would make me investigate why the hostname is pointing somewhere else.

---

## Commands I Practised

| Command | What I use it for |
|---|---|
| `ip addr` | View interfaces and assigned IP addresses |
| `ip link` | View and manage network interfaces |
| `getent hosts <hostname>` | Determine what IP a hostname resolves to |
| `ip route` | View the routing table |
| `ping <IP>` | Test IP reachability |
| `curl http://<IP>:<PORT>` | Test application connectivity directly using an IP |
| `ss -lntp` | Inspect TCP listeners, ports, and binding addresses |

---

## My Troubleshooting Approach

When investigating an IP-related issue, I can now ask separate questions:

```text
1. What IP does the hostname resolve to?
              ↓
       getent hosts

2. What IP does my machine actually have?
              ↓
          ip addr

3. Does Linux know how to reach the destination?
              ↓
          ip route

4. Is the application listening?
              ↓
          ss -lntp

5. Can I connect to the application?
              ↓
            curl
```

This prevents me from confusing name resolution, IP addressing, routing, and application problems.

---

## Key Lessons

From working with IP addresses and interfaces, I learned that:

- `lo` is the loopback interface.
- `127.0.0.1` refers back to the local machine through loopback.
- `eth0` is a network interface in my WSL environment.
- My lab's `eth0` IPv4 address was `172.23.210.163`.
- An interface and an IP address are related but are not the same thing.
- `ip addr` shows addresses configured on my machine.
- `getent hosts` shows what IP a hostname resolves to.
- `ip route` shows how Linux determines where packets should go.
- An interface being `UP` does not mean the application itself is healthy.
- Application binding determines which local addresses can accept connections for a service.

The most important lesson is to compare evidence from different networking layers instead of assuming that every connectivity problem is an IP problem.
