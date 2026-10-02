# Web/Application Tier Setup

## Overview

The web/application tier is responsible for receiving HTTP requests, executing the PHP application, communicating with the database tier, and returning the generated webpage to the client.

In my local lab, this tier runs inside:

```text
web-server
```

The main components are:

```text
Ubuntu 24.04
Apache
PHP
PHP MySQL extension
Ecommerce application
```

The request path is:

```text
Browser
   ↓
localhost:8080
   ↓
Docker port mapping
   ↓
web-server:80
   ↓
Apache
   ↓
PHP
   ↓
Application
```

---

## Entering the Web Container

From the WSL host:

```bash
sudo docker exec -it web-server bash
```

This opens a shell inside the web/application container.

---

## Inspecting the Network

The minimal Ubuntu container did not initially contain the `ip` command.

I installed:

```bash
apt update
apt install iproute2 -y
```

Then inspected the network configuration:

```bash
ip addr
```

During this lab, the web container had:

```text
172.18.0.3
```

The database container had:

```text
172.18.0.2
```

Both were connected to:

```text
two-tier-network
```

---

## Checking Listening Ports Before Apache

Before installing and starting Apache, I used:

```bash
ss -lntp
```

There was no service listening on:

```text
TCP 80
```

This established a useful baseline.

A running container does not automatically mean that a web server is running inside it.

---

## Testing Database Name Resolution

Before deploying the application, I verified that the web tier could resolve the database container:

```bash
getent hosts db-server
```

The hostname resolved to the database container.

This demonstrated Docker's internal DNS functionality on the custom network.

The application could therefore use:

```text
db-server
```

instead of relying on the container's current IP address.

---

## Installing the MariaDB Client

I installed a database client on the web tier:

```bash
apt install mariadb-client -y
```

This did not turn the web server into a database server.

It simply provided the client tools needed to test connectivity to the separate database tier.

---

## Testing the Database From the Web Tier

From `web-server`, I tested:

```bash
mariadb -h db-server -u ecomuser -p
```

After entering the database password, the connection succeeded.

I then ran:

```sql
USE ecomdb;
SELECT * FROM products;
```

All eight product records were returned.

This was important because it tested the database from the same network location as the application.

---

## Installing Apache and PHP

The web application requires Apache and PHP.

I installed:

```bash
apt install apache2 php libapache2-mod-php php-mysql -y
```

These packages provide:

```text
apache2
→ HTTP web server

php
→ PHP runtime

libapache2-mod-php
→ Apache integration for PHP

php-mysql
→ PHP support for MySQL/MariaDB connectivity
```

Without the PHP database extension, the application would not be able to use the required MySQL/MariaDB functions correctly.

---

## Checking the Apache Version

I verified Apache using:

```bash
apache2 -v
```

This confirmed that Apache had been installed.

However:

```text
Apache installed
```

does not necessarily mean:

```text
Apache running
```

These are separate conditions.

---

## Starting Apache

Because this minimal container was not using `systemd`, Apache was managed using:

```bash
service apache2 start
```

I then checked the listener:

```bash
ss -lntp | grep ':80'
```

Apache was listening on:

```text
0.0.0.0:80
```

This confirmed that the web server was accepting HTTP connections on container port 80.

---

## Apache ServerName Warning

When Apache was started or restarted, it displayed a warning similar to:

```text
AH00558: Could not reliably determine the server's fully qualified domain name
```

This warning did not mean Apache had failed.

The important evidence was that:

```bash
ss -lntp | grep ':80'
```

showed Apache listening and HTTP requests succeeded.

This reinforced an important troubleshooting lesson:

```text
Warning ≠ service failure
```

Warnings should be understood in context rather than automatically treated as the cause of an outage.

---

## Docker Port Publishing

The web container was created with:

```text
-p 8080:80
```

Therefore:

```text
WSL host port 8080
        ↓
web-server port 80
```

The application can be reached from the host using:

```text
http://localhost:8080
```

while Apache itself listens on:

```text
port 80
```

inside the container.

---

## Testing Apache From the Host

From WSL, I tested:

```bash
curl http://localhost:8080
```

Apache returned its default webpage.

This demonstrated that the path was working:

```text
WSL
 ↓
localhost:8080
 ↓
Docker port mapping
 ↓
web-server:80
 ↓
Apache
```

---

## HTTP Header Testing

Another useful test was:

```bash
curl -I http://localhost:8080
```

The response included:

```text
HTTP/1.1 200 OK
```

A successful HTTP response confirmed that the web server was reachable.

