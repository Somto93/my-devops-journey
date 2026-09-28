# Databases

This section documents my practical learning of database fundamentals as part of my DevOps journey.

The goal of this section is to understand how databases work, how database services are installed and managed on Linux, how applications and users connect to databases, and how to troubleshoot database-related issues.

The practical work covers both **relational databases (SQL)** and **NoSQL databases**, with a focus on **MySQL** and **MongoDB**.

---

## What I Learned

### Database Fundamentals

- What a database is
- Why applications use databases
- Relational (SQL) databases
- NoSQL databases
- Databases, tables, rows, and columns
- Databases, collections, documents, and fields
- SQL vs NoSQL database structures

### MySQL

I performed hands-on MySQL administration on Ubuntu, including:

- Installing MySQL Server
- Managing the MySQL systemd service
- Identifying the `mysqld` process
- Checking listening ports with `ss`
- Connecting to MySQL
- Viewing databases
- Creating and selecting databases
- Creating tables
- Describing table structures
- Inserting data
- Querying and filtering data
- Creating MySQL users
- Understanding authentication and authorization
- Granting database privileges
- Checking user grants
- Testing access using a non-root database user
- Inspecting MySQL configuration
- Understanding `bind-address`
- Inspecting MySQL logs
- Understanding MySQL's default ports

### MongoDB

I studied the MongoDB administration workflow, including:

- MongoDB installation concepts
- MongoDB package repositories
- The `mongod` database server
- MongoDB service management
- MongoDB logs
- `/etc/mongod.conf`
- MongoDB's default port `27017`
- `bindIp`
- MongoDB shell concepts
- Databases
- Collections
- Documents
- Fields
- Inserting documents
- Finding documents
- Filtering documents

> MongoDB was not installed directly during this lab because the host system was running Ubuntu 26.04 and the MongoDB package repository used in the learning material was not configured for this environment. Rather than forcing an incompatible repository configuration, the MongoDB installation and shell workflow was studied from the learning material and reserved for practical reproduction in a supported environment.

---

## SQL and NoSQL Structure

A useful conceptual mapping is:

| Relational / SQL | MongoDB |
|---|---|
| Database | Database |
| Table | Collection |
| Row / Record | Document |
| Column | Field |

For example:

```text
SQL

Database
└── Table
    └── Row
        └── Columns
```

Compared with:

```text
MongoDB

Database
└── Collection
    └── Document
        └── Fields
```

---

## Database Administration Troubleshooting Approach

One of the main goals of this section was to avoid immediately changing or reinstalling software when something fails.

Instead, I use an evidence-based troubleshooting process:

```text
Service
   ↓
Process
   ↓
Configuration
   ↓
Listening IP and Port
   ↓
Client Connection
   ↓
Authentication
   ↓
Authorization
   ↓
Database Operations
   ↓
Logs
```

For example, if a database client cannot connect, I should not immediately assume that the database needs to be reinstalled.

I can investigate:

1. Is the database service running?
2. Is the expected database process running?
3. Is the process listening on the expected port?
4. Which IP address/interface is it bound to?
5. Does the runtime state match the configuration?
6. Can the client reach the database?
7. Is authentication succeeding?
8. Does the authenticated user have the required privileges?
9. What do the service and database logs show?

This approach helps identify the failing layer before making changes.

---

## Directory Structure

```text
databases/
├── README.md
├── 01-database-fundamentals.md
├── 02-sql-vs-nosql.md
├── 03-mysql-installation-and-service.md
├── 04-mysql-databases-and-tables.md
├── 05-mysql-users-and-privileges.md
├── 06-mysql-configuration-and-logs.md
├── 07-mongodb-installation-and-service.md
├── 08-mongodb-configuration-and-logs.md
├── 09-mongodb-shell-and-operations.md
├── 10-database-troubleshooting.md
└── lab/
```

---

## Key Takeaway

Databases are not only about storing and querying data.

From a DevOps perspective, I also need to understand the complete path between the operating system and the database:

```text
Linux
  ↓
Database Package
  ↓
Database Service
  ↓
Database Process
  ↓
Configuration
  ↓
Network Socket
  ↓
Database Client
  ↓
Authentication and Authorization
  ↓
Data
```

Understanding each layer makes database deployment, administration, security, and troubleshooting much easier.
