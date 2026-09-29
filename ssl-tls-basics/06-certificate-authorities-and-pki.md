# Certificate Authorities and PKI

Digital certificates help associate identities with public keys, but another question remains:

```text
Why should a client trust the certificate?
```

A server can create its own key pair and certificate, but that alone does not establish trust for other systems.

This is where **Certificate Authorities (CAs)** and **Public Key Infrastructure (PKI)** become important.

---

# What Is a Certificate Authority?

A Certificate Authority is an organization or trusted entity that issues and digitally signs certificates.

A simplified relationship is:

```text
Certificate Authority
        |
        | Signs
        v
Server Certificate
        |
        | Associates identity
        | with public key
        v
Server / Domain
```

The CA's signature allows clients that trust the relevant CA to verify the certificate as part of a certificate trust chain.

---

# The Identity Problem

Suppose a server generates:

```text
Server Public Key
Server Private Key
```

The server could send its public key to a client.

However, the client still needs to determine:

```text
Does this public key really belong
to the server I intended to contact?
```

Without a trusted mechanism, an attacker could generate another key pair and make the same claim.

Certificates and CAs provide a mechanism for establishing trusted relationships between:

```text
Identity
+
Public Key
```

---

# Role of the Certificate Authority

At a simplified level, the CA process is:

```text
Server
   |
   | Generate key pair
   v
Private Key + Public Key
   |
   | Create CSR
   v
Certificate Signing Request
   |
   | Send CSR
   v
Certificate Authority
   |
   | Validate request
   | Sign certificate
   v
Issued Certificate
   |
   v
Server
```

The server can then configure the issued certificate with its corresponding private key.

---

# The Server Private Key Is Not Sent to the CA

One of the most important lessons from the certificate practical is:

> The server should not send its private key to the Certificate Authority.

The server generates and protects:

```text
server.key
```

locally.

The Certificate Signing Request contains the information needed for the certificate request, including the public key.

Conceptually:

```text
Server
  |
  +-- server.key
  |      |
  |      +-- KEEP PRIVATE
  |
  +-- server.csr
         |
         +-- Send to CA
```

The CA does not need the server's private key to issue a certificate for the server's public key.

---

# Why the Private Key Must Remain Private

The private key represents a sensitive cryptographic capability belonging to the server.

If the private key is exposed, an attacker may be able to misuse the identity associated with that key, depending on the protocol and circumstances.

Therefore:

```text
Private Key
    |
    v
Remain protected on server
```

while:

```text
CSR
    |
    v
Can be sent to CA
```

and:

```text
Certificate
    |
    v
Can be presented to clients
```

---

# Certificate Signing Request

A Certificate Signing Request, or CSR, acts as the request for a certificate.

In the practical, the CSR was created using:

```bash
openssl req -new -key server.key -out server.csr
```

The CSR contained information including:

```text
Identity information
Public key
Signature
```

The private key itself was not placed inside the CSR.

The CSR was inspected using:

```bash
openssl req -in server.csr -text -noout
```

and verified using:

```bash
openssl req -in server.csr -noout -verify
```

The result included:

```text
Certificate request self-signature verify OK
```

This verified the CSR's own signature.

It did **not** mean that a trusted CA had already issued the server a certificate.

---

# CA Signing

After receiving and validating an appropriate CSR, a CA can issue a certificate containing the requested public-key and identity information.

Conceptually:

```text
CSR
 |
 | Public key
 | Identity information
 | Proof associated with private key
 v
CA
 |
 | Validation
 | CA signing operation
 v
Certificate
```

The resulting certificate contains a signature from its issuer.

The server can then use:

```text
Issued Certificate
+
Corresponding Server Private Key
```

for TLS.

---

# Self-Signed vs CA-Signed Certificates

The lab used a self-signed certificate.

It was created using:

```bash
openssl x509 -req \
  -in server.csr \
  -signkey server.key \
  -out server.crt \
  -days 365
```

Because:

```text
server.key
```

was used to sign the server's own certificate, the certificate was self-signed.

