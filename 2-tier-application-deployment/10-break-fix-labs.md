# Two-Tier Application Break/Fix Labs

## Overview

After successfully deploying the two-tier ecommerce application, I used break/fix scenarios to practise troubleshooting.

The goal was not simply to restore the application.

The goal was to practise:

```text
Symptom
   ↓
Evidence collection
   ↓
Failure isolation
   ↓
Root cause
   ↓
Targeted fix
   ↓
Verification
```

The application architecture was:

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
db-server:3306
   ↓
MariaDB
   ↓
ecomdb.products
```

---

# Lab 1 — Reported Website Failure

## Reported Symptom

The initial report was:

```text
The website is not opening.
```

Rather than restarting Apache immediately, I first attempted to reproduce the problem.

I used:

```bash
curl -v http://localhost:8080
```

## Evidence

The request successfully returned the application HTML.

I then tested the dynamic database-backed content:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

All eight product records appeared.

## Diagnosis

The reported problem could not be reproduced at the time of investigation.

Current evidence showed:

```text
HTTP connectivity       ✓
Apache                   ✓
PHP/application          ✓
Database connectivity   ✓
Product data             ✓
```

## Action

No service was restarted and no configuration was changed.

## Lesson

A user report describes an observed symptom, but the system may have recovered or the issue may have been intermittent.

Always attempt to reproduce the problem before changing a healthy system.

```text
Report
  ≠
Current confirmed failure
```

---

# Lab 2 — Database Listening Interface

## Scenario

The application tier and database tier run on separate network namespaces.

MariaDB originally listened on:

```text
127.0.0.1:3306
```

## Investigation

I checked:

```bash
ss -lntp | grep 3306
```

and inspected:

```bash
grep -R "bind-address" /etc/mysql/
```

The active MariaDB configuration contained:

```ini
bind-address = 127.0.0.1
```

## Interpretation

`127.0.0.1` refers to the database container's loopback interface.

The separate `web-server` container cannot use `db-server`'s loopback interface.

The application requires:

```text
web-server
     │
     │ TCP 3306
     ▼
db-server
```

## Fix

For this isolated lab environment, the MariaDB configuration was changed to:

```ini
bind-address = 0.0.0.0
```

MariaDB was restarted so the configuration change could take effect.

## Verification

I checked:

```bash
ss -lntp | grep 3306
```

and confirmed MariaDB was listening on:

```text
0.0.0.0:3306
```

I then tested from `web-server`:

```bash
mariadb -h db-server -u ecomuser -p
```

The connection succeeded.

## Lesson

A service can be:

```text
Running
```

while still being:

```text
Unreachable from another host/container
```

because service state and network binding are separate concepts.

---

# Lab 3 — Database Credential Mismatch

## Symptom

The website loaded, but database-backed product content was unavailable.

This indicated that the web tier was at least partially healthy.

## Application Inspection

The PHP application was inspected using:

```bash
grep -n "mysqli_query\|mysqli_fetch" index.php
```

and:

```bash
sed -n '110,140p' index.php
```

The application used environment variables and:

```php
mysqli_connect()
```

to establish the database connection.

---

## Remote Database Test

From `web-server`:

```bash
mariadb -h db-server -u ecomuser -p
```

returned:

```text
ERROR 1045 (28000): Access denied
```

## Interpretation

This was important evidence.

`Access denied` showed that the request reached MariaDB.

Therefore:

```text
Name resolution/network path   functioning far enough
TCP connection                 reached MariaDB
MariaDB                        responding
Authentication                failed
```

This was not the same as:

```text
Connection refused
```

---

## Account Investigation

On `db-server`:

```sql
SELECT User, Host
FROM mysql.user
WHERE User='ecomuser';
```

showed:

```text
ecomuser
%
```

The privileges were inspected:

```sql
SHOW GRANTS FOR 'ecomuser'@'%';
```

The account had access to:

```text
ecomdb.*
```

The application configuration was also checked.

The account existed, the host matching was appropriate for the lab, and the expected database privileges were present.

The evidence narrowed the problem toward the credential.

---

## Fix

The intended application credential was restored using:

```sql
ALTER USER 'ecomuser'@'%' IDENTIFIED BY '<intended-password>';
```

The real password is intentionally omitted from this documentation.

---

## Verification

From `web-server`:

```bash
mariadb -h db-server -u ecomuser -p
```

was tested again.

The application was then tested from WSL:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

The product records were restored.

---

## Lesson

Error messages tell us how far a request progressed.

```text
Connection refused
→ investigate service/listener/network path

