# Certificate Signing Requests (CSR)

A Certificate Signing Request, commonly called a **CSR**, is created when an entity wants to request a digital certificate.

The CSR connects several concepts already studied:

```text
Private Key
Public Key
Identity Information
Digital Signature
Certificate Authority
```

The key security principle is:

> The private key remains with the server. The CSR is what can be sent to the Certificate Authority.

---

# CSR Workflow

The practical certificate workflow followed this sequence:

```text
Generate Private Key
        |
        v
    server.key
        |
        | Create CSR
        v
    server.csr
        |
        | Send request
        v
Certificate Authority
        |
        | Validate and sign
        v
Server Certificate
```

In the local lab, an external CA was not used.

Instead, the CSR was later used to create a self-signed certificate.

---

# Certificate Lab Directory

The practical work was performed inside:

```text
ssl-tls-basics/certificate-lab/
```

The main files created during this part of the lab included:

```text
server.key
server.csr
```

Later exercises also created:

```text
server.crt
san.ext
server-san.crt
```

---

# Step 1: Generate the Server Private Key

Before creating the CSR, an RSA private key was generated:

```bash
openssl genpkey -algorithm RSA -out server.key -pkeyopt rsa_keygen_bits:2048
```

This created:

```text
server.key
```

The private key used:

```text
RSA
```

with a key size of:

```text
2048 bits
```

---

# Inspecting the Private-Key File

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
Owner  → Read + Write
Group  → No access
Others → No access
```

This is appropriate because:

```text
server.key
```

contains sensitive private-key material.

---

# Step 2: Create the CSR

The Certificate Signing Request was generated using:

```bash
openssl req -new -key server.key -out server.csr
```

This command used the existing private key:

```text
server.key
```

and created:

```text
server.csr
```

---

# Understanding the CSR Command

The command was:

```bash
openssl req -new -key server.key -out server.csr
```

### `openssl`

Runs the OpenSSL command-line toolkit.

### `req`

Uses OpenSSL's certificate-request functionality.

### `-new`

Creates a new certificate request.

### `-key server.key`

Uses the specified private key when creating and signing the request.

### `-out server.csr`

Writes the Certificate Signing Request to:

```text
server.csr
```

---

# Identity Information Entered

During CSR creation, OpenSSL prompted for Distinguished Name information.

The values entered during the practical were:

```text
Country Name:
AU

State or Province Name:
South Australia

Locality Name:
Adelaide

Organization Name:
Somto DevOps Lab

Organizational Unit Name:
DevOps

Common Name:
localhost
```

The email field was left blank.

The optional challenge password was also left blank.

---

# Distinguished Name

The identity information became the CSR's Subject.

When inspected, the Subject appeared as:

```text
C=AU,
ST=South Australia,
L=Adelaide,
O=Somto DevOps Lab,
OU=DevOps,
CN=localhost
```

The abbreviations mean:

```text
C  → Country
ST → State or Province
L  → Locality
O  → Organization
OU → Organizational Unit
CN → Common Name
```

---

# Common Name

The Common Name used in the lab was:

```text
localhost
```

Therefore:

```text
CN=localhost
```

appeared in the request.

Later in the practical, Subject Alternative Names were added when generating a newer certificate because modern hostname verification primarily uses SAN information.

The SAN values used later were:

```text
DNS:localhost
IP:127.0.0.1
```

---

# Step 3: Inspect the CSR

The CSR was inspected using:

```bash
openssl req -in server.csr -text -noout
```

The output showed information including:

```text
Certificate Request
Subject
Subject Public Key Info
Public-Key
Attributes
Requested Extensions
Signature Algorithm
Signature
```

---

# CSR Subject

The CSR Subject contained the identity information entered during creation.

It included:

```text
C=AU
ST=South Australia
L=Adelaide
O=Somto DevOps Lab
OU=DevOps
CN=localhost
```

This represented the identity for which the certificate was being requested.

---

# Public Key in the CSR

The CSR contained:

```text
Subject Public Key Info
```

The public key was:

```text
RSA
```

and OpenSSL showed:

```text
Public-Key: (2048 bit)
```

This public key corresponded to:

```text
server.key
```

without exposing the private key itself.

The relationship can be represented as:

```text
server.key
   |
   | Contains private key
   |
   +-----------------------+
                           |
                           | Public component
                           v
                       server.csr
                           |
                           +-- Public Key
