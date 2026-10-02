# Deployment Security and Runtime Cleanup

## Overview

A successful application deployment is not only about making the application work.

The deployed environment should also avoid exposing unnecessary development files, repository metadata, database initialization files, credentials, and other information that the running application does not require.

During this lab, the initial deployment copied the complete Git repository into Apache's document root:

```text
/var/www/html
```

This worked for the application, but it also copied files that should not normally be part of a public web deployment.

This provided an opportunity to inspect and improve the runtime deployment.

---

# Source Repository vs Runtime Deployment

The source repository and the deployed application serve different purposes.

The source repository may contain:

```text
Application source
Git metadata
Documentation
Development assets
Database initialization scripts
Build files
Configuration examples
Testing resources
```

The runtime environment should contain only what is required to operate the application.

Conceptually:

```text
Source Repository
       │
       │ Build / Package / Select
       ▼
Deployment Artifact
       │
       ▼
Runtime Environment
```

Therefore:

```text
Source Repository ≠ Runtime Deployment
```

---

# Initial Runtime Inspection

After copying the repository into Apache's document root, I inspected it using:

```bash
ls -la /var/www/html
```

The directory contained:

```text
.git/
.gitignore
README.md
assets/
css/
fonts/
img/
index.php
js/
scss/
vendors/
```

The application worked, but not everything in this directory was required for runtime operation.

---

# Git Metadata

One of the most important findings was:

```text
/var/www/html/.git/
```

The `.git` directory contains repository metadata.

Depending on web server configuration, exposing repository metadata inside a public document root can create unnecessary information-disclosure risk.

The running application does not require Git history to serve the website.

Therefore, I removed the `.git` directory from the runtime deployment:

```bash
rm -rf /var/www/html/.git
```

---

## Verifying Removal

I checked:

```bash
ls -la /var/www/html | grep '\.git'
```

After removing `.git/`, only:

```text
.gitignore
```

remained.

This confirmed that the Git metadata directory had been removed.

---

# Database Initialization Script

I then inspected:

```text
/var/www/html/assets
```

using:

```bash
find /var/www/html/assets -maxdepth 2 -type f -ls
```

The directory contained:

```text
db-load-script.sql
```

This SQL script was used to initialize the database.

It was not required by PHP when serving the ecommerce website.

---

## Why the SQL Script Should Not Be in the Web Root

The database initialization script contains information about:

```text
Database name
Table name
Table structure
Seed data
```

Although the lab script did not contain the database password, it still exposes internal database information unnecessarily if served publicly.

Therefore, I removed the runtime copy:

```bash
rm /var/www/html/assets/db-load-script.sql
```

The original SQL script remained safely in the source repository on the WSL host.

---

# Runtime Cleanup Does Not Mean Deleting Source Files

This distinction is important.

Removing:

```text
/var/www/html/.git
```

and:

```text
/var/www/html/assets/db-load-script.sql
```

affected only the deployed copy inside `web-server`.

It did not remove those resources from:

```text
~/projects/learning-app-ecommerce
```

The relationship is:

```text
WSL Source Repository
        │
        │ docker cp
        ▼
Runtime Copy
/var/www/html
```

Changes to the runtime copy do not automatically modify the original repository.

---

# Verify After Security Changes

Security cleanup can accidentally break an application if a required file is removed.

Therefore, after removing unnecessary runtime files, I tested:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

The application still returned all eight products.

This demonstrated:

```text
.git/ removed                       ✓
db-load-script.sql removed          ✓
Apache still working                ✓
PHP still working                   ✓
Database connection still working   ✓
Products still rendering            ✓
```

This is an important operational principle:

```text
Change
  ↓
Verify
```

Even when a change appears harmless.

---

# Inspect Before Deleting

Rather than deleting every development-looking directory immediately, I inspected whether files were referenced.

For example:

```bash
grep -R -n -E 'README\.md|\.gitignore|scss/' /var/www/html \
  --exclude-dir=vendors
```

This returned a reference from:

```text
css/style.css.map
```

to files inside:

```text
scss/
```

This led to further investigation instead of blindly deleting the directory.

---

# CSS Source Maps

The compiled stylesheet ended with:

```css
/*# sourceMappingURL=style.css.map */
```

This tells browser developer tools that a CSS source map is available.

The source map referenced SCSS files such as:

```text
../scss/_variables.scss
../scss/_header.scss
../scss/_footer.scss
../scss/_responsive.scss
```

The relationship is approximately:

```text
SCSS source
    ↓
CSS compilation
    ↓
style.css
    ↓
Browser
```

The source map provides a development/debugging relationship:

```text
style.css
    ↓
style.css.map
    ↓
Original SCSS
```

The browser uses the compiled CSS for normal page styling.

The SCSS source is primarily a development resource.

---

# Avoid Unnecessary Cleanup During Troubleshooting

Although files such as:

```text
README.md
.gitignore
scss/
style.css.map
```

may not all be required for basic production runtime, I did not continue deleting files simply for the sake of removing them.

The important security findings had already been addressed:

```text
.git/
db-load-script.sql
```

Further optimization should ideally be handled by a defined build/deployment process.

This follows another useful principle:

```text
Do not make unnecessary changes to a healthy system.
```

---

# Better Deployment Strategy

Our learning deployment used:

```bash
docker cp . web-server:/var/www/html/
```

This was useful because it made the deployment process easy to understand.

However, it copied the entire repository.

A better production approach would be:

```text
Source Repository
       ↓
Identify runtime requirements
       ↓
Build/package application
       ↓
Create deployment artifact
       ↓
Deploy only required files
```

Rather than:

```text
Copy everything
       ↓
Delete unwanted files afterward
```

---

# Secrets

The application requires database credentials.

The PHP application reads:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

In this lab, Apache receives these through:

```text
/etc/apache2/envvars
```

The database password should not be committed to the public Git repository.

Documentation and examples should use placeholders such as:

```text
DB_PASSWORD=<database-password>
```

rather than the real credential.

---

# Environment Variables Are Not Automatically Secure

Moving a password from PHP source code into an environment variable improves configuration separation, but it does not automatically make the secret secure.

Environment values may potentially be visible through:

```text
Process inspection
Container inspection
Configuration files
Debug output
Logs
Administrative access
```

Therefore:

```text
Environment variable
```

should not be interpreted as:

```text
Encrypted secret
```

For this learning environment, environment variables provide a simple and useful configuration mechanism.

Production environments may use dedicated secret-management systems.

---

# Principle of Least Privilege

Another security concept demonstrated by the project is limiting application access.

The application uses:

```text
ecomuser
```

rather than relying on a database administrative account.

Its database access is scoped to:

```text
ecomdb.*
```

rather than every database on the MariaDB server.

Conceptually:

```text
Application
    ↓
Application-specific DB user
    ↓
Application database
```

This is preferable to unnecessarily giving an application broad administrative access.

---

# Database Exposure

The database container was not published to the WSL host using:

```text
-p 3306:3306
```

because the web tier could communicate with it directly through:

```text
two-tier-network
```

The architecture remained:

```text
Host
 │
 │ 8080
 ▼
web-server
 │
 │ private Docker network
 │ 3306
 ▼
db-server
```

Only the web application needed host-published access for this lab.

This demonstrates the principle:

```text
Do not expose a service externally when external access is unnecessary.
```

---

# Database Network Binding

MariaDB was configured with:

```ini
bind-address = 0.0.0.0
```

for this isolated Docker lab so the separate web container could reach it.

However:

```text
0.0.0.0
```

means MariaDB listens on all available IPv4 interfaces in that network namespace.

It should not be interpreted as a security control by itself.

Network exposure and database authorization still need to be considered separately.

---

# File Permissions

The deployed application files were readable by Apache.

For static/PHP application files, Apache generally needs sufficient permission to read the files and traverse their directories.

It does not automatically need ownership or write access to every application file.

This leads to the broader principle:

```text
Give a process only the permissions it actually requires.
```

If an application later needs writable directories for uploads, caches, or generated files, those locations can be handled specifically rather than making the entire web root writable.

---

# Security and Availability Must Be Verified Together

A security change can still cause an outage if performed incorrectly.

For example:

```text
Remove unnecessary file
        ↓
Test HTTP
        ↓
Test dynamic application content
```

This balances:

```text
Security
+
Availability
```

rather than treating them as completely separate concerns.

---

# Pre-Commit Security Review

Before committing or pushing application changes to GitHub, useful checks include:

```bash
git status
```

and:

```bash
git diff
```

I should review changes for accidental inclusion of:

```text
Passwords
API keys
Access tokens
Private keys
Connection strings
Environment files containing secrets
```

A secret should not be committed simply because the repository is currently private.

---

# Deployment Security Checklist

Before considering a deployment complete, I can review:

```text
[ ] Is repository metadata excluded from the public web root?

[ ] Are database initialization scripts excluded from the public runtime?

[ ] Are real credentials excluded from Git?

[ ] Is the application using a dedicated database account?

[ ] Are database privileges limited to what the application needs?

[ ] Are unnecessary ports exposed?

[ ] Are runtime files readable without unnecessary write permissions?

[ ] Have configuration changes been verified?

[ ] Has the application been retested after cleanup?

[ ] Does dynamic database-backed content still work?
```

---

# Key Lesson

Deployment security is not something that happens only after an application is running.

It is part of the deployment process.

The lab demonstrated the progression:

```text
Make it work
     ↓
Understand how it works
     ↓
Inspect what was deployed
     ↓
Remove unnecessary exposure
     ↓
Verify it still works
```

The long-term goal is to design the deployment process so that unnecessary files and secrets are never deployed in the first place.