Conceptually:

```text
Server Private Key
       |
       | signs
       v
Server Certificate
```

For a CA-issued certificate, the signing relationship is different:

```text
CA Private Key
       |
       | signs
       v
Server Certificate
```

The server still keeps its own private key.

---

# Subject and Issuer

The certificate fields help show the signing relationship.

For the self-signed lab certificate:

```text
Subject = Somto DevOps Lab / localhost
Issuer  = Somto DevOps Lab / localhost
```

The same identity appeared as both Subject and Issuer.

For a CA-issued certificate, the relationship is typically:

```text
Subject → Server identity
Issuer  → Issuing CA identity
```

For example:

```text
Subject:
example.com

Issuer:
Certificate Authority
```

---

# What Does the Client Trust?

A client does not simply trust every certificate it receives.

Instead, operating systems, browsers, and applications can maintain stores of trusted CA certificates.

These trusted certificates are often called:

```text
Trust Anchors
```

or:

```text
Root CA Certificates
```

A client can use these trusted roots when building and verifying a certificate chain.

---

# Trust Store

A trust store contains CA certificates that a system or application is configured to trust.

Conceptually:

```text
Client
  |
  v
Trust Store
  |
  +-- Trusted Root CA A
  +-- Trusted Root CA B
  +-- Trusted Root CA C
```

When a server presents a certificate, the client attempts to determine whether the certificate can be connected through a valid chain to a trust anchor it accepts.

---

# Certificate Chain

Public PKI commonly uses more than just:

```text
Root CA
   |
   v
Server Certificate
```

There may be one or more intermediate CAs.

A simplified chain is:

```text
Trusted Root CA
      |
      | signs
      v
Intermediate CA
      |
      | signs
      v
Server Certificate
```

The server certificate is often called the:

```text
Leaf Certificate
```

or:

```text
End-Entity Certificate
```

---

# Why Intermediate CAs Are Used

A root CA is highly sensitive because it acts as a trust anchor.

Rather than using the root key directly for every server certificate, PKI commonly uses intermediate CAs.

Conceptually:

```text
Root CA
   |
   v
Intermediate CA
   |
   v
Server Certificates
```

This creates a hierarchy of trust.

---

# Certificate Chain Verification

A client can evaluate a chain conceptually like this:

```text
Server Certificate
       |
       | signed by
       v
Intermediate CA
       |
       | signed by
       v
Root CA
       |
       | trusted by
       v
Client Trust Store
```

If the signatures, validity requirements, identity checks, and trust relationship succeed, the client can accept the certificate according to its verification policy.

---

# Self-Signed Certificate Trust

Our lab certificate did not have a chain leading to a normally trusted external CA.

When Apache presented the certificate, OpenSSL reported:

```text
Verify return code: 18 (self-signed certificate)
```

This did not mean TLS encryption had failed.

The connection still negotiated:

```text
TLSv1.3
```

with:

```text
TLS_AES_256_GCM_SHA384
```

The failure concerned automatic certificate trust.

---

# Explicitly Trusting the Lab Certificate

For testing, the SAN certificate was explicitly supplied as a trusted certificate:

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
Verify return code: 0 (ok)
```

For that OpenSSL invocation:

```text
-CAfile server-san.crt
```

explicitly provided trust for the lab certificate.

This did **not** make the certificate publicly trusted.

It only changed the trust configuration for that test.

---

# Trust Does Not Automatically Mean Correct Identity

The wrong-hostname experiment demonstrated another important PKI concept.

The certificate was explicitly trusted, but verification was requested for:

```text
www.example.com
```

using:

```bash
openssl s_client -connect localhost:443 \
  -servername localhost \
  -verify_hostname www.example.com \
  -CAfile server-san.crt
```

The certificate contained:

```text
DNS:localhost
IP Address:127.0.0.1
```

It did not contain:

```text
www.example.com
```

OpenSSL therefore reported:

```text
Verify return code: 62 (hostname mismatch)
```

This demonstrated:

```text
Trusted Certificate
        ≠
