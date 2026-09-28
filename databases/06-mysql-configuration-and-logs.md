# MySQL Configuration and Logs

## Overview

After installing MySQL and working with databases, tables, users, and privileges, I inspected how the MySQL server was configured and where it recorded operational events.

The main areas covered were:

- MySQL configuration locations
- Server-specific configuration
- `mysqld.cnf`
- `bind-address`
- `mysqlx-bind-address`
- MySQL ports
- Comparing configuration with runtime state
- MySQL error logs
- MySQL startup sequence
- Initialization warnings
- Root authentication configuration

The main troubleshooting principle was:

```text
Configuration
      ↓
Expected behaviour
      ↓
Runtime inspection
      ↓
Actual behaviour
      ↓
Logs
      ↓
Evidence about events/errors
```

---

# 1. Inspect MySQL Configuration Search Locations

I first ran:

```bash
mysql --help | grep -A 1 "Default options"
```

The output showed:

```text
Default options are read from the following files in the given order:
/etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf
```

This showed locations from which the MySQL client can read option files.

An important distinction is that this output should not automatically be interpreted as a complete list of every configuration file used by the MySQL server.

I therefore inspected the MySQL configuration directories directly.

---

# 2. Inspect /etc/mysql

I ran:

```bash
ls -l /etc/mysql/
```

The directory contained entries including:

```text
conf.d/
debian-start
debian.cnf
my.cnf
my.cnf.fallback
mysql.cnf
mysql.conf.d/
```

The `my.cnf` entry was a symbolic link:

```text
my.cnf -> /etc/alternatives/my.cnf
```

This demonstrated that MySQL configuration on Ubuntu can involve multiple files and directories rather than one single configuration file.

Conceptually:

```text
/etc/mysql/
│
├── my.cnf
├── mysql.cnf
├── conf.d/
└── mysql.conf.d/
```

---

# 3. Inspect Server Configuration Files

I inspected:

```bash
ls -l /etc/mysql/mysql.conf.d/
```

The directory contained:

```text
mysql.cnf
mysqld.cnf
```

The important server configuration file for this practical was:

```text
/etc/mysql/mysql.conf.d/mysqld.cnf
```

The name is significant:

```text
mysqld
```

is the MySQL server daemon.

Therefore:

```text
mysqld.cnf
     ↓
Configuration associated with the MySQL server daemon
```

---

# 4. Inspect Network-Related Configuration

Instead of reading the entire configuration file when I only needed particular settings, I searched for relevant network configuration:

```bash
grep -nE '^(bind-address|mysqlx-bind-address|port)' /etc/mysql/mysql.conf.d/mysqld.cnf
```

The output showed:

```text
31:bind-address         = 127.0.0.1
32:mysqlx-bind-address  = 127.0.0.1
```

This provided evidence about the network interfaces to which MySQL was configured to bind.

---

# 5. Understanding bind-address

The configuration contained:

```text
bind-address = 127.0.0.1
```

The address:

```text
127.0.0.1
```

is the IPv4 loopback address.

In this configuration, MySQL was bound to the local loopback interface.

This matched what I had previously observed using:

```bash
sudo ss -ltnp
```

which showed:

```text
127.0.0.1:3306
```

The relationship was:

```text
Configuration

bind-address = 127.0.0.1
            ↓
Expected runtime behaviour
            ↓
MySQL listens locally
            ↓
Observed with ss
            ↓
127.0.0.1:3306
```

This demonstrated how configuration can be compared with actual runtime state.

---

# 6. Understanding mysqlx-bind-address

The configuration also contained:

```text
mysqlx-bind-address = 127.0.0.1
```

During runtime inspection, I had observed:

```text
127.0.0.1:33060
```

associated with `mysqld`.

Port `33060` is used for the MySQL X Protocol.

The configuration and runtime observations therefore aligned:

```text
bind-address
     ↓
127.0.0.1
     ↓
MySQL connection on 3306
```

and:

```text
mysqlx-bind-address
     ↓
127.0.0.1
     ↓
MySQL X Protocol on 33060
```

---

# 7. No Explicit Port Was Found by the Search

The command searched for:

```text
bind-address
mysqlx-bind-address
port
```

but the output only displayed:

```text
bind-address
mysqlx-bind-address
```

No explicit `port` line was returned by that search.

However, runtime inspection showed that MySQL was listening on:

```text
3306
```

This demonstrated an important configuration lesson:

> A setting does not always need to be explicitly written in the configuration file for the software to have a value for that setting.

Software can use default values when a setting is not explicitly overridden.

---

# 8. Configuration vs Runtime State

A configuration file tells me how the service is configured or expected to behave.

It is still useful to inspect the actual runtime state.

For example:

```bash
grep -nE '^(bind-address|mysqlx-bind-address|port)' /etc/mysql/mysql.conf.d/mysqld.cnf
```

