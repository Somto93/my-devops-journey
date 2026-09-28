# Apache Tomcat

## Introduction

Apache Tomcat is used to run Java web applications.

In the learning material, Tomcat was introduced after Apache HTTP Server. The material covered:

- Installing Java
- Downloading and extracting Tomcat
- Starting Tomcat
- Tomcat's directory structure
- The `server.xml` configuration file
- Connector ports
- The `webapps` deployment directory
- Tomcat logs
- Changing the HTTP connector port

The practical lab used Apache Tomcat 11 installed under:

```text
/opt/apache-tomcat-11
```

---

# Apache HTTP Server vs Apache Tomcat

Although both contain the name Apache, Apache HTTP Server and Apache Tomcat perform different roles in these labs.

Apache HTTP Server was used primarily to serve web content such as:

```text
HTML
CSS
JavaScript
Images
```

Tomcat was used as the server environment for deploying a Java web application archive.

Conceptually:

```text
Apache HTTP Server
        |
        v
Static web content

Apache Tomcat
        |
        v
Java web application
        |
        v
WAR deployment
```

---

# Checking Java

Tomcat requires Java.

Before installing Tomcat, I checked the Java runtime:

```bash
java -version
```

The system reported:

```text
openjdk version "25.0.4.1" 2026-08-18
OpenJDK Runtime Environment (build 25.0.4.1+1-1-26.04.4-Ubuntu)
OpenJDK 64-Bit Server VM
```

This confirmed that Java was already installed before Tomcat was started.

---

# Checking for an Existing Tomcat Installation

Before installing Tomcat, I checked whether a Tomcat directory already existed under `/opt`.

The check did not return an existing Tomcat installation.

This was useful because repeated installation commands can otherwise create confusing directory structures or overwrite an existing lab.

---

# Checking the Default Tomcat Port

Before starting Tomcat, I also checked whether port 8080 was already in use:

```bash
sudo ss -lntp | grep ':8080'
```

There was no output.

This meant there was no matching TCP listener on port 8080 at that point.

The workflow was therefore:

```text
Check existing installation
          |
          v
Check required Java runtime
          |
          v
Check intended port
          |
          v
Install and start Tomcat
```

---

# Downloading Tomcat

The Tomcat 11 standard binary archive was downloaded as a `.tar.gz` file.

The downloaded archive was:

```text
apache-tomcat-11.0.26.tar.gz
```

Before extracting it, I inspected the archive contents:

```bash
tar -tzf apache-tomcat-11.0.26.tar.gz | head
```

The archive contained a top-level directory similar to:

```text
apache-tomcat-11.0.26/
```

and included Tomcat configuration files such as:

```text
conf/server.xml
```

Inspecting an archive before extraction is useful because it shows how the files will be laid out.

---

# Extracting Tomcat

I extracted the archive:

```bash
tar -xf apache-tomcat-11.0.26.tar.gz
```

The extracted Tomcat directory was then moved under `/opt`:

```bash
sudo mv ~/apache-tomcat-11.0.26 /opt/apache-tomcat-11
```

The final installation path was:

```text
/opt/apache-tomcat-11
```

Using a stable directory name such as:

```text
apache-tomcat-11
```

makes the installation path easier to work with than repeatedly typing the full version number.

---

# Why sudo Was Needed for /opt

The extraction could be performed in the user's home directory without elevated privileges.

The final move into:

```text
/opt
```

required `sudo` because `/opt` is normally controlled by root.

This demonstrated a useful principle:

```text
User-owned working directory
        |
        v
Normal user commands

System-managed directory such as /opt
        |
        v
Elevated privileges may be required
```

---

# Tomcat Directory Structure

After installation, I inspected:

```text
/opt/apache-tomcat-11
```

The directory contained:

```text
BUILDING.txt
CONTRIBUTING.md
LICENSE
NOTICE
README.md
RELEASE-NOTES
RUNNING.txt
bin
conf
lib
logs
temp
webapps
work
```

Several directories are especially important when administering Tomcat.

---

# bin

