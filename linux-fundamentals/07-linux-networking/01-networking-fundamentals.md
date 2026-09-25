# Networking Fundamentals

This section covers the basic networking concepts I learned and how they relate to troubleshooting applications in a DevOps environment.

## What Is Networking?

Networking allows devices and applications to communicate with each other.

During my learning, I found it useful to separate networking into different concepts rather than treating "the network" as one thing.

A simple way I now think about application communication is:

```text
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
Application
```

Each part answers a different question.

---

## 1. Hostname

A hostname gives a human-readable name to a machine or service.

For example, in my lab I used:

```text
app1.local
```

Instead of remembering an IP address, I could access the application using:

```text
http://app1.local:5000
```

However, the computer still needs to determine which IP address belongs to `app1.local`.

That is where name resolution comes in.

---

## 2. Name Resolution

Name resolution translates a hostname into an IP address.

In my lab:

```text
app1.local
      ↓
172.23.210.163
```

I created this mapping using `/etc/hosts`.

I could check the result with:

```bash
getent hosts app1.local
```

An important lesson for me was:

> DNS/name resolution does not carry the application traffic. It helps the system determine the IP address associated with a name.

---

## 3. IP Address

An IP address identifies a network interface.

For example, my WSL `eth0` interface had the address:

```text
172.23.210.163
```

I inspected my network interfaces using:

```bash
ip addr
```

I also learned that:

```text
127.0.0.1
```

is the loopback address.

It refers back to the local machine and is commonly associated with:

```text
localhost
```

So:

```text
127.0.0.1 = this machine through the loopback interface
```

while:

```text
172.23.210.163 = the IP assigned to my eth0 interface
```

---

## 4. Routing

Knowing the destination IP does not by itself explain how packets should reach that destination.

Linux uses its routing table to determine where packets should go.

I inspected the routing table using:

```bash
ip route
```

In my lab, I saw:

```text
default via 172.23.208.1 dev eth0
172.23.208.0/20 dev eth0 scope link src 172.23.210.163
```

The directly connected route:

```text
172.23.208.0/20 dev eth0
```

tells Linux that destinations belonging to this network can be reached directly through `eth0`.

The default route:

```text
default via 172.23.208.1 dev eth0
```

is used when there is no more specific matching route.

For example, if I wanted to communicate with:

```text
8.8.8.8
```

Linux would check its routing table.

Because there is no more specific route for `8.8.8.8`, it would use:

```text
default via 172.23.208.1 dev eth0
```

This helped me understand that routing answers the question:

> How should my machine send packets towards a particular destination?

---

## 5. Default Gateway

The default gateway is the next-hop router used by the default route.

In my lab:

```text
default via 172.23.208.1 dev eth0
```

means that traffic using the default route is sent towards:

```text
172.23.208.1
```

through:

```text
eth0
```

One important distinction I learned is that the default gateway is not involved in every connection.

For example, when I accessed my own `eth0` IP:

```bash
curl http://172.23.210.163:5000
```

the request did not need to travel through the default gateway because `172.23.210.163` is an address assigned to my own machine.

This helped me separate two concepts:

```text
IP Address
→ Where is the destination?

Routing
→ How do I reach that destination?

Default Gateway
→ Where do I send traffic when there is no more specific route?
```

---

## 6. Ports

An IP address identifies a network interface, while a port helps identify the service endpoint on that machine.

For example:

```text
172.23.210.163:5000
                 ↑
                Port
```

My Flask application used:

```text
Port 5000
```

Another application on the same machine could listen on another port such as:

```text
8080
```

This means:

```text
172.23.210.163:5000
```

and:

```text
172.23.210.163:8080
```

can lead to different services even though they use the same IP address.

I inspected listening TCP ports using:

```bash
ss -lntp
```

For example:

```text
LISTEN ... 0.0.0.0:5000 ... python3
```

told me that a Python process was listening on TCP port `5000`.

I learned not to think of a port as the address of the machine.

Instead:

```text
IP Address = identifies the network interface/destination

Port = identifies the service endpoint
```

---

## 7. Application Binding

I learned that knowing the correct port is not enough.

The address an application is listening on also matters.

For example:

```text
127.0.0.1:5000
```

means the application is listening on port `5000` through the loopback interface only.

In contrast:

```text
0.0.0.0:5000
```

means the application is listening on port `5000` on all IPv4 interfaces.

This became important during my Flask networking lab.

When Flask was configured as:

```python
app.run(host="127.0.0.1", port=5000)
```

this worked:

```bash
curl http://127.0.0.1:5000
```

However:

```bash
curl http://app1.local:5000
```

failed because `app1.local` resolved to:

```text
172.23.210.163
```

while Flask was only listening on:

```text
127.0.0.1:5000
```

I confirmed the problem using:

```bash
ss -lntp | grep 5000
```

which showed:

```text
127.0.0.1:5000
```

I then changed Flask from:

```python
app.run(host="127.0.0.1", port=5000)
```

to:

```python
app.run(host="0.0.0.0", port=5000)
```

After restarting the application, `ss` showed:

```text
0.0.0.0:5000
```

and I could access the application through `app1.local`.

This taught me an important distinction:

```text
127.0.0.1
→ Listen only through localhost/loopback

0.0.0.0
→ Listen on all IPv4 interfaces
```

---

## Putting Everything Together

When I access:

```text
http://app1.local:5000
```

I now think about what happens in stages:

```text
app1.local
     │
     │ Name Resolution
     ▼
172.23.210.163
     │
     │ Routing / Reachability
     ▼
Destination Interface
     │
     │ TCP Port
     ▼
5000
     │
     │ Application Binding
     ▼
0.0.0.0:5000
     │
     │ Listening Process
     ▼
Flask Application
```

This model makes troubleshooting easier because instead of simply saying:

> "The network is not working."

I can investigate which part of the communication path is actually failing.

---

## Key Commands

| Command | Question it helps me answer |
|---|---|
| `ip addr` | What network interfaces and IP addresses does this machine have? |
| `ip route` | How will Linux route packets towards a destination? |
| `getent hosts app1.local` | What IP does this hostname resolve to? |
| `ping <host>` | Can I test IP reachability to the destination? |
| `ss -lntp` | What TCP services are listening, on which addresses and ports? |
| `curl <URL>` | Can I connect to the application and receive a response? |
| `pgrep -af <name>` | Is a particular application process running? |
| `ps -fp <PID>` | What process or command belongs to a particular PID? |

---

## Key Lesson

The biggest lesson I took from networking fundamentals is that these concepts have different responsibilities:

- **Hostname** — provides a human-readable name.
- **Name resolution** — translates the name into an IP address.
- **IP address** — identifies a network interface.
- **Routing** — determines how packets should reach a destination.
- **Default gateway** — provides the next hop when the default route is used.
- **Port** — identifies a service endpoint.
- **Binding** — determines which local addresses/interfaces an application listens on.

When troubleshooting, I should not immediately assume that an unavailable application means "the network is down."

Instead, I can investigate the communication path one layer at a time and use evidence to identify where the failure is occurring.
