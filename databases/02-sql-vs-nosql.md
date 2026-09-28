# SQL vs NoSQL Databases

## Overview

Databases can use different models for organizing and storing data.

The two database approaches covered in this section are:

```text
Databases
├── SQL / Relational Databases
└── NoSQL Databases
```

The learning material introduces examples of relational databases such as:

- MySQL
- PostgreSQL
- Microsoft SQL Server

It also introduces NoSQL databases such as:

- MongoDB
- Amazon DynamoDB
- Apache Cassandra

For the practical learning in this repository, the main databases considered are **MySQL** and **MongoDB**.

---

# SQL / Relational Databases

A relational database organizes data into **tables**.

A table consists of:

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

In this structure:

- `people` can be the table name.
- Each horizontal entry is a row or record.
- `id`, `name`, `age`, and `location` are columns.

The structure can be represented as:

```text
Database
└── Table
    ├── Row
    │   ├── Column value
    │   ├── Column value
    │   └── Column value
    │
    └── Row
        ├── Column value
        ├── Column value
        └── Column value
```

---

# MySQL Example

During the practical, I created the database:

```sql
CREATE DATABASE somto_db;
```

I then selected it:

```sql
USE somto_db;
```

Inside the database, I created the `people` table:

```sql
CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    location VARCHAR(100)
);
```

The table structure was:

```text
people
│
├── id
├── name
├── age
└── location
```

I inserted several records:

```sql
INSERT INTO people (name, age, location)
VALUES
('John', 28, 'London'),
('Sarah', 32, 'New York'),
('Mike', 25, 'Sydney');
```

I could then retrieve the rows using:

```sql
SELECT * FROM people;
```

This demonstrates the relational structure:

```text
somto_db
└── people
    ├── John
    ├── Sarah
    └── Mike
```

---

# SQL Queries

SQL stands for:

```text
Structured Query Language
```

It provides commands for interacting with relational databases.

For example, to retrieve every column and row from the `people` table:

```sql
SELECT * FROM people;
```

To retrieve only particular columns:

```sql
SELECT name, location FROM people;
```

To filter rows:

```sql
SELECT * FROM people
WHERE age > 25;
```

The `WHERE` clause specifies a condition that records must satisfy.

---

# NoSQL Databases

NoSQL databases use database models that do not necessarily depend on the traditional relational table structure.

MongoDB is the NoSQL database covered in the practical learning material.

Instead of organizing information as tables, rows, and columns, MongoDB uses:

```text
Database
   ↓
Collection
   ↓
Document
   ↓
Fields
```

---

# MongoDB Collections

A **collection** can be compared conceptually with a table in a relational database.

For example:

```text
MySQL
people table

MongoDB
persons collection
```

The MongoDB learning material creates a collection using:

```javascript
db.createCollection("persons")
```

Collections can be displayed using:

```javascript
show collections
```

---

# MongoDB Documents

A **document** stores information inside a collection.

A document can be compared conceptually with a row or record in a relational database.

For example, the learning material demonstrates a document containing fields such as:

```text
name     → John Doe
age      → 45
location → New York
salary   → 5000
```

Using the shell syntax shown in the learning material, a document is inserted with:

```javascript
db.persons.insert({
    "name": "John Doe",
    "age": 45,
    "location": "New York",
    "salary": 5000
})
```

The document is stored inside the `persons` collection.

Conceptually:

```text
school
└── persons
    └── document
        ├── name: John Doe
        ├── age: 45
        ├── location: New York
        └── salary: 5000
```

---

# MongoDB Fields

The individual pieces of information within a document are called **fields**.

For example:

```javascript
{
    "name": "John Doe",
    "age": 45,
    "location": "New York",
    "salary": 5000
}
```

contains the fields:

```text
name
age
location
salary
```

At a conceptual level, fields can be compared with columns in a relational database.

---

# SQL and MongoDB Terminology

The most important terminology mapping from this section is:

| SQL / Relational | MongoDB |
|---|---|
| Database | Database |
| Table | Collection |
| Row / Record | Document |
| Column | Field |

This can be visualized as:

```text
SQL / Relational

Database
└── Table
    └── Row
        └── Columns
```

compared with:

```text
MongoDB

Database
└── Collection
    └── Document
        └── Fields
```

---

# Selecting a Database

In MySQL, I selected a database using:

```sql
USE somto_db;
```

In the MongoDB material, the database is selected using:

```javascript
use school
```

The Mongo shell responds with:

```text
switched to db school
```

So although the syntax differs, both operations establish the database being worked with.

---

# Viewing Databases

In MySQL:

```sql
SHOW DATABASES;
```

In the MongoDB shell material:

```javascript
show dbs
```

Both commands allow the user to inspect available databases, although the syntax is different.

---

# Retrieving Data

In MySQL, I retrieved all records from a table using:

```sql
SELECT * FROM people;
```

The MongoDB material retrieves documents from a collection using:

```javascript
db.persons.find()
```

At an introductory conceptual level:

```text
MySQL
SELECT * FROM people;

             ↓

Retrieve records from a table
```

and:

```text
MongoDB
db.persons.find()

             ↓

Retrieve documents from a collection
```

---

# Filtering Data

Both database systems can filter data, although their query syntax is different.

For example, in MySQL:

```sql
SELECT * FROM people
WHERE name = 'Sarah';
```

A conceptually similar MongoDB query is:

```javascript
db.persons.find({"name": "Sarah"})
```

The MongoDB learning material demonstrates the same pattern using:

```javascript
db.persons.find({"name": "John Doe"})
```

This searches the collection for documents whose `name` field matches the specified value.

---

# Identifiers

In the MySQL practical, the `people` table contained:

```sql
id INT AUTO_INCREMENT PRIMARY KEY
```

This caused MySQL to automatically generate identifiers such as:

```text
1
2
3
4
```

MongoDB documents can contain an automatically generated:

```text
_id
```

The learning material shows an `_id` containing an `ObjectId` when a document is retrieved.

This provides an identifier for the MongoDB document.

---

# Comparing the Examples

## MySQL

```text
somto_db
└── people
    ├── Row 1
    │   ├── id: 1
    │   ├── name: John
    │   ├── age: 28
    │   └── location: London
    │
    └── Row 2
        ├── id: 2
        ├── name: Sarah
        ├── age: 32
        └── location: New York
```

## MongoDB

```text
school
└── persons
    └── Document
        ├── _id: ObjectId(...)
        ├── name: John Doe
        ├── age: 45
        ├── location: New York
        └── salary: 5000
```

---

# Syntax Comparison

| Task | MySQL | MongoDB Shell |
|---|---|---|
| Select database | `USE somto_db;` | `use school` |
| List databases | `SHOW DATABASES;` | `show dbs` |
| List tables/collections | `SHOW TABLES;` | `show collections` |
| Retrieve all data | `SELECT * FROM people;` | `db.persons.find()` |
| Filter data | `WHERE name = 'Sarah'` | `{"name": "Sarah"}` |

---

# Important Shell Version Note

The learning material demonstrates the older MongoDB shell command:

```bash
mongo
```

Modern MongoDB environments commonly use:

```bash
mongosh
```

When following the course material, it is therefore important to distinguish between the syntax shown in the material and the MongoDB shell available in the environment being administered.

---

# Key Takeaway

The main difference to remember at this stage is the way the data is organized.

```text
SQL / Relational
Database
   ↓
Table
   ↓
Row
   ↓
Column values
```

Compared with:

```text
MongoDB
Database
   ↓
Collection
   ↓
Document
   ↓
Fields
```

The terminology and query syntax differ, but both systems provide ways to:

```text
Store data
Retrieve data
Filter data
Organize data
Manage databases
```

Understanding the structure of each database model makes it easier to understand the commands used to administer and query them.
