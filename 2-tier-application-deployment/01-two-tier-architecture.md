# Two-Tier Application Architecture

## What Is a Two-Tier Application?

A two-tier application separates an application into two main layers:

1. Web/Application Tier
2. Database Tier

In the ecommerce application used in this lab, the architecture can be represented as:

```text
             User / Browser
                   │
                   │ HTTP
                   ▼
        ┌─────────────────────┐
        │ Web/Application Tier│
        │                     │
        │ Apache              │
        │ PHP                 │
        │ Ecommerce App       │
        └──────────┬──────────┘
                   │
                   │ TCP 3306
                   ▼
        ┌─────────────────────┐
        │    Database Tier    │
        │                     │
        │ MariaDB             │
        │ ecomdb              │
        │ products table      │
        └─────────────────────┘
```

The two tiers have different responsibilities but work together to provide the complete application.

---

## Tier 1 — Web/Application Tier

The web/application tier receives requests from users.

In this project, the tier contains:

```text
Apache
PHP
Ecommerce application
```

Apache listens for HTTP requests.

PHP executes the application logic.

The application then communicates with the database when it needs product information.

For example, the application executes a query similar to:

```sql
SELECT * FROM products;
```

The returned database records are used by PHP to dynamically generate the product section of the webpage.

---

## Tier 2 — Database Tier

The database tier stores the application's persistent data.

In this project, the database server runs:

```text
MariaDB
```

The application database is:

```text
ecomdb
```

The main table used by the ecommerce application is:

```text
products
```

The table contains fields such as:

```text
id
Name
Price
ImageUrl
```

The database server listens for MariaDB connections on:

```text
TCP 3306
```

---

## Which Tier Initiates the Database Connection?

The web/application tier initiates the connection to the database tier.

The direction is:

```text
web-server
     │
     │ TCP 3306
     ▼
db-server
```

The database server does not normally initiate the application database connection back to the web server.

Instead, MariaDB listens for incoming connections.

---

## Listening vs Connecting

This distinction is important.

The database server:

```text
LISTENS on TCP 3306
```

The web server:

```text
CONNECTS to TCP 3306
```

For example:

```text
Web Server
172.18.0.3
      │
      │ connection request
      ▼
Database Server
172.18.0.2:3306
```

If MariaDB is not listening on an interface reachable from the web server, the application cannot establish the database connection.

---

## MariaDB Bind Address

MariaDB can be configured to listen on particular network interfaces.

For example:

```text
127.0.0.1:3306
```

means MariaDB is listening only on the local loopback interface.

A remote web server cannot use the database server's loopback interface.

In our lab, MariaDB was configured with:

```ini
bind-address = 0.0.0.0
```

This means MariaDB listens on all available IPv4 interfaces.

The result can be checked using:

```bash
ss -lntp | grep 3306
```

A healthy result in our lab looked like:

```text
0.0.0.0:3306
```

---

## 0.0.0.0 vs 127.0.0.1

These addresses have different meanings.

```text
127.0.0.1
```

means:

```text
Loopback only
This machine/container only
```

Whereas:

```text
0.0.0.0
```

when used as a listening address means:

```text
Listen on all available IPv4 interfaces
```

A specific address such as:

```text
172.18.0.2
```

would mean the service is bound specifically to that interface/address.

---

## Database Accounts and Network Binding Are Different

Two concepts that can look similar but perform different jobs are:

```text
bind-address = 0.0.0.0
```

and:

```sql
'ecomuser'@'%'
```

They are not the same thing.

### bind-address

This controls which network interfaces MariaDB listens on.

```ini
bind-address = 0.0.0.0
```

means MariaDB can listen for connections through all IPv4 interfaces.

### MariaDB Host Component

The account:

```sql
'ecomuser'@'%'
```

uses `%` as a MariaDB host wildcard.

It controls which source hosts are permitted to authenticate using that MariaDB account.

Therefore:

```text
0.0.0.0
→ network listening configuration

%
→ MariaDB account host matching
```

Both may affect remote database access, but at different layers.

---

## Application Database Connection

The PHP application uses `mysqli_connect()` to establish the database connection.

Conceptually:

```php
mysqli_connect(
    database_host,
    database_user,
    database_password,
    database_name
);
```

In this project, those values are provided through environment variables:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

The application therefore does not need the database credentials hard-coded directly into the PHP source.

---

## Application Request Flow

When a user requests the ecommerce website, the complete flow is:

```text
1. User requests website
          ↓
2. Request reaches Apache
          ↓
3. Apache processes index.php
          ↓
4. PHP reads database configuration
          ↓
5. PHP connects to MariaDB
          ↓
6. MariaDB authenticates the user
          ↓
7. PHP executes SELECT query
          ↓
8. MariaDB returns product records
          ↓
9. PHP generates HTML
          ↓
10. Apache returns the webpage
          ↓
11. User sees the products
```

A failure at any point in this chain can produce a different symptom.

---

## Static vs Dynamic Content

An important lesson from this lab was distinguishing static webpage content from database-backed dynamic content.

The website could still display:

```text
HTML
CSS
images
navigation
headings
```

even if the database connection failed.

Therefore:

```text
Website loads
```

does not automatically mean:

```text
Database works
```

We verified dynamic database content using:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

The application generates product descriptions containing the word:

```text
Purchase
```

from rows returned by the `products` table.

Seeing all eight product lines therefore provided stronger evidence that the complete application-to-database path was functioning.

---

## Two-Tier Troubleshooting Mindset

When troubleshooting this architecture, I learned to think in layers:

```text
Client
  ↓
HTTP connectivity
  ↓
Web server
  ↓
PHP/application
  ↓
Database configuration
  ↓
Name resolution
  ↓
Network connectivity
  ↓
Database listener
  ↓
Authentication
  ↓
Privileges
  ↓
Database
  ↓
Table
  ↓
Data
```

Rather than immediately changing configuration, I can test each layer and progressively narrow down the failure.

---

## Key Takeaway

A two-tier application is not simply "a website and a database."

It is a chain of dependent components:

```text
Web Server
    +
Application Runtime
    +
Application Configuration
    +
Network
    +
Database Service
    +
Authentication
    +
Database Structure
    +
Application Data
```

Understanding how these components communicate makes it possible to troubleshoot the application systematically instead of guessing.
