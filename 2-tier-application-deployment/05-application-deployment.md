# Ecommerce Application Deployment

## Overview

After preparing the database and web tiers, the next step was deploying the ecommerce application.

The application source used for this lab is the KodeKloud Learning App Ecommerce repository.

The original repository is:

```text
https://github.com/kodekloudhub/learning-app-ecommerce.git
```

The upstream application code was created by KodeKloud.

My work in this project focuses on deploying, configuring, networking, securing, testing, and troubleshooting the application.

---

## Source Repository vs Deployment

An important distinction in this project is:

```text
Source Repository
        ↓
Deployment Process
        ↓
Runtime Application
```

The source repository exists on my WSL environment.

The running application exists inside:

```text
web-server:/var/www/html
```

These should be treated as separate environments.

---

## Creating a Local Projects Directory

On my WSL host, I created a directory for application projects:

```bash
mkdir -p ~/projects
cd ~/projects
```

This keeps application projects separate from my DevOps learning documentation repository.

My DevOps documentation is stored in:

```text
~/my-devops-journey
```

while application source code is stored under:

```text
~/projects
```

---

## Cloning the Ecommerce Application

The application was cloned from the upstream KodeKloud repository.

```bash
git clone https://github.com/kodekloudhub/learning-app-ecommerce.git
```

This created:

```text
~/projects/learning-app-ecommerce
```

I then entered the repository:

```bash
cd ~/projects/learning-app-ecommerce
```

---

## Inspecting the Repository

The application contained files and directories including:

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

The main PHP application entry point is:

```text
index.php
```

The database initialization script was located at:

```text
assets/db-load-script.sql
```

---

## Finding SQL Files

Rather than using `grep` to search for a filename, I used:

```bash
find . -type f -name "*.sql"
```

This returned:

```text
./assets/db-load-script.sql
```

This reinforced the distinction:

```text
find
→ locate files/directories

grep
→ search text/content
```

---

## Inspecting the Database Script

The database initialization script contains:

```sql
USE ecomdb;
```

followed by creation of the `products` table and insertion of the initial product records.

Because the script begins by selecting:

```text
ecomdb
```

the database must exist before the script can be loaded successfully.

The database was therefore created first:

```sql
CREATE DATABASE ecomdb;
```

and the script was subsequently loaded on the database tier.

---

## Inspecting the Application Database Configuration

The application's `index.php` contains database connection logic based on environment variables.

The important values are:

```php
$dbHost = getenv('DB_HOST');
$dbUser = getenv('DB_USER');
$dbPassword = getenv('DB_PASSWORD');
$dbName = getenv('DB_NAME');
```

The connection is then established using:

```php
$link = mysqli_connect(
    $dbHost,
    $dbUser,
    $dbPassword,
    $dbName
);
```

This is important because the active application does not require us to hard-code the database connection details directly into the PHP source.

---

## Old Hard-Coded Configuration

The source also contained an older commented database connection example using a specific IP address.

Because that line was commented out, I did not uncomment or use it.

Instead, I kept the application's current environment-variable approach.

This allowed the deployment environment to provide the database configuration without modifying the PHP source for each environment.

---

## Database Host

For my Docker lab, the database hostname was configured as:

```text
db-server
```

rather than using:

```text
172.18.0.2
```

The reason is that both containers are connected to the custom Docker network:

```text
two-tier-network
```

Docker DNS resolves:

```text
db-server
```

to the current IP address of the database container.

This avoids making the application dependent on a container IP address that may change if the container is recreated.

---

## Preparing Apache's Document Root

Apache's default document root is:

```text
/var/www/html
```

Initially it contained Apache's default:

```text
index.html
```

The default file was removed:

```bash
sudo docker exec web-server rm /var/www/html/index.html
```

This prepared the document root for the ecommerce application.

---

## Copying the Application Into the Web Server

From the application repository on the WSL host, I copied the project into the running web container:

```bash
sudo docker cp . web-server:/var/www/html/
```

The runtime application was therefore placed at:

```text
/var/www/html
```

inside `web-server`.

---

## Verifying the Deployment Files

Inside the web container:

```bash
ls -la /var/www/html
```

showed application content including:

```text
index.php
css/
fonts/
img/
js/
vendors/
```

At this point, the PHP application files were available to Apache.

However, having the files in the document root still did not prove that the complete application was operational.

The database configuration also had to be provided.

---

## Environment-Based Configuration

The application expects:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

Without these values, PHP does not have the information required to establish the database connection.

The Docker container initially had no `DB_*` variables:

```bash
env | grep '^DB_'
```

returned no values.

