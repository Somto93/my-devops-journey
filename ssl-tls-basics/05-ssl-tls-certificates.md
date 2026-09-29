# SSL/TLS Certificates

Digital certificates are an important part of SSL/TLS because a public key by itself does not prove who owns that key.

A server can generate a public/private key pair:

```text
Public Key
Private Key
```

but a client still needs to answer an important question:

```text
How do I know this public key actually belongs
to the server or domain I intended to contact?
```

Digital certificates help solve this identity problem by associating a public key with information about an identity.

---

# Why a Public Key Alone Is Not Enough

Suppose a client receives a public key from a server.

The server claims:

```text
"This is the public key for example.com."
```

The client may have the key, but possession of the key alone does not prove that the claim is true.

An attacker could potentially generate their own key pair:

```text
Attacker Public Key
Attacker Private Key
```

and claim:

```text
"This is the public key for example.com."
```

Therefore, secure communication requires more than simply obtaining a public key.

There must also be a mechanism for establishing trust in the relationship between:

```text
Identity
+
Public Key
```

This is one of the main purposes of digital certificates and Certificate Authorities.

---

# What Is a Digital Certificate?

A digital certificate is an electronic document that associates a public key with information about an identity.

Conceptually:

```text
Certificate
   |
   +-- Subject / identity information
   |
   +-- Public key
   |
   +-- Issuer
   |
   +-- Validity period
   |
   +-- Extensions
   |
   +-- Digital signature
```

The certificate can be presented to clients during a TLS connection.

The corresponding private key remains protected by the server.

---

# Certificate and Private Key Relationship

A TLS server typically has:

```text
Server Private Key
+
Server Certificate
```

The certificate contains the public key associated with the private key.

Conceptually:

```text
             Server
          /          \
         /            \
Private Key         Certificate
   |                    |
   | Keep secret        +-- Public Key
   |                    +-- Identity
   |                    +-- Issuer
   |                    +-- Validity
   |                    +-- Signature
   |
   v
Protected locally
```

The private key is not supposed to be included inside the public certificate.

---

# Certificate Information

During the practical lab, the certificate was inspected using OpenSSL:

```bash
openssl x509 -in server.crt -text -noout
```

This displayed certificate information including:

```text
Version
Serial Number
Signature Algorithm
Issuer
Validity
Subject
Subject Public Key Info
X509v3 Extensions
Signature
```

These fields help describe the certificate and allow clients to validate different properties of it.

---

# Subject

The **Subject** identifies the entity represented by the certificate.

In the lab certificate, the Subject contained information entered when the Certificate Signing Request was created.

The values included:

```text
C  = AU
ST = South Australia
L  = Adelaide
O  = Somto DevOps Lab
OU = DevOps
CN = localhost
```

The resulting Subject appeared similar to:

```text
C=AU, ST=South Australia, L=Adelaide,
O=Somto DevOps Lab, OU=DevOps, CN=localhost
```

The Subject therefore described the identity associated with the certificate.

---

# Common Name

The lab used:

```text
CN=localhost
```

where:

```text
CN
```

means:

```text
Common Name
```

Historically, the Common Name was commonly used for hostname information in certificates.

However, modern hostname verification primarily relies on the:

```text
Subject Alternative Name
```

or:

```text
SAN
```

extension.

This became important later in the practical when the original certificate was replaced with a certificate containing SAN information.

---

# Issuer

The **Issuer** identifies the entity that issued or signed the certificate.

Conceptually:

```text
Subject
   ↓
Who the certificate represents
```

and:

```text
Issuer
   ↓
Who issued/signed the certificate
```

For a certificate issued by a Certificate Authority, the Issuer identifies the relevant CA identity.

For the self-signed certificate created in the lab, the Subject and Issuer contained the same identity information.

For example:

```text
Subject:
C=AU, ST=South Australia, L=Adelaide,
O=Somto DevOps Lab, OU=DevOps, CN=localhost
```

and:

```text
Issuer:
C=AU, ST=South Australia, L=Adelaide,
O=Somto DevOps Lab, OU=DevOps, CN=localhost
```

