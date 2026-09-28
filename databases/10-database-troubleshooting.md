# Database Troubleshooting

## Overview

This section brings together the troubleshooting principles learned while studying and working with MySQL and MongoDB.

The main principle is:

```text
Do not guess.
     ↓
Inspect.
     ↓
Identify the failing layer.
     ↓
Make a targeted change.
     ↓
Verify.
```

A database problem can occur at many different layers.

A useful troubleshooting model is:

```text
Package / Installation
        ↓
Service
        ↓
Process
        ↓
Configuration
        ↓
Network Port / Binding
        ↓
Client Connection
        ↓
Authentication
        ↓
Authorization
        ↓
Database
        ↓
Table / Collection
        ↓
Data
        ↓
Query / Operation
```

The goal is to determine **where the failure occurs** before changing anything.

---

# 1. Why Layered Troubleshooting Matters

Consider the statement:

```text
"The database is not working."
```

This does not provide enough information to identify the problem.

It could mean:

```text
Package is not installed
Service is stopped
Process failed
Wrong configuration
Wrong port
Wrong bind address
Client cannot connect
Authentication failed
User lacks privileges
Database does not exist
Table does not exist
Query is incorrect
Expected data does not exist
```

Each problem requires a different investigation.

Therefore:

```text
Symptom
   ↓
Evidence
   ↓
Failing layer
   ↓
Targeted action
```

---

# 2. Layer 1 — Package / Installation

The first question can be:

> Is the required database software installed?

During the MySQL practical, I initially ran:

```bash
mysql --version
```

and received:

```text
Command 'mysql' not found
```

I also checked:

```bash
systemctl status mysql
```

and received:

```text
Unit mysql.service could not be found.
```

At this stage, troubleshooting database tables, users, or ports would have been premature.

The evidence pointed toward the installation/package layer.

---

# 3. Check Package Availability

I checked:

```bash
apt policy mysql-server
```

The output showed that:

```text
mysql-server
```

was not installed but had an available candidate.

This provided evidence that the package could be installed using the configured Ubuntu package repositories.

I then installed it using:

```bash
sudo apt install mysql-server
```

The lesson was:

```text
Command missing
      +
Service unit missing
      ↓
Investigate installation
```

rather than:

```text
Immediately edit configuration
```

---

# 4. MongoDB Package Example

During the MongoDB investigation, I ran:

```bash
mongod --version
```

and received:

```text
mongod: command not found
```

I also checked:

```bash
mongosh --version
```

and the shell was not installed.

I then investigated package availability:

```bash
apt search mongodb 2>/dev/null | head -20
```

and:

```bash
apt policy mongodb-org
```

The system reported that it could not locate:

```text
mongodb-org
```

This was a package/repository-layer issue.

It was not evidence that:

```text
mongod had crashed
```

because the MongoDB server had not been installed.

---

# 5. Different Errors Point to Different Layers

Compare:

```text
Unable to locate package mongodb-org
```

with:

```text
mongod.service failed
```

These indicate different stages.

```text
Unable to locate package
       ↓
Repository / package layer
```

while:

```text
Service failed
       ↓
Installation progressed far enough
for a service to exist
       ↓
Investigate service/runtime layer
```

Recognizing this difference prevents wasted troubleshooting.

---

# 6. Layer 2 — Service

Once the software is installed, the next layer is often the service.

For MySQL:

```bash
systemctl status mysql
```

After installation, the output showed:

```text
Active: active (running)
```

and identified the main process.

This proved that the systemd service was running.

---

# 7. Active vs Enabled

The MySQL service also showed:

```text
enabled
```

and:

```text
active (running)
```

These describe different things.

```text
enabled
   ↓
Configured to start automatically
under the appropriate systemd target
```

while:

```text
active (running)
   ↓
Currently running
```

Therefore:

```text
Enabled
   ≠
Running
```

A service can be enabled but not currently running.

---

# 8. MongoDB Service Concept

The MongoDB learning material uses:

```bash
systemctl start mongod
```

and:

```bash
systemctl status mongod
```

If MongoDB were installed in an appropriate environment and the service showed:

```text
failed
```

the next step would be to inspect evidence.

For example:

```bash
sudo journalctl -u mongod -n 50
```

The goal would be to determine **why** the service failed before modifying configuration.

---

# 9. Layer 3 — Process

