# MySQL Users and Privileges

## Overview

After creating the `somto_db` database and the `people` table, I practised MySQL user management and access control.

The main concepts were:

- MySQL user accounts
- User and host combinations
- Authentication
- Authorization
- Database privileges
- `USAGE`
- `GRANT`
- `SHOW GRANTS`
- Testing permissions with a non-root account
- Verifying both read and write access

The practical workflow was:

```text
Connect as MySQL administrator
        ↓
Inspect existing users
        ↓
Create a new user
        ↓
Inspect initial privileges
        ↓
Grant database privileges
        ↓
Verify grants
        ↓
Connect as the new user
        ↓
Test database visibility
        ↓
Test read access
        ↓
Test write access
```

---

# 1. Inspect Existing MySQL Users

While connected to MySQL as an administrative user, I inspected the existing accounts:

```sql
SELECT user, host FROM mysql.user;
```

The initial output contained accounts including:

```text
debian-sys-maint    localhost
mysql.infoschema    localhost
mysql.session       localhost
mysql.sys           localhost
root                localhost
```

This showed that MySQL already contained several internal and administrative accounts.

These system accounts should not be modified or deleted without understanding their purpose.

---

# 2. MySQL User and Host

One important concept from this practical was that a MySQL account includes both:

```text
user
```

and:

```text
host
```

For example:

```text
root@localhost
```

or:

```text
somto_user@localhost
```

In SQL syntax, this is represented as:

```sql
'somto_user'@'localhost'
```

This means the account identity is not based only on the username.

Conceptually:

```text
MySQL Account
     ↓
Username + Host
```

The host component helps determine where the account is permitted to connect from.

---

# 3. Create a MySQL User

I created a new MySQL account using:

```sql
CREATE USER 'somto_user'@'localhost'
IDENTIFIED BY '<password>';
```

The actual password used during the lab is intentionally not included in this repository.

Passwords and other secrets should not be committed to source control.

After creating the account, I verified it using:

```sql
SELECT user, host
FROM mysql.user
WHERE user = 'somto_user';
```

The result showed:

```text
somto_user    localhost
```

This confirmed that the account had been created.

---

# 4. Creating a User Does Not Automatically Grant Database Access

Creating the user established the account, but it did not automatically give the account access to my application database.

I checked the account's privileges using:

```sql
SHOW GRANTS FOR 'somto_user'@'localhost';
```

Initially, the output contained:

```text
GRANT USAGE ON *.* TO `somto_user`@`localhost`
```

This was an important part of the practical.

The account existed and could be authenticated, but I had not yet granted it privileges on `somto_db`.

---

# 5. Understanding USAGE

The initial grant showed:

```text
USAGE
```

In this context, `USAGE` did not provide the user with application database privileges.

It indicated that the account existed without additional database privileges being granted by me.

Conceptually:

```text
Account exists
      ↓
Authentication can be considered
      ↓
No somto_db privileges yet
```

This demonstrated the difference between creating an account and authorizing that account to perform database operations.

---

# 6. Authentication vs Authorization

Two important concepts in database security are:

```text
Authentication
```

and:

```text
Authorization
```

They answer different questions.

## Authentication

Authentication asks:

> Who are you?

For example:

```bash
mysql -u somto_user -p
```

attempts to connect using the `somto_user` account.

MySQL must determine whether the supplied credentials are valid.

---

## Authorization

Authorization asks:

> What are you allowed to do?

A user may successfully authenticate but still lack permission to:

- Access a particular database
- Read a table
- Insert data
- Modify data
- Delete data
- Create database objects

Therefore:

```text
Authentication
      ↓
Identity verified
      ↓
Authorization
      ↓
Permissions checked
```

Successful authentication does not automatically mean unrestricted database access.

---

# 7. Grant Access to somto_db

I granted the new user privileges on my database:

```sql
GRANT ALL PRIVILEGES
ON somto_db.*
TO 'somto_user'@'localhost';
```

The important scope was:

```text
somto_db.*
```

This can be interpreted as:

```text
somto_db
    ↓
Database

*
    ↓
Objects within that database
```

The grant was therefore scoped to `somto_db`.

---

# 8. somto_db.* vs *.*

Understanding privilege scope is important.

The grant I used was:

```sql
somto_db.*
```

This targets objects within:

```text
somto_db
```

