# Troubleshooting Two-Tier Applications

## Overview

Troubleshooting a two-tier application should be based on evidence rather than guessing.

The architecture in this lab is:

```text
Browser
   ↓
Host port 8080
   ↓
Docker
   ↓
web-server:80
   ↓
Apache
   ↓
PHP Application
   ↓
Docker DNS / Network
   ↓
db-server:3306
   ↓
MariaDB
   ↓
ecomdb
   ↓
products
```

A problem at any layer can affect what the user sees.

The main troubleshooting method I practised was:

```text
Observe symptom
      ↓
Gather evidence
      ↓
Identify failing layer
      ↓
Form hypothesis
      ↓
Test hypothesis
      ↓
Apply fix
      ↓
Verify recovery
```

---

# Do Not Restart First

One of the most important lessons from this lab was:

```text
Do not immediately restart the service.
```

Restarting may restore a service temporarily, but it can also remove useful evidence about why the failure occurred.

A better approach is:

```text
1. Reproduce the problem
2. Inspect current state
3. Check processes
4. Check listeners
5. Inspect logs
6. Test dependencies
7. Identify the failing layer
8. Apply the appropriate fix
9. Verify
```

A restart is a possible fix, not a troubleshooting strategy by itself.

---

# Start With the User's Symptom

The symptom determines where investigation should begin.

For example:

```text
Website completely unavailable
```

is different from:

```text
Website loads but products are missing
```

These symptoms suggest different parts of the architecture.

---

# Scenario 1 — Website Completely Unavailable

Suppose the user reports:

```text
The website is not opening.
```

Start by reproducing the problem:

```bash
curl -v http://localhost:8080
```

Possible outcomes include:

```text
Connection refused
Timeout
HTTP response
Application error
```

Each result provides different evidence.

---

## Check the Container

If the website is unavailable, check whether the web container is running:

```bash
sudo docker ps
```

If `web-server` is running, that proves the container exists and is running.

It does not prove Apache is running inside it.

---

## Check Port 80

Inside `web-server`:

```bash
ss -lntp | grep ':80'
```

If nothing is returned, there is no TCP listener on port 80.

This strongly directs the investigation toward the web service.

---

## Check Apache

Use:

```bash
service apache2 status
```

If Apache is stopped, inspect available evidence before starting it.

For example:

```bash
tail -n 20 /var/log/apache2/error.log
```

After inspection, Apache can be started:

```bash
service apache2 start
```

Then verify:

```bash
ss -lntp | grep ':80'
```

---

## Verify Locally First

Inside `web-server`:

```bash
curl -I http://localhost:80
```

If this works, Apache is serving HTTP inside the container.

Then test from WSL:

```bash
curl -I http://localhost:8080
```

This verifies the Docker-published HTTP path.

Finally verify the dynamic application:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

This progressively verifies:

```text
Apache
   ↓
Container HTTP
   ↓
Docker port publishing
   ↓
Application
   ↓
Database-backed content
```

---

# Scenario 2 — Website Loads but Products Are Missing

This symptom immediately provides useful evidence.

If the webpage loads:

```text
Docker port publishing   probably functioning
Apache                   responding
PHP/HTML path            at least partially functioning
```

But database-backed content may still be failing.

The investigation should move toward:

```text
PHP configuration
Database hostname
Database connectivity
MariaDB
Authentication
Privileges
Database/table/data
```

---

## Verify Dynamic Content

Use:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

If no product lines appear, continue investigating.

Do not assume:

```text
Database server is down
```

because several layers exist between PHP and the product data.

---

# Scenario 3 — Test the Database From the Application Tier

From `web-server`:

```bash
mariadb -h db-server -u ecomuser -p
```

This is one of the strongest diagnostic tests in the lab.

Possible results provide different evidence.

---

## Successful Login

If the login succeeds:

```text
DNS                   ✓
Network path          ✓
TCP 3306              ✓
MariaDB listener      ✓
Authentication        ✓
```

Then test:

```sql
USE ecomdb;
SELECT * FROM products;
```

If the products are returned, the database path itself is healthy.

The investigation should move back toward PHP/application configuration.

---

## Connection Refused

If the result is:

```text
Connection refused
```

investigate:

```text
MariaDB process
TCP 3306 listener
bind-address
Network path
Destination host/port
```

Useful commands include:

```bash
service mariadb status
```

```bash
ss -lntp | grep 3306
```

and:

```bash
grep -R "bind-address" /etc/mysql/
```