```

---

# Does the CSR Contain the Private Key?

No.

The CSR contains the public-key information needed for the certificate request, but it does not contain the server's private key.

Therefore:

```text
server.csr
```

can be sent to a Certificate Authority.

But:

```text
server.key
```

should remain protected.

The correct relationship is:

```text
Server
  |
  +-- server.key
  |      |
  |      +--> KEEP PRIVATE
  |
  +-- server.csr
         |
         +--> Can be sent to CA
```

---

# Why Is the Private Key Used to Create the CSR?

Although the private key is not included inside the CSR, it is used to sign the CSR.

This provides cryptographic evidence that the request was created by someone possessing the corresponding private key.

Conceptually:

```text
CSR Information
      |
      | Sign using server.key
      v
CSR Signature
```

The CSR therefore contains:

```text
Identity Information
+
Public Key
+
Signature
```

but not:

```text
Private Key
```

---

# CSR Signature Algorithm

When the CSR was inspected, OpenSSL displayed:

```text
Signature Algorithm: sha256WithRSAEncryption
```

The CSR's signature was produced using the RSA private key.

This signature can be checked using the corresponding public key contained in the CSR.

---

# Step 4: Verify the CSR

The CSR was verified using:

```bash
openssl req -in server.csr -noout -verify
```

The output was:

```text
Certificate request self-signature verify OK
```

This demonstrated that the CSR's signature was internally valid.

---

# What Does "Self-Signature Verify OK" Mean?

This message can initially be confusing:

```text
Certificate request self-signature verify OK
```

It does **not** mean that the server already has a self-signed certificate.

At this stage, the file being checked is:

```text
server.csr
```

not:

```text
server.crt
```

The message means that OpenSSL successfully verified the CSR's own signature using the public key contained in the request.

---

# CSR Self-Signature vs Self-Signed Certificate

These are related cryptographic concepts but they should not be confused.

## CSR Self-Signature

The CSR is signed using the private key corresponding to the public key in the request.

```text
server.key
    |
    | signs request
    v
server.csr
```

Verification confirms that the CSR signature is valid.

This does not make the CSR a certificate.

---

## Self-Signed Certificate

A self-signed certificate is an actual certificate signed using its own corresponding private key.

In the lab, this was created later using:

```bash
openssl x509 -req \
  -in server.csr \
  -signkey server.key \
  -out server.crt \
  -days 365
```

The result was:

```text
server.crt
```

Therefore:

```text
server.csr → Certificate Signing Request

server.crt → Digital Certificate
```

They are different files serving different purposes.

---

# CSR vs Certificate

A useful comparison is:

| CSR | Certificate |
|---|---|
| Requests a certificate | Is the resulting digital certificate |
| Contains a public key | Contains a public key |
| Contains Subject information | Contains Subject information |
| Contains a request signature | Contains an issuer's certificate signature |
| Can be sent to a CA | Can be presented to clients |
| Does not establish CA trust itself | May participate in a trusted certificate chain |

---

# What Would Be Sent to a CA?

In a normal CA workflow, the server administrator would provide:

```text
server.csr
```

to the CA.

The CA can then perform its required validation before issuing a certificate.

The administrator should **not** send:

```text
server.key
```

to the CA.

---

# What Does the CA Do?

At a simplified level:

```text
Receive CSR
    |
    v
Inspect Request
    |
    v
Validate Identity / Authorization
    |
    v
Issue Certificate
    |
    v
Sign Certificate
```

The exact validation process depends on the type of CA and certificate being requested.

---

# What Comes Back from the CA?

After successful validation and issuance, the server receives a certificate associated with the public key from its CSR.

Conceptually:

```text
server.csr
    |
    v
Certificate Authority
    |
    | validation + signing
    v
Issued Certificate
```

The server can then use:

```text
Issued Certificate
+
server.key
```

for TLS.

---

# Private Key Stays on the Server

The private key remains the critical secret throughout the process.

```text
Generate server.key
       |
       +-------------------------------+
       |                               |
       | Keep private                  |
       |                               |
       v                               v
Create CSR                       Configure TLS later
       |                               |
       v                               |
Send CSR to CA                        |
       |                               |
       v                               |
Receive Certificate ------------------+
```

The same corresponding private key can then be paired with the issued certificate.

---

# The Lab's Self-Signed Workflow

The local lab did not send the CSR to an external CA.

Instead, the CSR was used locally:

```text
server.key
    |
    v
server.csr
    |
    v
Self-Sign
    |
    v
