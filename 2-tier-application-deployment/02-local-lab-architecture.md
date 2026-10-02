# Local Two-Tier Lab Architecture

## Overview

The original two-tier architecture requires separate web/application and database nodes.

For my local practical lab, I used Docker containers to reproduce this separation on my WSL Ubuntu environment.

The two containers were:

```text
web-server
db-server
```

Both containers run Ubuntu 24.04 and are connected to the same custom Docker network.

---

## Why Docker Was Used

Using different Linux users would not provide the type of infrastructure separation required for this lab.

Linux users on the same machine normally share:

```text
Kernel
Network stack
Network interfaces
IP addresses
Running system
```

Containers provide stronger isolation.

Each container has its own:

```text
Filesystem
Processes
Hostname
Network namespace
Network interface
IP address
```

while sharing the host's Linux kernel.

This allowed me to simulate two separate Linux nodes without creating two full virtual machines.

---

## Lab Architecture

```text
                       WSL HOST
                  Ubuntu on Windows
                         │
                         │
                 localhost:8080
                         │
                         │ Docker port mapping
                         │ 8080 → 80
                         ▼
              ┌─────────────────────┐
              │     web-server      │
              │                     │
              │ Ubuntu 24.04        │
              │ 172.18.0.3          │
              │                     │
              │ Apache :80          │
              │ PHP                 │
              │ Ecommerce App       │
              └──────────┬──────────┘
                         │
                         │ TCP 3306
                         │
                  two-tier-network
                         │
                         ▼
              ┌─────────────────────┐
              │      db-server      │
              │                     │
              │ Ubuntu 24.04        │
              │ 172.18.0.2          │
              │                     │
              │ MariaDB :3306       │
              │ ecomdb              │
              │ products table      │
              └─────────────────────┘
```

---

## Creating the Docker Network

A dedicated Docker network was created for the project:

```bash
sudo docker network create two-tier-network
```

The network could be inspected using:

```bash
sudo docker network ls
```

Using a custom Docker network allowed the two application tiers to communicate privately.

---

## Creating the Database Server

The database container was created with:

```bash
sudo docker run -dit \
  --name db-server \
  --network two-tier-network \
  ubuntu:24.04 bash
```

Important options:

```text
-dit
```

runs the container in detached interactive mode with a terminal.

```text
--name db-server
```

assigns the container a predictable name.

```text
--network two-tier-network
```

connects it to the custom application network.

---

## Creating the Web Server

The web server was created with:

```bash
sudo docker run -dit \
  --name web-server \
  --network two-tier-network \
  -p 8080:80 \
  ubuntu:24.04 bash
```

The important additional option is:

```text
-p 8080:80
```

This creates the port mapping:

```text
Host port 8080
       ↓
Container port 80
```

Therefore, from the WSL host, the application can be accessed using:

```text
http://localhost:8080
```

while Apache listens inside the container on:

```text
0.0.0.0:80
```

---

## Why MariaDB Port 3306 Was Not Published

The database container was not created with:

```text
-p 3306:3306
```

because the WSL host did not need direct published access to MariaDB for the application to work.

Both containers already share:

```text
two-tier-network
```

Therefore:

```text
web-server
     │
     │ private Docker network
     ▼
db-server:3306
```

is sufficient.

This keeps the database service internal to the application network rather than unnecessarily publishing it through the host.

---

## Container IP Addresses

After installing `iproute2`, I used:

```bash
ip addr
```

to inspect each container.

During this lab:

```text
db-server  → 172.18.0.2
web-server → 172.18.0.3
```

These addresses were useful for understanding the network topology.

However, the application was not configured to depend on the database container's IP address.

---

## Docker DNS

Docker provides name resolution between containers attached to the same user-defined network.

From `web-server`, I tested:

```bash
getent hosts db-server
```

The result resolved:

```text
db-server → 172.18.0.2
```

This allowed the application to use:

```text
DB_HOST=db-server
```

instead of:

```text
DB_HOST=172.18.0.2
```

This is preferable because container IP addresses can change when containers are recreated.

---

## Network Namespaces

An important concept demonstrated by this lab was the network namespace.

Inside `db-server`:

```text
127.0.0.1
```

means the database container itself.

Inside `web-server`:

```text
127.0.0.1
```

means the web container itself.

Therefore, configuring the web application with:

```text
DB_HOST=127.0.0.1
```

would incorrectly tell it to search for MariaDB inside `web-server`.

Instead, it uses:

```text
DB_HOST=db-server
```

to reach the separate database tier.

---

## Host vs Container Ports

There are two different HTTP ports involved in this lab.

Inside `web-server`:

```text
Apache → port 80
```

From the WSL host:

```text
localhost → port 8080
```

Docker connects them:

```text
WSL localhost:8080
        │
        │ Docker NAT/port publishing
        ▼
web-server:80
        │
        ▼
Apache
```

This distinction became important during troubleshooting.

---

## Inspecting Containers

Running containers can be checked with:

```bash
sudo docker ps
```

Entering the web server:

```bash
sudo docker exec -it web-server bash
```

Entering the database server:

```bash
sudo docker exec -it db-server bash
```

This allowed each tier to be administered independently.

---

## Testing Name Resolution

From the web tier:

```bash
getent hosts db-server
```

tests whether the database hostname resolves.

This tests a different layer from:

```bash
mariadb -h db-server -u ecomuser -p
```

The first tests hostname resolution.

The second tests much more of the path:

```text
DNS
 ↓
Network
 ↓
TCP 3306
 ↓
MariaDB
 ↓
Authentication
```

---

## Testing the Web Tier

Inside `web-server`:

```bash
curl -I http://localhost:80
```

tests Apache directly inside the container.

From the WSL host:

```bash
curl -I http://localhost:8080
```

tests the externally published application path.

These tests answer different questions.

---

## Failure Isolation

The architecture allowed problems to be isolated by layer.

For example:

```text
curl localhost:8080 fails
        ↓
Check Docker/container/web tier

Container running
        ↓
Check :80 listener

No :80 listener
        ↓
Check Apache

Apache working
        ↓
Check application/PHP

Website loads but products missing
        ↓
Investigate application → database path
```

---

## Containers vs Virtual Machines

Containers and virtual machines both provide isolation, but they operate differently.

### Container

```text
Application
Container filesystem/processes/network
Shared host kernel
Physical host
```

### Virtual Machine

```text
Application
Guest operating system
Guest kernel
Hypervisor
Physical host
```

Containers are lighter because they share the host kernel.

For this local learning lab, containers provided enough isolation to practise a multi-node architecture without requiring multiple full virtual machines.

---

## Future Cloud Deployment

The same architectural concepts can later be reproduced using cloud virtual machines.

For example:

```text
Internet
   ↓
Web VM
   ↓
Private network
   ↓
Database VM
```

The infrastructure implementation would change, but the core troubleshooting concepts would remain similar:

```text
IP addressing
DNS
Ports
Firewalls
Services
Application configuration
Authentication
Database permissions
Logs
```

---

## Key Lesson

Docker was not the application architecture itself.

Docker was the infrastructure used to reproduce the architecture locally.

The application architecture remained:

```text
Web/Application Tier
        ↓
Database Tier
```

Understanding this distinction prevents confusing the deployment platform with the architecture of the application running on it.
