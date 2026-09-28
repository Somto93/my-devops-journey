# MongoDB Installation and Service

## Overview

This section covers the MongoDB installation and service-management concepts from the database learning material.

Unlike the MySQL section, MongoDB was **not installed directly on my current Ubuntu 26.04 machine during this practical**.

Instead, I studied:

- MongoDB deployment options
- MongoDB package repositories
- MongoDB server packages
- `mongod`
- MongoDB service management
- `systemctl`
- Service troubleshooting
- The difference between the MongoDB server and client shell

The main conceptual workflow is:

```text
Configure Package Repository
        ↓
Install MongoDB Package
        ↓
Start MongoDB Service
        ↓
Check Service Status
        ↓
Verify Server
        ↓
Connect Using MongoDB Shell
```

---

# 1. MongoDB

MongoDB is a NoSQL database system.

Unlike the relational table structure used by MySQL, MongoDB works with concepts such as:

```text
Database
   ↓
Collection
   ↓
Document
   ↓
Fields
```

A simplified comparison is:

```text
MySQL                MongoDB
-----                -------
Database             Database
Table                Collection
Row                  Document
Column               Field
```

The detailed MongoDB data operations are covered separately in:

```text
09-mongodb-shell-and-operations.md
```

---

# 2. MongoDB Deployment

The learning material introduces MongoDB deployment through options including:

```text
MongoDB
├── Cloud
└── Server
```

A cloud deployment means that MongoDB is provided through a cloud-based environment.

A server deployment involves running MongoDB server software on a system.

For the server approach, the general installation process involves:

```text
Operating System
      ↓
Package Repository
      ↓
MongoDB Package
      ↓
MongoDB Server
      ↓
MongoDB Service
```

---

# 3. Package Repositories

The learning material demonstrates configuring an appropriate MongoDB package repository before installing the MongoDB server package.

This is important because a Linux package manager can only install packages that are available through its configured package sources.

Conceptually:

```text
Package Manager
      ↓
Configured Repositories
      ↓
Available Packages
```

If the required repository is not configured, the package manager may not be able to locate the MongoDB package.

---

# 4. What I Observed on My Ubuntu Machine

Before attempting installation, I checked whether MongoDB was already available.

I ran:

```bash
mongod --version
```

The result was:

```text
mongod: command not found
```

This showed that the MongoDB server executable was not currently available on the system.

---

# 5. Check the MongoDB Shell

I also checked:

```bash
mongosh --version
```

The result was:

```text
mongosh: command not found
```

Therefore, neither the MongoDB server daemon nor the modern MongoDB shell was installed on the machine.

At this point:

```text
mongod
  ↓
Not installed

mongosh
  ↓
Not installed
```

---

# 6. mongod vs mongosh

These commands represent different components.

## mongod

```text
mongod
```

is the MongoDB server daemon.

Its role is comparable conceptually to:

```text
mysqld
```

in MySQL.

Therefore:

```text
MySQL                 MongoDB
-----                 -------
mysqld                mongod
Server daemon         Server daemon
```

---

## mongosh

```text
mongosh
```

is a MongoDB shell/client used to interact with a MongoDB server.

Its role is conceptually similar to the MySQL client:

```text
mysql
```

Therefore:

```text
MySQL                 MongoDB
-----                 -------
mysql                 mongosh
Client                Client
```

This distinction is important.

A database server and a database client are not the same component.

---

# 7. Server and Client Architecture

The relationship can be represented as:

```text
mongosh
MongoDB Client
     |
     | connection
     ↓
mongod
MongoDB Server
     |
     ↓
Databases
     |
     ↓
Collections
     |
     ↓
Documents
```

This follows the same client/server concept observed with MySQL:

```text
mysql
Client
   |
   ↓
mysqld
Server
```

---

# 8. Search Ubuntu Packages

On my machine, I investigated the packages available through the currently configured Ubuntu repositories:

```bash
apt search mongodb 2>/dev/null | head -20
```

The search returned MongoDB-related packages and libraries, but it did not provide the MongoDB server package required for the course installation workflow.

This demonstrated that searching for a term such as:

```text
mongodb
```

does not necessarily mean that every result is the MongoDB database server itself.

Results may instead include:

- Drivers
- Libraries
- Plugins
- Integration packages
- Software with MongoDB support

The package name and purpose therefore need to be checked before installation.

---

# 9. Check mongodb-org

I also checked:

```bash
apt policy mongodb-org
```

The system reported:

```text
Unable to locate package mongodb-org
```

This indicated that `mongodb-org` was not available from the package sources configured on this machine at that time.

This is an important package-management troubleshooting clue.

The message:

```text
Unable to locate package
```

is different from:

```text
Service failed to start
```

They occur at different layers.

---

# 10. Package Problem vs Service Problem

If I see:

```text
Unable to locate package mongodb-org
```

the service has not yet reached the stage where it can start.

The problem occurs earlier:

```text
Package repository/source
       ↓
Package availability
       ↓
Installation
       ↓
Service
```

Therefore, troubleshooting:

```text
systemctl status mongod
```

would not solve a package-discovery problem if MongoDB has not been installed.

This reinforces the importance of identifying the failing layer first.

---

# 11. Course Installation Environment

The learning material demonstrates MongoDB installation using a package-management workflow that includes:

```bash
yum install mongodb-org
```

The material then manages MongoDB using:

```bash
systemctl
```

The course example therefore represents a Linux environment using `yum` for package installation.

My current practical environment is Ubuntu and uses:

```bash
apt
```

for package management.

Therefore, I should not blindly copy:

```bash
yum install mongodb-org
```

onto my Ubuntu machine.

The operating system and package-management environment must be considered first.

---

# 12. Package Manager Difference

The distinction from this lab is:

```text
Course Environment
       ↓
yum
```

compared with:

```text
My Ubuntu Environment
       ↓
apt
```

The underlying MongoDB concepts remain useful, but installation commands can differ between Linux distributions.

This is why identifying the operating system is important before following package installation instructions.

---

# 13. Check the Operating System

I verified my operating system using:

```bash
cat /etc/os-release | head -6
```

The output identified the machine as:

```text
Ubuntu 26.04.1 LTS
```

with:

```text
VERSION_ID="26.04"
VERSION_CODENAME=resolute
```

This confirmed that the package-management instructions needed to be appropriate for Ubuntu rather than copied directly from the `yum`-based course example.

---

# 14. Why I Did Not Force the Installation

At this point, I did not add an unrelated repository or force packages intended for another environment onto the machine simply to make the installation command work.

Instead, the MongoDB runtime practical was deferred until I use an appropriate supported environment or a container-based environment later in my DevOps learning.

This avoids turning:

```text
Learning MongoDB
```

into:

```text
Forcing incompatible package configuration
```

The important DevOps principle is:

> Understand the environment before changing it.

---

# 15. MongoDB Installation Workflow from the Learning Material

The learning material demonstrates the general process:

```text
Configure MongoDB repository
        ↓
Install mongodb-org
        ↓
MongoDB server becomes available
        ↓
Manage mongod service
```

The exact repository configuration and package-manager commands depend on the Linux environment being used.

---

# 16. Start MongoDB Service

After installation, the learning material demonstrates starting MongoDB using:

```bash
systemctl start mongod
```

This tells `systemd` to start:

```text
mongod
```

The relationship is:

```text
systemd
   ↓
mongod service
   ↓
MongoDB server process
```

---

# 17. Check MongoDB Service Status

The learning material then checks the service using:

```bash
systemctl status mongod
```

This is similar to what I used with MySQL:

```bash
systemctl status mysql
```

Conceptually:

```text
MySQL
systemctl status mysql

MongoDB
systemctl status mongod
```

The exact service unit names differ, but the Linux service-management principle is the same.

---

# 18. What systemctl status Helps Determine

For an installed MongoDB service, checking:

```bash
systemctl status mongod
```

can help determine whether the service is:

```text
active
inactive
failed
```

It can also provide information such as:

```text
Service unit
Main process
Recent service messages
Exit information
```

This makes service status an early troubleshooting step when the database server is not behaving as expected.

---

# 19. If mongod Fails to Start

If:

```bash
systemctl status mongod
```

reported that the service had failed, I should not immediately start changing random configuration values.

The next step would be to gather more evidence.

A useful command is:

```bash
sudo journalctl -u mongod
```

This displays systemd journal entries associated with the MongoDB service.

For a smaller set of recent entries:

```bash
sudo journalctl -u mongod -n 50
```

The workflow becomes:

```text
MongoDB does not work
       ↓
Check service status
       ↓
Service failed
       ↓
Inspect service logs
       ↓
Identify actual error
       ↓
Determine failing layer
       ↓
Make targeted change
       ↓
Restart and verify
```

---

# 20. systemd Journal

For a systemd-managed MongoDB installation:

```bash
sudo journalctl -u mongod
```

provides service-related events recorded by the system journal.

This is useful for questions such as:

```text
Did systemd attempt to start MongoDB?

Did the service exit?

Was an error reported during startup?

When did the service fail?

Did it restart?
```

The journal is therefore an important troubleshooting source.

---

# 21. MongoDB Also Has an Application Log

The learning material also identifies a MongoDB application log:

```text
/var/log/mongodb/mongod.log
```

This gives us two useful sources of information:

```text
systemd journal
      ↓
journalctl -u mongod
```

and:

```text
MongoDB application log
      ↓
/var/log/mongodb/mongod.log
```

These logs will be covered in more detail in:

```text
08-mongodb-configuration-and-logs.md
```

---

# 22. Service, Process, and Port Are Different Layers

As with MySQL, a MongoDB investigation should distinguish between:

```text
Service
Process
Port
Connection
```

For example:

```text
systemctl status mongod
```