A running service should normally result in the expected server process.

During the MySQL practical, the service status identified:

```text
mysqld
```

as the database server process.

This reinforced the distinction:

```text
mysql.service
      ↓
systemd service

mysqld
      ↓
MySQL server daemon
```

Similarly, MongoDB uses:

```text
mongod
```

as its server daemon.

---

# 10. Service vs Process

These concepts are related but different.

```text
systemd
   ↓
Service unit
   ↓
Starts/manages
   ↓
Server process
```

For MySQL:

```text
mysql.service
      ↓
mysqld
```

For MongoDB:

```text
mongod service
      ↓
mongod
```

This distinction helps when reading output from:

```bash
systemctl
```

and:

```bash
ss
```

---

# 11. Layer 4 — Configuration

If the service or application behaves differently from what is expected, configuration becomes another source of evidence.

For MySQL, I inspected:

```text
/etc/mysql/mysql.conf.d/mysqld.cnf
```

and searched for relevant settings using:

```bash
grep -nE '^(bind-address|mysqlx-bind-address|port)' /etc/mysql/mysql.conf.d/mysqld.cnf
```

The output included:

```text
bind-address = 127.0.0.1
mysqlx-bind-address = 127.0.0.1
```

This told me how the server was configured to bind its network interfaces.

---

# 12. MongoDB Configuration

The MongoDB learning material shows:

```text
/etc/mongod.conf
```

with network configuration including:

```yaml
net:
  port: 27017
  bindIp: 127.0.0.1
```

The configuration describes expected behaviour.

However:

```text
Configuration
      ≠
Proof of runtime state
```

The actual running process should also be inspected.

---

# 13. Layer 5 — Port and Binding

A database server may be running but still not be reachable in the expected way.

During the MySQL practical, I ran:

```bash
sudo ss -ltnp
```

The relevant output showed:

```text
127.0.0.1:3306
```

and:

```text
127.0.0.1:33060
```

associated with:

```text
mysqld
```

This provided several pieces of evidence:

```text
mysqld is running
       ↓
TCP sockets exist
       ↓
3306 is listening
       ↓
33060 is listening
       ↓
Both are bound to 127.0.0.1
```

---

# 14. Configuration vs Runtime

The MySQL configuration showed:

```text
bind-address = 127.0.0.1
```

and runtime inspection showed:

```text
127.0.0.1:3306
```

The configuration and runtime state therefore aligned.

This is stronger than checking only the configuration file.

The general approach is:

```text
Read configuration
      ↓
Form expectation
      ↓
Inspect runtime
      ↓
Compare expected vs actual
```

---

# 15. Understanding 127.0.0.1

The address:

```text
127.0.0.1
```

is the IPv4 loopback address.

When a database server is bound only to:

```text
127.0.0.1
```

its TCP service is available through the local loopback interface.

Therefore, if:

```text
Service = running
Port = listening
Bind address = 127.0.0.1
```

but a remote machine cannot connect, the investigation should consider the network binding rather than immediately assuming the database process is stopped.

---

# 16. Port Comparison

From the material and practical:

```text
Database            Port
--------            ----
MySQL               3306
MySQL X Protocol    33060
MongoDB             27017
```

A client must connect to the appropriate service endpoint.

Checking which process owns a port is more useful than simply asking whether a port number appears somewhere.

For example:

```bash
sudo ss -ltnp
```

can show:

```text
Address
Port
Process
PID
```

depending on the environment and permissions.

---

# 17. Layer 6 — Client Connection

Once the server is running and listening, the next question is:

> Can the client connect?

For MySQL, I used:

```bash
sudo mysql
```

and later:

```bash
mysql -u somto_user -p
```

Successful connection proved that several lower layers were already functioning.

For example:

```text
Server running
     ↓
Client reaches server
     ↓
Authentication can occur
```

---

# 18. Connection Failure Does Not Always Mean Service Failure

Suppose:

```text
systemctl status mysql
```

shows:

```text
active (running)
```

and:

```bash
sudo ss -ltnp
```

shows:

```text
127.0.0.1:3306
```

If a client still cannot connect, I now have evidence that:

```text
Service exists
Process is running
Port is listening
```

The investigation should move to the next relevant layer rather than repeatedly reinstalling MySQL.

---

# 19. Layer 7 — Authentication

Authentication answers:

> Who are you?

