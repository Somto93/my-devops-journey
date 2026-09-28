# Server Troubleshooting

## Introduction

The server labs demonstrated that troubleshooting should be based on evidence rather than assumptions.

Across Apache, Tomcat, Flask, Gunicorn, Node.js, and PM2, the same general principle repeatedly applied:

```text
Inspect first
     |
     v
Identify the failing layer
     |
     v
Make one appropriate change
     |
     v
Verify the result
```

A server problem can exist at several different layers.

For example:

```text
Application files
      |
      v
Application process
      |
      v
Listening socket
      |
      v
IP address / binding
      |
      v
Port
      |
      v
HTTP request
      |
      v
Application route/resource
      |
      v
Response
```

Understanding which layer has failed prevents unnecessary changes elsewhere.

---

# Troubleshooting Model

A useful server troubleshooting sequence developed throughout the labs was:

```text
1. Is the required software installed?
             |
             v
2. Is the process/service running?
             |
             v
3. Is the expected port listening?
             |
             v
4. Which process owns the port?
             |
             v
5. Is it listening on the correct address?
             |
             v
6. Does hostname resolution point to the intended server?
             |
             v
7. Can the client establish a connection?
             |
             v
8. What HTTP response is returned?
             |
             v
9. Does the requested route/resource exist?
             |
             v
10. What do the server logs show?
```

Not every incident requires every step.

The important principle is to begin with the observed symptom and collect evidence before changing the system.

---

# Core Troubleshooting Tools

Several commands were repeatedly useful throughout the server labs.

## systemctl

Used for inspecting and controlling system services:

```bash
systemctl status apache2
sudo systemctl start apache2
sudo systemctl stop apache2
sudo systemctl reload apache2
```

It was also used when working with NGINX:

```bash
sudo systemctl stop nginx
```

---

## ss

Used to inspect listening network sockets:

```bash
sudo ss -lntp
```

A specific port can be checked with:

```bash
sudo ss -lntp | grep ':80'
```

or:

```bash
sudo ss -lntp | grep ':5000'
```

This helped answer:

```text
Is anything listening?
Where is it listening?
Which process owns the socket?
What PID is associated with it?
```

---

## ps

Used to inspect processes:

```bash
ps -ef
```

or a specific PID:

```bash
ps -fp <PID>
```

This became especially useful when investigating parent and child processes.

---

## pgrep

Used to locate processes by name or command:

```bash
pgrep -af gunicorn
```

and:

```bash
pgrep -af 'org.apache.catalina.startup.Bootstrap'
```

The `-a` option displays the command line.

The `-f` option allows matching against the full command line.

---

## curl

Used to test services from the client perspective:

```bash
curl http://localhost
```

or headers only:

```bash
curl -I http://localhost
```

It was also used for health endpoints:

```bash
curl http://localhost:5000/health
```

and:

```bash
curl http://localhost:3000/health
```

---

## getent

Used to check hostname resolution:

```bash
getent hosts www.houses.com
```

This helped determine which IP address the operating system would use for a hostname.

---

# Incident 1: Apache Would Not Start

## Symptom

Apache was installed, but:

```bash
systemctl status apache2
```

showed that the service had failed.

The important error was:

```text
(98)Address already in use
```

followed by messages indicating that Apache could not bind to:

```text
[::]:80
```

and:

```text
0.0.0.0:80
```

---

# Avoiding the Wrong First Action

Possible reactions could have included:

```text
Reinstall Apache
Change Apache's port
Edit configuration randomly
Delete configuration
```

But the error already provided a clue:

```text
Address already in use
```

The correct next investigation was therefore the port.

---

# Inspecting Port 80

I ran:

```bash
sudo ss -lntp | grep ':80'
```

The output showed that:

```text
nginx
```

already owned the listening socket.

This changed the diagnosis from:

```text
Apache is broken
```

to:

```text
Apache cannot acquire its configured port because another process already owns it.
```

---

# Inspecting the Existing Server

I inspected NGINX processes:

```bash
ps -ef | grep '[n]ginx'
```

and verified the service from the HTTP layer:

```bash
curl -I http://localhost
```

The response included:

```text
HTTP/1.1 200 OK
Server: nginx/1.28.3 (Ubuntu)
```

This confirmed that NGINX was not merely an old process entry.

It was actively serving HTTP traffic on port 80.

---

# Resolving the Conflict

For the purpose of the Apache lab, I stopped NGINX:

```bash
sudo systemctl stop nginx
```

Before starting Apache, I checked the port again:

```bash
sudo ss -lntp | grep ':80'
```

There was no output.

Only after verifying that port 80 was free did I start Apache:

```bash
sudo systemctl start apache2
```

---

# Verifying the Fix

I verified the service:

```bash
systemctl status apache2
```

Then the socket:

```bash
sudo ss -lntp | grep ':80'
```

Then the HTTP layer:

```bash
curl -I http://localhost
```

The response now included:

```text
HTTP/1.1 200 OK
Server: Apache/2.4.66 (Ubuntu)
```

The troubleshooting path was:

```text
Apache failed
     |
     v
Read error
     |
     v
Address already in use
     |
     v
Inspect port 80
     |
     v
NGINX owns port
     |
     v
Verify NGINX
     |
     v
Stop NGINX
     |
     v
Verify port free
     |
     v
Start Apache
     |
     v
Verify process/socket/HTTP
```

---

# Lesson from the Apache Incident

A service startup failure does not necessarily mean the service itself is incorrectly installed.

The failing layer was:

```text
Network socket allocation
```

Apache wanted port 80.

NGINX already had port 80.

The error was therefore a resource conflict between two server processes.

---

# Incident 2: HTTP 404 vs Connection Failure

During the Apache and Tomcat labs, I encountered both:

```text
HTTP 404
```

and:

```text
curl: (7) Failed to connect
```

These are fundamentally different failure states.

---

# HTTP 404

For Apache, I deliberately requested:

```bash
curl -I http://localhost/does-not-exist.html
```

The response was:

```text
HTTP/1.1 404 Not Found
```

This means:

```text
TCP connection succeeded
       |
       v
HTTP server received request
       |
       v
HTTP server generated response
       |
       v
Requested resource was not found
```

Therefore, a `404` should not initially be investigated as though the server were unreachable.

---

# Connection Failure

Later, after Tomcat was moved from port 8080 to port 9090, requesting the old port resulted in:

```text
curl: (7) Failed to connect
```

That failure happened before an HTTP status could be returned.

Conceptually:

```text
Client
   |
   v
Attempt TCP connection
   |
   X
No required listener
```

Therefore:

```text
HTTP 404
```

and:

```text
Connection refused / failed
```

point to different troubleshooting layers.

---

# HTTP Error vs Network Failure

A useful distinction is:

```text
HTTP response received
        |
        v
Investigate HTTP/application/resource layer
```

versus:

```text
No connection
        |
        v
Investigate process/socket/address/port layer
```

This distinction prevents troubleshooting the wrong part of the system.

---

# Incident 3: Tomcat Configuration Changed but Port Did Not

Tomcat initially used:

```text
8080
```

The active connector in:

```text
/opt/apache-tomcat-11/conf/server.xml
```

was changed to:

```text
9090
```

After editing the file, I checked the socket.

Tomcat was still listening on:

```text
8080
```

---

# Why the Running Port Did Not Change

The configuration file on disk had changed.

The running Java process had not.

Conceptually:

```text
server.xml
port=9090
      |
      X
      |
Existing Tomcat process
still using 8080
```

The running process had already read its configuration when it started.

This produced one of the most important lessons from the server labs:

```text
Configuration on disk != runtime state
```

---

# Applying the Tomcat Change

I stopped Tomcat and verified that the old Bootstrap process was gone.

Then I started Tomcat again.

After restart:

```bash
sudo ss -lntp | grep ':9090'
```

showed Tomcat listening on:

```text
*:9090
```

Testing:

```bash
curl -I http://localhost:9090/somto/
```

returned:

```text
HTTP/1.1 200
```

while:

```bash
curl -I http://localhost:8080/somto/
```

failed to connect.

---

# Lesson from the Tomcat Incident

After editing configuration, always distinguish:

```text
What the configuration file says
```

from:

```text
What the running process is actually doing
```

Useful evidence includes:

```bash
grep
pgrep
ss
curl
```

Together they can answer:

```text
What is configured?
What process is running?
Where is it listening?
Can a client reach it?
```

---

# Incident 4: Flask Worked on One Address but Not Another

The Flask application normally used:

```python
app.run(host="0.0.0.0", port=5000)
```

Both:

```text
127.0.0.1:5000
```

and:

```text
172.23.210.163:5000
```

worked in the lab.

I then changed the binding to:

```python
app.run(host="127.0.0.1", port=5000)
```

---

# Observed Behaviour

The request:

```bash
curl http://127.0.0.1:5000/health
```

worked.

But:

```bash
curl http://172.23.210.163:5000/health
```

failed to connect.

A poor diagnosis would have been:

```text
Flask is down.
```

But that would conflict with the successful loopback request.

---

# Inspecting the Socket

I checked:

```bash
sudo ss -lntp | grep ':5000'
```

The result showed:

```text
127.0.0.1:5000
```

The application was running correctly.

It simply was not listening on the tested `eth0` address.

---

# Flask Binding Lesson

The incident demonstrated:

```text
Process running
       !=
Reachable through every local interface
```

The important question is not only:

```text
Is the application listening?
```

but also:

```text
Which address is it listening on?
```

---

# 127.0.0.1

When Flask used:

```text
127.0.0.1
```

the tested loopback request worked:

```text
127.0.0.1:5000 -> success
```

while the tested `eth0` request failed:

```text
172.23.210.163:5000 -> failure
```

---

# 0.0.0.0

After restoring:

```python
host="0.0.0.0"
```

Flask accepted connections through both tested IPv4 interfaces.

The operating-system listener appeared as:

```text
0.0.0.0:5000
```

This means the server was listening across the available IPv4 interfaces rather than only the loopback address.

---

# Incident 5: Local Virtual Hostname Resolved Publicly

During the Apache virtual-host lab, I configured:

```text
www.houses.com
```

Before assuming it pointed to the local machine, I checked:

```bash
getent hosts www.houses.com
```

It resolved to public Internet addresses.

Therefore, Apache's:

```apache
ServerName www.houses.com
```

did not itself make the operating system send requests to my local Apache server.

---

# Separating Resolution from Virtual Hosting

Two separate mechanisms were involved:

```text
Name resolution
      |
      v
Which IP address does www.houses.com mean?
```

and:

```text
Apache virtual hosting
      |
      v
Which site should Apache serve for that hostname?
```

The local lab required the hostname to resolve to the local machine.

I therefore used `/etc/hosts` for the local mapping.

Afterward:

```bash
getent hosts www.houses.com
```

returned:

```text
127.0.0.1 www.houses.com
```

and the request reached the intended Apache virtual host.

---

# Virtual Host Troubleshooting Lesson

If the wrong website appears, inspect both:

```text
Hostname resolution
```

and:

```text
Web server virtual-host configuration
```

Useful commands include:

```bash
getent hosts <hostname>
sudo apache2ctl -S
curl http://<hostname>
```

---

# Incident 6: npm start Was Not Available

The Node.js application worked when started with:

```bash
node app.js
```

However, the learning material also used:

```bash
npm run start
```

Initially, the project did not have a `start` script.

The problem was therefore not Node.js itself.

The missing layer was the npm project configuration.

---

# Inspecting npm Scripts

The available scripts can be checked using:

```bash
npm run
```

I then added:

```json
"start": "node app.js"
```

to:

```text
package.json
```

After the change:

```bash
npm run start
```

successfully started the application.

---

# JSON Syntax During Configuration

While editing `package.json`, I initially omitted a comma between entries.

I identified and corrected the problem before attempting to run the application.

This reinforced another troubleshooting principle:

```text
Configuration syntax matters.
```

When manually editing configuration or metadata files, inspect the changed section before assuming the application itself is faulty.

---

# Incident 7: Unexpected Node.js PID

When running:

```bash
node app.js
```

directly, the Node.js process appeared straightforward.

When running:

```bash
npm run start
```

I observed additional processes.

The hierarchy was:

```text
npm
 |
 v
shell
 |
 v
node
```

with observed PIDs:

```text
npm   -> 23482
shell -> 23493
node  -> 23494
```

---

# Process Hierarchy Lesson

An unexpected PID does not necessarily indicate the wrong process.

Commands can launch:

```text
wrappers
shells
child processes
workers
process managers
```

Useful investigation commands include:

```bash
ps -fp <PID>
```

and:

```bash
ps -ef
```

The parent PID helps explain how a process was launched.

The correct response to an unexpected process is:

```text
Inspect it
```

rather than immediately:

```text
Kill it
```

---

# Incident 8: Gunicorn Had More Processes Than Workers

I ran:

```bash
gunicorn main:app -w 2
```

and then:

```bash
pgrep -af gunicorn
```

