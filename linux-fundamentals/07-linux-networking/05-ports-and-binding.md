# Ports and Application Binding

This section documents what I learned about ports, TCP listeners, application binding, and how to troubleshoot an application that is running but cannot be reached through the expected address or port.

## 1. What Is a Port?

An IP address helps identify a network interface/destination.

A port helps identify the service endpoint that I want to communicate with on that machine.

For example:

```text
172.23.210.163:5000
│              │
│              └── Port
│
└── IP Address
```

In my Flask networking lab, the application normally listened on:

```text
Port 5000
```

So I could access it using:

```bash
curl http://app1.local:5000
```

or directly through the IP:

```bash
curl http://172.23.210.163:5000
```

---

## 2. Same Machine, Different Ports

A machine can run multiple network services.

Different services can listen on different ports.

For example:

```text
172.23.210.163:5000
172.23.210.163:8080
```

Both use the same IP address, but they represent different service endpoints.

This helped me understand that a port is not the address of the machine itself.

A useful distinction is:

```text
IP Address
→ Where is the destination/interface?

Port
→ Which service endpoint am I trying to reach?
```

---

## 3. Inspecting Listening Ports

I used:

```bash
ss -lntp
```

to inspect TCP listeners.

The options mean:

```text
-l → show listening sockets
-n → show numeric addresses and ports
-t → show TCP sockets
-p → show associated processes when available
```

A healthy result for my Flask application looked similar to:

```text
LISTEN 0 128 0.0.0.0:5000 0.0.0.0:* users:(("python3",pid=3056,fd=3))
```

This gave me several pieces of information:

```text
LISTEN
→ A service is waiting for connections.

0.0.0.0
→ Listening across IPv4 interfaces.

5000
→ The listening port.

python3
→ The process associated with the listener.

pid=3056
→ Process ID.
```

---

## 4. Why Checking Only the Port Is Not Enough

Initially, it was easy to think:

> If port 5000 appears in `ss`, then everything must be correct.

However, I learned that I also need to inspect the address before the port.

For example:

```text
127.0.0.1:5000
```

and:

```text
0.0.0.0:5000
```

both use port `5000`, but they do not have the same binding behaviour.

Therefore, when using:

```bash
ss -lntp
```

I should inspect both:

```text
Listening Address + Port
```

not just the port number.

---

## 5. Understanding Application Binding

Application binding determines which local address or addresses an application listens on.

In Flask, I controlled this using:

```python
app.run(host="0.0.0.0", port=5000)
```

The `host` value controls the listening address.

The `port` value controls the listening port.

---

## 6. Binding to `127.0.0.1`

When I configured Flask as:

```python
app.run(host="127.0.0.1", port=5000)
```

and checked:

```bash
ss -lntp | grep 5000
```

I saw:

```text
127.0.0.1:5000
```

This meant Flask was listening through the loopback interface.

I tested:

```bash
curl http://127.0.0.1:5000
```

and the application worked.

However:

```bash
curl http://app1.local:5000
```

failed.

This happened because:

```text
app1.local
     ↓
172.23.210.163
     ↓
eth0
```

while Flask was listening only on:

```text
127.0.0.1:5000
```

The port was correct, but the binding address was not appropriate for accessing the application through the `eth0` address.

---

## 7. Binding to `0.0.0.0`

I changed Flask to:

```python
app.run(host="0.0.0.0", port=5000)
```

Then:

```bash
ss -lntp | grep 5000
```

showed:

```text
0.0.0.0:5000
```

This means the application is listening on port `5000` across the machine's IPv4 interfaces.

I could then access the application using:

```bash
curl http://127.0.0.1:5000
```

and:

```bash
curl http://172.23.210.163:5000
```

and through my configured hostname:

```bash
curl http://app1.local:5000
```

---

## 8. `0.0.0.0` Is Not a Default Gateway

One distinction I learned during this lab was not to describe:

```text
0.0.0.0
```

as the "default."

In the context of application binding:

```text
0.0.0.0
→ Listen on all IPv4 interfaces
```

This is different from a default route such as:

```text
default via 172.23.208.1 dev eth0
```

which is a routing concept.

So:

```text
0.0.0.0:5000
→ Application binding/listening

default via 172.23.208.1
→ Routing/default gateway
```

These concepts should not be confused.

---

# Practical Incident 1 — Application on the Wrong Port

One of my troubleshooting exercises involved deliberately changing the Flask application from:

```python
app.run(host="0.0.0.0", port=5000)
```

to:

```python
app.run(host="0.0.0.0", port=8080)
```

The application was still running, but users expected it at:

```text
app1.local:5000
```

## Symptom

I tested:

```bash
curl --connect-timeout 3 http://app1.local:5000
```

and received a connection failure.

Instead of immediately changing the application, I investigated the listener.

## Investigation

I ran:

```bash
ss -lntp | grep 5000
```

There was no output.

This told me:

> Nothing was listening on TCP port 5000.

However, that did not yet prove that the application was completely stopped.

I then checked all TCP listeners:

```bash
ss -lntp
```

and discovered:

```text
0.0.0.0:8080
```

with a Python process associated with it.

This gave me a new hypothesis:

> The application might be running, but on port 8080 instead of port 5000.

## Testing the Hypothesis

I tested:

```bash
curl http://app1.local:8080
```

The application responded successfully.

This confirmed that:

```text
DNS             → Working
Destination IP  → Correct
Application     → Running
Binding         → Appropriate
Port 5000       → Wrong expectation
Port 8080       → Actual listener
```

## Root Cause

