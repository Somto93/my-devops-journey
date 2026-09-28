# Linux Servers

This section documents my practical learning and hands-on work with Linux servers, including web servers, application servers, Apache, Apache Tomcat, Python/Flask, Gunicorn, Node.js, PM2, application deployment, ports, binding, logs, processes, and troubleshooting.

The goal of these labs was not only to configure servers, but also to understand how an application moves from source code to a running process that listens on a network port and responds to client requests.

## Topics Covered

1. **Server Fundamentals**
   - Web servers and application servers
   - Static and dynamic content
   - Web frameworks
   - Basic multi-tier application architecture

2. **Apache Web Server**
   - Apache installation and service management
   - Port 80
   - Document roots
   - Static website hosting
   - Apache access and error logs

3. **Apache Configuration and Virtual Hosts**
   - Apache configuration files
   - `ServerName`
   - `DocumentRoot`
   - Name-based virtual hosts
   - Hosting multiple websites on one server
   - Local hostname resolution with `/etc/hosts`

4. **Apache Tomcat**
   - Java runtime requirements
   - Installing Tomcat under `/opt`
   - Tomcat directory structure
   - `server.xml`
   - Connector ports
   - Tomcat processes and logs
   - Changing Tomcat from port 8080 to 9090

5. **Application Deployment**
   - Creating a WAR file
   - Tomcat `webapps` directory
   - Automatic WAR deployment
   - Application context paths
   - Verifying deployments through logs and HTTP requests

6. **Python Application Servers**
   - Flask development server
   - Python virtual environments
   - Python dependencies
   - Gunicorn
   - Gunicorn workers
   - Development versus production application serving

7. **Node.js Applications**
   - npm
   - `package.json`
   - `package-lock.json`
   - Express
   - Running applications with Node.js
   - npm scripts
   - PM2 process management
   - PM2 fork and cluster modes

8. **Server Troubleshooting**
   - Port conflicts
   - Identifying listening processes
   - HTTP 404 versus connection failure
   - Application binding
   - Service logs
   - Process inspection
   - Configuration changes versus running state

## Practical Lab Structure

```text
08-servers/
├── README.md
├── 01-server-fundamentals.md
├── 02-apache-web-server.md
├── 03-apache-configuration-and-virtual-hosts.md
├── 04-apache-tomcat.md
├── 05-application-deployment.md
├── 06-python-production-servers.md
├── 07-nodejs-applications.md
├── 08-server-troubleshooting.md
├── .gitignore
└── lab/
    ├── flask-app/
    │   ├── main.py
    │   └── requirements.txt
    ├── node-app/
    │   ├── app.js
    │   ├── package.json
    │   └── package-lock.json
    └── tomcat-app/
        └── index.html
```

## Server Request Flow

A simplified application request can be viewed as:

```text
Client
  |
  v
Web Server / Application Server
  |
  v
Application
  |
  v
Database or other backend services
```

In larger architectures, multiple web servers can communicate with application servers, which in turn communicate with database servers.

## Web Server vs Application Server

A web server commonly serves web content such as HTML, CSS, JavaScript, and images.

An application server runs application/backend logic and generates dynamic responses.

During these labs I worked with both types of server technologies:

```text
Apache HTTP Server
        |
        +--> Static web content
        +--> Virtual hosts

Apache Tomcat
        |
        +--> Java web applications
        +--> WAR deployment

Flask + Gunicorn
        |
        +--> Python web application

Node.js + Express + PM2
        |
        +--> JavaScript web application
        +--> Process management
        +--> Cluster mode
```

## Important Server Troubleshooting Principle

A major lesson from these labs was to inspect the current state before changing configuration.

A useful troubleshooting flow is:

```text
Is the application/service running?
        |
        v
Is the expected port listening?
        |
        v
Which process owns the port?
        |
        v
Is it bound to the correct address?
        |
        v
Can the client establish a connection?
        |
        v
What HTTP response is returned?
        |
        v
What do the application/service logs show?
```

Commands used frequently during the labs included:

```bash
systemctl status <service>
ss -lntp
ps -ef
ps -fp <PID>
pgrep -af <process>
curl -I http://host:port
curl http://host:port/path
```

## Binding Addresses

One of the practical networking concepts reinforced during the server labs was the difference between loopback and all-interface binding.

For example:

```python
app.run(host="127.0.0.1", port=5000)
```

binds the application to loopback only.

In the lab this allowed:

```text
127.0.0.1:5000        -> reachable
172.23.210.163:5000    -> connection failed
```

Changing the application to:

```python
app.run(host="0.0.0.0", port=5000)
```

allowed the application to listen across the available IPv4 interfaces.

The application was then reachable using both:

```text
127.0.0.1:5000
172.23.210.163:5000
```

This reinforced the relationship between application configuration and the networking concepts covered in the previous Linux networking section.

## Environment

These practical labs were completed on Ubuntu running under WSL.

Some of the original learning material used RHEL/CentOS-style commands such as:

```bash
yum install httpd
service httpd start
```

On Ubuntu, the equivalent Apache package and systemd service used in the practical lab were:

```bash
sudo apt install apache2
sudo systemctl start apache2
sudo systemctl status apache2
```

This was useful for understanding that the underlying server concepts remain similar even when package names, service names, and configuration paths differ between Linux distributions.

## Key Takeaway

A server is more than an installed package.

For a service to be usable, several layers need to work together:

```text
Configuration
     +
Running Process
     +
Listening Socket
     +
Correct IP/Binding
     +
Correct Port
     +
Application/Content
     +
Successful Client Request
```

Understanding and verifying each of these layers makes server deployment and troubleshooting much more systematic.