The output showed three Gunicorn processes.

At first glance, someone might expect:

```text
-w 2
```

to mean:

```text
2 total processes
```

But the process model was:

```text
1 master
+
2 workers
=
3 Gunicorn processes
```

---

# Gunicorn Process Lesson

Command-line configuration should be interpreted in terms of the application's process model.

The master process manages the workers.

Therefore:

```text
worker count != total process count
```

This is why inspecting command lines and process relationships is useful.

---

# Incident 9: PM2 Changed the Process/Socket View

The Node.js application initially ran directly with:

```bash
node app.js
```

and the Node process could be connected directly to the port-3000 listener.

PM2 was then used to manage the application.

In single-instance fork mode, the application appeared with its managed Node.js PID.

Later I ran:

```bash
pm2 start app.js -i 4
```

PM2 created four cluster-mode instances.

---

# PM2 Cluster Observation

`pm2 list` showed four online instances with worker PIDs:

```text
24005
24012
24023
24034
```

However:

```bash
sudo ss -lntp | grep ':3000'
```

showed:

```text
PM2 v7.0.4: God
```

associated with the listening socket.

This differed from the earlier direct Node.js process view.

---

# PM2 Troubleshooting Lesson

A process manager can change how processes and sockets appear at the operating-system level.

Therefore, when a process manager is involved, use both:

```text
Operating-system tools
```

and:

```text
Process-manager tools
```

For PM2:

```bash
pm2 list
pm2 describe app
```

can be combined with:

```bash
ps
ss
curl
```

to understand the full state.

---

# Server Troubleshooting by Layer

A useful way to approach incidents is to identify the layer being tested.

| Layer | Question | Example Tool |
| --- | --- | --- |
| Installation | Is the software installed? | `dpkg`, `which` |
| Service | Is the service active? | `systemctl status` |
| Process | Is the process running? | `ps`, `pgrep` |
| Socket | Is the port listening? | `ss -lntp` |
| Binding | Which address is listening? | `ss -lntp` |
| Name resolution | Where does the hostname point? | `getent hosts` |
| Connection | Can the client connect? | `curl` |
| HTTP | What status did the server return? | `curl -I` |
| Application | Does the route/context exist? | `curl` |
| Server internals | What happened during startup/deployment? | logs |

The goal is to locate the first layer where reality differs from the expected state.

---

# Process, Port, and HTTP Verification

One of the most reusable patterns from these labs was:

```text
Process
   |
   v
Socket
   |
   v
HTTP
```

For example, with Tomcat:

```bash
pgrep -af 'org.apache.catalina.startup.Bootstrap'
```

checks the process.

Then:

```bash
sudo ss -lntp | grep ':9090'
```

checks the socket.

Then:

```bash
curl -I http://localhost:9090
```

checks HTTP.

This gives progressively stronger evidence that the service is functioning.

---

# Why Process Checks Alone Are Not Enough

Suppose:

```bash
pgrep -af python
```

shows the application process.

That proves a process exists.

It does not prove:

```text
The correct port is open
The correct interface is bound
The application accepts connections
The expected route exists
The HTTP response is correct
```

Therefore:

```text
Process exists
```

is evidence, but it is not complete service verification.

---

# Why Port Checks Alone Are Not Enough

Suppose:

```bash
ss -lntp
```

shows:

```text
*:9090
```

That proves something is listening.

It does not by itself prove:

```text
The application returns the expected content
The requested context exists
The application is healthy
```

A client-level request is still useful:

```bash
curl
```

---

# Why HTTP Checks Are Powerful

`curl` tests the service from a client perspective.

For example:

```bash
curl http://localhost:5000/health
```

can prove that:

```text
Connection succeeds
HTTP request succeeds
Application route executes
Expected response is returned
```

However, if `curl` fails, lower-level tools such as:

```text
ss
ps
pgrep
systemctl
```

help determine why.

---

# Logs as Evidence

Logs were important in both Apache and Tomcat labs.

Apache:

```text
/var/log/apache2/access.log
/var/log/apache2/error.log
```

Tomcat:

```text
/opt/apache-tomcat-11/logs/catalina.out
```

PM2:

```text
~/.pm2/logs/
```

Logs can answer questions such as:

```text
Did the request reach the server?
Did the server start successfully?
Did deployment occur?
Was an error generated?
```

Logs should be combined with runtime evidence rather than read in isolation.

---