However, this test alone did not prove that the database-backed portion of the application was functioning.

---

## Web Server Document Root

Apache's default web document root was:

```text
/var/www/html
```

Initially this directory contained the standard Apache page:

```text
index.html
```

The default page had to be replaced by the ecommerce application files.

---

## Static Content vs Application Health

A web server can return HTML successfully while another application dependency is broken.

For example:

```text
Apache       ✓
HTML         ✓
CSS          ✓
Images       ✓
MariaDB      ✗
```

could still result in a webpage that partially loads.

Therefore:

```bash
curl -I http://localhost:8080
```

proves HTTP availability but does not prove the complete application stack.

---

## Checking the Apache Process

During troubleshooting, I used:

```bash
ps aux | grep '[a]pache2'
```

This showed the Apache parent process and worker processes.

Using:

```text
[a]pache2
```

is useful because it prevents the `grep` command itself from appearing as a matching result.

---

## Checking the Listener

Another important command was:

```bash
ss -lntp | grep ':80'
```

This answers a different question from checking the process.

For example:

```text
Process exists
```

and:

```text
Service is listening on the expected port
```

are related but separate pieces of evidence.

---

## Apache Logs

The Apache error log used during troubleshooting was:

```text
/var/log/apache2/error.log
```

I inspected recent entries using:

```bash
tail -n 20 /var/log/apache2/error.log
```

This exposed PHP and Apache errors generated while processing requests.

---

## Log Timestamps Matter

One troubleshooting exercise revealed an older PHP error:

```text
mysqli_sql_exception: Connection refused
```

However, current tests showed that:

```text
MariaDB was listening
Database login worked
Products were displaying
```

Therefore, the error was historical rather than evidence of the current application state.

This reinforced the importance of checking:

```text
timestamp
+
current behaviour
+
current service state
```

before treating a log entry as the current root cause.

---

## Apache Failure Troubleshooting

During a break/fix exercise, the website was unavailable.

The investigation followed this path:

```text
Website unavailable
        ↓
Check web-server container
        ↓
Container running
        ↓
Check TCP listeners
        ↓
No :80 listener
        ↓
Check Apache status
        ↓
Apache not running
        ↓
Inspect logs
        ↓
Start service
        ↓
Verify listener
        ↓
Verify HTTP
        ↓
Verify dynamic application data
```

This was more useful than immediately restarting Apache because it identified which layer was actually failing.

---

## Local HTTP Testing

Inside `web-server`, a useful test is:

```bash
curl -I http://localhost:80
```

This tests Apache without depending on Docker's host port publishing.

If this fails while the container itself is running, the investigation should focus on the web tier before investigating the host-to-container port mapping.

---

## External HTTP Testing

From WSL:

```bash
curl -I http://localhost:8080
```

tests the complete host-to-container HTTP path:

```text
WSL
 ↓
Host port 8080
 ↓
Docker
 ↓
Container port 80
 ↓
Apache
```

---

## Why Testing From Different Locations Matters

Consider:

```text
Inside web-server:
curl localhost:80
```

versus:

```text
From WSL:
curl localhost:8080
```

They test different sections of the path.

If the first works but the second fails, Apache itself is probably not the first place to investigate.

Instead, the failure exists somewhere between:

```text
WSL
 ↓
Docker port publishing
 ↓
web-server
```

This is an example of using tests to progressively isolate the failing layer.

---

## Useful Web-Tier Commands

Check Apache:

```bash
service apache2 status
```

Start Apache:

```bash
service apache2 start
```

Restart Apache after a configuration change:

```bash
service apache2 restart
```

Check processes:

```bash
ps aux | grep '[a]pache2'
```

Check TCP port 80:

```bash
ss -lntp | grep ':80'
```

Check HTTP locally:

```bash
curl -I http://localhost:80
```

Check Apache/PHP errors:

```bash
tail -n 20 /var/log/apache2/error.log
```

Test database DNS:

```bash
getent hosts db-server
```

Test the database from the web tier:

```bash
mariadb -h db-server -u ecomuser -p
```

---

## Key Lesson

A healthy web tier requires several components to work together:

```text
Container running
       ↓
Apache installed
       ↓
Apache process running
       ↓
TCP 80 listening
       ↓
PHP available
       ↓
Application files available
       ↓
Database configuration available
       ↓
Database reachable
       ↓
Application can generate dynamic content
```

The most important lesson was not to equate:

```text
container running
```

with:

```text
application working
```

or:

```text
HTTP 200
```

with:

```text
entire two-tier application healthy
```

Each layer should be verified using evidence appropriate to that layer.
