# MySQL Installation and Service Management

## Overview

In this lab, I installed MySQL Server on Ubuntu and verified that the database service, process, and network sockets were operating correctly.

Rather than installing MySQL immediately, I first inspected the system to determine whether MySQL was already available.

The general workflow was:

```text
Check
  ↓
Install
  ↓
Verify Service
  ↓
Identify Process
  ↓
Verify Listening Ports
  ↓
Test Client
  ↓
Connect to Database Server
```

This follows an important DevOps principle:

> Inspect the current state before making changes.

---

# 1. Check Whether MySQL Is Installed

I first checked whether the MySQL client was available:

```bash
mysql --version
```

The system responded that the command could not be found.

This indicated that the `mysql` executable was not currently available in my environment.

I also checked whether a MySQL systemd service existed:

```bash
systemctl status mysql
```

The system reported:

```text
Unit mysql.service could not be found.
```

At this point, the evidence showed that MySQL had not yet been installed as a systemd-managed service.

---

# 2. Inspect the MySQL Package

Before installing the package, I checked its package information:

```bash
apt policy mysql-server
```

The output showed:

```text
mysql-server:
  Installed: (none)
  Candidate: 8.4.11-0ubuntu0.26.04.1
```

This provided two useful pieces of information.

```text
Installed: (none)
```

confirmed that the package was not currently installed.

The `Candidate` entry showed that a version of `mysql-server` was available from the configured Ubuntu repositories.

This demonstrates the difference between:

```text
Package exists in repository
             ≠
Package is installed
```

---

# 3. Install MySQL Server

I installed MySQL Server using:

```bash
sudo apt install mysql-server
```

During the installation, systemd integration was configured.

The installation output included:

```text
Created symlink '/etc/systemd/system/multi-user.target.wants/mysql.service'
→ '/usr/lib/systemd/system/mysql.service'
```

This indicated that the MySQL service was configured to participate in normal system startup.

---

# 4. Verify the MySQL Service

After installation, I checked the service:

```bash
systemctl status mysql
```

The important parts of the output included:

```text
● mysql.service - MySQL Community Server

Loaded: loaded (/usr/lib/systemd/system/mysql.service; enabled; preset: enabled)

Active: active (running)

Main PID: 25552 (mysqld)

Status: "Server is operational"
```

This provided several pieces of information.

---

## Loaded

```text
Loaded: loaded
```

means systemd successfully found and loaded the MySQL service unit.

---

## Enabled

```text
enabled
```

means the service is configured to start automatically as part of the appropriate system boot target.

This is different from the service currently running.

---

## Active

```text
Active: active (running)
```

means the service is currently running.

Therefore:

```text
enabled
   ↓
Should start automatically at boot

active (running)
   ↓
Running right now
```

A service can potentially be:

```text
enabled but not currently running
```

or:

```text
running but not enabled for automatic startup
```

Therefore, `enabled` and `active` describe different properties.

---

# 5. MySQL Service vs MySQL Process

The systemd service is called:

```text
mysql.service
```

However, the actual MySQL server process shown by systemd was:

```text
mysqld
```

This distinction is important.

```text
MySQL
│
├── systemd service
│   └── mysql.service
│
└── database server process
    └── mysqld
```

The `d` in `mysqld` refers to the server daemon.

This is why the service status contained:

```text
Main PID: 25552 (mysqld)
```

---

# 6. Verify MySQL Listening Ports

A service reporting:

```text
active (running)
```

does not by itself prove that the expected network socket is listening.

I therefore checked the listening TCP sockets:

```bash
sudo ss -ltnp
```

The relevant output showed MySQL listening on:

```text
127.0.0.1:3306
127.0.0.1:33060
```

Both sockets were associated with:

```text
mysqld
```

This provided evidence that the MySQL server process had successfully opened its expected network sockets.

---

# 7. MySQL Port 3306

The standard MySQL client/server connection port observed during the lab was:

```text
3306
```

The socket appeared as:

```text
127.0.0.1:3306
```

This can be interpreted as:

```text
127.0.0.1
    ↓
Listening interface/address

3306
    ↓
Listening TCP port
```

Because it was bound to `127.0.0.1`, MySQL was listening through the local loopback interface.

---

# 8. MySQL Port 33060

The same `mysqld` process was also listening on:

```text
127.0.0.1:33060
```

Port `33060` is associated with the MySQL X Protocol.

Therefore, seeing two MySQL listening ports did not mean that two separate MySQL database servers were necessarily running.

The same `mysqld` process could own multiple listening sockets:

```text
mysqld
│
├── 127.0.0.1:3306
│
└── 127.0.0.1:33060
```

---

# 9. Service Status vs Listening Socket

This lab demonstrated an important troubleshooting distinction.

Running:

```bash
systemctl status mysql
```

answers a question such as:

> Does systemd consider the MySQL service to be running?

Running:

```bash
sudo ss -ltnp
```

answers questions such as:

> Is a TCP socket actually listening?

> Which IP address is it bound to?

> Which port is being used?

> Which process owns the socket?

The commands provide different evidence.

---

# 10. Verify the MySQL Client

After installation, I checked the client version again:

```bash
mysql --version
```

The output showed:

```text
mysql Ver 8.4.11-0ubuntu0.26.04.1 for Linux on x86_64 ((Ubuntu))
```

This confirmed that the MySQL client executable was now installed and available.

---

# 11. Connect to MySQL

I connected to the MySQL server using:

```bash
sudo mysql
```

The connection succeeded and displayed the MySQL monitor.

The server version was:

```text
8.4.11
```

The prompt changed to:

```text
mysql>
```

At this point, I had moved from the Linux shell into the MySQL client.

```text
Linux shell
    ↓
sudo mysql
    ↓
MySQL client
    ↓
mysqld server
    ↓
mysql>
```

---

# 12. Linux Commands vs SQL Commands

It is important to distinguish between commands executed in the Linux shell and commands executed inside MySQL.

For example:

```bash
systemctl status mysql
```

is a Linux/systemd command.

```bash
sudo ss -ltnp
```

is a Linux networking command.

```bash
mysql --version
```

starts the MySQL client executable only to display version information.

After connecting and seeing:

```text
mysql>
```

I could execute SQL commands such as:

```sql
SHOW DATABASES;
```

This distinction helps prevent commands from being entered in the wrong environment.

---

# 13. Initial MySQL Databases

After connecting, I ran:

```sql
SHOW DATABASES;
```

Before creating my own database, MySQL displayed its existing system databases:

```text
information_schema
mysql
performance_schema
sys
```

These were already present as part of the MySQL installation.

I did not modify or delete these system databases.

---

# 14. Check the Currently Selected Database

I ran:

```sql
SELECT DATABASE();
```

The result was:

```text
NULL
```

This did **not** mean that the MySQL server had no databases.

It meant that I was connected to the MySQL server but had not yet selected a database as my current working database.

This is an important distinction:

```text
Connected to MySQL server
            ≠
Database currently selected
```

---

# 15. Installation Verification Chain

By the end of the installation process, I had verified several independent layers.

```text
APT package
    ↓
mysql-server installed
    ↓
systemd
    ↓
mysql.service active
    ↓
Process
    ↓
mysqld running
    ↓
Network
    ↓
127.0.0.1:3306
127.0.0.1:33060
    ↓
Client
    ↓
mysql available
    ↓
Connection
    ↓
MySQL monitor opened successfully
```

Each layer provided additional evidence that the installation was working correctly.

---

# 16. Useful Commands

## Check whether the client exists

```bash
mysql --version
```

## Check package availability and installation state

```bash
apt policy mysql-server
```

## Install MySQL Server

```bash
sudo apt install mysql-server
```

## Check the MySQL service

```bash
systemctl status mysql
```

## Check listening TCP sockets and processes

```bash
sudo ss -ltnp
```

## Connect to MySQL

```bash
sudo mysql
```

## List databases after connecting

```sql
SHOW DATABASES;
```

## Check the currently selected database

```sql
SELECT DATABASE();
```

---

# 17. Troubleshooting Lessons

The main troubleshooting lesson from this lab was not to assume that one successful check proves that every layer is functioning.

For example:

```text
mysql.service = active
```

does not automatically prove:

```text
Port 3306 is listening
```

Similarly:

```text
Port 3306 is listening
```

does not automatically prove:

```text
A particular database user can authenticate
```

And successful authentication does not automatically prove:

```text
The user has permission to access a particular database
```

Each layer should be tested according to the problem being investigated.

A useful sequence is:

```text
Package
   ↓
Service
   ↓
Process
   ↓
Port
   ↓
Connection
   ↓
Authentication
   ↓
Authorization
   ↓
Database operation
```

---

# Key Takeaway

Installing a database server is only the beginning.

A stronger verification process is:

```text
Install
   ↓
Check service
   ↓
Identify process
   ↓
Check listening sockets
   ↓
Verify client
   ↓
Connect
   ↓
Perform database operations
```

This lab showed how Linux package management, systemd, processes, networking, and database clients all work together to provide a functioning MySQL database service.