Access denied
→ request reached database authentication
```

Do not troubleshoot the wrong layer.

---

# Lab 4 — Apache Not Running

## Symptom

The website was completely unavailable.

## Initial Check

The `web-server` container itself was running.

I checked listening ports:

```bash
ss -lntp
```

There was no listener on:

```text
TCP 80
```

## Interpretation

The container was healthy enough to provide a shell, but the expected web service was not listening.

I checked:

```bash
service apache2 status
```

Apache was not running.

---

## Log Investigation

Before restarting the service, I inspected:

```bash
tail -n 20 /var/log/apache2/error.log
```

The log showed a shutdown event involving:

```text
SIGTERM
```

There was no obvious Apache configuration failure in the inspected entries.

A SIGTERM indicates that the process received a termination signal, but by itself it does not explain why the signal was sent.

---

## Local HTTP Test

A local request to port 80 failed because nothing was listening:

```bash
curl -I http://localhost:80
```

This reinforced that the immediate failure was inside the web tier rather than being caused first by Docker host port publishing.

---

## Fix

Apache was started:

```bash
service apache2 start
```

---

## Verification

First:

```bash
ss -lntp | grep ':80'
```

confirmed:

```text
0.0.0.0:80
```

Then local HTTP was tested:

```bash
curl -I http://localhost:80
```

Then from WSL:

```bash
curl -I http://localhost:8080
```

Finally:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

confirmed that database-backed product content was also available.

---

## Lesson

Verification should move outward through the architecture:

```text
Process
   ↓
Listener
   ↓
Local HTTP
   ↓
External HTTP
   ↓
