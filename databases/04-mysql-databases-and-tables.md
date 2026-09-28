# MySQL Databases and Tables

## Overview

After installing MySQL Server and verifying the service, process, and listening ports, I connected to MySQL and practised working with:

- Databases
- Tables
- Columns
- Rows
- Primary keys
- Auto-incrementing IDs
- Inserting data
- Retrieving data
- Selecting specific columns
- Filtering records

The practical workflow was:

```text
Connect to MySQL
       ↓
View Databases
       ↓
Create Database
       ↓
Select Database
       ↓
Create Table
       ↓
Inspect Table Structure
       ↓
Insert Data
       ↓
Query Data
       ↓
Filter Data
```

---

# 1. Connect to MySQL

I connected to the MySQL server using:

```bash
sudo mysql
```

After connecting, the prompt changed from the Linux shell to:

```text
mysql>
```

This indicated that I was now working inside the MySQL client.

---

# 2. View Existing Databases

I listed the databases using:

```sql
SHOW DATABASES;
```

Before creating my own database, MySQL displayed:

```text
information_schema
mysql
performance_schema
sys
```

These are system databases created and used by MySQL.

---

# 3. Check the Currently Selected Database

I checked whether a database was currently selected:

```sql
SELECT DATABASE();
```

The result was:

```text
NULL
```

This did not mean that MySQL had no databases.

It meant:

```text
Connected to MySQL Server
          ↓
No current database selected
```

A connection to the database server and the selection of a working database are separate concepts.

---

# 4. Create a Database

I created my own database:

```sql
CREATE DATABASE somto_db;
```

I then checked the available databases again:

```sql
SHOW DATABASES;
```

The new database appeared alongside the MySQL system databases:

```text
information_schema
mysql
performance_schema
somto_db
sys
```

This confirmed that the database had been created successfully.

---

# 5. Select the Database

Creating the database did not automatically make it my current working database.

I selected it using:

```sql
USE somto_db;
```

MySQL confirmed the change.

I then ran:

```sql
SELECT DATABASE();
```

The result was:

```text
somto_db
```

The workflow was therefore:

```text
CREATE DATABASE somto_db;
          ↓
Database exists
          ↓
USE somto_db;
          ↓
Database becomes current
```

---

# 6. Check for Tables

After selecting `somto_db`, I checked its tables:

```sql
SHOW TABLES;
```

No tables were displayed because I had not created any yet.

This demonstrated another useful distinction:

```text
Database exists
      ≠
Tables exist inside database
```

---

# 7. Create the People Table

I created a table named `people`:

```sql
CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    location VARCHAR(100)
);
```

The table contained four columns:

```text
people
│
├── id
├── name
├── age
└── location
```

---

# 8. Understanding the Table Definition

## id

```sql
id INT AUTO_INCREMENT PRIMARY KEY
```

The `id` column stores integer values.

```text
INT
```

means the column contains integers.

---

## AUTO_INCREMENT

```text
AUTO_INCREMENT
```

means MySQL can automatically generate the next numerical value for the column when a new row is inserted.

For example:

```text
First row  → id 1
Second row → id 2
Third row  → id 3
Fourth row → id 4
```

This meant I did not need to manually provide an `id` when inserting the records in this lab.

---

## PRIMARY KEY

The `id` column was also defined as:

```text
PRIMARY KEY
```

The primary key identifies records in the table.

In this table, `id` was used as the primary key.

---

## name

```sql
name VARCHAR(100)
```

This column stores variable-length character data.

The maximum length defined in this table is 100 characters.

---

## age

```sql
age INT
```

This stores integer values representing age.

---

## location

```sql
location VARCHAR(100)
```

This stores variable-length character data representing the person's location.

---

# 9. Verify the Table Exists

After creating the table, I ran:

```sql
SHOW TABLES;
```

The result showed:

```text
people
```

The database now had the following structure:

```text
somto_db
└── people
```

---

# 10. Inspect the Table Structure

I inspected the table using:

```sql
DESCRIBE people;
```

The result showed information similar to:

```text
Field       Type          Null    Key    Default    Extra
-----       ----          ----    ---    -------    -----
id          int           NO      PRI    NULL       auto_increment
name        varchar(100)  YES            NULL
age         int           YES            NULL
location    varchar(100)  YES            NULL
```

This allowed me to inspect how MySQL understood the table definition.

---

# 11. Understanding DESCRIBE

The `DESCRIBE` output contains useful metadata about each column.

## Field

```text
Field
```

shows the column name.

For example:

```text
id
name
age
location
```

---

## Type

```text
Type
```

shows the data type.

Examples from the table included:

```text
int
varchar(100)
```

---

## Null

```text
Null
```

indicates whether the column permits `NULL` values.

The `id` column showed:

```text
NO
```

while the other columns showed:

```text
YES
```

---

## Key

The `id` column showed:

```text
PRI
```

indicating that it was the primary key.

---

## Extra

The `id` column showed:

```text
auto_increment
```

confirming that MySQL automatically generates its values.

---

# 12. Insert Data into the Table

I inserted three records into the `people` table:

```sql
INSERT INTO people (name, age, location)
VALUES
('John', 28, 'London'),
('Sarah', 32, 'New York'),
('Mike', 25, 'Sydney');
```

MySQL reported:

```text
Query OK, 3 rows affected
```

and:

```text
Records: 3
Duplicates: 0
Warnings: 0
```

This indicated that all three rows had been inserted successfully.

---

# 13. Why ID Was Not Included

The insert statement specified:

```text
name
age
location
```

but did not specify:

```text
id
```

This worked because the `id` column had been configured as:

```text
AUTO_INCREMENT
```

MySQL generated the IDs automatically.

The resulting data was:

```text
1  John   28  London
2  Sarah  32  New York
3  Mike   25  Sydney
```

---

# 14. Retrieve All Data

I queried the table using:

```sql
SELECT * FROM people;
```

The result contained:

```text
+----+-------+-----+----------+
| id | name  | age | location |
+----+-------+-----+----------+
|  1 | John  |  28 | London   |
|  2 | Sarah |  32 | New York |
|  3 | Mike  |  25 | Sydney   |
+----+-------+-----+----------+
```

---

# 15. Understanding SELECT *

The query:

```sql
SELECT * FROM people;
```

contains several parts.

```text
SELECT
```

means retrieve data.

```text
*
```

means all columns.

```text
FROM people
```

specifies the table.

Therefore:

```sql
SELECT * FROM people;
```

means:

> Retrieve all columns from the `people` table.

In this case, the four columns were:

```text
id
name
age
location
```

---

# 16. Select Specific Columns

Instead of retrieving every column, I selected only:

```text
name
location
```

using:

```sql
SELECT name, location FROM people;
```

The result returned all three records but displayed only the requested columns.

Conceptually:

```text
Original table

id | name | age | location
```

became:

```text
Query result

name | location
```

This demonstrates that the columns returned by a query can be controlled.

---

# 17. Filter Records with WHERE

I filtered the table using:

```sql
SELECT * FROM people WHERE age > 25;
```

The condition was:

```text
age > 25
```

The records were:

```text
John  → 28
Sarah → 32
Mike  → 25
```

Therefore, the result contained:

```text
John
Sarah
```

Mike was not returned because:

```text
25 > 25
```

is false.

---

# 18. Greater Than vs Greater Than or Equal To

This lab reinforced the difference between:

```text
>
```

and:

```text
>=
```

For example:

```sql
WHERE age > 25
```

means:

```text
age must be greater than 25
```

Therefore, age `25` is excluded.

However:

```sql
WHERE age >= 25
```

would mean:

```text
age must be greater than or equal to 25
```

In that case, age `25` would also match.

---

# 19. Insert Another Record

Later in the lab, after connecting using the non-root MySQL account, I inserted another person:

```sql
INSERT INTO people (name, age, location)
VALUES ('David', 30, 'Adelaide');
```

MySQL reported:

```text
Query OK, 1 row affected
```

I then queried the table again:

```sql
SELECT * FROM people;
```

The data now contained:

```text
1  John   28  London
2  Sarah  32  New York
3  Mike   25  Sydney
4  David  30  Adelaide
```

---

# 20. AUTO_INCREMENT Continued Automatically

David received:

```text
id = 4
```

without the `id` being manually supplied.

This confirmed the behaviour of:

```sql
AUTO_INCREMENT
```

The sequence had progressed:

```text
John   → 1
Sarah  → 2
Mike   → 3
David  → 4
```

---

# 21. Database Hierarchy

At the end of this practical, the structure could be represented as:

```text
MySQL Server
└── somto_db
    └── people
        ├── Row 1
        │   ├── id: 1
        │   ├── name: John
        │   ├── age: 28
        │   └── location: London
        │
        ├── Row 2
        │   ├── id: 2
        │   ├── name: Sarah
        │   ├── age: 32
        │   └── location: New York
        │
        ├── Row 3
        │   ├── id: 3
        │   ├── name: Mike
        │   ├── age: 25
        │   └── location: Sydney
        │
        └── Row 4
            ├── id: 4
            ├── name: David
            ├── age: 30
            └── location: Adelaide
```

---

# 22. Useful Commands

## List databases

```sql
SHOW DATABASES;
```

## Create a database

```sql
CREATE DATABASE somto_db;
```

## Select a database

```sql
USE somto_db;
```

## Check the current database

```sql
SELECT DATABASE();
```

## List tables

```sql
SHOW TABLES;
```

## Create a table

```sql
CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    location VARCHAR(100)
);
```

## Inspect table structure

```sql
DESCRIBE people;
```

## Insert records

```sql
INSERT INTO people (name, age, location)
VALUES
('John', 28, 'London'),
('Sarah', 32, 'New York'),
('Mike', 25, 'Sydney');
```

## Retrieve all columns

```sql
SELECT * FROM people;
```

## Retrieve selected columns

```sql
SELECT name, location FROM people;
```

## Filter records

```sql
SELECT * FROM people WHERE age > 25;
```

---

# 23. Troubleshooting Lessons

This practical also demonstrated that database problems can occur at different levels.

For example:

```text
Can connect to MySQL
       ↓
Can I see the database?
       ↓
Can I select the database?
       ↓
Does the table exist?
       ↓
Does the table have the expected structure?
       ↓
Does the expected data exist?
       ↓
Does my query condition match that data?
```

If:

```sql
SHOW TABLES;
```

returns no tables, that does not automatically mean MySQL is broken.

The database may simply contain no tables yet.

Similarly, if:

```sql
SELECT DATABASE();
```

returns:

```text
NULL
```

the server may be working correctly while no current database has been selected.

The output should therefore be interpreted in context before making changes.

---

# Key Takeaway

The practical demonstrated the relational hierarchy:

```text
MySQL Server
      ↓
Database
      ↓
Table
      ↓
Rows
      ↓
Columns / Values
```

It also demonstrated the basic workflow for working with relational data:

```text
CREATE
   ↓
INSERT
   ↓
SELECT
   ↓
FILTER
```

Understanding the structure of the database and the meaning of query results is essential before moving into user permissions, configuration, and database troubleshooting.
