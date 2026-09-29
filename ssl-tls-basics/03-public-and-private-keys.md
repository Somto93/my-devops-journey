# Public and Private Keys

Public and private keys are the foundation of asymmetric cryptography.

Instead of using one shared secret for both sides, asymmetric cryptography uses a mathematically related **key pair**:

```text
Public Key
Private Key
```

The two keys have different roles.

A central security principle is:

```text
Public Key  → Can be shared
Private Key → Must be protected
```

This concept is important for technologies such as:

- SSH
- Digital certificates
- Certificate Signing Requests (CSRs)
- Digital signatures
- Public Key Infrastructure (PKI)
- TLS/HTTPS

---

## What Is a Key Pair?

A key pair consists of two mathematically related cryptographic keys.

```text
        Key Pair
       /        \
      /          \
Public Key    Private Key
```

The public key is designed to be distributed.

The private key remains under the control of its owner.

Although the keys are mathematically related, possession of the public key should not make it practical to calculate the corresponding private key when a secure algorithm and appropriate key size are used.

---

## Public Key

The public key is the shareable part of the key pair.

Examples of situations where public keys are distributed include:

```text
SSH authentication
Digital certificates
Public-key encryption
Digital signature verification
```

A public key does not need the same secrecy protection as a private key.

For example, an SSH public key may be placed on a server in:

```text
~/.ssh/authorized_keys
```

Similarly, a TLS certificate contains a public key that is presented to clients.

---

## Private Key

The private key is the sensitive part of the key pair.

It must remain protected.

Examples from the practical labs include:

```text
private_key.pem
lab_ssh_key
server.key
```

Private keys should not normally be:

- Shared publicly
- Sent to other users unnecessarily
- Uploaded to public repositories
- Included in documentation
- Sent to a Certificate Authority
- Stored with unnecessarily broad file permissions

A private key should remain under the control of the system or person that owns the key pair.

---

# RSA Key Pair Lab

OpenSSL was used to generate an RSA key pair.

The practical work was performed inside:

```text
ssl-tls-basics/asymmetric-lab/
```

---

## Generating the Private Key

The private RSA key was generated first:

```bash
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```

This produced:

```text
private_key.pem
```

The command specifies:

```text
genpkey
```

to generate a private key,

```text
-algorithm RSA
```

to use RSA, and:

```text
rsa_keygen_bits:2048
```

to generate a 2048-bit RSA key for the lab.

---

## Inspecting the Private-Key File

The generated private key had restrictive permissions:

```text
-rw-------
```

This corresponds to:

```text
600
```

Conceptually:

```text
Owner       → Read + Write
Group       → No permissions
Others      → No permissions
```

Restrictive permissions help prevent other local users from reading sensitive private-key material.

---

## Generating the Public Key

The public key was derived from the private key:

```bash
openssl pkey -in private_key.pem -pubout -out public_key.pem
```

This created:

```text
public_key.pem
```

The relationship was:

```text
private_key.pem
       |
       | OpenSSL derives public component
       v
public_key.pem
```

The public-key file had less restrictive permissions because it was not secret.

---

## Resulting Key Pair

After generation, the lab contained:

```text
private_key.pem
public_key.pem
```

Their roles were:

```text
private_key.pem → Keep secret
public_key.pem  → Can be distributed
```

---

# Public-Key Encryption Practical

The key pair was then used to demonstrate asymmetric confidentiality.

A message was created:

```bash
echo "Somto's confidential message" > message.txt
```

The plaintext was:

```text
Somto's confidential message
```

---

## Encrypting with the Public Key

The public key was used to encrypt the message:

```bash
openssl pkeyutl -encrypt -pubin -inkey public_key.pem -in message.txt -out message.enc
```

The process was:

```text
message.txt
     |
     | public_key.pem
     v
Encryption
     |
     v
message.enc
```

The resulting encrypted file could not simply be read as the original plaintext.

---

## Decrypting with the Private Key

The corresponding private key was used to decrypt the encrypted message:

```bash
openssl pkeyutl -decrypt -inkey private_key.pem -in message.enc -out recovered.txt
```

The recovered file was inspected:

```bash
cat recovered.txt
```

Output:

```text
Somto's confidential message
```

The complete process was:

```text
                Public Key
                    |
                    v
message.txt → Encryption → message.enc
                               |
                               | Private Key
                               v
                           Decryption
                               |
                               v
                         recovered.txt
```

---

# Recipient's Public Key

An important concept from the practical was determining **whose public key should be used**.

Suppose:

```text
Somto → wants to send a confidential message → David
```

