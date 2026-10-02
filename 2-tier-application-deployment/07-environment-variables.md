# Environment Variables and Application Configuration

## Overview

The ecommerce application needs configuration information before it can connect to MariaDB.

Instead of using active database connection details directly in the PHP source code, the application reads environment variables.

The four variables used are:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

This separates application code from deployment-specific configuration.

---

## Application Configuration

The PHP application reads the environment variables using:

```php
$dbHost = getenv('DB_HOST');
$dbUser = getenv('DB_USER');
$dbPassword = getenv('DB_PASSWORD');
$dbName = getenv('DB_NAME');
```

It then creates the database connection:

```php
$link = mysqli_connect(
    $dbHost,
    $dbUser,
    $dbPassword,
    $dbName
);
```

Conceptually:

```text
Environment
    │
    ├── DB_HOST
    ├── DB_USER
    ├── DB_PASSWORD
    └── DB_NAME
          │
          ▼
        PHP
          │
          ▼
   mysqli_connect()
          │
          ▼
       MariaDB
```

---

## Why Environment Variables Are Useful

Different environments may use different database settings.

For example:

```text
Development
Testing
Production
```

may each have different:

```text
Database hosts
Database users
Database names
Credentials
```

If these values are hard-coded into the application source, changing environments may require modifying the code.

Using environment-based configuration allows:

```text
Same application code
        +
Different environment configuration
```

---

## Database Host

In my local lab:

```text
DB_HOST=db-server
```

This uses Docker's internal DNS.

The application does not need to know that during this lab the database container had an address such as:

```text
172.18.0.2
```

Instead:

```text
db-server
    ↓
Docker DNS
    ↓
Database container
```

This makes the configuration less dependent on a particular container IP.

---

## Database User

The application connects using:

```text
DB_USER=ecomuser
```

This account was created specifically for application access to:

```text
ecomdb
```

The PHP application therefore does not need to connect using the MariaDB administrative account.

---

## Database Password

The lab application uses a password for:

```text
ecomuser
```

The password is supplied through:

```text
DB_PASSWORD
```

rather than being written into the active PHP database connection code.

However, using an environment variable does not automatically make a secret secure.

The value still has to be stored or supplied somewhere.

---

## Database Name

The application database is supplied through:

```text
DB_NAME=ecomdb
```

This tells PHP which database should be used when establishing the connection.

---

# Apache Environment Configuration

## Initial State

Before configuring Apache, I checked:

```bash
env | grep '^DB_'
```

There were no `DB_*` variables configured for the application.

The application therefore did not have the required database connection information.

---

## Apache Environment File

For this lab, the variables were added to:

```text
/etc/apache2/envvars
```

The configuration followed this structure:

```bash
export DB_HOST=db-server
export DB_USER=ecomuser
export DB_PASSWORD=<database-password>
export DB_NAME=ecomdb
```

The actual password should not be copied into public documentation or committed to Git.

---

## Verifying the Configuration File

The configured variables can be inspected using:

```bash
grep '^export DB_' /etc/apache2/envvars
```

This confirms what is written in the Apache environment configuration.

However, it does not necessarily prove that an already-running Apache process has inherited the latest values.

---

## Restarting Apache After Configuration Changes

After changing:

```text
/etc/apache2/envvars
```

Apache was restarted:

```bash
service apache2 restart
```

This allowed the new Apache processes to inherit the configured environment variables.

This demonstrates an important difference between:

```text
Changing configuration on disk
```

and:

```text
Running process using the configuration
```

A configuration change may require the affected service to reload or restart before it takes effect.

---

# Inspecting the Running Apache Environment

During troubleshooting, I checked the Apache processes:

```bash
ps aux | grep '[a]pache2'
```

Apache had a parent process running as root and worker processes running as the web server user.

The environment of the running parent process could then be inspected using:

```bash
tr '\0' '\n' < /proc/<PID>/environ | grep '^DB_'
```

where:

```text
<PID>
```

is replaced with the Apache parent process ID.

This is stronger evidence than checking only the configuration file.

It answers:

```text
What environment variables does the running process actually have?
```

rather than only:

```text
What values are written in the configuration file?
```

---

# Configuration File vs Runtime State

This distinction is important.

Suppose:

```text
/etc/apache2/envvars
```

contains:

```text
DB_HOST=db-server
```

but Apache was started before that value was added.

The file may be correct while the currently running process still has the old environment.

Therefore:

```text
Configuration file
        ≠
Guaranteed runtime state
```

A strong troubleshooting process verifies both when necessary.

---

# Environment Variables and Troubleshooting

Suppose the website loads but products do not appear.

The application database configuration becomes one possible area to investigate.

Useful checks include:

```bash
grep '^export DB_' /etc/apache2/envvars
```