server.crt
```

This allowed certificate and TLS concepts to be practised without requiring an external CA.

---

# Creating the Initial Self-Signed Certificate

The initial certificate was created with:

```bash
openssl x509 -req \
  -in server.csr \
  -signkey server.key \
  -out server.crt \
  -days 365
```

OpenSSL displayed:

```text
Certificate request self-signature ok
```

The resulting certificate was:

```text
server.crt
```

The certificate was later inspected separately using:

```bash
openssl x509 -in server.crt -text -noout
```

---

# CSR and Subject Alternative Names

The original CSR did not request SAN extensions in this lab.

When the first certificate was inspected, it did not contain:

```text
Subject Alternative Name
```

Later, a separate extension file was created:

```bash
echo "subjectAltName=DNS:localhost,IP:127.0.0.1" > san.ext
```

The CSR was then reused when creating:

```text
server-san.crt
```

with:

```bash
openssl x509 -req \
  -in server.csr \
  -signkey server.key \
  -out server-san.crt \
  -days 365 \
  -extfile san.ext
```

This added:

```text
DNS:localhost
IP Address:127.0.0.1
```

to the resulting certificate.

---

# CSR Security

The CSR is not treated like the private key.

The private key must remain secret:

```text
server.key
```

The CSR is designed to be shared with the certificate issuer:

```text
server.csr
```

However, a CSR still contains identity and public-key information, so it should be handled intentionally rather than confused with ordinary unrelated data.

---

# Important File Roles

By this stage of the lab, several files existed with different responsibilities:

```text
server.key
```

Private key. Must remain protected.

```text
server.csr
```

Certificate Signing Request. Contains identity information, public key, and request signature.

```text
server.crt
```

Initial self-signed certificate.

```text
san.ext
```

Extension configuration used to add SAN values.

```text
server-san.crt
```

Self-signed certificate containing SAN information.

Understanding these roles is essential when configuring and troubleshooting TLS.

---

# Private Keys and Git

The private key:

```text
certificate-lab/server.key
```

should not be committed to the Git repository.

The documentation can contain:

```bash
openssl genpkey ...
```

so another person can reproduce the lab by generating their own key.

The actual private-key contents do not need to be stored in Git.

This principle also applies to other private keys created during the SSL/TLS labs.

---

# Troubleshooting CSR Problems

When working with CSRs, useful questions include:

```text
Does the private key exist?
```

```text
Was the CSR actually created?
```

```text
Does the CSR contain the expected Subject?
```

```text
Does the CSR contain the expected public key?
```

```text
Does the CSR signature verify?
```

Useful commands include:

```bash
ls -l server.key server.csr
```

```bash
openssl req -in server.csr -text -noout
```

```bash
openssl req -in server.csr -noout -verify
```

The important approach is to inspect evidence rather than assume the request is correct.

---

# CSR Practical Flow

The entire practical can be summarized as:

```text
1. Generate RSA private key
           |
           v
      server.key
           |
           v
2. Create certificate request
           |
           v
      server.csr
           |
           v
3. Inspect CSR
           |
           v
4. Verify CSR signature
           |
           v
5. Keep server.key private
           |
           v
6. Use CSR for certificate issuance
```

---

# Key Takeaways

- CSR stands for Certificate Signing Request.
- A CSR is used to request a digital certificate.
- The private key should be generated before the CSR.
- The lab used a 2048-bit RSA private key.
- The private key was stored in `server.key`.
- The CSR was stored in `server.csr`.
- The CSR contained identity information and the public key.
- The CSR did not contain the private key.
- The private key was used to sign the CSR.
- The CSR signature demonstrates possession of the corresponding private key.
- `openssl req -in server.csr -text -noout` can inspect a CSR.
- `openssl req -in server.csr -noout -verify` can verify its signature.
- `Certificate request self-signature verify OK` refers to the CSR signature, not a self-signed certificate.
- A CSR and a certificate are different objects.
- The CSR can be sent to a CA.
- The server's private key should not be sent to the CA.
- The private key must remain protected.
- The original CSR did not contain SAN information in this lab.
- SAN information was later added to the resulting certificate using an extension file.
- Private keys should not be committed to Git.

---

# Next Topic

The next section documents self-signed certificates:

```text
08-self-signed-certificates.md
```

It covers creating `server.crt`, inspecting Subject, Issuer, validity and signatures, adding Subject Alternative Names, and understanding why a self-signed certificate can provide TLS encryption without being automatically trusted.
