# MongoDB Shell and Operations

## Overview

This section covers the MongoDB shell operations demonstrated in the database learning material.

The material demonstrates how to:

- Enter the MongoDB shell
- List databases
- Select a database
- Create a collection
- List collections
- Insert a document
- Understand MongoDB's generated `_id`
- Retrieve documents
- Filter documents

MongoDB was not installed on my current Ubuntu machine during this practical, so these operations were **studied from the learning material rather than executed locally**.

The general workflow is:

```text
MongoDB Shell
     ↓
List Databases
     ↓
Select Database
     ↓
Create Collection
     ↓
Insert Document
     ↓
Query Documents
     ↓
Filter Results
```

---

# 1. MongoDB Shell

The learning material demonstrates entering the MongoDB shell using:

```bash
mongo
```

The shell provides an interactive environment for communicating with the MongoDB server.

Conceptually:

```text
MongoDB Shell
      ↓
MongoDB Server
      ↓
Database
      ↓
Collection
      ↓
Documents
```

The course material uses the `mongo` command.

In newer MongoDB environments, the shell may instead be called:

```bash
mongosh
```

For this documentation, the examples preserve the syntax and workflow shown in the learning material.

---

# 2. Client vs Server

It is important to distinguish the MongoDB shell from the MongoDB server.

```text
mongo / mongosh
       ↓
Client shell
```

while:

```text
mongod
   ↓
MongoDB server daemon
```

This is conceptually similar to MySQL:

```text
MySQL                     MongoDB
-----                     -------
mysql                     mongo / mongosh
Client                    Client

mysqld                    mongod
Server daemon             Server daemon
```

A client connects to the database server and sends database operations to it.

---

# 3. List MongoDB Databases

The learning material uses:

```javascript
show dbs
```

to display databases.

The example shows databases including:

```text
admin
config
local
```

This is conceptually similar to the MySQL command:

```sql
SHOW DATABASES;
```

Therefore:

```text
MySQL

SHOW DATABASES;
```

maps conceptually to:

```text
MongoDB

show dbs
```

---

# 4. Select a Database

The learning material selects a database using:

```javascript
use school
```

MongoDB responds:

```text
switched to db school
```

The current database is now:

```text
school
```

Conceptually:

```text
MongoDB Server
     ↓
school
```

---

# 5. MySQL USE vs MongoDB use

During the MySQL practical, I used:

```sql
USE somto_db;
```

The MongoDB material uses:

```javascript
use school
```

Both operations change the database context in which subsequent operations are performed.

Conceptually:

```text
MySQL

USE somto_db;
      ↓
Current database = somto_db
```

and:

```text
MongoDB

use school
      ↓
Current database = school
```

The syntax differs, but the idea of working within a selected database is similar.

---

# 6. Collections

MongoDB stores documents inside collections.

The conceptual hierarchy is:

```text
Database
   ↓
Collection
   ↓
Document
   ↓
Fields
```

For example:

```text
school
└── persons
    └── document
```

This differs from the relational structure used by MySQL:

```text
Database
   ↓
Table
   ↓
Row
   ↓
Columns
```

---

# 7. Create a Collection

The learning material creates a collection using:

```javascript
db.createCollection("persons")
```

The collection name is:

```text
persons
```

The structure can now be represented as:

```text
school
└── persons
```

The `db` object refers to the current database context.

Since the material previously used:

```javascript
use school
```

the collection is being created within the `school` database.

---

# 8. MySQL Table vs MongoDB Collection

During the MySQL practical, I created:

```sql
CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    location VARCHAR(100)
);
```

In the MongoDB material, a collection is created using:

```javascript
db.createCollection("persons")
```

Conceptually:

```text
MySQL                     MongoDB
-----                     -------
Table                     Collection
people                    persons
```

A collection serves a role conceptually similar to a table as a container for records/documents, although MongoDB and relational databases organize data differently.

---

# 9. List Collections

After creating the collection, the material uses:

```javascript
show collections
```

The result includes:

```text
persons
```

This verifies that the collection exists in the current database.

The MySQL equivalent concept is:

```sql
SHOW TABLES;
```

Therefore:

```text
MySQL                     MongoDB
-----                     -------
SHOW TABLES;              show collections
```

---

# 10. Insert a Document

The learning material inserts a document using:

```javascript
db.persons.insert({
    "name": "John Doe",
    "age": 45,
    "location": "New York",
    "salary": 5000
})
```

The document contains the fields:

```text
name
age
location
salary
```

and their corresponding values.

Conceptually:

```text
Document
│
├── name: John Doe
├── age: 45
├── location: New York
└── salary: 5000
```

---

# 11. Understanding the Insert Syntax

The command begins with:

```javascript
db
```

which refers to the current database.

Then:

```javascript
.persons
```

refers to the collection.

Then:

```javascript
.insert(...)
```

performs the insert operation shown in the material.

Therefore:

```text
db.persons.insert(...)
│    │       │
│    │       └── operation
│    └────────── collection
└─────────────── current database
```

---

# 12. MongoDB Documents

The inserted data is represented as a document:

```javascript
{
    "name": "John Doe",
    "age": 45,
    "location": "New York",
    "salary": 5000
}
```

This is different from thinking about data as a fixed table row.

A useful conceptual comparison is:

```text
MySQL row

id | name | age | location
```

compared with:

```text
MongoDB document

{
    "name": "John Doe",
    "age": 45,
    "location": "New York",
    "salary": 5000
}
```

---

# 13. Fields

Within the document:

```text
name
age
location
salary
```

are fields.

Their associated values are:

```text
John Doe
45
New York
5000
```

Conceptually:

```text
Field        Value
-----        -----
name         John Doe
age          45
location     New York
salary       5000
```

---

# 14. MongoDB _id

When the document is retrieved in the learning material, MongoDB displays an additional field:

```text
_id
```

with a value represented using:

```text
ObjectId(...)
```

Conceptually:

```javascript
{
    "_id": ObjectId(...),
    "name": "John Doe",
    "age": 45,
    "location": "New York",
    "salary": 5000
}
```

The `_id` identifies the document.

---

# 15. Comparing MySQL id and MongoDB _id

In the MySQL practical, I explicitly created:

```sql
id INT AUTO_INCREMENT PRIMARY KEY
```

MySQL then generated values such as:

```text
1
2
3
4
```

The MongoDB example displays:

```text
_id: ObjectId(...)
```

for the inserted document.

Conceptually, both provide a way of identifying records/documents, although their implementation and generated values differ.

```text
MySQL                     MongoDB
-----                     -------
id                        _id
1                         ObjectId(...)
2                         ObjectId(...)
3                         ObjectId(...)
```

---

# 16. Retrieve Documents

The learning material retrieves documents using:

```javascript
db.persons.find()
```

Breaking this down:

```text
db
 ↓
Current database

persons
 ↓
Collection

find()
 ↓
Retrieve documents
```

Therefore:

```javascript
db.persons.find()
```

retrieves documents from the `persons` collection.

---

# 17. Comparing SELECT and find()

During the MySQL practical, I retrieved all rows using:

```sql
SELECT * FROM people;
```

The MongoDB material uses:

```javascript
db.persons.find()
```

Conceptually:

```text
MySQL

SELECT * FROM people;
```

maps to:

```text
MongoDB

db.persons.find()
```

Both are being used here to retrieve records/documents from their respective data structures.

---

# 18. Filter MongoDB Documents

The learning material also demonstrates filtering:

```javascript
db.persons.find({"name": "John Doe"})
```

The filter is:

```javascript
{"name": "John Doe"}
```

This asks MongoDB to find documents where the `name` field matches:

```text
John Doe
```

---

# 19. Comparing WHERE and MongoDB Filters

During the MySQL practical, I used:

```sql
SELECT * FROM people WHERE age > 25;
```

The `WHERE` clause determines which rows should be returned.

MongoDB passes a filter document to:

```javascript
find()
```

For example:

```javascript
db.persons.find({"name": "John Doe"})
```

Conceptually:

```text
MySQL
WHERE condition
```

maps to the idea of:

```text
MongoDB
find({filter})
```

---

# 20. Sarah Query Comparison

During the learning exercise, I compared a SQL query such as:

```sql
SELECT * FROM people WHERE name = 'Sarah';
```

with the corresponding MongoDB-style filtering concept.

Using the `persons` collection from the material:

```javascript
db.persons.find({"name": "Sarah"})
```

The comparison is:

```text
MySQL

SELECT * FROM people
WHERE name = 'Sarah';
```

and:

```text
MongoDB

db.persons.find({"name": "Sarah"})
```

Both express the idea:

```text
Return records/documents
where name equals Sarah
```

---

# 21. SQL vs MongoDB Syntax

The two systems use different query styles.

## MySQL

```sql
SELECT * FROM people WHERE name = 'Sarah';
```

## MongoDB

```javascript
db.persons.find({"name": "Sarah"})
```

The syntax is different, but both contain the same broad concepts:

```text
Data source
     +
Condition
     +
Matching results
```

---

# 22. Database Structure Comparison

The structures can be compared as follows:

```text
MySQL

somto_db
└── people
    ├── Row
    │   ├── id
    │   ├── name
    │   ├── age
    │   └── location
    │
    └── Row
```

MongoDB:

```text
school
└── persons
    ├── Document
    │   ├── _id
    │   ├── name
    │   ├── age
    │   ├── location
    │   └── salary
    │
    └── Document
```

---

# 23. SQL vs NoSQL Mapping

A useful conceptual mapping from this section is:

```text
Relational / MySQL          MongoDB
------------------          -------
Database                    Database
Table                       Collection
Row                         Document
Column                      Field
Primary-key identifier      _id
SHOW DATABASES;             show dbs
USE database;               use database
SHOW TABLES;                show collections
INSERT INTO ...             db.collection.insert(...)
SELECT * ...                db.collection.find()
WHERE ...                   find({...})
```

This is a conceptual learning comparison rather than a claim that the two database models behave identically.

---

# 24. Example MySQL Workflow

The MySQL practical followed a workflow such as:

```sql
CREATE DATABASE somto_db;

USE somto_db;

CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    location VARCHAR(100)
);

INSERT INTO people (name, age, location)
VALUES ('John', 28, 'London');

SELECT * FROM people;
```

Conceptually:

```text
Create database
      ↓
Select database
      ↓
Create table
      ↓
Insert row
      ↓
Retrieve row
```

---

# 25. Example MongoDB Workflow from the Material

The MongoDB material follows:

```javascript
show dbs
```

then:

```javascript
use school
```

then:

```javascript
db.createCollection("persons")
```

then:

```javascript
show collections
```

then:

```javascript
db.persons.insert({
    "name": "John Doe",
    "age": 45,
    "location": "New York",
    "salary": 5000
})
```

then:

```javascript
db.persons.find()
```

and:

```javascript
db.persons.find({"name": "John Doe"})
```

Conceptually:

```text
View databases
      ↓
Select database
      ↓
Create collection
      ↓
Insert document
      ↓
Retrieve documents
      ↓
Filter documents
```

---

# 26. MongoDB Does Not Use SQL Syntax Here

The commands shown in the MongoDB learning material are not SQL statements.

For example, MongoDB uses:

```javascript
show dbs
```

rather than:

```sql
SHOW DATABASES;
```

and:

```javascript
db.persons.find()
```

rather than:

```sql
SELECT * FROM persons;
```

Therefore, learning MongoDB involves understanding a different command/query style rather than simply replacing table names inside SQL commands.

---

# 27. Useful MongoDB Commands from the Material

## List databases

```javascript
show dbs
```

## Select the school database

```javascript
use school
```

## Create a collection

```javascript
db.createCollection("persons")
```

## List collections

```javascript
show collections
```

## Insert a document