By contrast:

```sql
*.*
```

represents a global scope across databases.

Conceptually:

```text
somto_db.*
     ↓
Privileges scoped to somto_db
```

compared with:

```text
*.*
 ↓
Global scope
```

Granting only the privileges and scope required by an account is an important access-control principle.

---

# 9. Verify the Privileges

After granting access, I checked the account again:

```sql
SHOW GRANTS FOR 'somto_user'@'localhost';
```

The output now contained:

```text
GRANT USAGE ON *.* TO `somto_user`@`localhost`
```

and:

```text
GRANT ALL PRIVILEGES ON `somto_db`.* TO `somto_user`@`localhost`
```

This provided direct evidence that the database-specific grant had been applied.

Rather than assuming the `GRANT` worked, I verified the resulting state.

The workflow was:

```text
Change
  ↓
Verify
```

---

# 10. Connect as the New User

After configuring the account, I exited the administrative MySQL session.

I then connected using:

```bash
mysql -u somto_user -p
```

The options mean:

```text
-u
 ↓
Specify username

-p
 ↓
Prompt for password
```

Using `-p` without putting the password directly on the command line allowed MySQL to prompt for it.

After entering the password, the connection succeeded.

This demonstrated successful authentication for:

```text
somto_user@localhost
```

---

# 11. Check Database Visibility

After connecting as `somto_user`, I ran:

```sql
SHOW DATABASES;
```

The visible databases included:

```text
information_schema
performance_schema
somto_db
```

The output was different from what I had seen while connected administratively.

For example, databases such as:

```text
mysql
sys
```

were not shown in that session.

This demonstrated that what a database user can see can depend on that account's privileges.

---

# 12. Select somto_db

I selected the database:

```sql
USE somto_db;
```

This succeeded.

The user was therefore authorized to access the database that had been granted to it.

---

# 13. Test Read Access

I tested whether the account could read from the `people` table:

```sql
SELECT * FROM people;
```

The query succeeded and returned the existing records:

```text
1    John     28    London
2    Sarah    32    New York
3    Mike     25    Sydney
```

This proved more than successful login.

It demonstrated:

```text
Authentication succeeded
          ↓
somto_db accessible
          ↓
people table accessible
          ↓
SELECT operation permitted
```

Therefore, the account had working read authorization.

---

# 14. Test Write Access

I then tested whether the account could modify data.

I inserted:

```sql
INSERT INTO people (name, age, location)
VALUES ('David', 30, 'Adelaide');
```

MySQL returned:

```text
Query OK, 1 row affected
```

This demonstrated that the account had permission to insert data into the table.

---

# 15. Verify the Write Operation

After inserting the record, I queried the table again:

```sql
SELECT * FROM people;
```

The result now contained:

```text
1    John     28    London
2    Sarah    32    New York
3    Mike     25    Sydney
4    David    30    Adelaide
```

This provided evidence that the write operation had succeeded.

It also showed that MySQL automatically generated:

```text
id = 4
```

because the `id` column had been configured with:

```text
AUTO_INCREMENT
```

---

# 16. Proving Authorization

The practical demonstrated several levels of verification.

Successfully running:

```bash
mysql -u somto_user -p
```

proved that authentication succeeded.

Successfully running:

```sql
USE somto_db;
```

proved that the account could access the database.

Successfully running:

```sql
SELECT * FROM people;
```

proved that read access worked.

Successfully running:

```sql
INSERT INTO people (name, age, location)
VALUES ('David', 30, 'Adelaide');
```

proved that write access worked.

Therefore:

```text
Login succeeds
      ↓
Authentication works

USE somto_db succeeds
      ↓
Database access works

SELECT succeeds
      ↓
Read authorization works

INSERT succeeds
      ↓
Write authorization works
```

This is stronger than assuming permissions are correct simply because a user can log in.

---

# 17. Root Authentication on This Ubuntu Installation

Later in the practical, I inspected the authentication plugin used by the MySQL `root` account:

```bash
sudo mysql -e "SELECT user, host, plugin FROM mysql.user WHERE user='root';"
```

The output showed:

```text
root    localhost    auth_socket
```

This explained why I could access the administrative MySQL session using:

```bash
sudo mysql
```

The root account on this installation was using:

```text
auth_socket
```

This is different from the password-based login I used for:

```text
somto_user@localhost
```