The Flask application had been configured to listen on:

```text
8080
```

instead of the expected:

```text
5000
```

## Fix

I restored:

```python
app.run(host="0.0.0.0", port=5000)
```

and restarted the application.

I then verified:

```bash
ss -lntp | grep 5000
```

and:

```bash
curl http://app1.local:5000/health
```

## Lesson Learned

A connection failure on a particular port does not automatically mean that the entire application is down.

I should check which ports are actually listening.

---

# Practical Incident 2 — Correct Port, Wrong Binding

Another exercise demonstrated that even the correct port can still be inaccessible.

I deliberately changed:

```python
app.run(host="0.0.0.0", port=5000)
```

to:

```python
app.run(host="127.0.0.1", port=5000)
```

## Symptom

I ran:

```bash
curl --connect-timeout 3 http://app1.local:5000
```

and the connection failed.

Because the request used port `5000`, I needed to determine whether something was actually listening there.

## Investigation

I ran:

```bash
ss -lntp | grep 5000
```

and saw:

```text
127.0.0.1:5000
```

This was important.

The application was:

- running
- using the correct port

but it was listening only through loopback.

Meanwhile:

```text
app1.local
```

resolved to:

```text
172.23.210.163
```

which was assigned to `eth0`.

The communication paths therefore looked like:

```text
127.0.0.1:5000
       ↓
Flask listener
       ↓
Works
```

but:

```text
172.23.210.163:5000
       ↓
No Flask listener on that address
       ↓
Fails
```

## Testing the Hypothesis

Before changing anything, I tested:

```bash
curl http://127.0.0.1:5000
```

The application responded successfully.

This was strong evidence that:

- Flask was running.
- Port `5000` was correct.
- The problem was not the application process itself.
- The problem was the listening/binding address.

## Root Cause

Flask was bound to:

```text
127.0.0.1:5000
```

instead of listening across the required IPv4 interfaces.

## Fix

I changed:

```python
app.run(host="127.0.0.1", port=5000)
```

back to:

```python
app.run(host="0.0.0.0", port=5000)
```

After restarting Flask, I verified:

```bash
ss -lntp | grep 5000
```

and expected:

```text
0.0.0.0:5000
```

I then tested:

```bash
curl http://app1.local:5000/health
```

and confirmed the application was healthy.

## Lesson Learned

This incident taught me:

> A correct port does not necessarily mean the service is accessible through every local network interface.

When checking a listener, I should inspect both:

```text
Address + Port
```

---

## Connection Failure vs Name-Resolution Failure

The lab also helped me recognise that different errors can point me towards different stages of investigation.

For example:

```text
Could not resolve host
```

suggests I should investigate name resolution.

An immediate connection failure after the hostname has resolved can lead me to investigate things such as:

```text
Listener
Port
Binding
Application process
```

A timeout may lead me to investigate possibilities such as:

```text
Wrong destination
Network reachability
Dropped traffic
Firewall
Routing
```

These are troubleshooting clues rather than absolute proof of the root cause.

I still need to collect evidence.

---

## Checking Which Process Owns a Port

During another investigation, I saw:

```text
0.0.0.0:8080
```

associated with:

```text
python
PID 2018
```

I did not immediately assume this was my networking application.

I used:

```bash
ps -fp 2018
```

to inspect the process.

The command showed that the process belonged to another project:

```text
/home/somto/linux-services-lab/
```

rather than:

```text
/home/somto/networking-lab/
```

This taught me another important troubleshooting principle:

> Do not assume that a process using a familiar port or programming language is the application I am investigating.

Verify the process.

---

## Useful Commands

| Command | Purpose |
|---|---|
| `ss -lntp` | Show listening TCP sockets and associated processes |
| `ss -lntp \| grep 5000` | Check specifically for a listener on port 5000 |
| `curl http://127.0.0.1:5000` | Test the loopback listener |
| `curl http://<IP>:5000` | Test the service through a specific IP |
| `curl http://app1.local:5000` | Test through hostname resolution |
| `curl --connect-timeout 3 <URL>` | Limit how long curl waits while establishing the connection |
| `ps -fp <PID>` | Inspect a specific process |
| `pgrep -af <name>` | Search running processes by full command line |

---

## My Troubleshooting Flow

When an application cannot be reached on an expected port, I can work through:

```text
curl application
      ↓
What error do I receive?
      ↓
Check listener
ss -lntp
      ↓
Is expected port listening?
     / \
   Yes  No
    |    |
    |    └── Investigate application/process
    |
    ↓
What address is it listening on?
      ↓
127.0.0.1?
0.0.0.0?
Specific IP?
      ↓
Compare with destination IP
      ↓
Test directly
      ↓
Fix
      ↓
Verify with ss and curl
```

---

## Key Lessons

From learning about ports and application binding, I learned that:

- An IP address and a port have different responsibilities.
- A machine can run multiple services on different ports.
- `ss -lntp` shows listening TCP sockets.
- I should inspect both the listening address and the port.
- `127.0.0.1:5000` means the service is listening through loopback.
- `0.0.0.0:5000` means the service is listening on port 5000 across IPv4 interfaces.
- `0.0.0.0` in application binding should not be confused with the default gateway.
- An application can be running successfully but on the wrong port.
- An application can be on the correct port but bound to the wrong address.
- I should verify which process owns a listener instead of assuming.
- After fixing an issue, I should verify both the listener and the application endpoint.

My main troubleshooting lesson is:

> Do not stop at "the port is open." Check which address the service is bound to, which process owns the listener, and whether the endpoint can actually be reached.