This was an important clue that the certificate was self-issued.

---

# Subject vs Issuer

A useful way to remember these fields is:

```text
Subject
   ↓
Who is this certificate about?
```

```text
Issuer
   ↓
Who issued/signed this certificate?
```

For a normal CA-issued server certificate:

```text
Subject → Server / domain identity

Issuer  → Certificate Authority
```

For our self-signed lab certificate:

```text
Subject → Somto DevOps Lab / localhost

Issuer  → Somto DevOps Lab / localhost
```

---

# Public Key Information

The certificate contained:

```text
Subject Public Key Info
```

The lab certificate used an RSA public key.

OpenSSL showed:

```text
Public-Key: (2048 bit)
```

This public key corresponded to the private key stored in:

```text
server.key
```

The relationship was:

```text
server.key
   |
   | Private key
   |
   +--------------------+
                        |
                        v
                  Public Key
                        |
                        v
                   Certificate
```

The certificate could therefore be distributed without distributing `server.key`.

---

# Certificate Validity

Certificates have a validity period.

The lab certificate displayed:

```text
Not Before
```

and:

```text
Not After
```

These define the period during which the certificate is intended to be considered valid with respect to time.

Conceptually:

```text
Not Before
     |
     | Certificate validity period
     |
Not After
```

A client can reject a certificate if it is:

```text
Not yet valid
```

or:

```text
Expired
```

Certificate expiration is therefore an important operational concern when maintaining HTTPS services.

---

# Signature Algorithm

The certificate displayed a signature algorithm:

```text
sha256WithRSAEncryption
```

The certificate signature allows verification that the certificate was signed using the corresponding issuer signing key.

For the self-signed lab certificate, the certificate was signed using the same server private key associated with the certificate itself.

For a CA-issued certificate, the certificate would instead be signed by the appropriate CA or intermediate CA private key.

---

# Certificate Signatures

A simplified certificate-signing relationship is:

```text
Certificate Information
        |
        | Issuer's Private Key
        v
Digital Signature
```

A client can use the issuer's public-key information as part of verifying the certificate signature.

This is one part of how certificate trust chains work.

---

# Self-Signed Certificate

The lab certificate was generated using:

```bash
openssl x509 -req -in server.csr -signkey server.key -out server.crt -days 365
```

The important part was:

```text
-signkey server.key
```

The server used its own private key to sign the resulting certificate.

Therefore, the certificate was self-signed.

The relationship was:

```text
server.key
    |
    | signs
    v
server.crt
```

---

# Identifying the Self-Signed Certificate

When the certificate was inspected, the Subject and Issuer were the same:

```text
Subject = Somto DevOps Lab / localhost
Issuer  = Somto DevOps Lab / localhost
```

This was an important indicator of the self-issued certificate.

The cryptographic self-signing relationship additionally means that the certificate's signature is verifiable using its own public key.

---

# Self-Signed Does Not Mean Unencrypted

One of the most important lessons from the practical was that:

```text
Self-signed certificate
```

does not mean:

```text
TLS encryption does not work
```

Apache successfully established TLS using the self-signed certificate.

The connection negotiated:

```text
TLSv1.3
```

with the cipher suite:

```text
TLS_AES_256_GCM_SHA384
```

However, normal certificate verification reported:

```text
Verify return code: 18 (self-signed certificate)
```

Therefore:

```text
Encryption succeeded
```

while:

```text
Automatic certificate trust failed
```

These are separate concepts.

---

# Certificate Trust

A client must decide whether it trusts the certificate presented by a server.

Operating systems and browsers maintain trusted Certificate Authority information.

A simplified trust model is:

```text
Trusted CA
    |
    | signs
    v
Certificate
    |
    | identifies
    v
Server / Domain
```

For a self-signed certificate, there is no separate publicly trusted CA signature.

Therefore, the certificate is not automatically trusted simply because it can establish an encrypted TLS connection.

---

# Subject Alternative Name

The original certificate created in the lab did not contain a:

```text
Subject Alternative Name
```

This was checked using:

```bash
openssl x509 -in server.crt -noout -text | grep -A2 "Subject Alternative Name"
```

No SAN information was returned.

A second certificate was therefore created with SAN information.

---

# Creating SAN Information

A small extension file was created:

```bash
echo "subjectAltName=DNS:localhost,IP:127.0.0.1" > san.ext
```

The file contained:

```text
subjectAltName=DNS:localhost,IP:127.0.0.1
```

This specified two identities:

```text
DNS:localhost
```

and:

```text
IP:127.0.0.1
```

---

# Generating a Certificate with SAN

A new certificate was created using:

```bash
openssl x509 -req \
  -in server.csr \
  -signkey server.key \
  -out server-san.crt \
  -days 365 \
  -extfile san.ext
```

The same server private key was used.

The new certificate was:

```text
server-san.crt
```

---

# Verifying the SAN

The SAN information was inspected using:

```bash
openssl x509 -in server-san.crt -noout -text | grep -A2 "Subject Alternative Name"
```

The output included:

```text
X509v3 Subject Alternative Name:
    DNS:localhost, IP Address:127.0.0.1
```

The certificate could therefore represent:

```text
localhost
```

and:

```text
127.0.0.1
```

for hostname/IP verification purposes.

---

# Why SAN Matters

When a client connects to:

```text
https://localhost
```

it needs to verify that the certificate is valid for:

```text
localhost
```

The SAN provides the identities for which the certificate is valid.

Modern clients primarily use SAN information for hostname verification rather than relying only on the Common Name.

Conceptually:

```text
Requested Hostname
       |
       v
localhost
       |
       | compare
       v
Certificate SAN
       |
       +-- DNS:localhost      ✓
       +-- IP:127.0.0.1
```

---

# Testing Correct Hostname Verification

The SAN certificate was explicitly trusted for a test using:

```bash
openssl s_client -connect localhost:443 \
  -servername localhost \
  -verify_hostname localhost \
  -CAfile server-san.crt
```

The result included:

```text
Verification: OK
```

and:

```text
Verified peername: localhost
```

with:

```text
Verify return code: 0 (ok)
```

This demonstrated that:

```text
Certificate trust
+
Correct hostname
```

allowed certificate verification to succeed in that explicit test environment.

---

# Testing the Wrong Hostname

The same certificate was tested against a hostname it did not contain:

```bash
openssl s_client -connect localhost:443 \
  -servername localhost \
  -verify_hostname www.example.com \
  -CAfile server-san.crt
```

The result included:

```text
hostname mismatch
```

and:

```text
Verify return code: 62 (hostname mismatch)
```

The TLS connection could still negotiate encryption, but certificate identity verification failed.

---

# Encryption, Trust, and Identity

This practical demonstrated three separate concepts.

## 1. Encryption

Can the client and server establish a protected TLS connection?

In the lab:

```text
TLSv1.3
```

was successfully negotiated.

## 2. Trust

Does the client trust the certificate or its issuer?

The self-signed certificate was not automatically trusted.

It could be explicitly trusted for the OpenSSL test using:

```text
-CAfile server-san.crt
```

## 3. Identity

Does the certificate represent the hostname the client intended to contact?

This was tested using:

```text
-verify_hostname
```

Therefore:

```text
Encryption
    +
Trust
    +
Hostname Identity
```

are related but distinct parts of TLS verification.

---

# `-servername` vs `-verify_hostname`

Another useful distinction from the practical is between:

```text
-servername
```

and:

```text
-verify_hostname
```

For example:

```bash
openssl s_client -connect localhost:443 \
  -servername localhost \
  -verify_hostname localhost
```

### `-servername`

Provides the Server Name Indication (SNI) value during the TLS handshake.

SNI helps a server choose the appropriate TLS virtual host/certificate when multiple hostnames are served from the same system.

### `-verify_hostname`

Explicitly checks whether the certificate is valid for the specified hostname.

They perform different jobs.

---

# Certificate File vs Private-Key File