Dynamic application
```

This identifies exactly which layers have recovered.

---

# Lab 5 — Missing Product Records

## Symptom

The website loaded, but no products appeared.

The database service and connection were available.

## Investigation

On `db-server`:

```sql
USE ecomdb;
SELECT * FROM products;
```

returned:

```text
Empty set
```

## Interpretation

This narrowed the problem significantly:

```text
MariaDB service        ✓
Database connection    ✓
Authentication         ✓
ecomdb                  ✓
products table          ✓
Product rows            ✗
```

---

## Inspecting the Schema

I checked:

```sql
DESCRIBE products;
```

The expected table structure was still present.

Therefore, rebuilding the entire database was unnecessary.

---

## Considering the Initialization Script

The original SQL initialization script contains both:

```sql
CREATE TABLE products ...
```

and:

```sql
INSERT INTO products ...
```

Since the table already existed, blindly re-running the complete initialization script was not the cleanest repair.

The failed component was the data, not the schema.

---

## Fix

The required product records were restored using the appropriate:

```sql
INSERT INTO products ...
```

statement.

---

## Verification

I checked:

```sql
SELECT COUNT(*) FROM products;
```

The expected result was:

```text
8
```

Then I verified from the application:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

All eight product lines appeared.

---

## No Restart Required

MariaDB was not restarted after restoring the rows.

The `INSERT` operation modifies data in the running database immediately.

This reinforced the difference between:

```text
Configuration change
→ may require reload/restart
```

and:

```text
Data change
→ generally does not require service restart
```

---

# Lab 6 — Historical Error Log

## Situation

During investigation of database-related behaviour, Apache's error log contained:

```text
mysqli_sql_exception: Connection refused
```

This initially appeared to identify the problem.

## Current-State Testing

However:

```bash
ss -lntp | grep 3306
```

showed MariaDB listening.

From `web-server`:

```bash
mariadb -h db-server -u ecomuser -p
```

worked.

The database query returned all eight records.

The application also returned:

```text
Purchase ...
```

for all products.

## Diagnosis

The log entry had an older timestamp.

It represented a previous connection failure rather than the application's current state.

## Lesson

A log entry is evidence, but its timing matters.

Always combine:

```text
Log message
+
Timestamp
+
Current system state
+
Current reproduction
```

before concluding that a log message represents the active incident.

---

# Lab 7 — Deployment Security Review

## Situation

The application was working correctly, but the deployed web root was inspected:

```bash
ls -la /var/www/html
```

The runtime contained:

```text
.git/
assets/db-load-script.sql
```

## Investigation

The `.git` directory was repository metadata and was not required for runtime operation.

The SQL file was a database initialization resource and was also unnecessary for normal web serving.

## Fix

The runtime Git metadata was removed:

```bash
rm -rf /var/www/html/.git
```

The runtime SQL initialization script was removed:

```bash
rm /var/www/html/assets/db-load-script.sql
```

These changes affected only the deployed copy inside the web container.

---

## Verification

After cleanup:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

still returned all eight product records.

## Lesson

Operational work does not end when:

```text
"The website works."
```

A deployment should also be inspected for unnecessary exposure.

At the same time, every security cleanup should be followed by functional verification.

---

# Commands and What They Prove

One of the biggest lessons from these exercises was understanding what each diagnostic command actually proves.

## `docker ps`

```bash
sudo docker ps
```

Proves:

```text
Container state
```

Does not prove:

```text
Application inside container is healthy
```

---

## `ps`

```bash
ps aux | grep '[a]pache2'
```

Proves:

```text
Apache process exists
```

Does not by itself prove:

```text
Apache is listening correctly
HTTP request succeeds
Application works
```

---

## `ss`

```bash
ss -lntp | grep ':80'
```

Proves:

```text
A process is listening on TCP 80
```

It does not prove the complete application works.

---

## `curl -I`

```bash
curl -I http://localhost:8080
```

Tests:

```text
HTTP response
```

It does not necessarily prove database-backed functionality.

---

## Dynamic Application Test

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

Provides stronger evidence that the ecommerce application's database-backed product rendering is functioning.

---

## `getent`

```bash
getent hosts db-server
```

Tests:

```text
Hostname resolution
```

It does not prove MariaDB is running.

---

## MariaDB Client

```bash
mariadb -h db-server -u ecomuser -p
```

Tests multiple layers:

```text
Name resolution
Network path
TCP connection
MariaDB listener
Authentication
```

Further SQL queries can then verify authorization and data.

---

# Troubleshooting Decisions

The goal of troubleshooting is not:

```text
Run every command I know.
```

Instead:

```text
Run the command that answers
the next important question.
```

For example:

```text
No port 80 listener
```

makes checking database rows a poor next step.

Similarly:

```text
Access denied from MariaDB
```

makes restarting Apache an unrelated response.

Each result should determine the next investigation step.

---

# Interview Explanation

A concise way I can describe this project in an interview is:

> I deployed a two-tier PHP ecommerce application using separate Ubuntu containers for the web and database tiers. I configured Apache, PHP, MariaDB, Docker networking, database users and application environment variables. After getting the application working end-to-end, I deliberately worked through failure scenarios involving web-service outages, database network binding, authentication failures, missing database records and stale log evidence. I focused on isolating failures by layer rather than restarting services blindly, and verified each repair from the component level through to the user-facing application.

---

# What This Project Reinforced

The break/fix exercises combined concepts from several areas of my DevOps learning:

```text
Linux
Services
Processes
Networking
Ports
DNS
Apache
PHP
MariaDB
SQL
Git
Docker
Logs
Security
Troubleshooting
```

Rather than treating these as isolated topics, the application demonstrated how they interact in a real deployment.

---

# Final Troubleshooting Principle

The most important principle from the project is:

```text
Symptom
   ↓
Evidence
   ↓
Layer
   ↓
Root cause
   ↓
Targeted change
   ↓
Verification
```

The objective is not simply to restore service.

The objective is to understand:

```text
What failed?
Why did it fail?
What evidence proves it?
What is the smallest appropriate fix?
How do I prove the system is healthy again?
```

That troubleshooting approach can be reused as I move from local containers to virtual machines, cloud infrastructure, CI/CD pipelines, Kubernetes, and larger distributed systems.