Correct Hostname Identity
```

Both checks matter.

---

# What Is PKI?

PKI stands for:

```text
Public Key Infrastructure
```

PKI is broader than just a Certificate Authority.

It describes the infrastructure, technologies, processes, and trust relationships used to manage public-key identities and certificates.

At a high level, PKI involves concepts such as:

```text
Public keys
Private keys
Digital certificates
Certificate Authorities
Certificate requests
Certificate issuance
Certificate validation
Trust stores
Certificate chains
Certificate lifecycle
```

---

# Simplified PKI Model

A simplified PKI relationship can be visualized as:

```text
             PKI
              |
      +-------+-------+
      |               |
      v               v
    Keys          Certificates
      |               |
      v               v
Public/Private      Identity
                      |
                      v
              Certificate Authority
                      |
                      v
                 CA Signature
                      |
                      v
                Trust Chain
                      |
                      v
                 Client Trust
```

The purpose is not merely encryption.

PKI helps systems establish trusted public-key identities.

---

# CA vs PKI

A Certificate Authority is one component of PKI.

Therefore:

```text
CA ≠ Entire PKI
```

A CA performs certificate-related functions such as issuing and signing certificates.

PKI includes the broader environment in which certificates and keys are:

```text
Generated
Requested
Issued
Distributed
Validated
Trusted
Managed
Renewed
Revoked
```

---

# Root CA

A Root Certificate Authority sits at the top of a certificate trust hierarchy.

A root certificate is typically self-signed.

Conceptually:

```text
Root CA
  |
  | Trust Anchor
  v
Intermediate CA
  |
  v
Server Certificate
```

The important difference between a root CA's self-signed certificate and our lab self-signed server certificate is not simply the fact that both are self-signed.

The important difference is whether the client has been configured to trust that certificate as a trust anchor.

---

# Intermediate CA

An Intermediate Certificate Authority sits between a root CA and end-entity certificates.

Conceptually:

```text
Root CA
   |
   | signs
   v
Intermediate CA
   |
   | signs
   v
Server Certificate
```

A client that trusts the root can verify the intermediate and then verify the server certificate through the chain.

---

# Server Certificate

The server certificate is presented by the TLS server.

It contains information such as:

```text
Server identity
Public key
Issuer
Validity period
Extensions
Digital signature
```

The server keeps the corresponding private key separately.

---

# PKI and HTTPS

For HTTPS, the relationship can be simplified as:

```text
Browser / Client
      |
      | HTTPS request
      v
Web Server
      |
      | Presents certificate
      v
Client validates
      |
      +-- Certificate signature/chain
      +-- Trusted issuer/root
      +-- Validity period
      +-- Hostname identity
      |
      v
TLS connection accepted
```

The exact TLS protocol contains additional cryptographic operations, but this model helps explain the certificate trust portion.

---

# Encryption vs Authentication vs Trust

PKI helps clarify several security concepts that should not be treated as identical.

## Encryption

```text
Can unauthorized observers read the protected traffic?
```

## Authentication / Identity

```text
Who is the system claiming to be?
```

## Trust

```text
Do I accept the evidence supporting that identity?
```

A properly verified HTTPS connection brings these concepts together.

---

# Certificate Validity Is Also Checked

Trusting an issuer alone is not enough.

Certificates also have:

```text
Not Before
Not After
```

values.

A certificate can therefore fail verification because it is:

```text
Expired
```

or:

```text
Not yet valid
```

even if other parts of its trust chain are correct.

---

# Hostname Verification Is Also Required

A certificate might have a valid signature and trusted chain but still be presented for the wrong hostname.

For example:

```text
Certificate SAN:
DNS:localhost
```

but the client expects:

```text
www.example.com
```

The certificate should not be accepted as proof of the `www.example.com` identity.

This is why SAN and hostname verification are important parts of HTTPS certificate validation.

---

# Private Keys in PKI

Private keys appear at multiple levels of PKI.

For example:

```text
Root CA Private Key
Intermediate CA Private Key
Server Private Key
```

Each must be protected appropriately.

The consequences of compromising a CA private key can be especially serious because that key may be trusted to issue or sign other certificates.

---

# Public Information vs Secret Information

A useful distinction is:

### Public / distributable information

```text
Public keys
Certificates
CSRs
CA certificates
```

### Sensitive information

```text
Server private keys
CA private keys
Private-key passphrases
```

The exact handling requirements depend on the system, but private keys must never be treated like ordinary public certificate files.

---

# Certificate Lifecycle

Certificates are not permanent.

They have a lifecycle.

A simplified lifecycle is:

```text
Generate Key Pair
       |
       v
