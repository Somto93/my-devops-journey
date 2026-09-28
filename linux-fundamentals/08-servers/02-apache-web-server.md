# Apache Web Server

## Introduction

Apache HTTP Server is web server software used to serve web content to clients over HTTP.

The learning material introduced Apache using RHEL/CentOS-style commands such as:

```bash
yum install httpd
service httpd start
service httpd status
```

The practical lab was completed on Ubuntu, where the Apache package and service are named:

```text
apache2
```

Therefore, the Ubuntu equivalents are:

```bash
sudo apt install apache2
sudo systemctl start apache2
sudo systemctl status apache2
```

This demonstrated an important Linux administration concept:

```text
Same server technology
        +
Different Linux distribution
        =
Different package/service names and configuration layout
```

---

# Checking the Operating System

Before working with Apache, I checked the Linux distribution:

```bash
cat /etc/os-release
```

The system was:

```text
Ubuntu 26.04.1 LTS
```

This explained why the course commands using `yum` and `httpd` were not the commands used in my practical environment.

On Ubuntu:

```text
Package -> apache2
Service -> apache2
```

---

# Checking Whether Apache Was Installed

I checked the installed Apache packages with:

```bash
dpkg -l | grep apache2
```

Apache was already installed.

The installed packages included components such as:

```text
apache2
apache2-bin
apache2-data
apache2-utils
```

This was an important reminder that:

```text
Installed != Running
```

A package can exist on the machine while its service is stopped or unable to start.

---

# Checking the Apache Service

I inspected Apache using:

```bash
systemctl status apache2
```

Apache was in a failed state.

The important errors included:

```text
(98)Address already in use: AH00072: make_sock: could not bind to address [::]:80
(98)Address already in use: AH00072: make_sock: could not bind to address 0.0.0.0:80
no listening sockets available, shutting down
```

Rather than immediately changing Apache configuration, I treated the error as evidence.

The key phrase was:

```text
Address already in use
```

Apache was attempting to use port 80, but something else already owned that port.

---

# Checking Apache's Listening Port Configuration

I inspected:

```bash
cat /etc/apache2/ports.conf
```

The relevant configuration was:

```apache
Listen 80

<IfModule ssl_module>
    Listen 443
</IfModule>

<IfModule mod_gnutls.c>
    Listen 443
</IfModule>
```

This confirmed that Apache was configured to listen on HTTP port:

```text
80
```

---

# Finding What Was Using Port 80

Instead of assuming which application caused the conflict, I inspected the listening socket:

```bash
sudo ss -lntp | grep ':80'
```

The output identified:

```text
nginx
```

as the process already listening on port 80.

I also inspected the NGINX processes using:

```bash
ps -ef | grep '[n]ginx'
```

The process structure showed:

```text
NGINX master process -> root
NGINX worker processes -> www-data
```

This connected three pieces of evidence:

```text
Apache cannot bind to port 80
            |
            v
Port 80 already has a listener
            |
            v
Listener belongs to NGINX
```

Therefore, the problem was not that Apache was missing or incorrectly installed.

The problem was a port conflict.

---

# Verifying NGINX Before Changing Anything

Before stopping NGINX, I confirmed that it was actually serving HTTP traffic.

I ran:

```bash
curl -I http://localhost
```

The response included:

```text
HTTP/1.1 200 OK
Server: nginx/1.28.3 (Ubuntu)
Content-Type: text/html
Content-Length: 10672
```

This confirmed that:

```text
Port 80
   |
   v
NGINX
   |
   v
HTTP 200 response
```

The `Server` header provided additional evidence that NGINX was handling the request.

---

# Inspecting the NGINX Document Root

I inspected the active NGINX configuration:

```bash
sudo nginx -T 2>/dev/null | grep -n 'root '
```

The active document root was:

```text
/var/www/html
```

I then inspected that directory:

```bash
ls -lah /var/www/html
```

It contained files including:

```text
index.html
index.nginx-debian.html
```

I also checked NGINX's index configuration:

```bash
sudo nginx -T 2>/dev/null | grep -n 'index '
```

It included:

```text
index index.html index.htm index.nginx-debian.html;
```

---

# Connecting HTTP Content-Length to the Actual File

The HTTP response from NGINX reported:

```text
Content-Length: 10672
```

I checked the size of the active HTML file:

```bash
stat -c '%n %s bytes' /var/www/html/index.html
```

