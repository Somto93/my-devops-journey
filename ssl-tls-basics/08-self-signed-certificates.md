# Self-Signed Certificates

A self-signed certificate is a digital certificate that is signed using the private key corresponding to the certificate itself rather than being issued by a separate Certificate Authority.

Self-signed certificates are useful for:

- Learning and testing
- Development environments
- Internal environments where trust is managed explicitly
- Understanding how certificates and TLS work

The practical lab used a self-signed certificate to configure HTTPS on Apache and explore the difference between:

```text
Encryption
Trust
Identity
```

---

# Starting Point

Before creating the certificate, the lab already had:

```text
server.key
server.csr
```

Their roles were:

```text
server.key → Server private key
server.csr → Certificate Signing Request
```

The private key had been generated using RSA:

```bash
openssl genpkey -algorithm RSA -out server.key -pkeyopt rsa_keygen_bits:2048
```

The CSR had been created using:

```bash
openssl req -new -key server.key -out server.csr
```

---

# Creating the Self-Signed Certificate

The initial self-signed certificate was created using:

```bash
openssl x509 -req \
  -in server.csr \
  -signkey server.key \
  -out server.crt \
  -days 365
```

The resulting certificate was:

```text
server.crt
```

OpenSSL reported:

```text
Certificate request self-signature ok
```

---

# Understanding the Command

The command was:

```bash
openssl x509 -req \
  -in server.csr \
  -signkey server.key \
  -out server.crt \
  -days 365
```

### `openssl x509`

Uses OpenSSL's X.509 certificate functionality.

### `-req`

Tells OpenSSL that the input is a Certificate Signing Request.

### `-in server.csr`

Specifies the CSR:

```text
server.csr
```

### `-signkey server.key`

Uses:

```text
server.key
```

to sign the resulting certificate.

Because the server's own corresponding private key was used to sign the certificate, the result was self-signed.

### `-out server.crt`

Writes the resulting certificate to:

```text
server.crt
```

### `-days 365`

Sets the certificate validity period to 365 days from issuance.

---

# Self-Signed Certificate Flow

The process can be represented as:

```text
server.key
    |
    | Used to create/sign CSR
    v
server.csr
    |
    | Signed using server.key
    v
server.crt
```

The important distinction is:

```text
server.key → Private key
server.csr → Certificate request
server.crt → Certificate
```

---

# Inspecting the Certificate

The certificate was inspected using:

```bash
openssl x509 -in server.crt -text -noout
```

The output displayed information including:

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

This allowed the certificate to be examined before it was configured in Apache.

---

# Certificate Version

OpenSSL showed:

```text
Version: 3
```

This indicated an X.509 version 3 certificate.

X.509 v3 supports certificate extensions such as:

```text
Subject Alternative Name
Subject Key Identifier
```

The original certificate did not contain a SAN extension, which was addressed later in the lab.

---

# Subject

The certificate Subject contained the identity information originally entered when creating the CSR:

```text
C=AU
ST=South Australia
L=Adelaide
O=Somto DevOps Lab
OU=DevOps
CN=localhost
```

Conceptually:

```text
Subject
   ↓
Who the certificate represents
```

The Common Name was:

```text
localhost
```

---

# Issuer

The certificate also contained an Issuer.

Conceptually:

```text
Issuer
   ↓
Who issued/signed the certificate
```

For this certificate, the Issuer contained the same identity information as the Subject.

Therefore:

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

---

# Why Were Subject and Issuer the Same?

The certificate was self-signed.

Instead of a separate CA signing the certificate:

```text
CA Private Key
      |
      v
Server Certificate
```

the server's own private key was used:

```text
server.key
    |
    v
server.crt
```

This resulted in the same identity appearing as:

```text
Subject
```

and:

```text
Issuer
```

in this lab.

Matching Subject and Issuer is an important clue that a certificate is self-issued.

The cryptographic self-signing relationship additionally means that the certificate signature can be verified using the public key contained in the certificate itself.

---

# Certificate Validity

The certificate contained:

```text
Not Before
```

and:

```text
Not After
```

values.

For the original lab certificate, OpenSSL showed a validity period beginning on:

```text
Sep 29 09:30:26 2026 GMT
```

and ending on:

```text
Sep 29 09:30:26 2027 GMT
```

This corresponded to the requested:

```text
-days 365
```

period.

---

# Why Validity Matters