David owns:

```text
David's Public Key
David's Private Key
```

Somto should obtain:

```text
David's Public Key
```

and use it for the confidentiality operation.

David keeps:

```text
David's Private Key
```

secret.

The conceptual flow becomes:

```text
Somto
  |
  | David's Public Key
  v
Encrypt Message
  |
  v
Ciphertext
  |
  v
David
  |
  | David's Private Key
  v
Decrypt Message
```

Somto does not need David's private key.

---

# Why the Private Key Is Important

The private key provides the private capability associated with the key pair.

In the RSA confidentiality exercise:

```text
Public Key
    ↓
Encrypt
```

and:

```text
Private Key
    ↓
Decrypt
```

Therefore, protecting the private key is essential.

An attacker who obtains sensitive private-key material may be able to impersonate its owner or perform operations that should only be possible for the legitimate key holder, depending on how that key is used.

---

# Can the Public Key Decrypt the Message?

In the confidentiality model demonstrated in the lab, the public key was used to encrypt the message and the corresponding private key was required to decrypt it.

Therefore:

```text
Public Key ≠ Replacement for Private Key
```

Possessing the public key does not provide the same capability as possessing the private key.

---

# Digital Signatures

Public/private key pairs can also be used for digital signatures.

Digital signatures should be understood separately from encryption.

A simplified signature process is:

```text
Data
 |
 | Private Key
 v
Sign
 |
 v
Digital Signature
```

A recipient can then use the corresponding public key to verify the signature:

```text
Data + Signature
       |
       | Public Key
       v
Verification
       |
       v
Valid / Invalid
```

This helps provide evidence that the signature was produced using the corresponding private key and that the signed data has not been altered in a way that invalidates the signature.

---

## Signing Is Not Simply "Private-Key Encryption"

A useful distinction is:

```text
Confidentiality:
Public Key → Encrypt
Private Key → Decrypt
```

versus:

```text
Digital Signature:
Private Key → Sign
Public Key → Verify
```

It is misleading to describe digital signatures simply as:

```text
Private key encrypts
Public key decrypts
```

Signing and encryption are different cryptographic operations with different security purposes.

---

# Public Keys Do Not Automatically Prove Identity

Suppose someone sends a public key and claims:

```text
"This is the public key for example.com."
```

Possessing the public key alone does not prove that the claim is true.

An attacker could potentially create their own key pair and claim that their public key belongs to another identity.

Therefore, there is another problem to solve:

```text
How do I know this public key really belongs
to the person or server it claims to represent?
```

This is where digital certificates and Certificate Authorities become important.

---

# Public Keys and Certificates

A digital certificate contains a public key together with identity and other certificate information.

Conceptually:

```text
Certificate
   |
   +-- Identity information
   |
   +-- Public key
   |
   +-- Validity information
   |
   +-- Issuer information
   |
   +-- Digital signature
```

A Certificate Authority can sign a certificate to help establish a trusted relationship between an identity and a public key.

The private key itself is not placed inside the public certificate.

---

# Public Keys and CSRs

When requesting a certificate from a Certificate Authority, a server can generate a Certificate Signing Request.

The CSR contains information such as:

```text
Identity information
Public key
Signature
```

The corresponding private key remains with the server.

The relationship is:

```text
Server Private Key
       |
       +----------------------+
       |                      |
       | signs CSR            | public component
       v                      v
      CSR --------------> Public Key
       |
       v
Certificate Authority
```

The server should **not send its private key to the CA**.

---

# Public and Private Keys in SSH

SSH also uses public/private key pairs for authentication.

In the SSH practical, a separate Ed25519 key pair was generated:

```bash
ssh-keygen -t ed25519 -f ./lab_ssh_key
```

This produced:

```text
lab_ssh_key
lab_ssh_key.pub
```

Their roles were:

```text
lab_ssh_key      → Private key
lab_ssh_key.pub  → Public key
```

The public key was installed on the SSH server.

The private key remained on the client.

Conceptually:

```text
SSH Client
    |
    | Private Key
    |
    v
Authentication
    |
    v
SSH Server
    |
    | Authorized Public Key
    v
~/.ssh/authorized_keys
```

The private key is not copied into `authorized_keys`.

---

# Private-Key Passphrases

A private-key file can itself be protected with a passphrase.

In the SSH lab, the generated lab private key required a passphrase when it was used:

```text
Enter passphrase for key './lab_ssh_key':
```

This passphrase was used locally to unlock the private key.

It was different from the user's remote account password.

Therefore:

```text
Private-key passphrase
        ↓
Protects/unlocks private-key file
```

while:

```text
Account password
        ↓
Authenticates user directly to server
```

They are separate credentials serving different purposes.

---

# File Permissions and Private Keys

Linux file permissions are an important layer of private-key protection.

For example:

```text
-rw-------
```

means that only the file owner has read/write permission.

SSH is particularly strict about private-key permissions.

During the lab, the public-key file was intentionally supplied as the SSH identity:

```bash
ssh -i ./lab_ssh_key.pub somto@localhost
```

SSH responded with a warning including:

```text
WARNING: UNPROTECTED PRIVATE KEY FILE!
```

and:

```text
Permissions 0644 for './lab_ssh_key.pub' are too open.
```

This did not mean that the public key should normally have private-key permissions.

Instead, `ssh -i` expected a **private identity key**, so SSH attempted to treat the supplied `.pub` file as though it were a private-key file.

The experiment reinforced that:

```text
ssh -i
```

expects the private identity key.

---

# Different Algorithms Can Be Used

The practical labs used more than one public-key algorithm.

The OpenSSL asymmetric encryption exercise used:

```text
RSA
```

The SSH exercise used:

```text
Ed25519
```

This demonstrates that:

```text
Public Key + Private Key
```

is a cryptographic concept rather than the name of one particular algorithm.

Different protocols and use cases can use different public-key algorithms.

---

# OpenSSL vs ssh-keygen

Two different tools were used during the practical exercises.

### OpenSSL

OpenSSL is a general-purpose cryptographic toolkit.

It was used for tasks including:

```text
RSA key generation
Encryption/decryption
CSR generation
Certificate generation
Certificate inspection
TLS testing
```

### ssh-keygen

`ssh-keygen` is specifically designed to manage SSH authentication keys.

For example:

```bash
ssh-keygen -t ed25519 -f ./lab_ssh_key
```

created both:

```text
lab_ssh_key
lab_ssh_key.pub
```

in one operation.

The tools serve different purposes even though both can work with public/private key concepts.

---

# Private Keys and Git

Private keys should not be committed to a Git repository.

Files from the labs that should be treated as private include:

```text
asymmetric-lab/private_key.pem
asymmetric-lab/ssh-lab/lab_ssh_key
certificate-lab/server.key
```

Documentation can contain commands showing how keys were generated.

It should not contain the actual private-key contents.

Before committing this SSL/TLS section, generated key material should be excluded or carefully reviewed.

---

# Key Management Principles

The practical work demonstrated several important principles:

```text
Generate keys securely
        ↓
Protect private keys
        ↓
Distribute public keys appropriately
        ↓
Use restrictive private-key permissions
        ↓
Avoid exposing keys in source control
        ↓
Replace compromised keys
```

Cryptography is only as secure as the protection applied to sensitive key material.

---

# Connection to TLS

Public/private keys become especially important in TLS.

A TLS server can possess:

```text
Private Key
+
Certificate containing Public Key
```

The server keeps the private key protected.

The certificate can be presented to clients.

Conceptually:

```text
Web Server
   |
   +-- Private Key → protected
   |
   +-- Certificate → presented to clients
                        |
                        +-- Public Key
                        +-- Identity
                        +-- Issuer
                        +-- Validity
                        +-- Signature
```

This allows TLS to use public-key cryptography while keeping the server's private key secret.

---

# Key Takeaways

- Asymmetric cryptography uses a public/private key pair.
- Public keys are designed to be distributed.
- Private keys must remain protected.
- A public key does not replace possession of the corresponding private key.
- RSA and Ed25519 are examples of public-key algorithms used in the labs.
- In the RSA confidentiality lab, the recipient's public key encrypted the message and the recipient's private key decrypted it.
- Digital signatures use private-key signing and public-key verification.
- Signing should not simply be described as private-key encryption.
- Public keys alone do not prove identity.
- Certificates help associate identities with public keys.
- A certificate contains a public key, not the server's private key.
- A CSR can contain the public key while the private key remains on the server.
- SSH servers store authorized public keys while clients retain their private keys.
- Private-key passphrases and account passwords are different.
- Private keys should have restrictive permissions.
- Private keys should not be committed to Git repositories.
- Protecting private keys is a fundamental security responsibility.

---

# Next Topic

The next section applies public/private key concepts directly to SSH authentication:

```text
04-ssh-key-authentication.md
```

It documents SSH key generation, `authorized_keys`, password authentication, key-based authentication, private-key passphrases, host verification, and the SSH practical completed on localhost.
