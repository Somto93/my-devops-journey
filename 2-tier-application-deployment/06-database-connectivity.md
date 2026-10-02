# Database Connectivity Between Application Tiers

## Overview

In a two-tier application, installing and configuring the web server and database server individually is not enough.

The two tiers must be able to communicate.

In this lab, the communication path is:

```text
web-server
172.18.0.3
     │
     │ TCP 3306
     ▼
db-server
172.18.0.2
     │
     ▼
MariaDB
```

The application uses:

```text
DB_HOST=db-server
```

rather than directly using the database container's IP address.

---

## The Connection Path

When PHP attempts to connect to MariaDB, several things must work:

```text
PHP Application
      ↓
DB_HOST value
      ↓
Hostname resolution
      ↓
Network route
      ↓
TCP connection
      ↓
MariaDB listener
      ↓
Database authentication
      ↓
Database privileges
      ↓
Database/table/data
```

A failure at any layer can prevent the application from retrieving product information.

---

## Step 1 — Database Host Configuration

The application needs to know where the database server is located.

In this lab:

```text
DB_HOST=db-server
```

The hostname corresponds to the name of the database Docker container.

The application therefore attempts to connect to:

```text
db-server:3306
```

---

## Step 2 — Name Resolution

Before connecting to MariaDB, the hostname must resolve.

From `web-server`:

```bash
getent hosts db-server
```

During the lab this resolved to:

```text
172.18.0.2 db-server
```

This demonstrated that Docker DNS could resolve the database container name.

If this test failed, I would investigate name resolution or Docker network membership before investigating database credentials.

---

## Step 3 — Network Connectivity

Both containers were attached to:

```text
two-tier-network
```

This provides the network path between them.

The database port did not need to be published to the WSL host because communication occurs directly across the Docker network:

```text
web-server
     │
     │ two-tier-network
     ▼
db-server:3306
```

---

## Step 4 — MariaDB Must Be Running

Even with correct networking, the application cannot connect if MariaDB is not running.

On `db-server`:

```bash
ps aux | grep mariadbd
```

can be used to inspect the MariaDB process.

The service can also be checked using:

```bash
service mariadb status
```

in this container environment.

---

## Step 5 — MariaDB Must Be Listening

A running process does not automatically prove that the expected network socket is available.

I checked:

```bash
ss -lntp | grep 3306
```

The required lab configuration was:

```text
0.0.0.0:3306
```

This showed that MariaDB was listening for TCP connections through the container's IPv4 interfaces.

---

## Loopback-Only Listening

Initially MariaDB listened on:

```text
127.0.0.1:3306
```

This would allow connections originating inside `db-server`, but not the separate `web-server` container.

The configuration was changed from:

```ini
bind-address = 127.0.0.1
```

to:

```ini
bind-address = 0.0.0.0
```

After restarting MariaDB, the listener was verified again.

---

## Step 6 — Test From the Correct Tier

One of the most useful tests was performed from `web-server`:

```bash
mariadb -h db-server -u ecomuser -p
```

This test is stronger than logging into MariaDB locally from `db-server`.

A successful local login only proves:

```text
Local client
    ↓
Local MariaDB
```

A successful login from `web-server` proves much more:

```text
web-server
    ↓
Docker DNS
    ↓
Docker network
    ↓
TCP 3306
    ↓
MariaDB listener
    ↓
Authentication
```

---

## Why the `-h` Option Matters

This command:

```bash
mariadb -u ecomuser -p
```

does not explicitly test the remote two-tier path.

For this architecture, the appropriate test is:

```bash
mariadb -h db-server -u ecomuser -p
```

because it targets the actual database tier used by the application.

---

## Step 7 — Authentication

After the TCP connection reaches MariaDB, the database server authenticates the account.

The application account is:

```text
'ecomuser'@'%'
```

The `%` represents MariaDB host matching.

The account password used in this lab is supplied to the application through:

```text
DB_PASSWORD
```

---

## Step 8 — Database Privileges

Successful authentication does not automatically mean that the account can access every database.

The application user was granted:

```sql
GRANT ALL PRIVILEGES ON ecomdb.* TO 'ecomuser'@'%';
```

The grants can be inspected using:

```sql
SHOW GRANTS FOR 'ecomuser'@'%';
```

The important scope is:

```text
ecomdb.*
```

which represents objects inside the ecommerce database.

---

## Step 9 — Verify the Actual Data

After connecting from the web tier:

```sql
USE ecomdb;
SELECT * FROM products;
```

returned the eight ecommerce product records.

This demonstrated that the network path and the application database access were functioning.

---

# Understanding Common Connection Errors

Different errors provide evidence about how far the connection progressed.

## Connection Refused

An error such as:

```text
Connection refused
```