showed the configuration.

Then:

```bash
sudo ss -ltnp
```

showed what was actually listening.

The two sources answered different questions:

```text
Configuration file
       ↓
What should the service use?

Runtime inspection
       ↓
What is the process actually doing?
```

Comparing both is stronger than relying on either one alone.

---

# 9. Locate MySQL Logs

I inspected the MySQL log directory:

```bash
sudo ls -lh /var/log/mysql/
```

The output contained:

```text
error.log
```

The main log inspected during this practical was therefore:

```text
/var/log/mysql/error.log
```

This log contained MySQL server startup and operational information.

---

# 10. Inspect Recent MySQL Log Entries

I inspected the most recent entries using:

```bash
sudo tail -20 /var/log/mysql/error.log
```

Using `tail` allowed me to inspect recent events without displaying the entire log file.

This is useful when investigating events that have just occurred.

---

# 11. MySQL Initialization Sequence

The log showed MySQL initialization beginning with messages indicating:

```text
MySQL Server Initialization - start
```

The log also showed:

```text
mysqld 8.4.11 initializing
```

and InnoDB initialization beginning and completing.

Conceptually, the log showed activity such as:

```text
MySQL initialization starts
        ↓
mysqld initializes
        ↓
InnoDB initializes
        ↓
Initial setup completes
```

This provided information that was not visible simply from:

```bash
systemctl status mysql
```

---

# 12. Initialization and Normal Server Startup

The log showed an initialization phase followed by a later normal server startup phase.

During initialization, the server performed the initial setup required for the MySQL installation.

The log then showed a shutdown associated with the initialization process.

Afterwards, MySQL started normally and eventually reported that it was ready for connections.

This demonstrated that seeing a shutdown message in a log does not automatically mean there was an unexpected failure.

The surrounding log entries and context matter.

---

# 13. InnoDB Initialization

The log contained messages indicating that:

```text
InnoDB initialization has started
```

and later that initialization had ended.

InnoDB is part of the MySQL server's storage system.

For troubleshooting purposes, the important lesson at this stage was recognizing the startup sequence and identifying whether major components completed initialization.

---

# 14. TLS Information

The log also contained information related to TLS configuration.

It reported that:

```text
ca.pem is self signed
```

and that the MySQL channel was configured to support TLS.

This demonstrated that the error log contains more than only fatal errors.

Despite its name:

```text
error.log
```

it can contain:

- Informational messages
- Warnings
- Startup events
- Configuration-related information
- Errors

Therefore, every entry in `error.log` should not automatically be interpreted as a failure.

---

# 15. MySQL X Plugin

The log showed the MySQL X Plugin becoming ready.

It reported a bind address of:

```text
127.0.0.1
```

and port:

```text
33060
```

This matched the runtime socket I had previously observed:

```text
127.0.0.1:33060
```

This provided another connection between:

```text
Configuration
     ↓
Logs
     ↓
Runtime network state
```

---

# 16. MySQL Ready for Connections

Near the end of the startup sequence, the log reported that:

```text
mysqld: ready for connections
```

and showed the normal MySQL port:

```text
3306
```

This was important evidence that the MySQL server had completed startup and was prepared to accept connections.

The overall sequence could be represented as:

```text
mysqld starts
     ↓
InnoDB initializes
     ↓
TLS configuration initialized
     ↓
MySQL X Plugin becomes ready
     ↓
33060 available
     ↓
MySQL server becomes ready
     ↓
3306 available
```

---

# 17. Initialization Warning About Root

During initial setup, the log contained a warning similar to:

```text
root@localhost is created with an empty password
```

and referenced:

```text
--initialize-insecure
```

It would have been incorrect to look at that initialization message alone and conclude that the current MySQL root account was still configured as an unrestricted passwordless account.

The message described an event during initialization.

To understand the **current state**, I needed to inspect the current MySQL account configuration.

This demonstrates an important troubleshooting principle:

```text
Historical log event
       ≠
Current configuration
```

---

# 18. Verify Current Root Authentication

Instead of assuming that the initialization warning represented the current state, I checked the root account directly:

```bash
sudo mysql -e "SELECT user, host, plugin FROM mysql.user WHERE user='root';"
```

The result showed:

```text
root    localhost    auth_socket
```

The current root account was therefore using:

```text
auth_socket
```

for authentication.

---

# 19. Understanding sudo mysql

The root authentication result helped explain why I had been connecting using:

```bash
sudo mysql
```

The relationship was:

```text
sudo mysql
     ↓
Local privileged operating-system context
     ↓
root@localhost
     ↓
auth_socket
```

This was different from the account I created during the user-management lab:

```text
somto_user@localhost
```

which I accessed using:

```bash
mysql -u somto_user -p
```

and a password.

Therefore, different MySQL accounts can use different authentication methods.

---

