# Database Tier Setup

## Overview

The database tier of the two-tier ecommerce application runs MariaDB.

In my local lab, the database tier runs inside the container:

```text
db-server
```

Its responsibilities include:

- running MariaDB
- storing the `ecomdb` database
- storing the `products` table
- accepting connections from the web/application tier
- authenticating the application database user
- returning product data to the PHP application

The communication path is:

```text
web-server
    │
    │ TCP 3306
    ▼
db-server
    │
    ▼
MariaDB
    │
    ▼
ecomdb
    │
    ▼
products
```

---

## Entering the Database Container

From the WSL host:

```bash
sudo docker exec -it db-server bash
```

This opens a shell inside the database container.

---

## Installing Networking Tools

The Ubuntu container image was minimal and did not initially contain the `ip` command.

I installed:

```bash
apt update
apt install iproute2 -y
```

I could then inspect the container's network configuration:

```bash
ip addr
```

During the lab, the database container had:

```text
172.18.0.2
```

This address helped me understand the network topology, although the application later used the hostname `db-server` rather than hard-coding this IP.

---

## Installing MariaDB

MariaDB was installed with:

```bash
apt install mariadb-server
```

I verified the installation using:

```bash
mariadb --version
```

The lab installed MariaDB 10.11.

---

## systemd Inside the Container

I initially attempted:

```bash
systemctl status mariadb
```

but received:

```text
systemctl: command not found
```

The minimal Ubuntu container was not running a normal `systemd`-based environment.

Therefore, I managed MariaDB using:

```bash
service mariadb start
```

instead.

This demonstrated an important lesson:

```text
Linux service management depends on the environment.
```

A command that works on a normal Ubuntu VM may not work inside a minimal container.

---

## Checking the MariaDB Process

I used:

```bash
ps aux | grep mariadbd
```

Before starting MariaDB, there was no actual MariaDB server process.

After:

```bash
service mariadb start
```

the MariaDB server process was running.

This confirmed the difference between:

```text
MariaDB package installed
```

and:

```text
MariaDB service actually running
```

Installing software does not automatically prove that the service is available.

---

## Checking Port 3306

I checked the MariaDB listener using:

```bash
ss -lntp | grep 3306
```

Initially MariaDB was listening on:

```text
127.0.0.1:3306
```

This meant MariaDB was only accepting connections through the database container's loopback interface.

That would prevent the separate `web-server` container from connecting remotely.

---

## Finding the MariaDB Bind Configuration

I searched the MariaDB configuration using:

```bash
grep -R "bind-address" /etc/mysql/
```

The active configuration contained:

```text
/etc/mysql/mariadb.conf.d/50-server.cnf:
bind-address = 127.0.0.1
```

Another configuration file contained a commented example, but the active setting was the one in:

```text
50-server.cnf
```

---

## Configuring MariaDB for Remote Connections

I edited:

```text
/etc/mysql/mariadb.conf.d/50-server.cnf
```

and changed:

```ini
bind-address = 127.0.0.1
```

to:

```ini
bind-address = 0.0.0.0
```

Because the minimal container did not initially include `nano`, I installed it before editing the file.

After changing the configuration, MariaDB was restarted.

I then verified the listener again:

```bash
ss -lntp | grep 3306
```

The expected result was:

```text
0.0.0.0:3306
```

This confirmed that MariaDB was listening on all available IPv4 interfaces.

---

## Connecting to MariaDB

I entered the MariaDB shell using:

```bash
mariadb
```

I inspected the existing databases:

```sql
SHOW DATABASES;
```

Initially the server contained the standard MariaDB databases such as:

```text
information_schema
mysql
performance_schema
sys
```

---

## Creating the Application Database

The ecommerce application requires:

```text
ecomdb
```

I created it using:

```sql
CREATE DATABASE ecomdb;
```

Then selected it:

```sql
USE ecomdb;
```

---

## Database Initialization Script

The application repository contained:

```text
assets/db-load-script.sql
```

The script creates the `products` table and inserts the initial ecommerce product records.

Because the script contains:

```sql
USE ecomdb;
```

the `ecomdb` database must already exist before the script is loaded.

---

## Copying the SQL Script to the Database Server

From the host repository, I copied the SQL file into the database container:

```bash
sudo docker cp assets/db-load-script.sql db-server:/opt/db-load-script.sql
```

The script was then available inside the database container at:

```text
/opt/db-load-script.sql
```

---

## Loading the Database Script

Inside MariaDB, I loaded the script using:

```sql
source /opt/db-load-script.sql;
```

The script created:

```text
products
```

and inserted eight records.

---

## Verifying the Product Data

I queried:

```sql
SELECT * FROM products;
```

The database contained:

```text
Laptop
Drone
VR
Tablet
Watch
Phone Covers
Phone
Laptop
```

with their corresponding prices and image filenames.

This confirmed:

```text
Database exists       ✓
Table exists          ✓
Schema exists         ✓
Product data exists   ✓
```

---

## Creating the Application Database User