During the MySQL practical, I created:

```text
somto_user@localhost
```

and connected using:

```bash
mysql -u somto_user -p
```

A successful login demonstrated that the account could authenticate.

This did **not** automatically prove that the user could perform every database operation.

---

# 20. Authentication Methods

I also inspected the root account using:

```bash
sudo mysql -e "SELECT user, host, plugin FROM mysql.user WHERE user='root';"
```

The output showed:

```text
root    localhost    auth_socket
```

Therefore:

```text
root@localhost
      ↓
auth_socket
```

while my lab user used password authentication.

This demonstrated that troubleshooting login problems may require checking:

```text
Username
Host
Authentication method
Credentials
```

---

# 21. Layer 8 — Authorization

Authorization answers:

> What are you allowed to do?

After creating:

```text
somto_user@localhost
```

I checked:

```sql
SHOW GRANTS FOR 'somto_user'@'localhost';
```

Initially, the account showed:

```text
GRANT USAGE ON *.* TO `somto_user`@`localhost`
```

The account existed, but I had not yet granted privileges on my application database.

---

# 22. Grant Database Access

I granted:

```sql
GRANT ALL PRIVILEGES
ON somto_db.*
TO 'somto_user'@'localhost';
```

I then verified:

```sql
SHOW GRANTS FOR 'somto_user'@'localhost';
```

The output now included privileges on:

```text
somto_db.*
```

This demonstrated:

```text
Change
   ↓
Verify
```

rather than assuming that the change worked.

---

# 23. Prove Read and Write Authorization

After connecting as:

```text
somto_user
```

I selected:

```sql
USE somto_db;
```

Then:

```sql
SELECT * FROM people;
```

succeeded.

This proved read access.

I then inserted:

```sql
INSERT INTO people (name, age, location)
VALUES ('David', 30, 'Adelaide');
```

This succeeded.

I queried the table again and confirmed David had been added.

Therefore:

```text
Login succeeds
      ↓
Authentication proven

USE somto_db succeeds
      ↓
Database access proven

SELECT succeeds
      ↓
Read authorization proven

INSERT succeeds
      ↓
Write authorization proven
```

---

# 24. Authentication vs Authorization Troubleshooting

Suppose:

```bash
mysql -u somto_user -p
```

works, but:

```sql
USE somto_db;
```

fails.

The evidence already tells me that:

```text
Client reached MySQL
Authentication succeeded
```

Therefore, I should investigate:

```text
Authorization / privileges
```

rather than immediately checking whether MySQL is installed.

This is the benefit of layered troubleshooting.

---

# 25. Layer 9 — Database Selection

A connection can succeed while no database is selected.

During the MySQL practical:

```sql
SELECT DATABASE();
```

initially returned:

```text
NULL
```

This did not mean:

```text
MySQL is broken
```

It meant:

```text
Connected to MySQL
      ↓
No current database selected
```

After:

```sql
USE somto_db;
```

the query:

```sql
SELECT DATABASE();
```

returned:

```text
somto_db
```

---

# 26. Layer 10 — Table or Collection

After selecting `somto_db`, I ran:

```sql
SHOW TABLES;
```

Initially, no table was displayed.

Again, this did not mean that MySQL had failed.

The database simply did not contain a table yet.

After creating:

```sql
CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    location VARCHAR(100)
);
```

the command:

```sql
SHOW TABLES;
```

displayed:

```text
people
```

---

# 27. Inspect Structure Before Guessing

If a query fails because I am unsure of a table's structure, I can inspect it.

For MySQL:

```sql
DESCRIBE people;
```

This showed:

```text
id
name
age
location
```

along with their types and other metadata.

This is better than guessing column names.

The principle is:

```text
Unsure about structure
       ↓
Inspect structure
       ↓
Construct query
```

---

# 28. Layer 11 — Data

A database and table can both exist while the expected data does not.

For example:

```sql
SELECT * FROM people;
```

allowed me to inspect the actual records.

The practical contained:

```text
John
Sarah
Mike
David
```

If I expected another person to exist but the query did not show that record, the next investigation would be at the data/query layer.

There would be no reason to reinstall the database server merely because one expected row was missing.

---

# 29. Layer 12 — Query

The query itself may also explain an unexpected result.

For example:

```sql
SELECT * FROM people WHERE age > 25;
```

returned:

```text
John
Sarah
```