# Configuration vs Runtime State

This became a recurring theme.

A configuration file may say:

```text
port 9090
```

while an old running process is still using:

```text
port 8080
```

A source file may say:

```text
host=0.0.0.0
```

but if the process was started before the change, the current process may still reflect the old configuration.

Therefore, after configuration changes, verify runtime state.

Useful tools include:

```bash
ps
pgrep
ss
curl
```

---

# Change One Thing at a Time

Another useful troubleshooting principle is to avoid making many unrelated changes simultaneously.

For example, if Apache cannot start because port 80 is occupied, changing:

```text
Apache port
Apache DocumentRoot
VirtualHost configuration
Firewall configuration
```

all at once would make it harder to know what actually solved the problem.

A better sequence is:

```text
Observe
   |
   v
Form a specific question
   |
   v
Run a diagnostic command
   |
   v
Interpret the result
   |
   v
Make one justified change
   |
   v
Verify
```

---

# Verification After a Fix

A fix is not complete merely because a command returned without an obvious error.

For example, after resolving the Apache port conflict, I verified:

```text
systemctl -> Apache active
ss        -> Apache listening on 80
curl      -> HTTP 200
header    -> Server: Apache
```

After changing Tomcat to 9090, I verified:

```text
pgrep -> new Tomcat process
ss    -> port 9090 listening
curl  -> /somto/ HTTP 200
8080  -> connection fails
```

Verification should prove that the intended final state has actually been reached.

---

# Practical Troubleshooting Checklist

When a server application is not working, I can work through:

```text
1. What exactly is the symptom?

2. Is the required software installed?

3. Is the service/process running?

4. What PID is running?

5. What address and port is it listening on?

6. Is another process already using the required port?

7. Does the hostname resolve to the intended address?

8. Can curl establish a connection?

9. Is an HTTP status returned?

10. Does the requested route/resource/context exist?

11. What do the server logs show?

12. Has configuration changed without restarting/reloading the process?

13. Is a wrapper or process manager involved?

14. After making a change, did I verify the final state?
```

---

# Common Evidence Patterns from the Labs

## Service Down

```text
No expected process
+
No expected listening socket
+
curl connection failure
```

Investigate startup/service state.

---

## Wrong Port

```text
Process running
+
Different port listening
+
curl to expected port fails
```

Investigate configured versus runtime port.

---

## Wrong Binding

```text
Process running
+
127.0.0.1:<port> listening
+
loopback works
+
interface address fails
```

Investigate listening address.

---

## Missing Resource

```text
Server reachable
+
HTTP 404
```

Investigate resource, route, application context, or document path.

---

## Port Conflict

```text
Service startup failure
+
"Address already in use"
+
another process owns port
```

Investigate the existing listener before changing the failing service.

---

## Configuration Not Applied

```text
Configuration file changed
+
running socket unchanged
```

Investigate whether the service requires reload or restart.

---

# Troubleshooting Philosophy

The practical server labs reinforced a consistent approach:

```text
Do not guess.
Inspect.
```

Then:

```text
Do not change everything.
Identify the failing layer.
```

Then:

```text
Do not assume the fix worked.
Verify it.
```

The complete approach is:

```text
Observe
   |
   v
Inspect
   |
   v
Understand
   |
   v
Change
   |
   v
Verify
```

---

# Key Takeaways

- Server troubleshooting should be evidence-driven.
- A service being installed does not mean it is running.
- A running process does not mean it is listening on the expected socket.
- A listening socket does not guarantee the expected application response.
- `ss -lntp` is one of the most useful tools for connecting ports to processes.
- `ps` and `pgrep` help identify processes and process models.
- `curl` tests the server from the client perspective.
- `getent hosts` helps verify hostname resolution.
- HTTP `404` is different from a connection failure.
- "Address already in use" should lead to inspection of the existing port owner.
- Configuration on disk can differ from the current runtime state.
- Binding to `127.0.0.1` and `0.0.0.0` produced different reachability in the Flask lab.
- Apache `ServerName` configuration and hostname resolution are separate concerns.
- Wrapper processes such as npm can introduce additional parent/child processes.
- Gunicorn worker count does not equal total Gunicorn process count because of its master process.
- Process managers such as PM2 can change how processes and listening sockets appear.
- Logs provide important evidence but should be interpreted alongside processes, sockets, and client requests.
- Make one justified change at a time.
- Always verify the final state after applying a fix.
