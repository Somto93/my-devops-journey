# SSL and TLS Basics

This section documents my practical learning of SSL/TLS, encryption, public and private keys, SSH key authentication, digital certificates, Certificate Authorities (CAs), Public Key Infrastructure (PKI), Certificate Signing Requests (CSRs), self-signed certificates, and configuring HTTPS with Apache.

The goal of this section is to understand not only how to configure SSL/TLS, but also how the underlying encryption, identity, and trust mechanisms work and how to troubleshoot them.

---

## Topics Covered

### 1. Encryption Fundamentals

Learn the purpose of encryption and the difference between:

- Plaintext
- Ciphertext
- Encryption
- Decryption
- Encryption keys

A practical symmetric encryption exercise was completed using OpenSSL and AES-256-CBC.

---

### 2. Symmetric and Asymmetric Encryption

Two major encryption models were explored.

**Symmetric encryption**

The same secret/key is used for encryption and decryption.

```text
Plaintext
    |
    | Secret Key
    v
Encryption
    |
    v
Ciphertext
    |
    | Same Secret Key
    v
Decryption
    |
    v
Plaintext
```

A major challenge with symmetric encryption is securely distributing and protecting the shared secret.

**Asymmetric encryption**

Asymmetric cryptography uses a key pair:

```text
Public Key
Private Key
```

In the confidentiality exercise:

```text
Public Key  → Encrypt
Private Key → Decrypt
```

The public key can be shared, while the private key must remain protected.

---

## 3. Public and Private Keys

RSA public and private keys were generated using OpenSSL.

The practical demonstrated that a message encrypted using the recipient's public key could be recovered using the corresponding private key.

This helped establish the basic relationship between public-key cryptography and confidentiality.

Modern TLS does not normally use asymmetric cryptography to encrypt all application data directly. Public-key mechanisms are used for authentication and key establishment, while symmetric session keys efficiently protect bulk application traffic.

---

## 4. SSH Key Authentication

SSH public-key authentication was explored using an Ed25519 key pair.

The lab included:

- Generating an SSH key pair
- Understanding public and private SSH keys
- Installing an SSH server
- Understanding SSH socket activation
- Connecting to localhost using a password
- Adding a public key to `authorized_keys`
- Authenticating using the corresponding private key
- Understanding private-key passphrases
- Testing what happens when a public key is incorrectly supplied as the SSH identity file

The authentication relationship was:

```text
Client
  |
  | Keeps private key
  |
  v
SSH Server
  |
  | Stores authorized public key
  v
~/.ssh/authorized_keys
```

The private key is not copied to the SSH server.

---

## 5. SSL/TLS Certificates

Digital certificates were studied as a way of associating an identity with a public key.

A certificate can contain information such as:

- Subject
- Issuer
- Public key
- Validity period
- Signature
- Subject Alternative Names (SANs)

Certificates help clients determine which identity a public key represents.

---

## 6. Certificate Authorities and PKI

Certificate Authorities (CAs) and Public Key Infrastructure (PKI) provide mechanisms for establishing trust.

A CA can verify a certificate request and digitally sign a certificate.

The server's private key should remain on the server and should not be sent to the CA.

A simplified trust relationship is:

```text
Trusted CA
    |
    | signs
    v
Server Certificate
    |
    | identifies
    v
Server / Domain
```

PKI includes the broader system of:

- Public and private keys
- Certificates
- Certificate Authorities
- Certificate issuance
- Certificate verification
- Trust relationships

---

## 7. Certificate Signing Requests

A Certificate Signing Request (CSR) was generated using OpenSSL.

The CSR contained:

- Identity information
- Public key
- A signature proving possession of the corresponding private key

The private key itself was not included in the CSR.

The CSR was inspected and verified using OpenSSL.

---

## 8. Self-Signed Certificates

A self-signed certificate was created using the server's private key and CSR.

Because the certificate was self-signed:

```text
Subject = Certificate owner
Issuer  = Same identity
```

The certificate successfully supported TLS encryption, but clients did not automatically trust it because it was not anchored to a trusted CA.

This demonstrated an important distinction:

```text
Encryption working ≠ Certificate automatically trusted
```

---

## 9. Subject Alternative Name (SAN)

The first certificate created in the lab contained:

```text
CN=localhost
```

but did not contain a Subject Alternative Name.

A second certificate was therefore created with:

```text
DNS:localhost
IP Address:127.0.0.1
```

The SAN was verified using OpenSSL.

Modern hostname verification primarily relies on the Subject Alternative Name extension.

---

## 10. Apache HTTPS Configuration

Apache was configured to serve HTTPS.

The practical included:

- Checking the Apache service
- Checking listening ports
- Enabling the Apache SSL module
- Running configuration tests
- Enabling the default SSL virtual host
- Inspecting Apache virtual hosts
- Inspecting the default snakeoil certificate configuration
- Installing the lab certificate and private key
- Configuring `SSLCertificateFile`
- Configuring `SSLCertificateKeyFile`
- Reloading Apache safely
- Verifying port 443
- Testing TLS connections with OpenSSL

The certificate and private key were stored under:

```text
/etc/ssl/certs/
/etc/ssl/private/
```

Apache was configured to use the lab certificate and its corresponding private key.

---

## 11. TLS Verification

TLS connections were inspected using:

```bash
openssl s_client -connect localhost:443 -servername localhost
```

The lab successfully negotiated:

```text
Protocol: TLSv1.3
Cipher: TLS_AES_256_GCM_SHA384
```

The server presented the configured RSA certificate.

Because the certificate was self-signed, normal verification produced:

```text
Verify return code: 18 (self-signed certificate)
```

This was expected.

---

## 12. Trust vs Identity vs Encryption

One of the most important lessons from the practical was that these are separate concepts.

### Encryption

TLS can successfully establish an encrypted connection.

### Trust

The client must determine whether it trusts the certificate issuer.

A self-signed certificate is not automatically trusted by clients.

### Identity

The client must also verify that the certificate identifies the hostname it intended to contact.

The lab certificate contained:

```text
DNS:localhost
IP Address:127.0.0.1
```

Verification for `localhost` succeeded when the certificate was explicitly trusted.

Verification using an incorrect hostname produced:

```text
Verify return code: 62 (hostname mismatch)
```

Therefore:

```text
TLS encryption
      +
Certificate trust
      +
Hostname verification
      =
Properly verified TLS connection
```

---

## 13. SSL/TLS Troubleshooting

A controlled Apache certificate failure was introduced to practise troubleshooting.

The Apache configuration was deliberately pointed to a nonexistent certificate:

```text
/etc/ssl/certs/somto-lab-broken.crt
```

Running:

```bash
sudo apache2ctl configtest
```

identified the problem before Apache was reloaded.

The actual certificate files were inspected, the correct path was restored, and the configuration was tested again.

The troubleshooting workflow used was:

```text
Inspect
   ↓
Identify failing layer
   ↓
Read the error
   ↓
Verify files/configuration
   ↓
Make the smallest necessary change
   ↓
Validate configuration
   ↓
Reload service
   ↓
Verify listener
   ↓
Verify TLS
```

This reinforced an important operational principle:

> Validate configuration changes before applying them to a running service.

---

## Practical Tools Used

The main commands and tools used throughout this section include:

```bash
openssl
ssh-keygen
ssh
ssh-copy-id
apache2ctl
a2enmod
a2ensite
systemctl
ss
journalctl
grep
ls
```

---

## Directory Structure

```text
ssl-tls-basics/
├── README.md
├── 01-encryption-fundamentals.md
├── 02-symmetric-and-asymmetric-encryption.md
├── 03-public-and-private-keys.md
├── 04-ssh-key-authentication.md
├── 05-ssl-tls-certificates.md
├── 06-certificate-authorities-and-pki.md
├── 07-certificate-signing-requests.md
├── 08-self-signed-certificates.md
├── 09-apache-https-configuration.md
├── 10-ssl-tls-troubleshooting.md
└── lab/
```

---

## Key Takeaways

- Encryption protects data from unauthorized reading.
- Symmetric encryption uses the same secret for encryption and decryption.
- Asymmetric cryptography uses public and private keys.
- Public keys can be distributed; private keys must remain protected.
- SSH can authenticate users using public/private key pairs.
- Certificates associate identities with public keys.
- Certificate Authorities provide trusted certificate issuance.
- A CSR contains identity information and a public key but not the private key.
- Self-signed certificates can provide encryption but are not automatically trusted.
- SANs are important for modern hostname verification.
- Apache requires an SSL-enabled virtual host and certificate/private-key configuration for HTTPS.
- Port 443 listening does not by itself prove that TLS is correctly configured.
- A successful TLS handshake does not automatically mean certificate verification succeeded.
- Trust, hostname identity, and encryption are related but distinct concepts.
- Apache configuration should be validated before reload or restart.
- Troubleshooting should be based on evidence rather than assumptions.

---

## Learning Objective

By completing this section, I developed a practical understanding of how encryption, key pairs, certificates, trust, and HTTPS work together and how to configure and troubleshoot SSL/TLS services on Linux.

The next files in this section document each concept and practical lab in greater detail.