A certificate is intended to be used only within its validity period.

A client may reject a certificate if it is:

```text
Not yet valid
```

or:

```text
Expired
```

Therefore, certificate expiration is an important operational issue for HTTPS services.

A production environment should monitor certificate expiration and renew certificates before they expire.

---

# Public Key in the Certificate

The certificate contained:

```text
Subject Public Key Info
```

OpenSSL showed an RSA public key of:

```text
2048 bits
```

This public key corresponded to:

```text
server.key
```

The relationship was:

```text
server.key
   |
   | Private key
   |
   +-------------------------+
                             |
                             v
                     Corresponding
                       Public Key
                             |
                             v
                        server.crt
```

The private key itself was not stored inside the certificate.

---

# Signature Algorithm

The certificate showed:

```text
sha256WithRSAEncryption
```

as its signature algorithm.

Because the certificate was self-signed, its own corresponding private key was used for the certificate-signing operation.

---

# Self-Signed Does Not Mean Unencrypted

One of the most important lessons from this practical was:

```text
Self-signed
```

does not mean:

```text
Unencrypted
```

The self-signed certificate was successfully used by Apache to establish TLS.

OpenSSL later showed:

```text
TLSv1.3
```

with:

```text
TLS_AES_256_GCM_SHA384
```

Therefore, the connection was encrypted even though the certificate was self-signed.

---

# The Trust Problem

Although TLS encryption succeeded, normal verification produced:

```text
Verify return code: 18 (self-signed certificate)
```

This happened because the certificate did not chain to a trust anchor that OpenSSL was using for normal verification.

Therefore:

```text
TLS Encryption       → Working
Certificate Presented → Working
Automatic Trust       → Failed
```

This demonstrated that encryption and certificate trust are different concepts.

---

# Self-Signed vs CA-Issued

A simplified comparison is:

| Self-Signed Certificate | CA-Issued Certificate |
|---|---|
| Signed using its own corresponding private key | Signed by an issuing CA |
| Does not automatically establish public trust | Can chain to a trusted root |
| Useful for labs/testing/internal controlled trust | Common for public HTTPS |
| Trust may need to be configured explicitly | Clients may already trust the relevant CA hierarchy |

A self-signed certificate is not inherently incapable of encryption.

The main issue is how clients establish trust in it.

---

# Checking for Subject Alternative Name

The original certificate was checked for SAN information:

```bash
openssl x509 -in server.crt -noout -text | grep -A2 "Subject Alternative Name"
```

No output was returned.

This showed that the original certificate did not contain a:

```text
Subject Alternative Name
```

extension.

---

# Why SAN Was Needed

The certificate had:

```text
CN=localhost
```

but modern hostname verification primarily uses:

```text
Subject Alternative Name
```

or:

```text
SAN
```

Therefore, the certificate was improved by adding explicit SAN entries for:

```text
localhost
```

and:

```text
127.0.0.1
```

---

# Creating the SAN Extension File

A small extension file was created:

```bash
echo "subjectAltName=DNS:localhost,IP:127.0.0.1" > san.ext
```

The file was inspected:

```bash
cat san.ext
```

Output:

```text
subjectAltName=DNS:localhost,IP:127.0.0.1
```

This specified:

```text
DNS:localhost
```

and:

```text
IP:127.0.0.1
```

---

# Creating the SAN Certificate

A second certificate was created:

```bash
openssl x509 -req \
  -in server.csr \
  -signkey server.key \
  -out server-san.crt \
  -days 365 \
  -extfile san.ext
```

The new certificate was:

```text
server-san.crt
```

The same:

```text
server.key
```

was used because the certificate was still associated with the same key pair.

---

# Verifying the SAN

The new certificate was inspected using:

```bash
openssl x509 -in server-san.crt -noout -text | grep -A2 "Subject Alternative Name"
```

The output included:

```text
X509v3 Subject Alternative Name:
    DNS:localhost, IP Address:127.0.0.1
```

This confirmed that the new certificate contained the required SAN extension.

---

# Original Certificate vs SAN Certificate

The lab now had:

```text
server.crt
```

and:

```text
server-san.crt
```

The original certificate:

```text
server.crt
```

had:

```text
CN=localhost
```

but no SAN.

The newer certificate:

```text
server-san.crt
```

contained:

```text
DNS:localhost
IP Address:127.0.0.1
```