The web application should not depend on unrestricted administrative database access.

I created:

```sql
CREATE USER 'ecomuser'@'%' IDENTIFIED BY 'ecompassword';
```

The account consists of two parts:

```text
ecomuser
```

which is the username, and:

```text
%
```

which is the MariaDB host-matching component.

The `%` wildcard allows the account to match connections from different source hosts.

It should not be confused with:

```ini
bind-address = 0.0.0.0
```

The two settings operate at different layers.

---

## Checking Initial Privileges

I checked the account using:

```sql
SHOW GRANTS FOR 'ecomuser'@'%';
```

Initially the account had only basic `USAGE` privileges and did not yet have application database permissions.

---

## Granting Application Privileges

I granted access to the ecommerce database:

```sql
GRANT ALL PRIVILEGES ON ecomdb.* TO 'ecomuser'@'%';
```

Then verified:

```sql
SHOW GRANTS FOR 'ecomuser'@'%';
```

The important scope is:

```text
ecomdb.*
```

This means:

```text
all objects inside ecomdb
```

It does **not** mean:

```text
all databases on the MariaDB server
```

---

## Testing the Application User

I tested the account using:

```bash
mariadb -u ecomuser -p
```

After authentication:

```sql
SHOW DATABASES;
```

showed the application database and the databases visible to that user.

I then tested:

```sql
USE ecomdb;
SELECT * FROM products;
```

The eight product records were returned successfully.

---

## Testing From the Web Tier

A local database login from `db-server` is useful, but it does not prove that the separate web tier can reach MariaDB.

From `web-server`, I used:

```bash
mariadb -h db-server -u ecomuser -p
```

This is a much stronger test.

The `-h db-server` option is important because it tells the MariaDB client to connect to the separate database container.

The successful connection demonstrated that:

```text
Docker DNS              ✓
Container networking    ✓
TCP 3306                ✓
MariaDB listener        ✓
Remote authentication   ✓
Database privileges     ✓
Database access         ✓
```

I then ran:

```sql
USE ecomdb;
SELECT * FROM products;
```

and received all eight product records from the database tier.

---

## Why `-h db-server` Matters

Running:

```bash
mariadb -u ecomuser -p
```

from the web container would attempt to use a local database connection rather than explicitly testing the remote database tier.

For the two-tier architecture, the useful test is:

```bash
mariadb -h db-server -u ecomuser -p
```

because the real application path is:

```text
web-server
    ↓
db-server
    ↓
MariaDB
```

---

## Database Troubleshooting Checks

Useful database-tier checks from this lab include:

```bash
ps aux | grep mariadbd
```

Check whether the MariaDB process exists.

```bash
ss -lntp | grep 3306
```

Check whether MariaDB is listening and on which interface.

```bash
grep -R "bind-address" /etc/mysql/
```

Locate MariaDB network binding configuration.

```bash
mariadb -h db-server -u ecomuser -p
```

Test the database from the application tier.

Inside MariaDB:

```sql
SHOW DATABASES;
SHOW TABLES;
DESCRIBE products;
SELECT * FROM products;
SHOW GRANTS FOR 'ecomuser'@'%';
```

These commands test different parts of the database environment.

---

## Connection Refused vs Access Denied

One of the most important troubleshooting lessons was distinguishing these errors.

### Connection Refused

An error such as:

```text
Connection refused
```

suggests investigating areas such as:

```text
Is MariaDB running?
Is port 3306 listening?
Is MariaDB bound to the correct interface?
Can the destination be reached?
```

The connection has not successfully progressed to normal database authentication.

### Access Denied

An error such as:

```text
ERROR 1045 (28000): Access denied
```

means the request reached MariaDB and MariaDB rejected the authentication attempt.

That shifts the investigation toward:

```text
Username
Password
Host matching
Authentication configuration
Account configuration
```

If authentication succeeds but an SQL operation is denied, database/object privileges should then be investigated.

---

## Data Changes Usually Do Not Require a Service Restart

Another lesson from the break/fix exercises was understanding when MariaDB needs to be restarted.

Changing configuration such as:

```ini
bind-address
```

normally requires MariaDB to reload/restart for the new configuration to take effect.

However, SQL operations such as:

```sql
INSERT
UPDATE
DELETE
CREATE TABLE
```

operate against the running database.

After restoring missing product rows with an `INSERT`, there was no reason to restart MariaDB.

Instead, the correct next step was verification:

```sql
SELECT COUNT(*) FROM products;
```

followed by application-level verification.

---

## Key Lesson

A healthy database tier requires more than simply having MariaDB installed.

The complete path includes:

```text
MariaDB installed
       ↓
MariaDB process running
       ↓
TCP 3306 listening
       ↓
Correct network binding
       ↓
Network reachable
       ↓
User exists
       ↓
Authentication succeeds
       ↓
Privileges are correct
       ↓
Database exists
       ↓
Table exists
       ↓
Required data exists
```

Each layer can be tested independently, making database troubleshooting systematic rather than based on guesswork.
