# Linux Network Troubleshooting

This section documents the troubleshooting approach I developed while working through my Linux networking lab.

The main lesson I learned was that when an application is reported as "unavailable," I should not immediately restart it or assume that the network is down.

Instead, I should collect evidence and identify which part of the communication path is failing.

---

## 1. My Troubleshooting Mental Model

When accessing an application such as:

```text
http://app1.local:5000
```

I think about the request as a chain:

```text
Hostname
   ↓
Name Resolution
   ↓
Destination IP
   ↓
Routing / Reachability
   ↓
Port
   ↓
Application Binding
   ↓
Listening Process
   ↓
Application Response
```

A failure can occur at any of these stages.

Therefore, "the application is unavailable" is only a symptom.

My job during troubleshooting is to determine where the failure is occurring.

---

## 2. Inspect First, Change Second

One of the most important habits I developed during this lab was:

> Inspect first, change second.

For example, if a user reports:

```text
app1.local is unavailable
```

I should not immediately run:

```bash
python3 app1.py
```

or restart the application.

Instead, I first try to reproduce the problem:

```bash
curl --connect-timeout 3 http://app1.local:5000
```

The result gives me evidence that helps determine what to investigate next.

---

## 3. Understanding Different Failure Symptoms

Different errors can provide useful clues.

### Name Resolution Failure

For example:

```text
Could not resolve host: app1.local
```

This tells me that the system could not translate the hostname into an address.

I would investigate name resolution using commands such as:

```bash
getent hosts app1.local
```

and inspect:

```text
/etc/hosts
/etc/nsswitch.conf
/etc/resolv.conf
```

---

### Immediate Connection Failure

An error such as:

```text
Failed to connect to app1.local port 5000
```

may lead me to investigate whether anything is listening on the expected port.

For example:

```bash
ss -lntp
```

I should not treat the error itself as absolute proof of the root cause.

It provides a direction for further investigation.

---

### Connection Timeout

A timeout can lead me to investigate possibilities such as:

```text
Wrong destination IP
Network reachability
Routing
Dropped traffic
Firewall
```

Again, the timeout is a clue rather than proof of one specific problem.

---

# Incident 1 — Incorrect Hostname-to-IP Mapping

## Symptom

My Flask application was expected to be available at:

```text
http://app1.local:5000
```

I deliberately changed the `/etc/hosts` mapping from:

```text
172.23.210.163 app1.local
```

to:

```text
172.23.210.200 app1.local
```

I then ran:

```bash
curl --connect-timeout 3 http://app1.local:5000
```

The request timed out.

---

## Investigation

I checked name resolution:

```bash
getent hosts app1.local
```

and found:

```text
172.23.210.200 app1.local
```

I then checked my machine's addresses:

```bash
ip addr
```

My `eth0` address was:

```text
172.23.210.163
```

So I had:

```text
app1.local → 172.23.210.200

eth0       → 172.23.210.163
```

I also checked:

```bash
ip route
```

and saw:

```text
172.23.208.0/20 dev eth0
```

This showed that Linux still had a route covering the incorrect destination.

Therefore, the problem was not simply that Linux had no route.

The hostname was pointing to the wrong destination.

---

## Root Cause

Incorrect local hostname-to-IP mapping in:

```text
/etc/hosts
```

---

## Fix

I restored:

```text
172.23.210.163 app1.local
```

and verified:

```bash
getent hosts app1.local
```

Then:

```bash
curl http://app1.local:5000/health
```

returned:

```json
{"status":"healthy"}
```

---

## Lesson

Successful name resolution does not necessarily mean that the resolved destination is correct.

I should verify:

```text
What does the name resolve to?

AND

Is that actually the destination I expect?
```

---

# Incident 2 — Application Listening on the Wrong Port

## Symptom

The application was expected on:

```text
app1.local:5000
```

but I deliberately configured Flask to listen on:

```text
8080
```

I ran:

```bash
curl --connect-timeout 3 http://app1.local:5000
```

and the connection failed.

---

## Investigation

I checked:

```bash
ss -lntp | grep 5000
```

There was no listener on port `5000`.

Instead of immediately concluding that the application had stopped, I checked all listeners:

```bash
ss -lntp
```

and found a Python process listening on:

```text
0.0.0.0:8080
```

I then tested:

```bash
curl http://app1.local:8080
```

and confirmed that the application responded.

---

## Root Cause

The application was running on:

```text
8080
```

instead of the expected:

```text
5000
```

---

## Fix

I restored:

```python
app.run(host="0.0.0.0", port=5000)
```

and restarted Flask.

Then I verified:

```bash
ss -lntp | grep 5000
```

and:

```bash
curl http://app1.local:5000/health
```

