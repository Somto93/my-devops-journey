# Apache Configuration and Virtual Hosts

## Introduction

Apache can host more than one website on the same server.

The learning material demonstrated this using two websites:

```text
www.houses.com
www.oranges.com
```

Each website can have its own:

```text
ServerName
DocumentRoot
```

while both websites use the same Apache server and HTTP port.

This is known as name-based virtual hosting.

---

# Basic Virtual Host Concept

A client connects to the server on port 80 and includes the hostname it wants to access.

For example:

```text
www.houses.com
```

or:

```text
www.oranges.com
```

Apache examines the requested hostname and selects the matching virtual host configuration.

Conceptually:

```text
                     Apache
                       |
                 Port 80
                       |
          +------------+------------+
          |                         |
          v                         v
 www.houses.com              www.oranges.com
          |                         |
          v                         v
 /var/www/houses             /var/www/oranges
```

This allows multiple websites to share the same server and port.

---

# ServerName

`ServerName` identifies the hostname associated with a virtual host.

For example:

```apache
ServerName www.houses.com
```

and:

```apache
ServerName www.oranges.com
```

When Apache receives an HTTP request containing one of these hostnames, it can select the corresponding virtual host.

---

# DocumentRoot

`DocumentRoot` identifies the directory containing the website's files.

For example:

```apache
DocumentRoot /var/www/houses
```

means that the files for the Houses website are stored under:

```text
/var/www/houses
```

Similarly:

```apache
DocumentRoot /var/www/oranges
```

points Apache to:

```text
/var/www/oranges
```

for the Oranges website.

---

# Creating the Website Directories

For the practical lab, I created separate directories for the two websites:

```text
/var/www/houses
/var/www/oranges
```

This kept the content for each website separate.

The resulting structure was conceptually:

```text
/var/www/
├── html/
├── houses/
│   └── index.html
└── oranges/
    └── index.html
```

---

# Houses Website

The Houses website used:

```text
/var/www/houses/index.html
```

with content:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Houses</title>
</head>
<body>
    <h1>Welcome to Houses.com</h1>
    <p>This website is served from /var/www/houses.</p>
</body>
</html>
```

---

# Apache Virtual Host Configuration

The original learning material demonstrated a virtual host similar to:

```apache
<VirtualHost *:80>
    ServerName www.houses.com
    DocumentRoot /var/www/houses
</VirtualHost>
```

and another for:

```apache
<VirtualHost *:80>
    ServerName www.oranges.com
    DocumentRoot /var/www/oranges
</VirtualHost>
```

The practical Ubuntu lab followed the same concept using Apache's `sites-available` and `sites-enabled` configuration structure.

---

# Ubuntu Apache Site Configuration

On Ubuntu, site configuration files are commonly stored in:

```text
/etc/apache2/sites-available/
```

Enabled sites appear under:

```text
/etc/apache2/sites-enabled/
```

The second directory normally contains symbolic links to configurations in `sites-available`.

This gives a useful separation between:

```text
Configuration exists
```

and:

```text
Configuration is enabled
```

---

# Creating houses.conf

I created:

```text
/etc/apache2/sites-available/houses.conf
```

with:

```apache
<VirtualHost *:80>
    ServerName www.houses.com
    DocumentRoot /var/www/houses
</VirtualHost>
```

Breaking this down:

```text
<VirtualHost *:80>
```

means this virtual host handles requests on port 80.

```text
ServerName www.houses.com
```

identifies the hostname.

```text
DocumentRoot /var/www/houses
```

identifies the website's content directory.

---

# Testing Apache Configuration

Before enabling/reloading the configuration, I tested Apache's configuration:

```bash
sudo apache2ctl configtest
```

The result was:

```text
Syntax OK
```

This is an important step because it allows configuration syntax to be checked before applying the change.

A useful workflow is:

```text
Edit configuration
       |
       v
Test configuration
       |
       v
Enable/reload
       |
       v
Verify
```

---

# Enabling the Houses Site

I enabled the site with:

```bash
sudo a2ensite houses.conf
```

Apache created a symbolic link under:

```text
/etc/apache2/sites-enabled/
```

pointing back to:

```text
/etc/apache2/sites-available/houses.conf
```

Conceptually:

```text
sites-available/houses.conf
          ^
          |
          | symbolic link
          |