In the Apache lab, the certificate and private key were stored separately.

The certificate was placed under:

```text
/etc/ssl/certs/
```

The private key was placed under:

```text
/etc/ssl/private/
```

For the SAN certificate, Apache used:

```text
/etc/ssl/certs/somto-lab-san.crt
```

and the corresponding private key:

```text
/etc/ssl/private/somto-lab.key
```

The certificate had permissions suitable for a public certificate file, while the private key had restrictive permissions:

```text
-rw-------
```

This reinforces:

```text
Certificate → Can be presented publicly
Private Key → Must remain protected
```

---

# Certificates During a TLS Connection

When a client connects to an HTTPS server, the server can present its certificate during the TLS handshake.

Conceptually:

```text
Client
   |
   | Connect to HTTPS server
   v
Server
   |
   | Presents certificate
   v
Client
   |
   +-- Inspect certificate
   +-- Check trust
   +-- Check validity
   +-- Check hostname
   +-- Verify relevant signatures
```

The server does not send its private key to the client.

The private key remains on the server.

---

# Certificates and HTTPS

A simplified HTTPS relationship is:

```text
HTTP
+
TLS
=
HTTPS
```

The TLS layer provides cryptographic protection for the HTTP communication.

Certificates participate in server authentication and trust.

After the TLS connection is established, HTTP application traffic can travel through the protected TLS connection.

---

# Certificates Do Not Encrypt Files by Themselves

A certificate should not be thought of simply as:

```text
An encrypted file
```

or:

```text
A secret key
```

A certificate contains public information, including a public key and identity information.

Its security role is closely connected to:

```text
Identity
Trust
Public-key cryptography
Authentication
```

The associated private key is stored separately and protected.

---

# Certificate Authorities

The self-signed certificate helped demonstrate TLS mechanics, but public HTTPS services normally require a trust relationship that clients can validate.

This leads to Certificate Authorities.

A Certificate Authority can issue/sign certificates so that clients with an appropriate trust chain can validate them.

Conceptually:

```text
Server
   |
   | Creates key pair
   |
   | Creates CSR
   v
Certificate Authority
   |
   | Validates request
   | Signs certificate
   v
Server Certificate
```

The server's private key remains with the server.

---

# Practical Security Lessons

The certificate practical reinforced several important security principles.

### Protect the private key

Files such as:

```text
server.key
```

must remain private.

### Certificates can be distributed

Files such as:

```text
server.crt
server-san.crt
```

contain public certificate information.

### Verify hostname identity

A certificate can be trusted but still be invalid for the requested hostname.

### Check validity periods

Expired or not-yet-valid certificates can cause verification failures.

### Trust and encryption are different

A TLS handshake may establish encryption even when certificate trust verification reports an error.

---

# Key Takeaways

- A public key alone does not prove who owns it.
- Digital certificates associate public keys with identity information.
- A certificate contains a public key, not the server's private key.
- The Subject identifies who the certificate represents.
- The Issuer identifies who issued or signed the certificate.
- Certificates have validity periods.
- Certificate signatures help support authenticity and trust verification.
- A self-signed certificate is signed using its own associated key.
- Self-signed certificates can still establish encrypted TLS connections.
- Self-signed certificates are not automatically trusted by normal clients.
- Modern hostname verification primarily uses Subject Alternative Names.
- The lab SAN certificate contained `DNS:localhost` and `IP:127.0.0.1`.
- A trusted certificate can still fail verification if its hostname does not match.
- `-servername` provides SNI, while `-verify_hostname` performs hostname verification.
- Encryption, certificate trust, and hostname identity are separate concepts.
- Private keys must remain protected.
- Certificates can be presented to clients.
- Certificate Authorities provide the next layer of the certificate trust model.

---

# Next Topic

The next section focuses on Certificate Authorities and Public Key Infrastructure:

```text
06-certificate-authorities-and-pki.md
```

It explains how CAs participate in certificate trust, why the server does not send its private key to the CA, and how certificates, keys, trust stores, and verification fit together within PKI.
