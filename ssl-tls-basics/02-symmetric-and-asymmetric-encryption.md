# Symmetric and Asymmetric Encryption

Cryptography can use different approaches to protect information.

Two important models studied in this section are:

```text
Symmetric Encryption
Asymmetric Encryption
```

The major difference between them is how cryptographic keys are used.

Understanding this difference is important because technologies such as SSH, certificates, PKI, HTTPS, and TLS depend on these concepts.

---

## Symmetric Encryption

Symmetric encryption uses the **same secret key** for both encryption and decryption.

The basic process is:

```text
                 Shared Secret Key
                        |
                        v
Plaintext  →  Encryption  →  Ciphertext
                                |
                                | Same Secret Key
                                v
                           Decryption
                                |
                                v
                            Plaintext
```

Both sides must have access to the same secret.

For example:

```text
Sender
  |
  | Shared Secret
  v
Encrypt Data
  |
  v
Ciphertext
  |
  | Network / Storage
  v
Receiver
  |
  | Same Shared Secret
  v
Decrypt Data
```

---

## Symmetric Encryption Lab

In the practical exercise, OpenSSL was used with AES-256-CBC.

The plaintext file was:

```text
secret.txt
```

It was encrypted using:

```bash
openssl enc -aes-256-cbc -salt -pbkdf2 -in secret.txt -out secret.enc
```

The result was:

```text
secret.txt
    |
    | AES-256-CBC
    | Password-derived key
    v
secret.enc
```

The encrypted file was later decrypted using:

```bash
openssl enc -aes-256-cbc -d -salt -pbkdf2 -in secret.enc -out decrypted.txt
```

The same password was required to derive the key needed to recover the plaintext.

This demonstrated the central idea behind symmetric encryption:

```text
Same Secret → Encryption and Decryption
```

---

## The Key Distribution Problem

Symmetric encryption can efficiently protect data, but it creates an important challenge.

Both communicating parties need access to the same secret.

For example:

```text
Alice
  |
  | Secret Key
  |
  | ? How is the secret transferred securely?
  |
  v
Bob
```

If the secret is sent through an insecure channel and an attacker obtains it, the attacker may also be able to decrypt protected information.

Therefore, a major challenge is not simply:

```text
Can we encrypt the data?
```

It is also:

```text
How do we securely distribute and protect the secret?
```

This is known as the **key distribution problem**.

---

## Interception vs Key Distribution

Network interception is a security threat, but it is useful to distinguish interception from the symmetric-key problem itself.

If an attacker intercepts only properly encrypted ciphertext, the plaintext is not automatically revealed.

For example:

```text
Attacker obtains:

secret.enc
```

but does not know the required secret.

The attacker still needs to defeat the cryptographic protection.

However, if the attacker obtains:

```text
Ciphertext
+
Correct Secret
```

the encrypted information may be recoverable.

Therefore, protecting and distributing the secret is critical.

---

# Asymmetric Encryption

Asymmetric cryptography uses a **pair of mathematically related keys** instead of one shared secret.

The pair consists of:

```text
Public Key
Private Key
```

The public key can be distributed.

The private key must remain protected by its owner.

For the confidentiality model demonstrated in the practical:

```text
Public Key  → Encrypt
Private Key → Decrypt
```

This means someone can encrypt information for a recipient using the recipient's public key without receiving the recipient's private key.

---

## Basic Asymmetric Confidentiality Model

Suppose Bob owns a key pair:

```text
Bob's Public Key
Bob's Private Key
```

Bob can distribute his public key.

Alice can then use Bob's public key to encrypt a message intended for Bob:

```text
Alice
  |
  | Bob's Public Key
  v
Encrypt Message
  |
  v
Ciphertext
  |
  | Send ciphertext
  v
Bob
  |
  | Bob's Private Key
  v
Decrypt Message
```

Bob's private key does not need to be sent to Alice.

---

# Practical RSA Encryption Lab

A practical asymmetric encryption exercise was completed using OpenSSL and RSA.

A separate lab directory was used:

```text
asymmetric-lab/
```

---