The variables therefore had to be provided to the Apache/PHP runtime.

---

## Application Query

The PHP application executes:

```sql
SELECT * FROM products;
```

against the ecommerce database.

The application then loops through the returned rows and generates HTML for each product.

Conceptually:

```text
PHP
 ↓
SELECT * FROM products
 ↓
MariaDB
 ↓
Product rows returned
 ↓
PHP loop
 ↓
HTML generated
 ↓
Browser
```

---

## Verifying Dynamic Content

A simple HTTP test such as:

```bash
curl -I http://localhost:8080
```

can confirm that Apache is reachable.

However, it does not prove that the database query succeeded.

A stronger application-level test was:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

When the application was fully working, this returned eight product lines.

Examples included:

```text
Purchase Laptop at the lowest price
Purchase Drone at the lowest price
Purchase VR at the lowest price
Purchase Tablet at the lowest price
Purchase Watch at the lowest price
Purchase Phone Covers at the lowest price
Purchase Phone at the lowest price
Purchase Laptop at the lowest price
```

This provided evidence that:

```text
Apache served the request
        ↓
PHP executed
        ↓
Application connected to MariaDB
        ↓
Query executed
        ↓
Product rows were returned
        ↓
PHP rendered database-backed content
```

---

## Static Text Can Be Misleading

During testing, I initially searched the returned webpage for product-related words such as:

```text
Laptop
Drone
VR
```

However, some of those words could already exist in static parts of the HTML.

Therefore, finding those words alone was not strong evidence that the database query had worked.

Searching for:

```text
Purchase
```

was more useful because that text was generated in the application's database-backed product loop.

This demonstrated an important troubleshooting principle:

```text
Choose a test that proves the specific component
you are trying to verify.
```

---

## Runtime Deployment Cleanup

The command:

```bash
docker cp .
```

copied the complete repository into Apache's document root.

That included files that were not required by the running application.

For example:

```text
.git/
assets/db-load-script.sql
```

These were identified during the deployment review.

The `.git` directory was removed from the runtime:

```bash
rm -rf /var/www/html/.git
```

The database initialization script was also removed from the web runtime:

```bash
rm /var/www/html/assets/db-load-script.sql
```

These changes affected only the deployed copy inside `web-server`.

They did not delete the files from the original repository on the WSL host.

---

## Verifying After Cleanup

After removing unnecessary runtime files, I tested:

```bash
curl -s http://localhost:8080 | grep "Purchase"
```

All eight products were still returned.

This proved that:

```text
.git/
```

and:

```text
assets/db-load-script.sql
```

were not required for the running web application.

---

## Development Files

Further inspection showed that the repository also contained development-oriented files such as:

```text
README.md
.gitignore
scss/
css/style.css.map
```

The compiled CSS contained:

```css
/*# sourceMappingURL=style.css.map */
```

and the source map referenced the original SCSS files.

This demonstrated the difference between development assets and the files strictly required to serve the application.

For this learning lab, I did not continue aggressively deleting every non-essential file because the main deployment-security lesson had already been demonstrated.

A more mature deployment process would explicitly select the runtime artifact rather than copying the entire source repository and removing files afterward.

---

## Better Deployment Model

The simple learning approach was:

```text
Git Repository
      ↓
Copy everything
      ↓
Remove unwanted files
      ↓
Runtime
```

A better deployment pipeline would follow:

```text
Git Repository
      ↓
Build / Package
      ↓
Select runtime files
      ↓
Deploy artifact
      ↓
Runtime
```

This reduces the chance of accidentally publishing development or repository metadata.

---

## Source Attribution

The ecommerce application's upstream source should remain clearly attributed to KodeKloud.

When I later place my worked version in my own GitHub account, I should distinguish:

```text
Upstream application code
```

from:

```text
My deployment and DevOps work
```

My work includes areas such as:

```text
Two-tier infrastructure
Linux configuration
Apache/PHP setup
MariaDB setup
Database initialization
Networking
Environment configuration
Testing
Troubleshooting
Break/fix exercises
Deployment security
Documentation
```

This accurately represents the project as a DevOps deployment project rather than claiming authorship of the original ecommerce application.

---

## Key Lesson

Deploying an application involves much more than copying source files onto a server.

The complete deployment path includes:

```text
Application source
       ↓
Runtime dependencies
       ↓
Web server configuration
       ↓
Application configuration
       ↓
Network connectivity
       ↓
Database authentication
       ↓
Database data
       ↓
End-to-end verification
       ↓
Deployment cleanup
```

A successful deployment should be verified from the user's perspective while also testing the individual infrastructure layers underneath it.