---

## Access Denied

If the result is:

```text
ERROR 1045 (28000): Access denied
```

the request reached MariaDB.

Therefore, do not immediately troubleshoot Docker networking.

Instead investigate:

```text
Username
Password
Host matching
Account configuration
Authentication
```

Check:

```sql
SELECT User, Host
FROM mysql.user
WHERE User='ecomuser';
```

and:

```sql
SHOW GRANTS FOR 'ecomuser'@'%';
```

---

# Scenario 4 — Credential Mismatch

During one break/fix exercise:

```text
Website loaded
Products were missing
```

A remote MariaDB test from `web-server` returned:

```text
Access denied
```

This proved that:

```text
web-server
   ↓
network
   ↓
db-server
   ↓
MariaDB
```

was functioning far enough for MariaDB to reject authentication.

The MariaDB account existed:

```text
'ecomuser'@'%'
```

and the grants were correct.

The application expected its configured database password, but authentication with that expected credential failed.

This narrowed the failure to a credential mismatch.

The account credential was restored with:

```sql
ALTER USER 'ecomuser'@'%' IDENTIFIED BY '<intended-password>';
```

The actual password should not be placed in public documentation.

After fixing the credential, verification should be performed from `web-server` and then through the application.

---

# Scenario 5 — Missing Database Records

Another break/fix scenario produced:

```text
Website loads
Products missing
Database connection works
```

The database was inspected:

```sql
USE ecomdb;
SELECT * FROM products;
```

The result was:

```text
Empty set
```

This proved:

```text
MariaDB running      ✓
Database exists      ✓
Connection works     ✓
Authentication       ✓
Table exists         ✓
Rows                 ✗
```

The problem was therefore not Apache, Docker networking, or database authentication.

---

## Check the Table Structure

Before restoring data:

```sql
DESCRIBE products;
```

The schema was still correct.

Therefore, only the missing data needed to be restored.

---

## Restore Only What Is Broken

The original SQL script contained both:

```sql
CREATE TABLE products ...
```

and:

```sql
INSERT INTO products ...
```

Running the complete initialization script against an already-existing table could produce a table-creation error.

Since the table already existed and its schema was correct, only the required data needed to be restored.

This demonstrated:

```text
Fix the failed component.
Do not rebuild healthy components unnecessarily.
```

---

## Database Data Changes Do Not Require Restart

After inserting the missing records, there was no need to restart MariaDB.

SQL operations such as:

```text
INSERT
UPDATE
DELETE
```

operate against the running database.

Verification was performed using:

```sql
SELECT COUNT(*) FROM products;
```

and then:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

---

# Scenario 6 — MariaDB Network Binding

MariaDB initially listened on:

```text
127.0.0.1:3306
```

This allows connections only through the database container's loopback interface.

For the two-tier architecture, the separate `web-server` needs to reach MariaDB.

The configuration was changed to:

```ini
bind-address = 0.0.0.0
```

After restarting MariaDB:

```bash
ss -lntp | grep 3306
```

showed:

```text
0.0.0.0:3306
```

The application tier could then connect through the Docker network.

---

# Understanding 127.0.0.1

An important networking lesson was:

```text
127.0.0.1 means "this network namespace"
```

Inside `web-server`:

```text
127.0.0.1
→ web-server
```

Inside `db-server`:

```text
127.0.0.1
→ db-server
```

Therefore:

```text
DB_HOST=127.0.0.1
```

inside the web container would tell PHP to look for MariaDB inside the web container.

The correct database host is:

```text
DB_HOST=db-server
```

---

# Scenario 7 — Historical Log Evidence

During troubleshooting, the Apache error log contained:

```text
PHP Fatal error
mysqli_sql_exception
Connection refused
```

At first this looked like strong evidence of the current problem.

However, current tests showed:

```text
MariaDB listening       ✓
Remote DB login         ✓
SELECT query            ✓
Products rendering      ✓
```

The log entry had an older timestamp.

Therefore, it described a previous failure.

This produced an important rule:

```text
Never interpret a log entry without checking its timestamp
and comparing it with current system behaviour.
```

---

# Scenario 8 — User Report Cannot Be Reproduced

In one exercise, the report was:

```text
Website not opening.
```

I tested:

```bash
curl -v http://localhost:8080
```

and received the webpage.

I then tested:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

and all eight products appeared.

Therefore, the application was currently healthy.

The correct response was not to restart services.

Instead:

```text
Reported problem
      ↓
Attempt reproduction
      ↓
Problem not reproduced
      ↓
Confirm current system health
      ↓
Preserve healthy state
```

A reported incident does not automatically mean the system is still failing when investigation begins.

---

# Process vs Port vs Application

These three checks answer different questions.

## Process

```bash
ps aux | grep '[a]pache2'
```

asks:

```text
Is the Apache process running?
```

## Port

```bash
ss -lntp | grep ':80'
```

asks:

```text
Is something listening on TCP 80?
```

## Application

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

asks:

```text
Is the application producing expected dynamic output?
```

One successful check does not automatically prove the others.

---

# Useful Troubleshooting Commands

## Processes

```bash
ps aux
```

```bash
ps aux | grep '[a]pache2'
```

```bash
ps aux | grep mariadbd
```

## Ports

```bash
ss -lntp
```

```bash
ss -lntp | grep ':80'
```

```bash
ss -lntp | grep 3306
```

## HTTP

```bash
curl -v http://localhost:8080
```

```bash
curl -I http://localhost:8080
```

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

## DNS

```bash
getent hosts db-server
```

## Database

```bash
mariadb -h db-server -u ecomuser -p
```

## Logs

```bash
tail -n 20 /var/log/apache2/error.log
```

## Configuration Search

```bash
grep -R "bind-address" /etc/mysql/
```

## File Search

```bash
find . -type f -name "*.sql"
```

---

# `find` vs `grep`

Another useful command distinction from this project:

```text
find
→ find files/directories
```

Example:

```bash
find . -type f -name "*.sql"
```

Whereas:

```text
grep
→ find text inside files/input
```

Example:

```bash
grep -R "bind-address" /etc/mysql/
```

Choosing the correct tool makes troubleshooting faster.

---

# `grep` vs `sed`

Another distinction:

```text
grep
→ search for matching content

sed
→ process/edit text and print selected ranges
```

For example, to display lines 110 through 140:

```bash
sed -n '110,140p' index.php
```

This is different from asking `grep` to search for the literal text `110,140p`.

---

# Troubleshooting by Layers

A reusable troubleshooting model for this application is:

```text
Layer 1
Client
↓
Can the user make the request?

Layer 2
Host / Docker publishing
↓
Does localhost:8080 reach the container?

Layer 3
Web server
↓
Is Apache running and listening on :80?

Layer 4
Application runtime
↓
Is PHP executing?

Layer 5
Application configuration
↓
Are the DB_* settings correct?

Layer 6
Name resolution
↓
Does db-server resolve?

Layer 7
Network
↓
Can the application tier reach the database tier?

Layer 8
Database service
↓
Is MariaDB running and listening on :3306?

Layer 9
Authentication
↓
Can ecomuser authenticate?

Layer 10
Authorization
↓
Does ecomuser have access to ecomdb?

Layer 11
Database structure
↓
Does ecomdb.products exist?

Layer 12
Data
↓
Are the expected product rows present?
```

---

# Verification After a Fix

A fix is not complete until it is verified.

For example, after repairing Apache:

```bash
ss -lntp | grep ':80'
```

then:

```bash
curl -I http://localhost:8080
```

then:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

After repairing database authentication:

```bash
mariadb -h db-server -u ecomuser -p
```

then:

```sql
SELECT * FROM ecomdb.products;
```

then test the application.

Verification should follow the same path the real application uses.

---

# Troubleshooting Principle

The main troubleshooting principle I developed during this project is:

```text
Do not ask:

"What command can I run to fix this?"

Ask:

"What evidence do I currently have,
which layer could produce this symptom,
and what test will narrow it down?"
```

That changes troubleshooting from random command execution into structured diagnosis.

---

# Final Troubleshooting Workflow

```text
1. Understand the reported symptom
                ↓
2. Reproduce the problem
                ↓
3. Determine what is already working
                ↓
4. Identify the next uncertain layer
                ↓
5. Run a targeted diagnostic test
                ↓
6. Interpret the result
                ↓
7. Narrow the failure domain
                ↓
8. Identify the root cause
                ↓
9. Change only what needs changing
                ↓
10. Verify locally
                ↓
11. Verify end-to-end
```

## Key Lesson

Good troubleshooting is not about knowing the largest number of Linux commands.

It is about knowing:

```text
what each command proves
```

and:

```text
what it does not prove.
```

That principle allows the same troubleshooting approach to be applied later to virtual machines, cloud infrastructure, containers, CI/CD systems, and more complex distributed applications.