## Generating an RSA Private Key

A 2048-bit RSA private key was generated:

```bash
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```

The resulting file was:

```text
private_key.pem
```

The private key had restrictive permissions:

```text
-rw-------
```

This is appropriate because private keys should not be readable by other users unnecessarily.

---

## Generating the Public Key

The corresponding public key was derived from the private key:

```bash
openssl pkey -in private_key.pem -pubout -out public_key.pem
```

This created:

```text
public_key.pem
```

The lab now contained a key pair:

```text
private_key.pem
public_key.pem
```

The relationship was:

```text
private_key.pem
      |
      | derive public component
      v
public_key.pem
```

The private key must remain protected.

The public key can be distributed.

---

## Creating a Message

A plaintext message was created:

```bash
echo "Somto's confidential message" > message.txt
```

The file contained:

```text
Somto's confidential message
```

---

## Encrypting with the Public Key

The message was encrypted using the public key:

```bash
openssl pkeyutl -encrypt -pubin -inkey public_key.pem -in message.txt -out message.enc
```

The important part is:

```text
public_key.pem
      |
      v
Encrypt message.txt
      |
      v
message.enc
```

The public key was sufficient to encrypt the message.

---

## Decrypting with the Private Key

The encrypted message was recovered using:

```bash
openssl pkeyutl -decrypt -inkey private_key.pem -in message.enc -out recovered.txt
```

The result was inspected:

```bash
cat recovered.txt
```

Output:

```text
Somto's confidential message
```

The complete lab demonstrated:

```text
message.txt
    |
    | Recipient's Public Key
    v
message.enc
    |
    | Recipient's Private Key
    v
recovered.txt
```

The recovered message matched the original message.

---

## Whose Public Key Should Be Used?

If I want to send confidential information to another person, I use the **recipient's public key** in this simplified confidentiality model.

For example:

```text
Somto wants to send data to David.

David has:

David Public Key
David Private Key
```

Somto obtains:

```text
David Public Key
```

and uses it to encrypt the message.

David then uses:

```text
David Private Key
```

to decrypt it.

The sender should not need David's private key.

---

## Why the Public Key Can Be Shared

The public key is designed to be distributed.

Someone possessing the public key can perform the public operations for which it is intended, such as encrypting to the key in this RSA confidentiality exercise.

But the public key does not replace possession of the private key.

In the practical:

```text
public_key.pem
```

was used to create the ciphertext, while:

```text
private_key.pem
```

was required to recover the plaintext.

---

## Private Keys Must Remain Secret

The private key is the sensitive part of an asymmetric key pair.

It should not normally be:

- Published
- Shared publicly
- Committed to a public Git repository
- Sent to a Certificate Authority
- Stored with unnecessarily broad permissions

If an attacker obtains a private key, the security provided by that key pair may be compromised.

Private-key protection is therefore a critical part of asymmetric cryptography.

---

# Symmetric vs Asymmetric Encryption

The main conceptual difference is:

| Symmetric Encryption | Asymmetric Cryptography |
|---|---|
| Uses a shared secret | Uses a public/private key pair |
| Same secret is used by both sides | Public and private keys have different roles |
| Secret must be protected by all parties using it | Public key can be distributed |
| Efficient for bulk data encryption | Public-key operations are more computationally expensive |
| Key distribution is a major challenge | Helps support secure key establishment and authentication |

---

## A Common Misconception

Asymmetric cryptography should not be understood as simply:

```text
Public key encrypts
Private key decrypts
```

for every possible cryptographic operation.

That describes the confidentiality exercise performed in this lab.

Asymmetric cryptography is also used for **digital signatures**.

A better distinction is:

### Confidentiality

```text
Recipient's Public Key
        ↓
Encrypt
        ↓
Recipient's Private Key
        ↓
Decrypt
```

### Digital Signatures

```text
Private Key
     ↓
Sign
     ↓
Digital Signature

Public Key
     ↓
Verify Signature
```

Signing is not the same operation as encrypting a message with the private key.

---

# Why Not Use Asymmetric Encryption for Everything?