The result showed:

```text
/var/www/html/index.html 10672 bytes
```

The values matched.

This connected the HTTP response to the actual file being served:

```text
HTTP Content-Length
       10672
          |
          v
/var/www/html/index.html
       10672 bytes
```

---

# Resolving the Port Conflict

Since the purpose of the lab was to work with Apache, I stopped NGINX:

```bash
sudo systemctl stop nginx
```

Then I checked port 80 again:

```bash
sudo ss -lntp | grep ':80'
```

There was no output.

That was important.

No output meant that there was no matching TCP listener on port 80 at that moment.

I now had evidence that the port was available before attempting to start Apache.

---

# Starting Apache

I started Apache:

```bash
sudo systemctl start apache2
```

Then checked its state:

```bash
systemctl status apache2 --no-pager
```

Apache reported:

```text
active (running)
```

The main Apache process had a PID, confirming that the service was now running.

---

# Verifying Apache's Listening Socket

A running service does not automatically prove that the expected network socket exists.

I checked:

```bash
sudo ss -lntp | grep ':80'
```

The output now showed:

```text
apache2
```

listening on:

```text
*:80
```

This established:

```text
Apache service
     |
     v
Running processes
     |
     v
TCP port 80 listener
```

---

# Verifying Apache with HTTP

I then tested the server from the client perspective:

```bash
curl -I http://localhost
```

The response included:

```text
HTTP/1.1 200 OK
Server: Apache/2.4.66 (Ubuntu)
Content-Length: 10672
Content-Type: text/html
```

Previously, the same request had returned:

```text
Server: nginx/1.28.3 (Ubuntu)
```

Now it returned:

```text
Server: Apache/2.4.66 (Ubuntu)
```

This demonstrated that the software handling port 80 had changed from NGINX to Apache.

---

# Apache Document Root

The learning material introduced Apache's `DocumentRoot` as the directory containing content served by the web server.

On the Ubuntu lab system, the default virtual host used:

```text
/var/www/html
```

as its document root.

Conceptually:

```text
HTTP Request
     |
     v
Apache
     |
     v
DocumentRoot
     |
     v
/var/www/html
```

A request for the site's root page can therefore result in Apache serving an index file from this directory.

---

# Backing Up the Existing Page

Before replacing the existing page, I created a backup:

```bash
sudo cp /var/www/html/index.html /var/www/html/index.html.backup
```

This preserved the original file before modification.

This is a useful administration habit:

```text
Inspect
   |
   v
Backup
   |
   v
Change
   |
   v
Verify
```

---

# Creating My Apache Web Page

I replaced `/var/www/html/index.html` with:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Somto's Apache Server</title>
</head>
<body>
    <h1>Apache Web Server Lab</h1>
    <p>This page is being served by Apache from /var/www/html.</p>
</body>
</html>
```

I then requested the page:

```bash
curl http://localhost
```

Apache returned the new HTML.

No Apache restart was required.

---

# Why a Restart Was Not Required

I changed a static content file:

```text
/var/www/html/index.html
```

I did not change Apache's server configuration.

Apache reads the requested static file when serving the request, so the new content could be returned immediately.

This is different from modifying server configuration.

For example:

```text
Static file change
      |
      v
Usually available on next request
```

while:

```text
Apache configuration change
      |
      v
Configuration must be reloaded/restarted as appropriate
```

This distinction became important later when working with virtual hosts.

---

# Apache Logs

The learning material introduced Apache access and error logs.

On the Ubuntu system, I inspected:

```bash
ls -lh /var/log/apache2/
```

The directory contained:

```text
access.log
error.log
other_vhosts_access.log
```

These logs provide different types of evidence when troubleshooting a web server.

---

# Access Log

The Apache access log records HTTP requests handled by the server.

Example entries from the lab included:

```text
The lab showed successful requests in the access log, including:

```text
"HEAD / HTTP/1.1" 200
"GET / HTTP/1.1" 200

Important fields include:

```text
::1
```

The client used IPv6 loopback.

```text
HEAD / HTTP/1.1
```

The request method was `HEAD`, the requested path was `/`, and the protocol was HTTP/1.1.

```text
200
```

The server successfully handled the request.

```text
curl/8.18.0
```

The client user-agent was curl.

---

# HEAD vs GET

During the lab I used both:

```bash
curl -I http://localhost
```

and:

```bash
curl http://localhost
```

`curl -I` sends a request for the HTTP headers, which resulted in a `HEAD` request appearing in the Apache access log.

A normal `curl` request resulted in:

```text
GET
```

in the access log.

This allowed the HTTP commands I ran in the terminal to be connected directly with entries written by Apache.

---

# Testing a Missing Resource

I deliberately requested a page that did not exist:

```bash
curl -I http://localhost/does-not-exist.html
```

Apache responded:

```text
HTTP/1.1 404 Not Found
```

The access log recorded the request with status:

```text
404
```

This demonstrated an important troubleshooting distinction.

A `404 Not Found` means:

```text
Client reached Apache
        |
        v
Apache processed the HTTP request
        |
        v
Requested resource was not found
```

It does not mean that the web server is unreachable.

---

# 404 vs Connection Failure

These two failures represent different layers.

## HTTP 404

Example:

```text
HTTP/1.1 404 Not Found
```

This means an HTTP response was successfully received.

Therefore:

```text
Network connection -> successful
HTTP server         -> reachable
Resource            -> not found
```

## Connection Failure

An error such as:

```text
curl: (7) Failed to connect
```

means the client could not establish the required connection.

Possible investigation areas include:

```text
Is the process running?
Is the port listening?
Is the service bound to the expected address?
Is the correct port being used?
```

This distinction became useful throughout the Tomcat, Flask, and Node.js labs.

---

# Apache Error Log

The Apache error log is located at:

```text
/var/log/apache2/error.log
```

This is useful for investigating server-side problems such as:

```text
startup failures
configuration problems
binding problems
module errors
runtime server errors
```

The initial Apache startup failure was an example of a server-side problem where error information helped identify that port 80 was already occupied.

---

# Apache Configuration on Ubuntu

The original learning material referenced the RHEL/CentOS Apache configuration path:

```text
/etc/httpd/conf/httpd.conf
```

The practical Ubuntu environment uses the Apache configuration structure under:

```text
/etc/apache2/
```

Important locations encountered during the lab included:

```text
/etc/apache2/ports.conf
/etc/apache2/sites-available/
/etc/apache2/sites-enabled/
```

This reinforces that configuration paths can differ between Linux distributions even when the underlying server concepts remain the same.

---

# Useful Apache Commands

Check Apache status:

```bash
systemctl status apache2
```

Start Apache:

```bash
sudo systemctl start apache2
```

Stop Apache:

```bash
sudo systemctl stop apache2
```

Reload Apache:

```bash
sudo systemctl reload apache2
```

Inspect port 80:

```bash
sudo ss -lntp | grep ':80'
```

Test the web server:

```bash
curl -I http://localhost
```

Inspect the document root:

```bash
ls -lah /var/www/html
```

Inspect Apache logs:

```bash
ls -lh /var/log/apache2/
```

---

# Practical Troubleshooting Lesson

The most important part of this Apache lab was the troubleshooting process.

When Apache failed, I did not immediately reinstall it or change its port.

The investigation followed:

```text
Apache failed
     |
     v
Read the error
     |
     v
"Address already in use"
     |
     v
Inspect port 80
     |
     v
NGINX owns port 80
     |
     v
Verify NGINX is actually serving HTTP
     |
     v
Stop NGINX
     |
     v
Verify port 80 is free
     |
     v
Start Apache
     |
     v
Verify Apache process
     |
     v
Verify port 80
     |
     v
Verify HTTP 200
```

This is more reliable than changing several things at once because each step produces evidence about the current state.

---

# Key Takeaways

- Apache HTTP Server can serve static web content over HTTP.
- Apache commonly uses port 80 for HTTP.
- Ubuntu uses the `apache2` package/service rather than the `httpd` naming shown in the RHEL/CentOS course examples.
- `/var/www/html` was the document root used in the practical lab.
- Installing Apache does not guarantee that the service is running.
- Two services cannot normally bind the same address/port combination independently.
- `ss -lntp` is useful for identifying which process owns a listening TCP port.
- `curl` can verify the HTTP layer after the process and socket layers have been checked.
- Static HTML changes can be served without restarting Apache.
- Apache access logs provide evidence of client requests and HTTP status codes.
- A `404` response proves that the HTTP server was reached; it is different from a connection failure.
- Troubleshooting should begin by inspecting evidence rather than immediately changing configuration.