Create CSR
       |
       v
Validate Request
       |
       v
Issue Certificate
       |
       v
Deploy Certificate
       |
       v
Monitor Validity
       |
       v
Renew / Replace
```

Certificate management is therefore an ongoing operational responsibility.

---

# Certificate Revocation

A certificate may sometimes need to stop being trusted before its normal expiration date.

For example, this may be necessary if:

```text
Private key is compromised
Certificate was issued incorrectly
Identity information changes
```

PKI includes mechanisms for communicating certificate revocation status.

This is part of the broader certificate lifecycle rather than something demonstrated directly in the local self-signed lab.

---

# Practical Lab Relationship

The certificate lab can now be viewed as a simplified local PKI exercise.

The process was:

```text
1. Generate server.key
          |
          v
2. Create server.csr
          |
          v
3. Inspect and verify CSR
          |
          v
4. Self-sign certificate
          |
          v
5. Create SAN certificate
          |
          v
6. Configure Apache
          |
          v
7. Connect using TLS
          |
          v
8. Observe trust failure
          |
          v
9. Explicitly trust lab certificate
          |
          v
10. Verify hostname
```

Because no external CA was used, the certificate was self-signed.

---

# Security Principle: Never Send the Server Private Key to the CA

The correct relationship is:

```text
SERVER
  |
  +-- Private Key
  |      |
  |      +--> STAYS PRIVATE
  |
  +-- CSR
         |
         v
         CA
         |
         | signs certificate
         v
     Certificate
         |
         v
       Server
```

Not:

```text
Server Private Key
       |
       v
      CA
```

The private key should remain protected by the entity that owns it.

---

# Key Takeaways

- A public key alone does not establish trusted identity.
- Certificate Authorities issue and digitally sign certificates.
- A CA is one component of Public Key Infrastructure.
- PKI includes keys, certificates, CAs, trust relationships, issuance, validation, and lifecycle management.
- The server generates and protects its own private key.
- The server private key should not be sent to the CA.
- A CSR contains the public key and request information, not the server private key.
- Clients use trust stores containing trusted CA certificates.
- Root CA certificates can act as trust anchors.
- Intermediate CAs can create a hierarchy between root CAs and server certificates.
- Certificate chains connect server certificates to trusted roots.
- A self-signed certificate can provide TLS encryption without being automatically trusted.
- Explicitly trusting the lab certificate made verification possible for the OpenSSL test.
- Explicit trust does not make a certificate publicly trusted.
- Trust and hostname verification are separate checks.
- A trusted certificate can still fail because of a hostname mismatch.
- Certificate validity periods also affect verification.
- Private keys must be protected at every level of PKI.
- Certificate lifecycle management includes issuance, deployment, renewal, replacement, and potentially revocation.

---

# Source and Practical Scope Note

The learning material for this section introduces Certificate Authorities, certificates, public/private keys, and PKI as part of the SSL/TLS progression.

The certificate-chain, trust-store, root/intermediate CA, lifecycle, and revocation explanations above provide additional modern PKI context around those core concepts. The local practical lab itself used a self-signed certificate rather than building a complete public CA hierarchy.

---

# Next Topic

The next section focuses specifically on Certificate Signing Requests:

```text
07-certificate-signing-requests.md
```

It documents how `server.key` and `server.csr` were created, what information the CSR contained, how the CSR signature was verified, and why the private key remained on the server.
