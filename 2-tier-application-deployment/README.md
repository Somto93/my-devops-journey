# Two-Tier Application Deployment

## Overview

This module documents my practical deployment of a two-tier ecommerce application.

The project was used to combine several concepts I previously learned, including:

- Linux administration
- Linux services
- Networking
- Apache
- PHP
- MariaDB
- SQL
- Git
- Environment variables
- Ports and listening services
- Application troubleshooting
- Deployment security

The application used for the practical lab is the KodeKloud Learning App Ecommerce project.

## What Is a Two-Tier Application?

A two-tier application separates the system into two major tiers:

1. Web/Application Tier
2. Database Tier

In this lab:

```text
User
 │
 │ HTTP
 ▼
Web/Application Tier
Apache + PHP
 │
 │ TCP 3306
 ▼
Database Tier
MariaDB
```

The web server handles HTTP requests and executes the PHP application.

The PHP application communicates with MariaDB to retrieve product information.

---

## My Local Lab Architecture

I used Docker containers to simulate separate Linux servers on my local machine.

```text
                     WSL Host
                        │
                 localhost:8080
                        │
                 Docker Port Map
                   8080 → 80
                        │
                        ▼
              ┌──────────────────┐
              │    web-server    │
              │   172.18.0.3     │
              │                  │
              │ Apache           │
              │ PHP              │
              │ Ecommerce App    │
              └────────┬─────────┘
                       │
                       │ TCP 3306
                       │
                two-tier-network
                       │
                       ▼
              ┌──────────────────┐
              │    db-server     │
              │   172.18.0.2     │
              │                  │
              │ MariaDB          │
              │ ecomdb           │
              │ products table   │
              └──────────────────┘
```

Docker was used as the local lab infrastructure to provide separate network namespaces, filesystems, processes, and IP addresses for the two tiers.

The application itself was manually configured inside the containers so that I could practise Linux administration rather than simply running a pre-built application stack.

---

## Application Flow

A normal request follows this path:

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
mysqli_connect()
   ↓
db-server:3306
   ↓
MariaDB
   ↓
ecomdb
   ↓
products table
   ↓
PHP renders products
   ↓
Browser
```

---

## Database Configuration

The application database is:

```text
ecomdb
```

The application database user is:

```text
ecomuser
```

The PHP application receives its database configuration through environment variables:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

The database hostname used by the application is:

```text
db-server
```

Docker DNS resolves this hostname to the database container.

This means the application does not need to hard-code the database container's IP address.

---

## Application Source

The application used in this lab originated from:

```text
https://github.com/kodekloudhub/learning-app-ecommerce.git
```

The upstream application code is not my original application code.

My work in this project focuses on:

- infrastructure setup
- deployment
- Linux configuration
- Apache configuration
- PHP runtime setup
- MariaDB configuration
- database initialization
- environment configuration
- networking
- troubleshooting
- deployment security
- break/fix exercises

---

## Troubleshooting Approach

Throughout this lab I followed the principle:

```text
Observe the symptom
        ↓
Gather evidence
        ↓
Identify the failing layer
        ↓
Form a hypothesis
        ↓
Test the hypothesis
        ↓
Apply the fix
        ↓
Verify recovery
```

I avoided immediately restarting services or modifying configuration without first collecting evidence.

---

## Troubleshooting Tools Used

Commands used throughout the project included:

```bash
curl
ss
ps
grep
sed
tail
find
getent
mariadb
docker
service
```

Examples:

```bash
ss -lntp
```

Check listening TCP ports and processes.

```bash
curl -v http://localhost:8080
```

Test HTTP connectivity and inspect the request/response process.

```bash
tail -n 20 /var/log/apache2/error.log
```

Inspect recent Apache and PHP errors.

```bash
mariadb -h db-server -u ecomuser -p
```

Test database connectivity from the web tier.

---

## Break/Fix Scenarios Practised

The lab included troubleshooting scenarios involving:

- Apache not running
- No listener on TCP port 80
- MariaDB connectivity failures
- MariaDB listening-interface configuration
- Database authentication failures
- Incorrect database credentials
- Missing database records
- PHP database connection failures
- Historical versus current log evidence

These exercises reinforced that similar user-facing symptoms can have very different root causes.

---

## Deployment Security Lessons

The initial lab deployment copied the complete Git repository into Apache's document root.

Inspection identified files that should not be part of the public runtime deployment, including:

```text
.git/
assets/db-load-script.sql
```

These were removed from the deployed runtime.

This demonstrated an important distinction:

```text
Source Repository
       ≠
Production Deployment Artifact
```

A source repository may contain development files, documentation, Git metadata, database initialization scripts, and other resources that the running web application does not require.

---

## Key Lesson

The most important lesson from this project was that troubleshooting should be evidence-driven.

For example:

```text
Connection refused
```

suggests investigating whether the destination service is reachable and listening.

Whereas:

```text
Access denied
```

shows that the request reached the database server and shifts the investigation toward authentication, accounts, or privileges.

Understanding these distinctions makes troubleshooting faster and reduces unnecessary changes to healthy parts of the system.