sites-enabled/houses.conf
```

This is how Ubuntu Apache distinguishes between available and enabled site configurations.

---

# Inspecting Apache Virtual Hosts

I used:

```bash
sudo apache2ctl -S
```

to inspect Apache's virtual-host configuration.

Before adding the custom sites, Apache showed the default server configuration.

After enabling `houses.conf`, the output included:

```text
www.houses.com
```

This confirmed that Apache had parsed and recognised the new virtual host.

---

# Reloading Apache

After the configuration was valid and enabled, I used:

```bash
sudo systemctl reload apache2
```

rather than stopping and starting the service.

The Apache service remained running and performed a graceful reload.

This demonstrated the difference between:

```text
restart
```

and:

```text
reload
```

For this configuration change, a reload allowed Apache to read the updated configuration without a full stop/start cycle.

---

# Hostname Resolution

Creating:

```apache
ServerName www.houses.com
```

inside Apache does not automatically make the operating system resolve that hostname to the local server.

Two different mechanisms are involved:

```text
Hostname resolution
        |
        v
Which IP address should www.houses.com use?

Apache virtual host selection
        |
        v
Which Apache site should handle that hostname?
```

Both need to work for the request to reach the intended local website.

---

# Checking www.houses.com Resolution

Before modifying local hostname resolution, I ran:

```bash
getent hosts www.houses.com
```

The hostname resolved to real public IP addresses.

The results included addresses such as:

```text
The hostname resolved to public IP addresses rather than the local machine.

This showed that configuring `ServerName www.houses.com` in Apache does not automatically make the hostname resolve to the local Apache server.```

This was an important discovery.

If I simply ran:

```bash
curl http://www.houses.com
```

without changing name resolution, the request could be directed toward the public hostname instead of my local Apache lab.

Therefore, I needed to deliberately map the lab hostname to my local machine.

---

# Using /etc/hosts

I added a local hostname mapping:

```text
127.0.0.1 www.houses.com
```

to:

```text
/etc/hosts
```

After the change:

```bash
getent hosts www.houses.com
```

returned:

```text
127.0.0.1 www.houses.com
```

Now the request path became:

```text
www.houses.com
      |
      v
/etc/hosts
      |
      v
127.0.0.1
      |
      v
Apache :80
      |
      v
ServerName www.houses.com
      |
      v
/var/www/houses
```

---

# Testing the Houses Virtual Host

I requested:

```bash
curl http://www.houses.com
```

Apache returned:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Houses</title>
</head>
<body>
    <h1>Welcome to Houses.com</h1>
    <p>This website is served from /var/www/houses.</p>
</body>
</html>
```

This verified the complete chain:

```text
Hostname resolution
        +
TCP connection to Apache
        +
Host-based virtual host selection
        +
Correct DocumentRoot
        +
Correct HTML response
```

---

# Creating the Oranges Virtual Host

I then created a second site for:

```text
www.oranges.com
```

using:

```text
/var/www/oranges
```

The Apache configuration was:

```apache
<VirtualHost *:80>
    ServerName www.oranges.com
    DocumentRoot /var/www/oranges
</VirtualHost>
```

The configuration file was:

```text
/etc/apache2/sites-available/oranges.conf
```

and the site was enabled in Apache.

---

# Oranges Website

The Oranges website contained:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Oranges</title>
</head>
<body>
    <h1>Welcome to Oranges.com</h1>
    <p>This website is served from /var/www/oranges.</p>
</body>
</html>
```

Requesting:

```bash
curl http://www.oranges.com
```

returned the Oranges website.

---

# Final Virtual Host State

After configuring both websites, I inspected Apache again:

```bash
sudo apache2ctl -S
```

The output showed:

```text
*:80 is a NameVirtualHost
 default server Somto.localdomain (/etc/apache2/sites-enabled/000-default.conf:1)
 port 80 namevhost Somto.localdomain (/etc/apache2/sites-enabled/000-default.conf:1)
 port 80 namevhost www.houses.com (/etc/apache2/sites-enabled/houses.conf:1)
 port 80 namevhost www.oranges.com (/etc/apache2/sites-enabled/oranges.conf:1)