checks the service layer.

A socket inspection command such as:

```bash
sudo ss -ltnp
```

can be used to inspect listening TCP sockets and the processes associated with them.

The learning material later identifies MongoDB's default port as:

```text
27017
```

Therefore, in a running MongoDB environment, I could compare:

```text
Service state
      ↓
mongod process
      ↓
Listening socket
      ↓
MongoDB connection
```

---

# 23. Installation Verification

After installing a database server, installation should not be considered verified merely because the package manager completed.

A stronger verification chain would be:

```text
Package installed
       ↓
Executable available
       ↓
Service exists
       ↓
Service running
       ↓
Process running
       ↓
Expected port listening
       ↓
Client can connect
```

This is the same evidence-based approach used during the MySQL practical.

---

# 24. MySQL and MongoDB Comparison

The database server components can be compared conceptually:

```text
MySQL                        MongoDB
-----                        -------
mysql-server                 mongodb-org
mysql.service                mongod service
mysqld                       mongod
mysql                        mongo/mongosh
3306                         27017
mysqld.cnf                   mongod.conf
MySQL error log              mongod.log
```

The exact installation commands and configuration details depend on the environment.

---

# 25. What Was Actually Executed

On my Ubuntu machine, I actually executed checks including:

```bash
mongod --version
```

```bash
mongosh --version
```

```bash
apt search mongodb 2>/dev/null | head -20
```

```bash
apt policy mongodb-org
```

```bash
cat /etc/os-release | head -6
```

These checks established that MongoDB was not installed and that `mongodb-org` was not available through the package sources configured on the machine at that time.

---

# 26. What Was Studied Rather Than Executed

The following MongoDB service workflow was studied from the learning material:

```bash
yum install mongodb-org
```

```bash
systemctl start mongod
```

```bash
systemctl status mongod
```

I did **not** present these commands as successfully executed on my Ubuntu 26.04 machine.

This distinction keeps the documentation accurate:

```text
Executed
   ↓
Actual evidence from my machine

Studied
   ↓
Concept demonstrated by learning material
```

---

# 27. Troubleshooting Scenario

Suppose MongoDB has been installed on a suitable environment, but:

```bash
systemctl status mongod
```

reports:

```text
failed
```

A good next step would be to inspect evidence such as:

```bash
sudo journalctl -u mongod -n 50
```

Then I would interpret the reported error before deciding what to change.

I should not immediately assume:

```text
wrong port
bad configuration
permissions problem
network problem
```

without evidence.

The failure could originate from different layers.

---

# 28. Troubleshooting Layers

A useful MongoDB troubleshooting model is:

```text
Repository
    ↓
Package
    ↓
Executable
    ↓
Service
    ↓
Process
    ↓
Configuration
    ↓
Port
    ↓
Connection
    ↓
Authentication
    ↓
Database Operation
```

The goal is to identify which layer has failed.

For example:

```text
Unable to locate package
```

points toward the package/repository layer.

While:

```text
mongod service failed
```

means installation progressed further and the service/runtime layer now needs investigation.

These should not be treated as the same problem.

---

# 29. Useful Commands

## Check whether the MongoDB server executable exists

```bash
mongod --version
```

## Check whether the MongoDB shell exists

```bash
mongosh --version
```

## Search available Ubuntu packages

```bash
apt search mongodb
```

## Inspect mongodb-org package availability

```bash
apt policy mongodb-org
```

## Identify the operating system

```bash
cat /etc/os-release
```

## Start MongoDB in the course service example

```bash
systemctl start mongod
```

## Check MongoDB service status

```bash
systemctl status mongod
```

## Inspect systemd journal entries

```bash
sudo journalctl -u mongod
```

## Inspect recent service journal entries

```bash
sudo journalctl -u mongod -n 50
```

## Inspect listening TCP sockets

```bash
sudo ss -ltnp
```

---

# 30. DevOps Lesson

This section reinforced an important DevOps principle:

```text
Do not copy commands blindly.
```

Before installing software, identify:

```text
Operating system
      ↓
Distribution/version
      ↓
Package manager
      ↓
Required repository
      ↓
Correct package
      ↓
Service name
```

Only then should installation proceed.

A command that is appropriate for one Linux distribution may not be appropriate for another.

---

# Key Takeaway

The MongoDB installation section demonstrated the same layered architecture that appeared during the MySQL practical:

```text
Repository
     ↓
Package
     ↓
Service
     ↓
Daemon
     ↓
Configuration
     ↓
Network Port
     ↓
Client
     ↓
Database Operations
```

For MongoDB:

```text
MongoDB repository
      ↓
mongodb-org
      ↓
mongod service
      ↓
mongod process
      ↓
27017
      ↓
mongo/mongosh client
```

The most important troubleshooting lesson is to identify the failing layer before making changes.

On my current machine, the MongoDB runtime practical was intentionally deferred rather than presenting an unexecuted or unsuitable installation procedure as a successful practical.
