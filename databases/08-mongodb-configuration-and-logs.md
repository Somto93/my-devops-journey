# MongoDB Configuration and Logs

## Overview

This section covers MongoDB configuration and logging concepts from the database learning material.

The material introduces:

- `/etc/mongod.conf`
- `systemLog`
- `/var/log/mongodb/mongod.log`
- `storage`
- `dbPath`
- `journal`
- `net`
- Port `27017`
- `bindIp`
- `journalctl -u mongod`

MongoDB was not installed directly on my current Ubuntu machine during this practical, so the configuration below was **studied from the learning material rather than executed on the current host**.

The general relationship is:

```text
MongoDB Service
      ↓
mongod
      ↓
/etc/mongod.conf
      ↓
Storage + Network + Logging
      ↓
Runtime Behaviour
```

---

# 1. MongoDB Configuration File

The learning material identifies the MongoDB configuration file as:

```text
/etc/mongod.conf
```

This file contains configuration used by the MongoDB server daemon:

```text
mongod
```

Conceptually:

```text
mongod
  ↓
reads configuration
  ↓
/etc/mongod.conf
```

The configuration shown in the learning material includes sections for:

```text
systemLog
storage
net
```

---

# 2. Example Configuration from the Learning Material

The material shows configuration similar to:

```yaml
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

storage:
  dbPath: /var/lib/mongo
  journal:
    enabled: true

net:
  port: 27017
  bindIp: 127.0.0.1
```

Each section controls a different part of MongoDB's behaviour.

Conceptually:

```text
/etc/mongod.conf
│
├── systemLog
│   └── Logging
│
├── storage
│   └── Data storage
│
└── net
    └── Network behaviour
```

---

# 3. systemLog

The configuration contains:

```yaml
systemLog:
```

This section controls MongoDB logging behaviour.

The example contains:

```yaml
destination: file
```

This tells MongoDB to send its application log output to a file.

The material identifies that file as:

```text
/var/log/mongodb/mongod.log
```

---

# 4. MongoDB Application Log

The configuration specifies:

```yaml
path: /var/log/mongodb/mongod.log
```

Therefore:

```text
mongod
   ↓
Application events
   ↓
/var/log/mongodb/mongod.log
```

This log can provide evidence about MongoDB server behaviour.

For troubleshooting, this may include information relating to:

```text
Startup
Shutdown
Configuration
Network activity
Warnings
Errors
```

The exact content depends on what the MongoDB server records during operation.

---

# 5. logAppend

The material shows:

```yaml
logAppend: true
```

This configures MongoDB to append new log entries to the configured log file.

Conceptually:

```text
Existing mongod.log
       +
New log entries
       ↓
Updated mongod.log
```

This allows log information to continue accumulating in the configured file rather than treating every startup as a completely unrelated log file.

---

# 6. storage

The next configuration section shown is:

```yaml
storage:
```

This section contains settings associated with MongoDB data storage.

The learning material shows:

```yaml
dbPath: /var/lib/mongo
```

This identifies the configured location for MongoDB database data in the example.

Therefore:

```text
MongoDB data
     ↓
/var/lib/mongo
```

This is different from:

```text
/var/log/mongodb/mongod.log
```

which is used for logs.

---

# 7. Data vs Logs

The two paths have different purposes.

```text
/var/lib/mongo
```

represents the configured database data location in the material.

```text
/var/log/mongodb/mongod.log
```

represents the MongoDB application log.

Conceptually:

```text
MongoDB
│
├── Data
│   └── /var/lib/mongo
│
└── Logs
    └── /var/log/mongodb/mongod.log
```

This distinction is important when troubleshooting.

A data-storage problem and a logging problem occur at different layers.

---

# 8. Journal Setting

The material also shows:

```yaml
journal:
  enabled: true
```

under the storage configuration.

This `journal` setting is part of the MongoDB storage configuration shown in the material.

It should not be confused with the Linux command:

```bash
journalctl
```

Although both contain the word `journal`, they refer to different things.

---

# 9. MongoDB Journal vs systemd Journal

This distinction is important.

The configuration:

```yaml
storage:
  journal:
    enabled: true
```

belongs to MongoDB's storage configuration.

By contrast:

```bash
journalctl -u mongod
```

is a Linux/systemd command used to inspect service-related journal entries.

Therefore:

```text
MongoDB storage journal
          ≠
systemd journal
```

They should not be treated as the same component simply because they use similar terminology.

---

# 10. Network Configuration

The material contains:

```yaml
net:
  port: 27017
  bindIp: 127.0.0.1
```

This controls MongoDB's network behaviour.

The two important settings are:

```text
port
bindIp
```

---

# 11. MongoDB Port

The configuration shows:

```yaml
port: 27017
```

The MongoDB server therefore uses:

```text
27017
```

as the configured port in the learning material.

Conceptually:

```text
MongoDB Client
      ↓
TCP connection
      ↓
Port 27017
      ↓
mongod
```

This is comparable to the MySQL connection we previously observed:

```text
MySQL
  ↓
3306
```

and:

```text
MongoDB
   ↓
27017
```

---

# 12. bindIp

The configuration also contains:

```yaml
bindIp: 127.0.0.1
```

The address:

```text
127.0.0.1
```

is the IPv4 loopback address.

With this configuration, MongoDB is listening on the local loopback interface.

Conceptually:

```text
bindIp
   ↓
127.0.0.1
   ↓
Local machine
```

A client running on the same machine can connect through the loopback interface.

A remote machine cannot directly connect to that loopback address as though it were the MongoDB server's externally reachable interface.

---

# 13. Comparing MySQL and MongoDB Binding

This concept is very similar to what I observed during the MySQL practical.

MySQL configuration:

```text
bind-address = 127.0.0.1
```

MongoDB configuration from the material:

```text
bindIp: 127.0.0.1
```

Both demonstrate the concept of binding a database service to a network interface/address.

Conceptually:

```text
Database service
      ↓
Configured bind address
      ↓
Network interface
      ↓
Listening socket
```

---

# 14. Remote MongoDB Access

If MongoDB is configured with:

```yaml
bindIp: 127.0.0.1
```

the configuration is local-only from the network-binding perspective.

A configuration such as:

```yaml
bindIp: 0.0.0.0
```

would mean binding to all IPv4 interfaces.

However, changing a database from loopback-only to broader network exposure should not be treated as simply a connectivity fix.

Additional security considerations include:

```text
Authentication
Firewall rules
Network access controls
Host exposure
User permissions
```

A safer design may also involve binding specifically to an appropriate private interface rather than unnecessarily exposing the database on every interface.

The important principle is:

> Network reachability and database security must be considered together.

---

# 15. Configuration Does Not Prove Runtime State

Suppose the configuration contains:

```yaml
port: 27017
bindIp: 127.0.0.1
```

This tells me what MongoDB is configured to use.

It does not by itself prove that:

```text
mongod is currently running
```

or that:

```text
27017 is currently listening
```

To establish runtime state, I would inspect the running system.

For example:

```bash
sudo ss -ltnp
```

could be used on a system where MongoDB is running.

I would then look for evidence of:

```text
127.0.0.1:27017
```

and the associated process.

---

# 16. Expected Configuration-to-Runtime Relationship

If the configuration contains:

```yaml
net:
  port: 27017
  bindIp: 127.0.0.1
```

and MongoDB starts successfully, I would expect the runtime network state to correspond with those settings.

Conceptually:

```text
/etc/mongod.conf
       ↓
bindIp: 127.0.0.1
port: 27017
       ↓
mongod starts
       ↓
Expected listening socket
       ↓
127.0.0.1:27017
```

I would verify this rather than assume it.

---

# 17. systemd Journal

For a systemd-managed MongoDB service, service-related events can be inspected using:

```bash
sudo journalctl -u mongod
```

This can help investigate questions such as:

```text
Did mongod start?

Did mongod stop?

Did systemd report a failure?

Was an exit status recorded?

When did the service fail?
```

To inspect a smaller number of recent entries:

```bash
sudo journalctl -u mongod -n 50
```

---

# 18. MongoDB Application Log vs systemd Journal

MongoDB troubleshooting may involve both:

```bash
sudo journalctl -u mongod
```

and:

```text
/var/log/mongodb/mongod.log
```

They are related but should not automatically be treated as identical sources.

Conceptually:

```text
Linux / systemd
      ↓
journalctl -u mongod
```

and:

```text
MongoDB application
      ↓
/var/log/mongodb/mongod.log
```

Looking at both can provide complementary evidence.

---

# 19. Troubleshooting a Failed MongoDB Service

Suppose:

```bash
systemctl status mongod
```

reports:

```text
failed
```

A good troubleshooting process would be:

```text
Service failed
      ↓
Inspect systemd journal
      ↓
journalctl -u mongod
      ↓
Inspect MongoDB application log
      ↓
/var/log/mongodb/mongod.log
      ↓
Identify reported error
      ↓
Inspect relevant configuration
      ↓
Make targeted correction
      ↓
Restart
      ↓
Verify
```

The key principle is not to edit `mongod.conf` randomly before identifying the actual error.

---

# 20. Configuration Problems Can Affect Startup

Because `/etc/mongod.conf` controls several aspects of MongoDB operation, configuration-related failures could potentially involve different areas.

For example:

```text
Logging
Storage
Networking
```

A troubleshooting investigation should use the error evidence to determine which area needs attention.

Conceptually:

```text
mongod fails
    ↓
Read error
    ↓
Which area?
    ├── Logging
    ├── Storage
    └── Network
```

The error should guide the investigation.

---

# 21. Storage Path Investigation

The material configures:

```yaml
dbPath: /var/lib/mongo
```

If a MongoDB startup error specifically referenced the database path, I would investigate that path rather than immediately changing the network configuration.

For example, I could inspect the path using Linux commands appropriate to the reported problem.

The reasoning would be:

```text
Error references storage
        ↓
Investigate storage
```

rather than:

```text
Error references storage
        ↓
Randomly change port
```

This is an example of identifying the failing layer first.

---

# 22. Network Investigation

If MongoDB is running but a client cannot connect, the investigation changes.

I could check:

```bash
systemctl status mongod
```

and then:

```bash
sudo ss -ltnp
```

If the process is running, I would examine:

```text
Which address is it listening on?

Which port is it listening on?

Does that match /etc/mongod.conf?
```

For the configuration in the learning material, I would expect:

```text
127.0.0.1
```

and:

```text
27017
```

---

# 23. Service Running Does Not Guarantee Remote Connectivity

A service can be:

```text
active (running)
```

while a remote client still cannot connect.

For example:

```text
mongod running
      ↓
Listening only on 127.0.0.1
      ↓
Local connections possible
      ↓
Remote connection not available through that binding
```

Therefore:

```text
Service status
```

and:

```text
Network reachability
```

are different troubleshooting layers.

---

# 24. Configuration Change Workflow

If evidence shows that a MongoDB configuration change is actually required, a general workflow would be:

```text
Inspect current configuration
        ↓
Understand existing value
        ↓
Make required change
        ↓
Restart/reload as appropriate
        ↓
Check service status
        ↓
Check listening socket
        ↓
Test connection
        ↓
Inspect logs if needed
```

The important part is verification after the change.

Editing a configuration file alone does not prove that the running service is using the new value.

---

# 25. Comparing MongoDB and MySQL Configuration

The two database systems use different configuration formats, but the operational principles are similar.

```text
MySQL                         MongoDB
-----                         -------
mysqld.cnf                    mongod.conf
bind-address                  bindIp
3306                          27017
/var/log/mysql/error.log      /var/log/mongodb/mongod.log
mysql.service                 mongod service
mysqld                        mongod
```

The same DevOps reasoning can be applied:

```text
Service
   ↓
Process
   ↓
Configuration
   ↓
Port
   ↓
Logs
   ↓
Connection
```

---

# 26. Configuration Hierarchy from the Material

The MongoDB configuration shown can be visualized as:

```text
/etc/mongod.conf
│
├── systemLog
│   ├── destination: file
│   ├── logAppend: true
│   └── path: /var/log/mongodb/mongod.log
│
├── storage
│   ├── dbPath: /var/lib/mongo
│   └── journal
│       └── enabled: true
│
└── net
    ├── port: 27017
    └── bindIp: 127.0.0.1
```

This gives a useful mental model for understanding the configuration.

---

# 27. Useful Commands

The following commands are useful when working on a system where MongoDB is actually installed.

## Check service status

```bash
systemctl status mongod
```

## Inspect service journal

```bash
sudo journalctl -u mongod
```

## Inspect recent journal entries

```bash
sudo journalctl -u mongod -n 50
```

## Inspect listening TCP sockets

```bash
sudo ss -ltnp
```

## View MongoDB configuration

```bash
cat /etc/mongod.conf
```

## Inspect the MongoDB application log

```bash
sudo tail -50 /var/log/mongodb/mongod.log
```

These commands are documented here as part of the MongoDB operational workflow. They were not executed against a locally installed `mongod` instance during this practical.

---

# 28. Evidence-Based Troubleshooting

A useful MongoDB troubleshooting sequence is:

```text
Problem reported
      ↓
Check service
      ↓
Check logs
      ↓
Check process/socket
      ↓
Inspect relevant configuration
      ↓
Compare expected vs actual state
      ↓
Identify failing layer
      ↓
Make targeted change
      ↓
Restart if required
      ↓
Verify
```

For example:

```text
mongod active
     +
127.0.0.1:27017 listening
     +
local client connects
```

would provide very different evidence from:

```text
mongod failed
     +
nothing listening on 27017
```

The evidence determines the next troubleshooting step.

---

# 29. What Was Studied vs Executed

The MongoDB configuration in this document comes from the learning material.

I studied:

```text
/etc/mongod.conf
/var/log/mongodb/mongod.log
/var/lib/mongo
27017
127.0.0.1
systemLog
storage
net
```

I did not claim that these files currently exist or that `mongod` is running on my Ubuntu 26.04 machine.

This maintains an accurate distinction:

```text
Course material
      ↓
MongoDB concepts studied

Current machine
      ↓
MongoDB runtime practical deferred
```

---

# Key Takeaway

MongoDB configuration can be understood through three major areas shown in the learning material:

```text
Logging
   ↓
systemLog

Storage
   ↓
storage

Networking
   ↓
net
```

The operational relationship is:

```text
/etc/mongod.conf
       ↓
mongod
       ↓
Runtime behaviour
       ↓
Port 27017
       ↓
Client connection
```

When troubleshooting, configuration should be compared with the actual service, process, network socket, and logs.

The core principle remains:

```text
Inspect
   ↓
Identify failing layer
   ↓
Change
   ↓
Verify
```

rather than changing configuration based on assumptions.