```

This confirmed that Apache knew about three port-80 virtual hosts:

```text
Default site
www.houses.com
www.oranges.com
```

---

# How Apache Chooses the Website

Both custom sites listen on:

```text
*:80
```

Therefore, the port alone does not distinguish them.

Apache uses the hostname from the HTTP request to determine which virtual host should handle the request.

For example:

```text
GET / HTTP/1.1
Host: www.houses.com
```

can be matched to:

```apache
ServerName www.houses.com
```

and Apache serves content from:

```text
/var/www/houses
```

A request with:

```text
Host: www.oranges.com
```

matches:

```apache
ServerName www.oranges.com
```

and Apache serves:

```text
/var/www/oranges
```

Therefore:

```text
Same server
Same IP
Same port
Different hostname
Different website
```

---

# Virtual Hosting Request Flow

The complete request flow can be represented as:

```text
Client requests www.houses.com
            |
            v
Hostname resolves to server IP
            |
            v
Connection reaches Apache port 80
            |
            v
Apache reads requested hostname
            |
            v
ServerName www.houses.com matches
            |
            v
DocumentRoot /var/www/houses
            |
            v
index.html returned
```

For the second website:

```text
Client requests www.oranges.com
            |
            v
Hostname resolves to server IP
            |
            v
Connection reaches Apache port 80
            |
            v
Apache reads requested hostname
            |
            v
ServerName www.oranges.com matches
            |
            v
DocumentRoot /var/www/oranges
            |
            v
index.html returned
```

---

# Configuration vs Content Changes

The lab also reinforced the difference between changing website content and changing Apache configuration.

If I modify:

```text
/var/www/houses/index.html
```

that is a content change.

Apache can serve the updated file on the next request.

If I modify:

```text
/etc/apache2/sites-available/houses.conf
```

that is an Apache configuration change.

The configuration should be tested and then reloaded as appropriate:

```bash
sudo apache2ctl configtest
sudo systemctl reload apache2
```

---

# Useful Commands

Check Apache virtual hosts:

```bash
sudo apache2ctl -S
```

Test Apache configuration:

```bash
sudo apache2ctl configtest
```

Enable a site:

```bash
sudo a2ensite houses.conf
```

Reload Apache:

```bash
sudo systemctl reload apache2
```

Check hostname resolution:

```bash
getent hosts www.houses.com
```

Test a virtual host:

```bash
curl http://www.houses.com
```

Inspect available sites:

```bash
ls -l /etc/apache2/sites-available/
```

Inspect enabled sites:

```bash
ls -l /etc/apache2/sites-enabled/
```

---

# Troubleshooting Virtual Hosts

If a virtual host does not return the expected website, I can investigate the layers individually.

```text
Does the hostname resolve correctly?
             |
             v
Does it resolve to the intended server?
             |
             v
Is Apache running?
             |
             v
Is Apache listening on port 80?
             |
             v
Does apache2ctl -S show the virtual host?
             |
             v
Does ServerName match the requested hostname?
             |
             v
Is DocumentRoot correct?
             |
             v
Does the expected index file exist?
             |
             v
What do the Apache logs show?
```

Useful commands include:

```bash
getent hosts <hostname>
systemctl status apache2
sudo ss -lntp | grep ':80'
sudo apache2ctl configtest
sudo apache2ctl -S
curl -I http://<hostname>
```

---

# Key Takeaways

- Apache can host multiple websites on the same server.
- `ServerName` identifies the hostname associated with a virtual host.
- `DocumentRoot` identifies the directory containing that site's content.
- Multiple virtual hosts can share the same IP address and port.
- Apache uses the requested hostname to choose between name-based virtual hosts.
- Ubuntu stores site configurations under `/etc/apache2/sites-available/`.
- `a2ensite` enables a site by creating the appropriate configuration link under `sites-enabled`.
- `apache2ctl configtest` should be used to validate configuration before applying changes.
- `apache2ctl -S` is useful for seeing how Apache interprets its virtual-host configuration.
- Apache configuration and hostname resolution are separate concerns.
- `/etc/hosts` can provide local hostname resolution for a lab environment.
- A real public domain may already resolve on the Internet, so hostname resolution should be inspected rather than assumed.
- Configuration changes can be applied with an appropriate Apache reload.
- Virtual-host troubleshooting should verify DNS/host resolution, Apache configuration, listening sockets, document roots, and HTTP responses separately.
