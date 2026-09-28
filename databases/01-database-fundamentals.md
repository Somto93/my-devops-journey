# Database Fundamentals

## What Is a Database?

A database is an organized collection of data that can be stored, accessed, managed, and updated.

Applications commonly use databases to store information that needs to remain available even after the application or server process stops.

Examples of information stored in databases include:

- User accounts
- Customer information
- Products
- Orders
- Transactions
- Application configuration
- Employee records

Instead of storing all application information directly inside application code, the application can communicate with a database to store and retrieve data.

A simplified architecture is:

```text
User
  ↓
Application
  ↓
Database
  ↓
Stored Data
```

---

## Database Management System

A Database Management System (DBMS) is software used to manage databases.

It provides mechanisms for applications and users to:

- Create data
- Read data
- Update data
- Delete data
- Organize data
- Control access to data

These common operations are often referred to as **CRUD**:

```text
C → Create
R → Read
U → Update
D → Delete
```

---

## Types of Databases

The two main database models covered in this section are:

```text
Databases
├── Relational / SQL
└── NoSQL
```

Examples of relational databases introduced in the learning material include:

- MySQL
- PostgreSQL
- Microsoft SQL Server

Examples of NoSQL databases introduced include:

- MongoDB
- Amazon DynamoDB
- Apache Cassandra

---

# Relational Databases

A relational database organizes data into **tables**.

A table contains:

```text
Table
├── Columns
└── Rows
```

For example:

| id | name | age | location |
|---:|---|---:|---|
| 1 | John | 28 | London |
| 2 | Sarah | 32 | New York |
| 3 | Mike | 25 | Sydney |

In this example:

```text
people
│
├── Columns
│   ├── id
│   ├── name
│   ├── age
│   └── location
│
└── Rows
    ├── John
    ├── Sarah
    └── Mike
```

Each row represents a record.

Each column represents a particular attribute of the records.

---

## SQL

SQL stands for **Structured Query Language**.

It is used to interact with relational databases.

During the MySQL practical, I used SQL commands such as:

```sql
SHOW DATABASES;
```

```sql
CREATE DATABASE somto_db;
```

```sql
USE somto_db;
```

```sql
CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    location VARCHAR(100)
);
```

```sql
SELECT * FROM people;
```

SQL therefore provides a structured way to work with databases, tables, and their data.

---

# NoSQL Databases

NoSQL databases do not necessarily organize information using the traditional relational table structure.

MongoDB was the NoSQL database covered in the learning material.

MongoDB organizes information using:

```text
Database
   ↓
Collection
   ↓
Document
   ↓
Fields
```

For example, a document could conceptually contain:

```text
name     → John Doe
age      → 45
location → New York
salary   → 5000
```

The learning material demonstrated this type of document inside a MongoDB collection.

---

# Relational and MongoDB Terminology

A useful conceptual mapping is:

| Relational Database | MongoDB |
|---|---|
| Database | Database |
| Table | Collection |
| Row / Record | Document |
| Column | Field |

For example:

```text
Relational Database

school
└── persons table
    └── row
        ├── name
        ├── age
        └── location
```

The MongoDB equivalent can be represented as:

```text
MongoDB

school
└── persons collection
    └── document
        ├── name
        ├── age
        └── location
```

---

# Database Server and Database Client

Another important distinction is between the **database server** and the **database client**.

The database server is responsible for running the database engine and managing the stored data.

The client is used to connect to and communicate with that server.

For the databases covered in this section:

```text
Database       Server/Daemon       Client/Shell
--------       -------------       ------------
MySQL          mysqld              mysql
MongoDB        mongod              mongo/mongosh
```

For example:

```text
mysql client
     ↓
MySQL server (mysqld)
     ↓
Database
     ↓
Tables
     ↓
Rows
```

This distinction is useful when troubleshooting because the database server can be running while a client connection may still fail.

---

# Databases as Linux Services

Database servers commonly run as background services on Linux.

For example, during the MySQL practical I checked the MySQL service using:

```bash
systemctl status mysql
```

The service was:

```text
Active: active (running)
```

The actual database server process was:

```text
mysqld
```

For MongoDB, the learning material uses:

```bash
systemctl start mongod
```

and:

```bash
systemctl status mongod
```

This creates an important distinction:

```text
Database Product
       ↓
Linux Service
       ↓
Database Process
       ↓
Listening Network Socket
       ↓
Client Connection
```

A service reporting `active (running)` does not by itself prove that the database is listening on the expected network address and port.

---

# Database Ports

Database servers can listen for network connections on TCP ports.

During the MySQL practical, I used:

```bash
sudo ss -ltnp
```

and observed MySQL listening on:

```text
127.0.0.1:3306
127.0.0.1:33060
```

The important ports covered during this section were:

| Database | Port | Purpose |
|---|---:|---|
| MySQL | 3306 | Standard MySQL client/server connections |
| MySQL | 33060 | MySQL X Protocol |
| MongoDB | 27017 | MongoDB connections |

A listening socket can therefore provide evidence that a database process is accepting network connections.

---

# Loopback Address

During both the MySQL practical and MongoDB configuration study, I encountered:

```text
127.0.0.1
```

This is the IPv4 loopback address.

If a database is listening only on:

```text
127.0.0.1
```

it is accepting network connections through the local machine's loopback interface rather than through all external network interfaces.

For example:

```text
127.0.0.1:3306
```

means MySQL is listening locally on port `3306`.

The MongoDB learning material similarly showed:

```yaml
bindIp: 127.0.0.1
```

with MongoDB using port:

```text
27017
```

Understanding the bind address is important when troubleshooting local versus remote database connections.

---

# Authentication and Authorization

Database access involves two different concepts.

## Authentication

Authentication answers:

> Who are you?

For example, connecting to MySQL using:

```bash
mysql -u somto_user -p
```

requires MySQL to authenticate the specified database account.

---

## Authorization

Authorization answers:

> What are you allowed to do?

A user may successfully authenticate but still lack permission to access a database or perform an operation.

During the MySQL practical, I granted a user privileges on a specific database:

```sql
GRANT ALL PRIVILEGES ON somto_db.* TO 'somto_user'@'localhost';
```

This allowed the user to work with objects inside `somto_db`.

Therefore:

```text
Authentication
      ↓
Who are you?
      ↓
Authorization
      ↓
What can you access/do?
```

These are separate stages and should be considered separately during troubleshooting.

---

# Configuration, Runtime State, and Logs

Database administration involves more than querying data.

A DevOps engineer may need to inspect:

```text
Service
Process
Configuration
Network ports
Bind addresses
Authentication
Authorization
Logs
```

Configuration describes how the service **should** operate.

Runtime inspection shows how it is **actually** operating.

Logs provide evidence about what has happened inside the service.

For example:

```text
Configuration
     ↓
Expected behaviour

ss / process inspection
     ↓
Actual runtime behaviour

Logs
     ↓
Events, warnings and errors
```

Comparing these layers is useful when diagnosing database problems.

---

# Key Takeaway

A database should not be viewed only as somewhere an application stores data.

From a DevOps perspective, the complete system includes:

```text
Operating System
       ↓
Database Package
       ↓
Database Service
       ↓
Database Process
       ↓
Configuration
       ↓
Network Interface + Port
       ↓
Database Client
       ↓
Authentication
       ↓
Authorization
       ↓
Database
       ↓
Tables / Collections
       ↓
Rows / Documents
```

Understanding these layers provides a foundation for installing, operating, securing, and troubleshooting database systems.