followed, when needed, by inspection of the running Apache process environment.

The values should correspond to the intended application configuration:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

---

## Testing the Same Credentials Manually

One useful troubleshooting technique is to test the application's database credentials manually from the application tier.

For example:

```bash
mariadb -h db-server -u ecomuser -p
```

This separates database connectivity/authentication testing from the PHP application.

If manual authentication fails with:

```text
Access denied
```

the problem exists before the application can successfully query the database.

If manual authentication succeeds, investigation can continue further up the application stack.

---

# Credential Mismatch Exercise

During a troubleshooting exercise, the application was unable to authenticate to MariaDB.

The remote database test produced:

```text
ERROR 1045 (28000): Access denied
```

Because MariaDB returned an authentication error, the connection had reached the database server.

The investigation then focused on:

```text
Application username
Application password
MariaDB account
Host matching
Authentication configuration
```

rather than restarting Apache or changing Docker networking.

---

## Inspecting the MariaDB Account

The account could be inspected using:

```sql
SELECT User, Host
FROM mysql.user
WHERE User='ecomuser';
```

The result showed:

```text
ecomuser
%
```

The account grants were checked using:

```sql
SHOW GRANTS FOR 'ecomuser'@'%';
```

The account had access to:

```text
ecomdb.*
```

This narrowed the investigation further toward the credential mismatch.

---

## Password Hashes Are Not Plaintext Passwords

MariaDB stores authentication information rather than providing the original plaintext password for retrieval.

Inspecting fields such as:

```text
authentication_string
```

does not reveal the original password.

Therefore, troubleshooting should not rely on trying to "read back" a user's plaintext password from MariaDB.

Instead, the known intended credential can be tested or reset when appropriate.

---

# Secrets and Git

Environment variables are useful for configuration, but secrets still require careful handling.

A real database password should not be committed into a public Git repository.

For example, documentation should use:

```text
DB_PASSWORD=<database-password>
```

instead of publishing the actual secret.

Likewise, an example configuration file might contain:

```text
DB_HOST=db-server
DB_USER=ecomuser
DB_PASSWORD=CHANGE_ME
DB_NAME=ecomdb
```

The real value should be supplied separately.

---

## `.env.example`

A common project pattern is to provide an example configuration file such as:

```text
.env.example
```

containing variable names and safe placeholder values:

```text
DB_HOST=db-server
DB_USER=ecomuser
DB_PASSWORD=CHANGE_ME
DB_NAME=ecomdb
```

This documents what configuration the application requires without publishing the real credential.

---

## `.env` and `.gitignore`

If a project uses a local `.env` file containing real secrets, it should normally not be committed.

For example:

```text
.env
```

can be included in:

```text
.gitignore
```

while:

```text
.env.example
```

can be committed.

Conceptually:

```text
.env.example
→ safe template
→ Git repository

.env
→ real environment configuration
→ excluded from Git
```

Our current Apache lab uses `/etc/apache2/envvars`, but the same secret-management principle applies.

---

# Environment Variables Are Not a Secret Manager

It is important not to assume:

```text
Environment variable = automatically secure
```

Environment variables can potentially be visible through:

```text
Process inspection
Debug output
Configuration files
Container inspection
Logs
Administrative tools
```

For this learning lab, Apache environment variables provide a simple way to separate configuration from application code.

More mature production environments may use dedicated secret-management mechanisms.

---

# Do Not Commit Secrets

Before pushing application changes to GitHub, I should inspect the repository for accidental credentials.

Useful checks include reviewing:

```bash
git diff
```

and:

```bash
git status
```

before committing.

I should pay particular attention to files containing:

```text
passwords
API keys
tokens
private keys
connection strings
```

---

# Configuration vs Code

The overall principle demonstrated by this project is:

```text
Application Code
      │
      │ expects configuration
      ▼
Environment
      │
      │ supplies configuration
      ▼
Running Application
```

This allows the application code to remain relatively independent of where it is deployed.

For example, the same application could conceptually use:

```text
Local:
DB_HOST=db-server
```

and later:

```text
Cloud:
DB_HOST=<private-database-hostname>
```

without rewriting the application's database connection logic.

---

# Key Lesson

Environment variables helped separate:

```text
What the application does
```

from:

```text
Where and how the application connects
```

But configuration should still be treated carefully.

The important lessons from this lab were:

```text
Do not hard-code environment-specific values unnecessarily.

Do not commit real secrets to Git.

Verify configuration files.

Verify what running processes actually inherited when troubleshooting.

Restart/reload services when required for configuration changes.

Test credentials from the same tier as the application.

Use error messages to determine how far the connection progressed.
```

Environment configuration is part of the application deployment and should be treated as carefully as the application code itself.