The SAN certificate was therefore used for the later Apache HTTPS configuration.

---

# Installing the Certificate for Apache

The original certificate was initially copied to:

```text
/etc/ssl/certs/somto-lab.crt
```

using:

```bash
sudo cp server.crt /etc/ssl/certs/somto-lab.crt
```

The private key was copied to:

```text
/etc/ssl/private/somto-lab.key
```

using:

```bash
sudo cp server.key /etc/ssl/private/somto-lab.key
```

The private key retained restrictive permissions:

```text
-rw-------
```

---

# Installing the SAN Certificate

After the SAN certificate was created, it was copied to:

```text
/etc/ssl/certs/somto-lab-san.crt
```

using:

```bash
sudo cp server-san.crt /etc/ssl/certs/somto-lab-san.crt
```

Apache was then configured to use:

```text
SSLCertificateFile /etc/ssl/certs/somto-lab-san.crt
```

while continuing to use:

```text
SSLCertificateKeyFile /etc/ssl/private/somto-lab.key
```

This worked because `server-san.crt` contained the public key corresponding to the same `server.key`.

---

# Certificate and Key Pairing

The Apache configuration effectively paired:

```text
somto-lab-san.crt
```

with:

```text
somto-lab.key
```

Conceptually:

```text
Certificate
    |
    | Contains public key
    |
    +------------------+
                       |
                       | Corresponding pair
                       |
    +------------------+
    |
Private Key
```

A certificate must be used with its corresponding private key for the server to perform the required TLS private-key operations.

---

# Testing the Self-Signed Certificate

The Apache TLS service was tested with:

```bash
openssl s_client -connect localhost:443 -servername localhost
```

The server presented the lab certificate.

The connection successfully negotiated:

```text
TLSv1.3
```

and:

```text
TLS_AES_256_GCM_SHA384
```

However, verification returned:

```text
Verify return code: 18 (self-signed certificate)
```

This was expected.

---

# Explicitly Trusting the Certificate

For a controlled test, the SAN certificate was explicitly provided as a trusted CA file:

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

This demonstrated that the certificate could pass verification when:

```text
1. It was explicitly trusted
2. Its hostname matched
```

---

# What `-CAfile` Did

The option:

```text
-CAfile server-san.crt
```

told OpenSSL to use the supplied certificate as trusted material for that verification test.

It did not:

```text
Make the certificate publicly trusted
```

and it did not:

```text
Turn the certificate into a public CA-issued certificate
```

It simply established explicit trust for that OpenSSL invocation.

---

# Hostname Verification

The command also used:

```text
-verify_hostname localhost
```

This checked whether the certificate was valid for:

```text
localhost
```

The SAN contained:

```text
DNS:localhost
```

so hostname verification succeeded.

---

# Wrong Hostname Experiment

The same certificate was then tested using:

```bash
openssl s_client -connect localhost:443 \
  -servername localhost \
  -verify_hostname www.example.com \
  -CAfile server-san.crt
```

The result included:

```text
verify error:num=62:hostname mismatch
```

and:

```text
Verify return code: 62 (hostname mismatch)
```

---

# Why Did the Wrong Hostname Fail?

The certificate contained:

```text
DNS:localhost
IP Address:127.0.0.1
```

but the client attempted to verify:

```text
www.example.com
```

These identities did not match.

Therefore:

```text
Certificate Trust → Satisfied for the test

TLS Encryption → Successfully negotiated

Hostname Identity → Failed
```

This is an important TLS troubleshooting distinction.

---

# Three Separate TLS Questions

The self-signed certificate lab demonstrated that TLS troubleshooting can involve at least three different questions.

## 1. Did TLS Negotiate?

Example evidence:

```text
Protocol: TLSv1.3
Cipher: TLS_AES_256_GCM_SHA384
```

If yes, encrypted communication was established.

---

## 2. Is the Certificate Trusted?

Example failure:

```text
Verify return code: 18 (self-signed certificate)
```

The certificate was not automatically trusted.

---

## 3. Does the Certificate Match the Requested Identity?

Example failure:

```text
Verify return code: 62 (hostname mismatch)
```

The certificate did not represent the hostname being verified.

---

# TLS Success Does Not Equal Certificate Verification Success

A major lesson from the lab was:

```text
TLS handshake succeeds
```

does not automatically mean:

```text
Certificate verification succeeds
```