Public-key cryptography is extremely useful, but it is generally more computationally expensive than symmetric encryption.

Symmetric algorithms are highly efficient for protecting large amounts of application data.

Therefore, modern secure protocols often combine both approaches.

This is known broadly as a **hybrid approach**.

---

## Hybrid Cryptography

At a high level:

```text
Asymmetric / Public-Key Mechanisms
                |
                | Authentication
                | Key establishment
                v
        Symmetric Session Key
                |
                v
       Bulk Data Encryption
```

This allows a system to benefit from:

```text
Public-key cryptography
+
Efficient symmetric encryption
```

rather than relying exclusively on one approach.

---

# Connection to TLS

TLS uses this combination of cryptographic ideas.

At a simplified level:

```text
Client
   |
   | TLS handshake
   | Authentication / key establishment
   v
Server
   |
   v
Shared Session Keys Established
   |
   v
Symmetric Encryption
   |
   v
Protected Application Traffic
```

Modern TLS does **not** simply RSA-encrypt all web traffic using the server's public key.

Instead, public-key cryptography participates in authentication and key establishment, while symmetric cryptography protects the bulk application traffic.

---

## Why Session Keys Are Useful

A TLS connection can establish symmetric session keys for that connection.

Once established, those keys can efficiently protect application data such as:

```text
HTTP requests
HTTP responses
Cookies
Form submissions
API traffic
```

This allows HTTPS to provide efficient encrypted communication.

---

# Encryption vs Authentication

Encryption and authentication solve different problems.

### Encryption asks:

```text
Can an unauthorized party read this information?
```

### Authentication asks:

```text
Who am I communicating with?
```

Asymmetric cryptography alone does not automatically prove that a public key belongs to the person or server claiming to own it.

For example, receiving a file called:

```text
facebook-public-key.pem
```

does not by itself prove that the key actually belongs to Facebook.

A trusted mechanism is needed to associate:

```text
Identity
+
Public Key
```

This leads to:

```text
Digital Certificates
Certificate Authorities
Public Key Infrastructure
```

which are covered later in this section.

---

# Key Management Comparison

Symmetric encryption requires protection of the shared secret:

```text
Sender Secret
     =
Receiver Secret
```

Asymmetric cryptography separates the key roles:

```text
Public Key  → Shareable
Private Key → Secret
```

However, asymmetric cryptography still requires strong key management.

The private key must remain secure.

If the private key is exposed, the security assumptions of the key pair can be broken.

---

# Practical Security Lesson

Generated private-key files from cryptographic labs should not be casually committed to source-control repositories.

Examples from this section include:

```text
private_key.pem
server.key
lab_ssh_key
```

These are private keys and should remain protected.

Documentation may show the commands used to generate keys without publishing the actual private-key material.

Similarly, plaintext files containing credentials or secrets should not be committed merely for demonstration purposes.

---

# Key Takeaways

- Symmetric encryption uses the same secret for encryption and decryption.
- Symmetric encryption is efficient for protecting large amounts of data.
- Secure distribution and protection of shared secrets is a major challenge.
- Asymmetric cryptography uses a public/private key pair.
- Public keys can be distributed.
- Private keys must remain protected.
- In the RSA confidentiality lab, the public key encrypted the message and the private key decrypted it.
- To send confidential data to a recipient in that model, use the recipient's public key.
- Digital signatures use private-key signing and public-key verification.
- Signing should not simply be described as "encrypting with the private key."
- Public-key cryptography is generally not used to encrypt all application traffic directly.
- Modern secure protocols combine asymmetric mechanisms with symmetric encryption.
- TLS uses public-key mechanisms for authentication/key establishment and symmetric keys for efficient traffic protection.
- Possessing a public key does not automatically prove who owns it.
- Certificates and Certificate Authorities help solve the public-key identity and trust problem.
- Private keys should never be casually committed to Git repositories.

---

# Next Topic

The next section focuses specifically on public and private keys:

```text
03-public-and-private-keys.md
```

It examines the roles of key pairs in greater detail and prepares for SSH key authentication and TLS certificates.