from the original three records.

Mike was:

```text
25
```

and therefore did not satisfy:

```text
age > 25
```

This was not a database failure.

It was the correct result of the query condition.

---

# 30. > vs >=

Understanding operators is part of troubleshooting query results.

```text
age > 25
```

means:

```text
strictly greater than 25
```

while:

```text
age >= 25
```

means:

```text
greater than or equal to 25
```

A query returning fewer rows than expected may therefore be caused by the query logic rather than the database infrastructure.

---

# 31. Logs

Logs become especially important when services fail, restart unexpectedly, or report errors.

For MySQL, I inspected:

```text
/var/log/mysql/error.log
```

using:

```bash
sudo tail -20 /var/log/mysql/error.log
```

The log showed information about:

```text
Initialization
InnoDB
TLS
MySQL X Plugin
Server startup
Ports
Ready-for-connections state
```

---

# 32. Logs Are Historical Evidence

The MySQL log also contained an initialization warning relating to:

```text
root@localhost
```

and an empty password during initialization.

It would have been incorrect to assume that this historical message represented the current authentication configuration.

I verified the current state and found:

```text
root@localhost
```

using:

```text
auth_socket
```

Therefore:

```text
Historical log event
       ≠
Current state
```

Logs should be interpreted in context.

---

# 33. MongoDB Logs

The MongoDB learning material identifies:

```text
/var/log/mongodb/mongod.log
```

as the MongoDB application log.

For a systemd-managed MongoDB service, another useful source is:

```bash
sudo journalctl -u mongod
```

These can provide complementary evidence.

```text
systemd
   ↓
journalctl -u mongod
```

and:

```text
MongoDB
   ↓
/var/log/mongodb/mongod.log
```

---

# 34. Scenario — Command Not Found

Suppose:

```bash
mysql --version
```

returns:

```text
command not found
```

A reasonable investigation begins at:

```text
Installation / package layer
```

Useful evidence may include:

```bash
apt policy mysql-server
```

The wrong response would be to immediately modify:

```text
bind-address
```

because there is not yet evidence of a network-binding problem.

---

# 35. Scenario — Service Does Not Exist

Suppose:

```bash
systemctl status mysql
```

returns:

```text
Unit mysql.service could not be found
```

This suggests investigating whether the relevant package/service is installed.

Again:

```text
Service unit missing
       ↓
Investigate installation
```

before troubleshooting database queries.

---

# 36. Scenario — Service Failed

Suppose an installed database service reports:

```text
failed
```

The next step should be evidence collection.

For MySQL, useful sources could include:

```bash
systemctl status mysql
```

and:

```bash
sudo tail -50 /var/log/mysql/error.log
```

For MongoDB in the studied environment:

```bash
systemctl status mongod
```

and:

```bash
sudo journalctl -u mongod -n 50
```

The reported error should guide the next action.

---

# 37. Scenario — Service Running but No Connection

Suppose the database service is:

```text
active (running)
```

but the client cannot connect.

The next questions include:

```text
Is the process listening?

Which port?

Which address?

Which process owns the socket?
```

A useful command is:

```bash
sudo ss -ltnp
```

This moves the investigation from:

```text
Service
```

to:

```text
Process / Network
```

---

# 38. Scenario — Local Connection Works but Remote Does Not

Suppose:

```text
Local client connects
```

but:

```text
Remote client cannot connect
```

and runtime inspection shows:

```text
127.0.0.1:3306
```

or, for MongoDB conceptually:

```text
127.0.0.1:27017
```

This evidence suggests investigating network binding and remote-access controls.

Relevant areas can include:

```text
Bind address
Firewall
Network path
Authentication
Access controls
```

The service should not automatically be exposed on all interfaces without considering security.

---

# 39. Scenario — Login Works but Database Access Fails

Suppose:

```bash
mysql -u somto_user -p
```

succeeds.

Then:

```sql
USE somto_db;
```

fails with a permission-related error.

This tells me:

```text
Client connection works
Authentication works
```

The next layer is:

```text
Authorization
```

I could inspect:

```sql
SHOW GRANTS FOR 'somto_user'@'localhost';
```

The evidence should determine whether a privilege change is required.

---

# 40. Scenario — SELECT Works but INSERT Fails

Suppose:

```sql
SELECT * FROM people;
```

works but:

```sql
INSERT INTO people ...
```

fails because permission is denied.

This already proves:

```text
Server reachable
Authentication works
Database accessible
Table accessible
SELECT permitted
```

The investigation should focus on the permission required for the failed operation.

This is much more precise than saying:

```text
"MySQL is broken."
```

---

# 41. Scenario — Database Query Returns NULL

During the practical:

```sql
SELECT DATABASE();
```

returned:

```text
NULL
```

The correct interpretation was:

```text
No current database selected
```

not:

```text
No databases exist
```

The next action was:

```sql
USE somto_db;
```

followed by verification:

```sql
SELECT DATABASE();
```

---

# 42. Scenario — SHOW TABLES Returns Nothing

If:

```sql
SHOW TABLES;
```

returns no tables after selecting a database, possible evidence is simply:

```text
The current database contains no tables
```

The database server may still be functioning correctly.

Context matters.

---

# 43. Scenario — Query Returns Fewer Records Than Expected

Suppose:

```sql
SELECT * FROM people WHERE age > 25;
```

does not return Mike, whose age is `25`.

Before investigating services or logs, inspect the query condition.

```text
25 > 25
```

is false.

The database is behaving correctly.

The issue is the expectation about the query.

---

# 44. MongoDB Connection Troubleshooting Model

For MongoDB, a conceptual connection investigation would be:

```text
Can mongosh reach MongoDB?
       ↓
Is mongod running?
       ↓
Is the process listening?
       ↓
Is 27017 the expected port?
       ↓
Which address is it bound to?
       ↓
Does runtime match /etc/mongod.conf?
       ↓
Do logs report an error?
       ↓
Can authentication succeed?
       ↓
Can the required database operation succeed?
```

This follows the same layered reasoning as MySQL.

---

# 45. MongoDB Data Operation Troubleshooting

The learning material demonstrates:

```javascript
use school
```

```javascript
db.createCollection("persons")
```

```javascript
show collections
```

```javascript
db.persons.find()
```

If an expected collection or document is not visible, the investigation should consider:

```text
Current database
      ↓
Collection
      ↓
Documents
      ↓
Query/filter
```

rather than immediately assuming that the `mongod` service has failed.

---

# 46. Inspect Before Changing

A recurring lesson throughout the database practical was:

```text
Inspect first.
```

Examples include:

```bash
systemctl status mysql
```

before changing service configuration.

```bash
sudo ss -ltnp
```

before assuming a port problem.

```sql
SHOW GRANTS FOR 'somto_user'@'localhost';
```

before changing privileges.

```sql
DESCRIBE people;
```

before guessing table structure.

```bash
sudo tail -20 /var/log/mysql/error.log
```

before guessing why the server behaved a certain way.

---

# 47. Make One Targeted Change

Once evidence identifies a problem, make the smallest appropriate change.

The workflow is:

```text
Observe problem
      ↓
Collect evidence
      ↓
Form explanation
      ↓
Make targeted change
      ↓
Verify
```

Avoid:

```text
Change configuration
Change firewall
Reinstall package
Reset permissions
Restart everything
```

all at once.

If many changes are made simultaneously, it becomes difficult to know which change actually solved the problem.

---

# 48. Verification

Troubleshooting is not complete when a command runs without an obvious error.

The final state should be verified.

Examples:

After installing:

```bash
mysql --version
```

and:

```bash
systemctl status mysql
```

After checking network state:

```bash
sudo ss -ltnp
```

After creating a database:

```sql
SHOW DATABASES;
```

After selecting it:

```sql
SELECT DATABASE();
```

After creating a table:

```sql
SHOW TABLES;
```

After granting privileges:

```sql
SHOW GRANTS FOR 'somto_user'@'localhost';
```

After inserting data:

```sql
SELECT * FROM people;
```

The principle is:

```text
Change
   ↓
Verify resulting state
```

---

# 49. Database Troubleshooting Decision Flow

A simplified decision flow is:

```text
Database problem
      ↓
Is software installed?
      │
      ├── No → investigate package/repository
      │
      └── Yes
           ↓
Is service running?
      │
      ├── No → inspect service status/logs
      │
      └── Yes
           ↓
Is process listening?
      │
      ├── No → inspect process/config/logs
      │
      └── Yes
           ↓
Correct IP and port?
      │
      ├── No → investigate network configuration
      │
      └── Yes
           ↓
Can client connect?
      │
      ├── No → investigate connection/network
      │
      └── Yes
           ↓
Can user authenticate?
      │
      ├── No → investigate account/authentication
      │
      └── Yes
           ↓
Is operation authorized?
      │
      ├── No → inspect privileges
      │
      └── Yes
           ↓
Correct database/table/collection?
      │
      ├── No → inspect database structure
      │
      └── Yes
           ↓
Correct query/data?
      │
      ├── No → inspect query/data
      │
      └── Yes
           ↓
Operation succeeds
```

---

# 50. Core Troubleshooting Commands

## Package

```bash
apt policy <package>
```

```bash
apt search <package>
```

---

## Service

MySQL:

```bash
systemctl status mysql
```

MongoDB:

```bash
systemctl status mongod
```

---

## Network

```bash
sudo ss -ltnp
```

---

## MySQL Configuration

```bash
grep -nE '^(bind-address|mysqlx-bind-address|port)' /etc/mysql/mysql.conf.d/mysqld.cnf
```

---

## MySQL Logs

```bash
sudo tail -50 /var/log/mysql/error.log
```

---

## MongoDB Service Journal

```bash
sudo journalctl -u mongod -n 50
```

---

## MongoDB Application Log

```bash
sudo tail -50 /var/log/mongodb/mongod.log
```

---

## MySQL Databases

```sql
SHOW DATABASES;
```

---

## Current MySQL Database

```sql
SELECT DATABASE();
```

---

## MySQL Tables

```sql
SHOW TABLES;
```

---

## MySQL Table Structure

```sql
DESCRIBE people;
```

---

## MySQL User Privileges

```sql
SHOW GRANTS FOR 'somto_user'@'localhost';
```

---

# 51. MySQL Practical Troubleshooting Chain

The MySQL practical can now be understood as one complete operational chain:

```text
mysql command missing
       ↓
Check package
       ↓
Install mysql-server
       ↓
Check mysql.service
       ↓
Identify mysqld
       ↓
Check listening sockets
       ↓
3306 + 33060
       ↓
Inspect bind-address
       ↓
Connect to server
       ↓
Create/select database
       ↓
Create table
       ↓
Insert/query data
       ↓
Create user
       ↓
Inspect grants
       ↓
Grant privileges
       ↓
Test authentication
       ↓
Test authorization
       ↓
Inspect configuration
       ↓
Inspect logs
       ↓
Correlate evidence
```

---

# 52. MongoDB Learning Chain

The MongoDB material can be understood through a similar model:

```text
Repository
     ↓
mongodb-org package
     ↓
mongod service
     ↓
mongod process
     ↓
/etc/mongod.conf
     ↓
bindIp + port
     ↓
27017
     ↓
MongoDB shell
     ↓
Database
     ↓
Collection
     ↓
Document
     ↓
Query
```

On my current Ubuntu machine, the MongoDB runtime portion was intentionally deferred.

Therefore, the MongoDB troubleshooting sections describe the concepts studied rather than claiming that MongoDB incidents were reproduced locally.

---

# 53. Final Troubleshooting Mental Model

When a database application fails, I can now ask:

```text
1. Is the software installed?

2. Does the service exist?

3. Is the service running?

4. Is the expected process running?

5. What does the configuration say?

6. What address and port are actually listening?

7. Can the client reach the server?

8. Can the user authenticate?

9. Does the user have authorization?

10. Is the correct database selected?

11. Does the table/collection exist?

12. Does the expected data exist?

13. Is the query correct?

14. What do the logs say?
```

The order can change depending on the evidence, but the purpose remains the same:

> Identify the failing layer rather than treating every problem as a generic database failure.

---

# Key Takeaway

Database troubleshooting is a process of narrowing the problem.

```text
Package
   ↓
Service
   ↓
Process
   ↓
Configuration
   ↓
Network
   ↓
Connection
   ↓
Authentication
   ↓
Authorization
   ↓
Database Structure
   ↓
Data
   ↓
Query
```

At every stage:

```text
Inspect
   ↓
Gather evidence
   ↓
Interpret
   ↓
Change only what is necessary
   ↓
Verify
```

The most important lesson from this database section is that a symptom at the application level does not automatically mean the database server itself is broken.

Strong troubleshooting means determining **which layer failed and proving it with evidence** before making changes.