# 20. Historical Evidence vs Current State

The root authentication investigation provided an important general troubleshooting lesson.

The log contained a historical initialization warning.

The current account configuration showed:

```text
auth_socket
```

These pieces of evidence answered different questions.

```text
Log
 ↓
What happened at a point in time?
```

compared with:

```text
Current database query
 ↓
How is the account configured now?
```

When investigating a system, I should avoid treating an old log message as proof of the current state without verification.

---

# 21. UTC Log Timestamps

The MySQL error log timestamps contained:

```text
Z
```

For example:

```text
2026-09-28T05:02:43...Z
```

The `Z` indicates UTC.

At the same time, `systemctl status mysql` displayed the service start time using the system's local timezone.

This meant that timestamps from different tools could look different even though they referred to the same startup period.

When correlating events across logs and system tools, timezone differences should therefore be considered.

---

# 22. Configuration and Runtime Correlation

One of the most useful parts of this practical was comparing evidence from several sources.

## Configuration

```text
/etc/mysql/mysql.conf.d/mysqld.cnf
```

showed:

```text
bind-address = 127.0.0.1
mysqlx-bind-address = 127.0.0.1
```

## Runtime Network State

```bash
sudo ss -ltnp
```

showed:

```text
127.0.0.1:3306
127.0.0.1:33060
```

owned by:

```text
mysqld
```

## Logs

```text
/var/log/mysql/error.log
```

showed MySQL becoming ready on port:

```text
3306
```

and the X Plugin becoming ready on:

```text
33060
```

The evidence therefore aligned:

```text
Configuration
      ↓
127.0.0.1

Runtime
      ↓
127.0.0.1:3306
127.0.0.1:33060

Logs
      ↓
Server ready on 3306
X Plugin ready on 33060
```

This is stronger evidence than checking only one layer.

---

# 23. Useful Commands

## Show MySQL option-file search locations

```bash
mysql --help | grep -A 1 "Default options"
```

## Inspect the MySQL configuration directory

```bash
ls -l /etc/mysql/
```

## Inspect server configuration files

```bash
ls -l /etc/mysql/mysql.conf.d/
```

## Find network-related server settings

```bash
grep -nE '^(bind-address|mysqlx-bind-address|port)' /etc/mysql/mysql.conf.d/mysqld.cnf
```

## Inspect listening TCP sockets

```bash
sudo ss -ltnp
```

## Inspect the MySQL log directory

```bash
sudo ls -lh /var/log/mysql/
```

## View recent MySQL log entries

```bash
sudo tail -20 /var/log/mysql/error.log
```

## Check the MySQL service

```bash
systemctl status mysql
```

## Inspect current root authentication

```bash
sudo mysql -e "SELECT user, host, plugin FROM mysql.user WHERE user='root';"
```

---

# 24. Troubleshooting Workflow

If MySQL has a startup or connection problem, a useful evidence-based workflow is:

```text
Check service
     ↓
systemctl status mysql
     ↓
Check process/socket
     ↓
sudo ss -ltnp
     ↓
Inspect configuration
     ↓
/etc/mysql/mysql.conf.d/mysqld.cnf
     ↓
Inspect logs
     ↓
/var/log/mysql/error.log
     ↓
Identify actual failure
     ↓
Make targeted change
     ↓
Restart if required
     ↓
Verify again
```

The important principle is:

> Do not change configuration before understanding the evidence.

---

# 25. Configuration Changes Require Verification

If a configuration setting is changed, I should not assume that editing the file alone changed the running process.

The general workflow should be:

```text
Inspect current configuration
        ↓
Make required change
        ↓
Restart/reload service as appropriate
        ↓
Check service status
        ↓
Inspect runtime socket/process
        ↓
Test connection
        ↓
Inspect logs if necessary
```

The goal is to verify the effect of the change rather than assuming it succeeded.

---

# 26. Main Lessons

This practical connected several Linux and database concepts.

```text
MySQL Package
     ↓
mysql.service
     ↓
mysqld
     ↓
mysqld.cnf
     ↓
bind-address
     ↓
Listening socket
     ↓
3306 / 33060
     ↓
Client connection
     ↓
Database operations
```

It also showed the role of logs:

```text
Something unexpected happens
          ↓
Do not guess
          ↓
Inspect service/runtime
          ↓
Inspect logs
          ↓
Interpret evidence
          ↓
Identify the failing layer
```

---

# Key Takeaway

Configuration, runtime state, and logs provide different types of evidence.

```text
Configuration
     ↓
How the service is intended to operate

Runtime inspection
     ↓
How the service is actually operating now

Logs
     ↓
What events occurred over time
```

A strong troubleshooting process compares these sources instead of relying on only one.

During this lab, the MySQL configuration, `ss` output, service state, and error log all provided complementary evidence that helped explain how the MySQL server was operating.