The `bin` directory contains Tomcat scripts.

```text
/opt/apache-tomcat-11/bin
```

Scripts used during the lab included:

```text
startup.sh
shutdown.sh
```

Tomcat was started with:

```bash
sudo /opt/apache-tomcat-11/bin/startup.sh
```

and stopped with the corresponding shutdown script.

---

# conf

Tomcat configuration files are stored under:

```text
/opt/apache-tomcat-11/conf
```

One of the most important files encountered in the lab was:

```text
server.xml
```

This file contains server configuration including HTTP connector settings.

---

# logs

Tomcat logs are stored under:

```text
/opt/apache-tomcat-11/logs
```

The practical installation contained files including:

```text
catalina.2026-09-27.log
catalina.out
localhost.2026-09-27.log
localhost_access_log.2026-09-27.txt
```

These logs were useful for confirming server startup and application deployment.

---

# webapps

Applications deployed to Tomcat are stored under:

```text
/opt/apache-tomcat-11/webapps
```

The default installation contained applications such as:

```text
ROOT
docs
examples
host-manager
manager
```

Later, the custom `somto.war` application was also placed in this directory.

---

# temp

The `temp` directory is used for temporary files required by Tomcat.

```text
/opt/apache-tomcat-11/temp
```

---

# work

The `work` directory contains files generated by Tomcat while processing deployed applications.

```text
/opt/apache-tomcat-11/work
```

---

# Tomcat server.xml

The learning material introduced:

```text
conf/server.xml
```

as an important Tomcat configuration file.

In the practical lab, I inspected the connector configuration using:

```bash
grep -n 'Connector port=' /opt/apache-tomcat-11/conf/server.xml
```

The output included:

```text
70: <Connector port="8080" protocol="HTTP/1.1"
88: <Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
```

The active HTTP connector used:

```text
8080
```

---

# Connector Port

The HTTP connector determines the port on which Tomcat accepts HTTP connections.

The relevant configuration looked like:

```xml
<Connector port="8080" protocol="HTTP/1.1"
```

Conceptually:

```text
Client
   |
   v
TCP port 8080
   |
   v
Tomcat HTTP Connector
   |
   v
Web Application
```

---

# Starting Tomcat

Tomcat was started using:

```bash
sudo /opt/apache-tomcat-11/bin/startup.sh
```

Starting a script successfully does not by itself prove that the server is running correctly.

I therefore verified the process, socket, HTTP response, and logs separately.

---

# Verifying the Tomcat Process

I searched for the Tomcat Java process with:

```bash
pgrep -af 'org.apache.catalina.startup.Bootstrap'
```

The output showed a Java process containing:

```text
org.apache.catalina.startup.Bootstrap start
```

The initial Tomcat process had PID:

```text
22056
```

This confirmed that a Java process associated with Tomcat was running.

---

# Verifying Port 8080

Next, I inspected the network socket:

```bash
sudo ss -lntp | grep ':8080'
```

The output showed Java listening on:

```text
*:8080
```

with PID:

```text
22056
```

This connected the Tomcat process to its network listener:

```text
Tomcat Java process
PID 22056
      |
      v
*:8080
```

---

# Verifying Tomcat with HTTP

I then tested the HTTP layer:

```bash
curl -I http://localhost:8080
```

The response included:

```text
HTTP/1.1 200
```

At this point I had verified:

```text
Tomcat process running
        |
        v
Port 8080 listening
        |
        v
HTTP request successful
```

---

# Testing the Documentation Application

The default Tomcat installation included:

```text
webapps/docs
```

I tested it with:

```bash
curl -I http://localhost:8080/docs/
```

The response was:

```text
HTTP/1.1 200
```

This demonstrated how directories under `webapps` can become application context paths.

For example:

```text
webapps/docs
      |
      v
/docs/
```

---

# Tomcat Logs

I inspected the Tomcat logs:

```bash
ls -lh /opt/apache-tomcat-11/logs/
```

One important file was:

```text
catalina.out
```

I inspected recent entries with:

```bash
sudo tail -n 20 /opt/apache-tomcat-11/logs/catalina.out
```

The output included messages such as:

```text
Initializing ProtocolHandler ["http-nio-8080"]
```

and:

```text
Starting Servlet engine: [Apache Tomcat/11.0.26]
```

It also showed deployment of Tomcat's default applications and:

```text
Starting ProtocolHandler ["http-nio-8080"]
```

followed by a server startup time.

These messages provided evidence that Tomcat had initialized its HTTP connector and completed startup.

---

# Tomcat Native/OpenSSL Message

The startup log also contained an informational message indicating that the Tomcat Native/OpenSSL library was not found.

Tomcat still:

```text
started successfully
listened on port 8080
returned HTTP 200
```

This reinforced an important troubleshooting principle:

```text
A log message must be interpreted in context.
```

Not every message in a server log represents a fatal failure.

The actual runtime state should also be checked.

---

# Configuration on Disk vs Running State

One of the most important Tomcat lessons came from changing the HTTP connector port.

The connector was changed in:

```text
/opt/apache-tomcat-11/conf/server.xml
```

from:

```xml
<Connector port="8080" protocol="HTTP/1.1"
```

to:

```xml
<Connector port="9090" protocol="HTTP/1.1"
```

However, immediately after editing the file, the existing Tomcat process was still listening on:

```text
8080
```

This demonstrated:

```text
Configuration file on disk
          !=
Current running process state
```

The running Tomcat process had already read its configuration during startup.

Changing the file did not automatically change the existing process.

---

# Inspecting 8080 Before Editing

Before changing the connector, I searched the file for references to `8080`.

The file contained more than one reference.

These included:

- A comment
- The active HTTP connector
- A commented-out connector example

Instead of performing a blind global replacement, I inspected the relevant section and changed only the active connector.

This avoided unnecessarily modifying unrelated or commented configuration.

---

# Changing Tomcat from 8080 to 9090

The active connector was changed to:

```xml
<Connector port="9090" protocol="HTTP/1.1"
```

I verified the connector configuration again:

```bash
grep -n 'Connector port=' /opt/apache-tomcat-11/conf/server.xml
```

The result showed:

```text
70: <Connector port="9090" protocol="HTTP/1.1"
88: <Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
```

The configuration file now specified port 9090.

---

# Checking the Running State Before Restart

Before restarting Tomcat, I checked:

```bash
sudo ss -lntp | grep -E ':8080|:9090'
```

Tomcat was still listening on:

```text
*:8080
```

This proved that editing `server.xml` had not changed the running process.

The sequence was:

```text
server.xml says 9090
        |
        v
Running process still says 8080
```

A restart cycle was required for Tomcat to read the new configuration.

---

# Stopping Tomcat

I shut Tomcat down using its shutdown script.

After shutdown, I checked:

```bash
pgrep -af 'org.apache.catalina.startup.Bootstrap'
```

There was no matching Tomcat process.

This was important because I wanted to confirm that the old process was actually gone before starting a new one.

---

# Starting Tomcat with the New Configuration

I started Tomcat again:

```bash
sudo /opt/apache-tomcat-11/bin/startup.sh
```

A new Tomcat Java process was created.

The new process had PID:

```text
22969
```

---

# Verifying Port 9090

I checked the listening socket again.

Tomcat was now listening on:

```text
*:9090
```

instead of:

```text
*:8080
```

This proved that the restarted process had read the updated `server.xml`.

---

# Testing the New Port

The deployed application was tested on the new port:

```bash
curl -I http://localhost:9090/somto/
```

The response included:

```text
HTTP/1.1 200
```

I then tested the old port:

```bash
curl -I http://localhost:8080/somto/
```

The result was:

```text
curl: (7) Failed to connect
```

This provided strong evidence that the port migration was complete:

```text
8080 -> no listener
9090 -> Tomcat listening
9090 -> application responds
```

---

# Tomcat Port Change Workflow

The complete workflow was:

```text
Inspect current connector
          |
          v
Confirm current listener
          |
          v
Edit active Connector port
          |
          v
Verify configuration file
          |
          v
Observe old process still using old port
          |
          v
Stop Tomcat
          |
          v
Verify old process is gone
          |
          v
Start Tomcat
          |
          v
Verify new process
          |
          v
Verify new listening port
          |
          v
Test application with curl
```

---

# Important Tomcat Paths

Installation:

```text
/opt/apache-tomcat-11
```

Startup script:

```text
/opt/apache-tomcat-11/bin/startup.sh
```

Shutdown script:

```text
/opt/apache-tomcat-11/bin/shutdown.sh
```

Configuration:

```text
/opt/apache-tomcat-11/conf
```

Main server configuration:

```text
/opt/apache-tomcat-11/conf/server.xml
```

Applications:

```text
/opt/apache-tomcat-11/webapps
```

Logs:

```text
/opt/apache-tomcat-11/logs
```

Catalina output:

```text
/opt/apache-tomcat-11/logs/catalina.out
```

---

# Useful Tomcat Commands

Check Java:

```bash
java -version
```

Inspect Tomcat:

```bash
ls -lh /opt/apache-tomcat-11
```

Inspect connector ports:

```bash
grep -n 'Connector port=' /opt/apache-tomcat-11/conf/server.xml
```

Start Tomcat:

```bash
sudo /opt/apache-tomcat-11/bin/startup.sh
```

Stop Tomcat:

```bash
sudo /opt/apache-tomcat-11/bin/shutdown.sh
```

Find the Tomcat process:

```bash
pgrep -af 'org.apache.catalina.startup.Bootstrap'
```

Check port 8080:

```bash
sudo ss -lntp | grep ':8080'
```

Check port 9090:

```bash
sudo ss -lntp | grep ':9090'
```

Test Tomcat:

```bash
curl -I http://localhost:9090
```

Inspect logs:

```bash
sudo tail -n 20 /opt/apache-tomcat-11/logs/catalina.out
```

---

# Apache HTTP Server and Tomcat Ports

During the labs, the two server technologies were running on different ports:

```text
Apache HTTP Server -> 80
Tomcat             -> 9090
```

Therefore, the port identifies which listening service the connection is intended for.

For example:

```text
http://localhost
```

uses HTTP's default port 80 and reaches Apache.

While:

```text
http://localhost:9090
```

explicitly targets Tomcat on port 9090.

---

# Troubleshooting Tomcat

A useful troubleshooting sequence is:

```text
Is Java installed?
        |
        v
Does the Tomcat directory exist?
        |
        v
Is the Tomcat process running?
        |
        v
Which connector port is configured?
        |
        v
Is that port actually listening?
        |
        v
Can curl establish a connection?
        |
        v
What HTTP status is returned?
        |
        v
What does catalina.out show?
```

Useful commands include:

```bash
java -version
pgrep -af 'org.apache.catalina.startup.Bootstrap'
grep -n 'Connector port=' /opt/apache-tomcat-11/conf/server.xml
sudo ss -lntp
curl -I http://localhost:<port>
sudo tail -n 20 /opt/apache-tomcat-11/logs/catalina.out
```

---

# Key Takeaways

- Tomcat runs Java web applications.
- Java should be verified before starting Tomcat.
- The practical Tomcat installation was stored under `/opt/apache-tomcat-11`.
- Tomcat has separate directories for binaries, configuration, logs, applications, temporary files, and runtime work.
- `server.xml` contains important server configuration including HTTP connector ports.
- Tomcat initially listened on port 8080.
- A running Java process can be identified with `pgrep`.
- `ss -lntp` connects the running process to its listening socket.
- `curl` verifies the HTTP layer.
- `catalina.out` provides important startup and deployment information.
- Editing `server.xml` does not automatically modify the already-running Tomcat process.
- Tomcat needed to be stopped and started before the new connector port took effect.
- After changing the connector to 9090, port 9090 responded while port 8080 produced a connection failure.
- Configuration files, running processes, network sockets, HTTP responses, and logs should be verified as separate layers.
