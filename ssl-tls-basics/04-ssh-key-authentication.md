# SSH Key Authentication

SSH (Secure Shell) provides secure remote access to Linux systems.

SSH supports several authentication methods. In this practical, I explored both:

```text
Password Authentication
Public-Key Authentication
```

The main focus was understanding how SSH uses a public/private key pair to authenticate a client without sending the private key to the server.

---

## SSH Authentication Overview

When connecting to an SSH server, there are two different identity questions involved:

```text
1. Is this the correct SSH server?
2. Is this client/user authorized to log in?
```

These are separate processes.

The client can verify the server using the server's **host key**.

The server can authenticate the user using mechanisms such as:

```text
Password
SSH public/private key pair
```

Understanding this distinction is important when troubleshooting SSH connections.

---

# Checking Existing SSH Keys

Before generating another SSH key, I inspected the existing SSH directory:

```bash
ls -la ~/.ssh
```

The system already contained:

```text
id_ed25519
id_ed25519.pub
known_hosts
known_hosts.old
```

The existing files:

```text
id_ed25519
id_ed25519.pub
```

were already being used for other SSH purposes, including my existing GitHub setup.

Instead of overwriting them, I created a separate key pair specifically for the lab.

This demonstrated an important operational principle:

> Inspect existing configuration before creating or replacing keys.

---

# Creating a Separate SSH Lab

A separate directory was used:

```text
ssl-tls-basics/asymmetric-lab/ssh-lab/
```

This kept the learning exercise separate from the existing SSH configuration.

---

# Generating an Ed25519 SSH Key Pair

The lab key pair was generated with:

```bash
ssh-keygen -t ed25519 -f ./lab_ssh_key
```

The command created:

```text
lab_ssh_key
lab_ssh_key.pub
```

Their roles were:

```text
lab_ssh_key      → Private key
lab_ssh_key.pub  → Public key
```

---

## Understanding the Command

The command was:

```bash
ssh-keygen -t ed25519 -f ./lab_ssh_key
```

### `ssh-keygen`

Generates and manages SSH keys.

### `-t ed25519`

Specifies the Ed25519 key type.

### `-f ./lab_ssh_key`

Specifies the filename for the private key.

The corresponding public key was automatically created with:

```text
.pub
```

appended to the filename.

---

# SSH Key File Permissions

The private key had restrictive permissions similar to:

```text
-rw-------
```

or:

```text
600
```

The public key had permissions similar to:

```text
-rw-r--r--
```

or:

```text
644
```

This makes sense because:

```text
Private Key → Secret
Public Key  → Shareable
```

The public key does not require the same secrecy protection as the private key.

---

# Inspecting an SSH Public Key

An SSH public key generally appears in a format similar to:

```text
ssh-ed25519 <encoded-public-key-data> user@host
```

The main components are:

```text
ssh-ed25519
```

The key type.

```text
<encoded-public-key-data>
```

The encoded public-key information.

```text
user@host
```

A comment or label that can help identify the key.

The comment does not provide the cryptographic security of the key.

---

# OpenSSL vs ssh-keygen

Earlier, OpenSSL was used to generate an RSA private key:

```bash
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```

The public key was then derived separately.

With `ssh-keygen`, both SSH key files were generated together:

```bash
ssh-keygen -t ed25519 -f ./lab_ssh_key
```

This produced:

```text
lab_ssh_key
lab_ssh_key.pub
```

The difference is mainly related to the purpose of the tools.

### OpenSSL

A general-purpose cryptographic toolkit used for:

```text
Keys
Encryption
CSRs
Certificates
TLS testing
```

### ssh-keygen

A tool specifically designed for SSH key management.

The lab also demonstrated that key-pair concepts are not limited to RSA.

The SSH key used:

```text
Ed25519
```

while the earlier OpenSSL exercise used:

```text
RSA
```

---

# Checking for the SSH Server

Before testing SSH authentication, I checked the SSH service:

```bash
sudo systemctl status ssh
```

Initially, the system returned:

```text
Unit ssh.service could not be found.
```

Rather than immediately assuming that SSH itself was broken, I checked which OpenSSH packages were installed:

```bash
dpkg -l | grep openssh
```

The system had:

```text
openssh-client
```

but the SSH server was not yet installed.

This explained why the system could run SSH client commands but did not initially have an SSH server service available.

---

# SSH Client vs SSH Server

These are different components.

### SSH Client

The SSH client allows the machine to connect to another SSH server.

For example:

```bash
ssh user@server
```

### SSH Server

The SSH server accepts incoming SSH connections.

On Ubuntu, this functionality is provided by:

```text
openssh-server
```

Therefore:

```text
SSH Client
    |
    | initiates connection
    v
SSH Server
```

A system can have the SSH client installed without having the SSH server installed.

---

# Installing OpenSSH Server

The OpenSSH server package was installed.

After installation, the SSH environment could accept incoming SSH connections.

When the SSH service was inspected, it was not continuously running in the traditional way.

Instead, the system showed that it was associated with:

```text
ssh.socket
```

---

# SSH Socket Activation

The SSH socket was inspected using:

```bash
sudo systemctl status ssh.socket
```

The socket was:

```text
active (listening)
```

and listening on:

```text
0.0.0.0:22
[::]:22
```

Port:

```text
22
```

is the standard SSH port.

The socket could trigger the SSH service when a connection arrived.

Conceptually:

```text
Client connects to port 22
          |
          v
      ssh.socket
          |
          | triggers
          v
      ssh.service
          |
          v
     SSH connection
```

This is known as **socket activation**.

It demonstrates that a service does not always need to appear continuously active as a traditional daemon for its network endpoint to be available.

---

# First SSH Connection

Before installing the lab public key, I tested a normal SSH connection:

```bash
ssh somto@localhost
```

Because this was the first SSH connection to that host identity, SSH displayed a host authenticity prompt.

The prompt showed an Ed25519 host-key fingerprint and asked whether the connection should continue.

After confirming:

```text
yes
```

the server's host information was added to:

```text
~/.ssh/known_hosts
```

The connection then requested the user's account password.

After entering the correct account password, the SSH login succeeded.

---

# What `known_hosts` Does

The `known_hosts` file helps the SSH client remember server host identities.

Conceptually:

```text
SSH Client
    |
    | Connects to server
    v
Server presents host key
    |
    v
Client checks known_hosts
```

This helps answer:

```text
"Am I connecting to the server identity I previously trusted?"
```

This is different from the server asking:

```text
"Is this user authorized to log in?"
```

---

# Two Authentication Directions

The SSH practical demonstrated two separate trust/authentication relationships.

## Client Verifies Server

The SSH server presents its host key.

The client checks the host identity using:

```text
known_hosts
```

Conceptually:

```text
Server Host Key
      |
      v
SSH Client
      |
      v
known_hosts
```

## Server Authenticates User

The SSH server then determines whether the user is authorized.

This can involve:

```text
Password authentication
```

or:

```text
Public-key authentication
```

These processes should not be confused.

---

# Installing the Public Key on the SSH Server

The lab public key was copied to the SSH server using:

```bash
ssh-copy-id -i ./lab_ssh_key.pub somto@localhost
```

The account password was required during this operation because the new public key had not yet been authorized.

The command reported:

```text
Number of key(s) added: 1
```

The public key was added to the user's SSH authorization configuration.

---

# The `authorized_keys` File

The installed public key was inspected using:

```bash
cat ~/.ssh/authorized_keys
```

The lab Ed25519 public key was present.

The important relationship is:

```text
SSH Client
    |
    | Keeps private key
    v
lab_ssh_key

SSH Server
    |
    | Stores authorized public key
    v
~/.ssh/authorized_keys
```

The private key was **not** copied to the server's `authorized_keys` file.

---

# What `authorized_keys` Means

The `authorized_keys` file tells the SSH server which public keys are authorized for the account.

Conceptually:

```text
~/.ssh/authorized_keys
          |
          v
List of authorized public keys
          |
          v
SSH server can authenticate
clients proving possession of
corresponding private keys
```

The server does not need a copy of the client's private key.

---

# Authenticating with the Private Key

After installing the public key, I connected using:

```bash
ssh -i ./lab_ssh_key somto@localhost
```

The `-i` option specifies the SSH **identity file**.

For public-key authentication, this should be the private identity key:

```text
lab_ssh_key
```

not:

```text
lab_ssh_key.pub
```

---

# Private-Key Passphrase

When the private key was used, SSH displayed:

```text
Enter passphrase for key './lab_ssh_key':
```

The key had been created with a passphrase.

After the correct key passphrase was entered, the SSH login succeeded without requesting the user's normal account password.

This demonstrated that:

```text
Private-Key Passphrase
```

and:

```text
Account Password
```

are not the same thing.

---

## Private-Key Passphrase vs Account Password

### Private-Key Passphrase

The passphrase protects the private-key file locally.

```text
Private Key File
       |
       | Protected by passphrase
       v
Unlocked private key
```

The passphrase is used locally to unlock the private key.

It is not sent to the SSH server as the user's account password.

### Account Password

The account password is an authentication credential recognized by the server.

```text
User
  |
  | Account password
  v
SSH Server
  |
  v
Authenticate account
```

Therefore, entering a private-key passphrase does not mean SSH has fallen back to password authentication.

---

# How SSH Public-Key Authentication Works

A simplified model is:

```text
SSH Client
    |
    | Has private key
    v
Proves possession of private key
    |
    | SSH protocol
    v
SSH Server
    |
    | Has corresponding public key
    v
authorized_keys
    |
    v
Authentication succeeds
```

The private key itself is not transmitted to the server.

This is an important security property.

---

# Can Someone Log In with Only the Public Key?

No.

The server already has the public key.

The public key identifies which corresponding private key can be accepted for authentication, but the connecting client must demonstrate possession of the private key.

Therefore, stealing only:

```text
lab_ssh_key.pub
```

does not provide the same authentication capability as obtaining:

```text
lab_ssh_key
```

The private key is the sensitive credential.

---

# Testing the Public Key as an Identity File

To understand the difference between the two files, I intentionally tried:

```bash
ssh -i ./lab_ssh_key.pub somto@localhost
```

SSH responded with a warning similar to:

```text
WARNING: UNPROTECTED PRIVATE KEY FILE!
```

and:

```text
Permissions 0644 for './lab_ssh_key.pub' are too open.
```

It then ignored the file and fell back toward another available authentication method, including the account password.

---

## Why Did SSH Complain About Public-Key Permissions?

The `.pub` file normally having permissions such as:

```text
644
```

is not itself a problem.

The important detail is the command:

```bash
ssh -i
```

The `-i` option expects a **private identity key**.

Therefore, when this was supplied:

```text
lab_ssh_key.pub
```

SSH attempted to process it as an identity/private-key file.

Because private keys must have restrictive permissions, SSH produced the warning.

The correct command was:

```bash
ssh -i ./lab_ssh_key somto@localhost
```

This reinforced the distinction:

```text
lab_ssh_key      → Private identity key used by client
lab_ssh_key.pub  → Public key installed on server
```

---

# SSH Is Not Encrypting the Account Password with the Public Key

A common misconception is that SSH key authentication works like this:

```text
Password
   |
   | Encrypt with public key
   v
Send encrypted password
```

That is not what the lab demonstrated.

With SSH public-key authentication, the private key is used as part of a cryptographic proof that the client possesses the key corresponding to an authorized public key.

The account password does not need to be encrypted and sent as part of successful key-based authentication.

---

# SSH Authentication Flow

The practical can be summarized as:

```text
1. Client connects to server
           |
           v
2. Server presents host identity
           |
           v
3. Client checks known_hosts
           |
           v
4. Client offers public-key identity
           |
           v
5. Server checks authorized_keys
           |
           v
6. Client proves possession of private key
           |
           v
7. Authentication succeeds
```

This separates:

```text
Server identity verification
```

from:

```text
User authentication
```

---

# `known_hosts` vs `authorized_keys`

These two files serve different purposes.

| File | Purpose |
|---|---|
| `~/.ssh/known_hosts` | Helps the SSH client verify server host identities |
| `~/.ssh/authorized_keys` | Tells the SSH server which public keys are authorized for a user |

A useful way to remember them is:

```text
known_hosts
    ↓
Which servers does the client recognize?
```

```text
authorized_keys
    ↓
Which client public keys may authenticate to this account?
```

---

# Protecting SSH Private Keys

SSH private keys should be treated as sensitive credentials.

Good practices include:

- Keep private keys private
- Use restrictive file permissions
- Consider protecting private keys with strong passphrases
- Do not send private keys to SSH servers
- Do not publish private keys
- Do not commit private keys to Git
- Use separate keys where appropriate
- Replace keys if compromise is suspected

The lab private key:

```text
asymmetric-lab/ssh-lab/lab_ssh_key
```

should therefore not be committed to the repository.

---

# Troubleshooting Lessons

The SSH lab reinforced the evidence-based troubleshooting process used throughout the DevOps journey.

When:

```bash
sudo systemctl status ssh
```

returned:

```text
Unit ssh.service could not be found.
```

the next step was to inspect the installed packages rather than guessing.

```bash
dpkg -l | grep openssh
```

This showed that only the client was installed.

After installing the server, service behavior was inspected again, revealing socket activation.

The troubleshooting chain was:

```text
Observe symptom
      ↓
Inspect service
      ↓
Inspect installed packages
      ↓
Identify missing server component
      ↓
Install required component
      ↓
Inspect service/socket state
      ↓
Test connection
      ↓
Verify authentication
```

---

# Key Takeaways

- SSH provides secure remote access to systems.
- An SSH client and SSH server are separate components.
- `openssh-client` allows outgoing SSH connections.
- `openssh-server` allows incoming SSH connections.
- SSH normally uses port 22.
- SSH can use systemd socket activation.
- `ssh-keygen` can generate public/private SSH key pairs.
- The private key remains on the client.
- The public key can be installed on the server.
- `authorized_keys` stores public keys authorized for an account.
- `known_hosts` helps clients verify SSH server identities.
- Server verification and user authentication are separate processes.
- `ssh-copy-id` can install a public key into the remote account.
- `ssh -i` expects the private identity key.
- A public `.pub` file cannot replace the private identity key.
- A private-key passphrase is different from an account password.
- The private-key passphrase is used locally to unlock the private key.
- SSH public-key authentication does not send the client's private key to the server.
- Possessing only the public key is not sufficient to authenticate as the corresponding key holder.
- Private SSH keys should not be committed to Git.

---

# Next Topic

The next section moves from SSH keys to digital certificates:

```text
05-ssl-tls-certificates.md
```

It explains why a public key alone does not prove identity and how certificates associate public keys with server or domain identities.