suggests that the connection did not successfully reach an accepting service on the requested destination and port.

Useful checks include:

```bash
service mariadb status
```

```bash
ss -lntp | grep 3306
```

and checking the MariaDB bind configuration.

Conceptually:

```text
web-server
    │
    │ TCP connection attempt
    ▼
db-server:3306
    X
No accepting connection
```

Possible areas to investigate include:

```text
MariaDB stopped
Wrong destination
Wrong port
Incorrect bind-address
Network path
Firewall/network filtering
```

The exact cause should be established from evidence rather than assumed from the error alone.

---

## Access Denied

During a troubleshooting exercise, the remote client returned an error similar to:

```text
ERROR 1045 (28000):
Access denied for user 'ecomuser'@'172.18.0.3'
```

This tells us something very different from `Connection refused`.

MariaDB was able to identify:

```text
user = ecomuser
source = 172.18.0.3
```

Therefore the request had reached MariaDB.

The investigation should shift toward:

```text
Username
Password
Host matching
Authentication configuration
Account configuration
```

rather than immediately assuming the network is broken.

---

## Authentication vs Authorization

These concepts should also be separated.

### Authentication

```text
Who are you?
```

Examples:

```text
Username
Password
Authentication plugin
Host matching
```

### Authorization

```text
What are you allowed to do?
```

Examples:

```text
Can the user access ecomdb?
Can the user SELECT from products?
Can the user INSERT records?
```

A user can successfully authenticate but still receive permission errors when attempting unauthorized database operations.

---

# Troubleshooting From the Application Symptom

Suppose the report is:

```text
The website opens, but products are missing.
```

This tells me that at least some of the web path is functioning.

Instead of restarting everything, I can investigate progressively.

```text
Website loads
      ↓
Apache likely responding
      ↓
Check dynamic product output
      ↓
Inspect application DB configuration
      ↓
Test DB connection from web-server
      ↓
Check MariaDB listener
      ↓
Check authentication
      ↓
Check privileges
      ↓
Check products table/data
```

---

## Testing Application Output

From WSL:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

If eight product lines appear, the complete application/database path is functioning.

If the page responds but those dynamic lines are absent, further investigation is required.

---

## Inspecting Application Configuration

The PHP application reads:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

During troubleshooting, these can be checked in the Apache environment configuration.

For example:

```bash
grep '^export DB_' /etc/apache2/envvars
```

However, configuration files show what is configured on disk.

They do not always prove what a currently running process actually inherited.

---

## Inspecting the Running Apache Environment

During the lab, I identified the Apache parent process:

```bash
ps aux | grep '[a]pache2'
```

I then inspected its environment through `/proc`.

Conceptually:

```bash
tr '\0' '\n' < /proc/<APACHE_PARENT_PID>/environ | grep '^DB_'
```

This provided stronger evidence that the running Apache process had actually inherited the database environment variables.

---

## Historical Log Errors

During one troubleshooting exercise, Apache's error log contained:

```text
mysqli_sql_exception: Connection refused
```

But subsequent tests showed:

```text
MariaDB listening             ✓
Remote MariaDB login          ✓
Product query                 ✓
Application product output    ✓
```

The error log entry had an older timestamp.

Therefore, it described a previous failure rather than the current state.

This demonstrated:

```text
Log message
    +
Timestamp
    +
Current tests
    =
Useful evidence
```

A log entry without time context can lead to the wrong conclusion.

---

# Layer-by-Layer Database Connectivity Checklist

When the application cannot retrieve database content, I can work through the following path:

```text
1. Is the web application responding?
              ↓
2. Is DB_HOST correct?
              ↓
3. Does db-server resolve?
              ↓
4. Can web-server reach the database path?
              ↓
5. Is MariaDB running?
              ↓
6. Is TCP 3306 listening?
              ↓
7. Is MariaDB bound to a reachable interface?
              ↓
8. Can ecomuser authenticate?
              ↓
9. Does ecomuser have the required privileges?
              ↓
10. Does ecomdb exist?
              ↓
11. Does products exist?
              ↓
12. Does products contain the expected rows?
```

The goal is not to run every command automatically.

The goal is to use the current evidence to decide which layer should be tested next.

---

# Key Lesson

The most important lesson from database connectivity troubleshooting was learning to interpret evidence rather than simply seeing:

```text
Database error
```

and assuming:

```text
Database server is broken.
```

Different symptoms point toward different layers.

For example:

```text
Hostname cannot resolve
→ investigate name resolution

Connection refused
→ investigate service/listener/network path

Access denied
→ investigate authentication/account configuration

Permission denied after login
→ investigate privileges

Successful query but application still fails
→ investigate application/runtime configuration
```

Understanding how far a request progressed through the connection path makes troubleshooting faster, safer, and more systematic.