---

## Lesson

No listener on the expected port does not automatically mean the entire application is stopped.

The application may be listening somewhere else.

---

# Incident 3 — Correct Port, Wrong Binding

## Symptom

I deliberately changed Flask from:

```python
app.run(host="0.0.0.0", port=5000)
```

to:

```python
app.run(host="127.0.0.1", port=5000)
```

Then:

```bash
curl --connect-timeout 3 http://app1.local:5000
```

failed.

---

## Investigation

I checked:

```bash
ss -lntp | grep 5000
```

and found:

```text
127.0.0.1:5000
```

The port was correct.

However, the application was listening only through loopback.

Meanwhile:

```text
app1.local
```

resolved to:

```text
172.23.210.163
```

I tested my hypothesis using:

```bash
curl http://127.0.0.1:5000
```

and the application worked.

This proved that Flask was running and port `5000` was correct.

The problem was the binding address.

---

## Root Cause

The application was bound to:

```text
127.0.0.1:5000
```

instead of listening on the required IPv4 interfaces.

---

## Fix

I restored:

```python
app.run(host="0.0.0.0", port=5000)
```

Then I verified:

```bash
ss -lntp | grep 5000
```

and:

```bash
curl http://app1.local:5000/health
```

---

## Lesson

When inspecting a listener, I should check:

```text
Address + Port
```

not just:

```text
Port
```

---

# Incident 4 — Application Process Stopped

This incident helped me connect Linux networking troubleshooting with Linux process and service management.

## Incident Report

The simulated ticket was:

> Users report that `app1.local:5000` is unavailable. It was working earlier.

I did not initially know that the Flask process had been stopped.

---

## Step 1 — Reproduce the Problem

I started with:

```bash
curl --connect-timeout 3 http://app1.local:5000
```

The connection failed immediately.

This confirmed that I could reproduce the reported problem.

---

## Step 2 — Check the Listener

I ran:

```bash
ss -lntp
```

There was nothing listening on:

```text
5000
```

However, I noticed:

```text
0.0.0.0:8080
```

with a Python process:

```text
PID 2018
```

I did not assume this was my Flask networking application.

---

## Step 3 — Identify the Other Process

I investigated PID `2018` using:

```bash
ps -fp 2018
```

The command showed that the process belonged to another project under:

```text
/home/somto/linux-services-lab/
```

My networking application was located under:

```text
/home/somto/networking-lab/
```

Therefore, the process listening on `8080` was unrelated to the incident.

This was important because I learned not to assume that every Python process belongs to the application I am troubleshooting.

---

## Step 4 — Check Whether `app1.py` Is Running

I used:

```bash
pgrep -af app1.py
```

There was no output.

At this point I had multiple pieces of evidence:

```text
curl
   ↓
Connection failed

ss
   ↓
Nothing listening on :5000

ps
   ↓
The Python process on :8080 belongs to another application

pgrep
   ↓
No app1.py process
```

This gave me strong evidence that my application process was not running.

---

## Root Cause

The `app1.py` process had stopped.

Because the application process was not running, nothing was listening on:

```text
0.0.0.0:5000
```

---

## Fix

Because I was running the application manually in the lab, I restored it using:

```bash
python3 app1.py
```

---

## Step 5 — Verify the Fix

Starting the application was not enough.

I first verified the listener:

```bash
ss -lntp | grep 5000
```

I expected:

```text
0.0.0.0:5000
```

Then I tested the actual application health endpoint:

```bash
curl http://app1.local:5000/health
```

and expected:

```json
{"status":"healthy"}
```

This completed the troubleshooting process.

---

# Process Troubleshooting Commands

During the stopped-application incident, I learned several useful process commands.

## `pgrep`

I used:

```bash
pgrep -af app1.py
```

The options helped search the full command line and display it.

This was useful because the actual process may appear as:

```text
python3
```

while:

```text
app1.py
```

appears in the process command line.

---

## `ps`

I used:

```bash
ps -fp <PID>
```

to inspect a specific process.

For example:

```bash
ps -fp 2018
```

helped me determine that the Python process on port `8080` belonged to another project.

---

## `lsof`

Another useful command for inspecting network listeners is:

```bash
sudo lsof -i -P -n | grep LISTEN
```

This can help identify processes listening on network ports.

---

# Connecting Networking With systemd

The lab application was started manually using:

```bash
python3 app1.py
```

However, I learned that this would not be ideal for a production service.

If the application crashed at night, I would not want the normal recovery method to depend on someone manually logging in and running:

```bash
python3 app1.py
```

A Linux service manager such as `systemd` can manage long-running applications.

---

## Checking Service Status

For a systemd-managed application, I could start my investigation with:

```bash
sudo systemctl status app1
```

This can help determine whether the service is:

```text
active
inactive
failed
```

---

## Investigating Logs

I could inspect the service logs using:

```bash
sudo journalctl -u app1
```

This can help answer:

> Why did the service stop or fail?

This is different from simply restarting the service without understanding what happened.

---

## Restarting a Service

After identifying and fixing the problem, I could use:

```bash
sudo systemctl restart app1
```

or start an inactive service when appropriate:

```bash
sudo systemctl start app1
```

Then verify:

```bash
sudo systemctl status app1
```

and finally test the application:

```bash
curl http://app1.local:5000/health
```

---

## When to Use `daemon-reload`

I also learned that:

```bash
sudo systemctl daemon-reload
```

is not something I need to run after every application failure.

It is needed when systemd needs to reload changed unit-file configuration.

For example, if I modify the service unit file, I may use:

```bash
sudo systemctl daemon-reload
sudo systemctl restart app1
```

If I did not change the unit configuration, `daemon-reload` is generally not part of a normal application restart.

---

## Automatic Restart

A systemd service can also be configured to restart after certain failures.

For example:

```ini
[Service]
ExecStart=/home/somto/networking-lab/venv/bin/python /home/somto/networking-lab/app1.py
Restart=on-failure
RestartSec=5
```

This connects my Linux Services learning with my Linux Networking learning.

The application can be:

```text
Managed by systemd
       ↓
Listening on an IP/interface
       ↓
Listening on a port
       ↓
Reached through the network
```

---

# My Overall Troubleshooting Workflow

After completing these exercises, my troubleshooting approach is:

```text
Application reported unavailable
              ↓
1. Reproduce the problem
              ↓
            curl
              ↓
2. Check name resolution if relevant
              ↓
         getent hosts
              ↓
3. Check local IP/interface information
              ↓
           ip addr
              ↓
4. Check routing when relevant
              ↓
           ip route
              ↓
5. Check listening sockets
              ↓
          ss -lntp
              ↓
6. Check listening address + port
              ↓
7. Identify the process
              ↓
       ps / pgrep / lsof
              ↓
8. Investigate application/service state
              ↓
 systemctl / journalctl when applicable
              ↓
9. Identify root cause
              ↓
10. Make the smallest appropriate fix
              ↓
11. Verify listener/service
              ↓
12. Test the application again
              ↓
             curl
```

This is not a rigid checklist where every command must always be run.

The error and evidence determine which command I should use next.

---

# Troubleshooting Command Cheat Sheet

| Command | Question I am trying to answer |
|---|---|
| `curl <URL>` | Can I connect to the application and receive a response? |
| `getent hosts <hostname>` | What IP does this hostname resolve to? |
| `ip addr` | What interfaces and IP addresses does this machine have? |
| `ip route` | How would Linux route traffic to the destination? |
| `ping <host>` | Can I test IP reachability? |
| `ss -lntp` | What TCP services are listening, where, and on which ports? |
| `pgrep -af <name>` | Is the application process running? |
| `ps -fp <PID>` | What exactly is this process? |
| `sudo lsof -i -P -n \| grep LISTEN` | Which processes are listening on network ports? |
| `systemctl status <service>` | What is the state of a systemd service? |
| `journalctl -u <service>` | What has the service logged? |

---

# What I Learned From the Four Incidents

The four failures looked similar from the user's perspective:

```text
"The application is unavailable."
```

But they had completely different causes.

| Incident | Root Cause | Main Evidence |
|---|---|---|
| Wrong IP mapping | `app1.local` pointed to the wrong IP | `getent hosts` + `ip addr` |
| Wrong port | Flask was listening on `8080` instead of `5000` | `ss -lntp` |
| Wrong binding | Flask was listening only on `127.0.0.1:5000` | `ss` + successful localhost `curl` |
| Process stopped | `app1.py` was not running | `ss` + `pgrep` |

This showed me why troubleshooting should be based on evidence rather than assumptions.

---

# Final Key Lessons

Through this networking lab, I learned to:

- Reproduce a reported problem before making changes.
- Separate hostname resolution from routing.
- Separate an IP address from a port.
- Understand the purpose of the default gateway.
- Inspect both the address and port of a listening socket.
- Distinguish `127.0.0.1` from `0.0.0.0`.
- Verify which process owns a listening socket.
- Check whether the expected application process is actually running.
- Use logs and service state when troubleshooting systemd-managed applications.
- Verify a fix instead of assuming that restarting something solved the problem.

The troubleshooting principle I want to keep using throughout my DevOps journey is:

> **Inspect first, identify the failing layer, make the appropriate change, and verify the result.**