For example, the wrong-hostname test still established TLS encryption.

But identity verification failed.

Therefore, when troubleshooting HTTPS, it is important to identify which layer is actually failing.

---

# Self-Signed Certificates in Production

Self-signed certificates can be appropriate where trust is deliberately managed, such as some internal or development environments.

For public websites, a certificate that chains to a CA trusted by normal client software is generally used so visitors do not need to manually configure trust.

The lab intentionally used a self-signed certificate so that certificate creation, trust, and verification could be studied directly.

---

# Protecting the Private Key

The private key used for the certificate was:

```text
server.key
```

and the installed Apache copy was:

```text
/etc/ssl/private/somto-lab.key
```

The private key should remain protected.

It should not be:

- Published
- Shared publicly
- Sent to clients
- Sent to a CA as part of a normal CSR workflow
- Committed to Git

The certificate itself is public information.

---

# Certificate Files in Git

The most important rule for the repository is:

```text
Do not commit private keys.
```

The following file is private:

```text
certificate-lab/server.key
```

The lab also contains generated certificate artifacts.

For a learning repository, the safest approach is to document the commands required to reproduce the certificates rather than depending on committed private-key material.

Before committing the SSL/TLS section, all generated lab files should be reviewed carefully.

---

# Troubleshooting Self-Signed Certificates

Useful diagnostic commands include:

### Inspect a certificate

```bash
openssl x509 -in server-san.crt -text -noout
```

### Check SAN

```bash
openssl x509 -in server-san.crt -noout -text | grep -A2 "Subject Alternative Name"
```

### Test TLS

```bash
openssl s_client -connect localhost:443 -servername localhost
```

### Test trust and hostname explicitly

```bash
openssl s_client -connect localhost:443 \
  -servername localhost \
  -verify_hostname localhost \
  -CAfile server-san.crt
```

These commands answer different diagnostic questions rather than simply telling us that "SSL is broken."

---

# Practical Workflow

The complete self-signed certificate practical can be summarized as:

```text
server.key
    |
    v
server.csr
    |
    v
server.crt
    |
    | Inspect
    v
No SAN detected
    |
    v
Create san.ext
    |
    v
server-san.crt
    |
    | Verify SAN
    v
DNS:localhost
IP:127.0.0.1
    |
    v
Install in Apache
    |
    v
Test TLS
    |
    +--> Encryption works
    |
    +--> Self-signed trust error
    |
    v
Explicitly trust certificate
    |
    v
Verify localhost
    |
    +--> Success
    |
    v
Verify wrong hostname
    |
    +--> Hostname mismatch
```

---

# Key Takeaways

- A self-signed certificate is signed using its own corresponding private key.
- The lab certificate was created from `server.csr` using `server.key`.
- `server.key` remained the private key.
- `server.crt` was the initial certificate.
- The certificate contained an RSA 2048-bit public key.
- Subject identifies who the certificate represents.
- Issuer identifies who issued/signed the certificate.
- Subject and Issuer matched in the self-signed lab certificate.
- Matching Subject and Issuer is a clue that a certificate is self-issued.
- Certificates have validity periods.
- Self-signed certificates can establish encrypted TLS connections.
- Self-signed certificates are not automatically trusted by normal clients.
- The original certificate did not contain SAN information.
- A second certificate was created with `DNS:localhost` and `IP:127.0.0.1`.
- Modern hostname verification primarily uses SAN.
- Explicitly trusting the SAN certificate allowed the OpenSSL test to verify it.
- Explicit trust in one test does not make the certificate publicly trusted.
- A certificate can be trusted but still fail hostname verification.
- TLS negotiation, certificate trust, and hostname identity are separate troubleshooting layers.
- Private keys must remain protected and should not be committed to Git.

---

# Source and Practical Scope Note

The learning material introduces private keys, CSRs, self-signed certificates, Apache certificate configuration, and OpenSSL verification as part of the SSL/TLS progression.

The SAN and explicit hostname-verification exercises in this document extend that practical with modern TLS identity verification concepts.

---

# Next Topic

The next section documents the Apache HTTPS practical:

```text
09-apache-https-configuration.md
```

It covers enabling Apache SSL support, understanding port 443 versus an SSL VirtualHost, enabling `default-ssl`, replacing the default snakeoil certificate with the lab certificate, safely validating configuration, reloading Apache, and verifying the TLS service with OpenSSL.