The two connection methods were therefore:

```text
sudo mysql
     ↓
root@localhost
     ↓
auth_socket
```

and:

```text
mysql -u somto_user -p
     ↓
somto_user@localhost
     ↓
password authentication
```

---

# 18. Authentication Method Is Part of Troubleshooting

When a database login fails, it is not enough to know only the username.

Useful questions include:

```text
Which MySQL account?
       ↓
Which host?
       ↓
Which authentication method?
       ↓
Are the credentials valid?
       ↓
What privileges does the account have?
```

For example:

```text
root@localhost
```

and:

```text
somto_user@localhost
```

were configured differently during this lab.

Understanding the authentication method helps explain why different accounts may require different connection procedures.

---

# 19. Security Lesson: Do Not Commit Passwords

The password used during this lab should not be placed in GitHub documentation.

Instead of writing:

```sql
IDENTIFIED BY 'actual-password';
```

documentation should use a placeholder:

```sql
IDENTIFIED BY '<password>';
```

The same principle applies to:

- API keys
- Tokens
- Private keys
- Database credentials
- Cloud credentials
- Application secrets

A public or shared Git repository should not be treated as a secure location for secrets.

---

# 20. Useful Commands

## List MySQL users and hosts

```sql
SELECT user, host FROM mysql.user;
```

## Create a user

```sql
CREATE USER 'somto_user'@'localhost'
IDENTIFIED BY '<password>';
```

## Verify the user exists

```sql
SELECT user, host
FROM mysql.user
WHERE user = 'somto_user';
```

## Inspect privileges

```sql
SHOW GRANTS FOR 'somto_user'@'localhost';
```

## Grant privileges on a database

```sql
GRANT ALL PRIVILEGES
ON somto_db.*
TO 'somto_user'@'localhost';
```

## Connect as the user

```bash
mysql -u somto_user -p
```

## Select the database

```sql
USE somto_db;
```

## Test read access

```sql
SELECT * FROM people;
```

## Test write access

```sql
INSERT INTO people (name, age, location)
VALUES ('David', 30, 'Adelaide');
```

## Inspect the root authentication plugin

```bash
sudo mysql -e "SELECT user, host, plugin FROM mysql.user WHERE user='root';"
```

---

# 21. Troubleshooting Access Problems

A database access problem can occur at several different stages.

A useful troubleshooting sequence is:

```text
Can the client reach MySQL?
          ↓
Can the account authenticate?
          ↓
Is the correct user@host being used?
          ↓
What authentication method is configured?
          ↓
What does SHOW GRANTS report?
          ↓
Can the user access the database?
          ↓
Can the user perform the required operation?
```

For example, if:

```bash
mysql -u somto_user -p
```

succeeds but:

```sql
USE somto_db;
```

fails, the problem is probably not simply that MySQL is stopped.

The client has already reached the server and authenticated.

The next layer to investigate would be authorization and database privileges.

Similarly, if:

```sql
SELECT * FROM people;
```

works but an `INSERT` fails, this would indicate that connectivity and at least some database access are already working.

The failed operation and the user's privileges should then be investigated.

---

# 22. Evidence-Based Verification

This practical reinforced the principle:

```text
Do not assume
     ↓
Test
     ↓
Observe
     ↓
Interpret
```

After creating the user, I checked that it existed.

After granting privileges, I used:

```sql
SHOW GRANTS
```

After configuring the account, I connected as that account.

After connecting, I tested a read.

After proving read access, I tested a write.

After the write, I queried the table again to verify the resulting data.

The complete verification chain was:

```text
CREATE USER
     ↓
Verify user
     ↓
SHOW GRANTS
     ↓
GRANT privileges
     ↓
SHOW GRANTS again
     ↓
Authenticate as user
     ↓
USE database
     ↓
SELECT
     ↓
INSERT
     ↓
SELECT again
```

---

# Key Takeaway

Database access is not a single step.

It involves:

```text
Network Connection
        ↓
Authentication
        ↓
Authorization
        ↓
Database Access
        ↓
Operation Permission
```

A successful login proves authentication, but it does not automatically prove that the user can perform every database operation.

By creating a restricted MySQL account, inspecting its grants, granting access specifically to `somto_db`, and testing both `SELECT` and `INSERT`, I verified the complete access-control path instead of assuming that the permissions were working.