```javascript
db.persons.insert({
    "name": "John Doe",
    "age": 45,
    "location": "New York",
    "salary": 5000
})
```

## Retrieve documents

```javascript
db.persons.find()
```

## Filter by name

```javascript
db.persons.find({"name": "John Doe"})
```

---

# 28. Troubleshooting the MongoDB Shell

The same layered troubleshooting approach still applies.

Suppose the MongoDB shell cannot connect.

I should not immediately assume that the database itself has been deleted.

I could investigate:

```text
Is mongod installed?
      ↓
Is the mongod service running?
      ↓
Is the mongod process running?
      ↓
Is MongoDB listening on the expected port?
      ↓
Which IP address is it bound to?
      ↓
Does runtime match /etc/mongod.conf?
      ↓
Can the client reach that socket?
```

For example:

```bash
systemctl status mongod
```

would help inspect the service.

Then:

```bash
sudo ss -ltnp
```

could help inspect the network socket and associated process.

---

# 29. If the Service Is Running but the Client Cannot Connect

An important troubleshooting lesson is that:

```text
active (running)
```

does not automatically prove that a client can connect successfully.

For example:

```text
mongod active
      ↓
Process running
```

but the next questions are:

```text
Which address is it listening on?

Which port?

Does that match the client destination?

Does it match /etc/mongod.conf?
```

The investigation moves from:

```text
Service
```

to:

```text
Process
```

to:

```text
Network
```

to:

```text
Connection
```

---

# 30. Evidence-Based Troubleshooting

A useful sequence is:

```text
Client cannot connect
       ↓
Check service
       ↓
Check listening socket
       ↓
Identify process
       ↓
Check bind address and port
       ↓
Compare with configuration
       ↓
Inspect logs
       ↓
Identify failing layer
       ↓
Make targeted change
       ↓
Verify
```

This follows the same troubleshooting method used throughout the Linux, server, and MySQL practical work.

---

# 31. What Was Studied vs Executed

The MongoDB commands in this document were studied from the database learning material.

The course material demonstrates operations including:

```text
show dbs
use school
db.createCollection("persons")
show collections
db.persons.insert(...)
db.persons.find()
db.persons.find({...})
```

These operations were not executed against a locally installed MongoDB server on my current Ubuntu 26.04 machine.

Therefore:

```text
MongoDB syntax
      ↓
Studied from learning material

MongoDB local runtime
      ↓
Deferred
```

This distinction keeps the repository documentation accurate.

---

# 32. Main Learning Progression

At this stage, the database learning progression is:

```text
Database Fundamentals
       ↓
SQL vs NoSQL
       ↓
MySQL Installation
       ↓
MySQL Service
       ↓
MySQL Database
       ↓
MySQL Tables
       ↓
MySQL Data
       ↓
MySQL Users
       ↓
MySQL Privileges
       ↓
MySQL Configuration
       ↓
MySQL Logs
       ↓
MongoDB Installation Concepts
       ↓
MongoDB Service Concepts
       ↓
MongoDB Configuration
       ↓
MongoDB Logs
       ↓
MongoDB Shell
       ↓
MongoDB Collections
       ↓
MongoDB Documents
       ↓
MongoDB Queries
```

---

# Key Takeaway

The main structural difference demonstrated in this section is:

```text
MySQL

Database
   ↓
Table
   ↓
Row
   ↓
Column
```

compared with:

```text
MongoDB

Database
   ↓
Collection
   ↓
Document
   ↓
Field
```

The query styles are also different:

```text
MySQL

SELECT * FROM people
WHERE name = 'Sarah';
```

compared conceptually with:

```text
MongoDB

db.persons.find({"name": "Sarah"})
```

Despite these differences, the same DevOps operational thinking still applies around the database:

```text
Service
   ↓
Process
   ↓
Configuration
   ↓
Port
   ↓
Client Connection
   ↓
Database Operation
```

Understanding both the database operations and the infrastructure supporting them makes it easier to determine which layer is responsible when something goes wrong.
