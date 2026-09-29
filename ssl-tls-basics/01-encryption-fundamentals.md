# Encryption Fundamentals

Encryption is one of the foundations of secure communication and data protection.

The purpose of encryption is to transform readable information into a form that cannot easily be understood by an unauthorized person.

In this section, I learned the basic concepts behind encryption before moving into symmetric encryption, asymmetric encryption, SSH, certificates, and TLS.

---

## What Is Encryption?

Encryption is the process of converting readable data into an unreadable form using a cryptographic algorithm and a key.

The original readable information is called **plaintext**.

The encrypted information is called **ciphertext**.

A simplified encryption process is:

```text
Plaintext
    |
    | Encryption algorithm + key
    v
Encryption
    |
    v
Ciphertext
```

For example:

```text
Username: john
Password: Pass123
```

is readable plaintext.

After encryption, the resulting data appears unreadable without the information required to decrypt it.

---

## Plaintext

Plaintext is the original readable information before encryption.

Examples include:

```text
Hello World
```

```text
Username: john
Password: Pass123
```

or the contents of a normal text file.

If an unauthorized person obtains plaintext, they can read the information immediately.

---

## Ciphertext

Ciphertext is the encrypted form of plaintext.

Instead of storing or transmitting the original readable information, an encryption algorithm transforms it into encrypted data.

The relationship is:

```text
Plaintext
    ↓
Encryption
    ↓
Ciphertext
```

Ciphertext is designed to be unusable without the appropriate cryptographic secret or key.

However, encryption does not mean that ciphertext can never be attacked. The security also depends on factors such as:

- The encryption algorithm
- Key strength
- Password strength
- Key management
- Implementation security

---

## Decryption

Decryption reverses the encryption process.

```text
Ciphertext
    |
    | Correct key
    v
Decryption
    |
    v
Original Plaintext
```

If the correct cryptographic key or secret is available, the encrypted data can be transformed back into its original readable form.

---

## Encryption Keys

A cryptographic key is information used by an encryption algorithm to control encryption and decryption.

The key is a critical part of the security of an encrypted system.

Depending on the type of cryptography being used, the system may use:

- One shared secret key
- A public/private key pair
- Session keys generated during a secure connection

This leads to two major cryptographic models:

```text
Symmetric Encryption
Asymmetric Encryption
```

These are covered in greater detail in the next section.

---

## Why Encryption Is Important

Without encryption, sensitive information transmitted or stored as plaintext could be readable if an unauthorized person gains access to it.

Encryption can help protect information such as:

- Credentials
- Personal information
- Application data
- Database information
- Files
- Network communications

Encryption is therefore important for protecting both:

```text
Data at rest
```

and:

```text
Data in transit
```

### Data at Rest

Data at rest refers to information stored somewhere, such as:

- Files
- Disks
- Databases
- Backups

Encrypting stored data can reduce the risk of the information being immediately readable if the storage is accessed without authorization.

### Data in Transit

Data in transit refers to information moving between systems.

For example:

```text
Browser
   |
   | Network
   v
Web Server
```

Without appropriate protection, network traffic may be exposed to interception.

HTTPS uses TLS to protect data transmitted between clients and web servers.

---

# Practical Lab: Encrypting a File with OpenSSL

OpenSSL was used to practise encryption and decryption from the Linux command line.

First, I confirmed that OpenSSL was installed:

```bash
openssl version
```

The environment used:

```text
OpenSSL 3.5.5
```

---

## Creating a Plaintext File

A simple file containing readable information was created:

```bash
echo "Username: john Password: Pass123" > secret.txt
```

The file was inspected:

```bash
cat secret.txt
```

Output:

```text
Username: john Password: Pass123
```

At this point, the information was plaintext.

Anyone with permission to read the file could immediately understand its contents.

---

## Encrypting the File

The file was encrypted using AES-256-CBC through OpenSSL:

```bash
openssl enc -aes-256-cbc -salt -pbkdf2 -in secret.txt -out secret.enc
```

OpenSSL requested an encryption password.

After entering and confirming the password successfully, a new file was created:

```text
secret.enc
```

The original file remained:

```text
secret.txt
```

Therefore:

```text
secret.txt → plaintext
secret.enc → encrypted data
```

---

## Understanding the Command

The command used was:

```bash
openssl enc -aes-256-cbc -salt -pbkdf2 -in secret.txt -out secret.enc
```

### `openssl`

Runs the OpenSSL command-line toolkit.

### `enc`

Uses OpenSSL's symmetric encryption functionality.

### `-aes-256-cbc`

Specifies AES using a 256-bit key in CBC mode for this lab.

### `-salt`

Uses a random salt as part of password-based key derivation.

### `-pbkdf2`

Uses PBKDF2 to derive cryptographic key material from the password.

The password itself is therefore not simply stored inside the encrypted file.

### `-in secret.txt`

Specifies the input plaintext file.

### `-out secret.enc`

Specifies the encrypted output file.

---

## Password Confirmation Failure

During the practical, the first encryption attempt failed because the password and confirmation did not match.

OpenSSL returned:

```text
Verify failure
bad password read
```

The encrypted file was therefore not successfully produced by that attempt.

This demonstrated an important troubleshooting lesson:

> Never assume a command successfully created its expected output.

The directory was inspected using:

```bash
ls -l
```

and the encryption command was run again correctly.

---

## Inspecting the Encrypted Data

The encrypted file was inspected using:

```bash
xxd secret.enc
```

The output contained binary/hexadecimal data rather than the original readable credentials.

The beginning included:

```text
Salted__
```

This indicated OpenSSL's salted encrypted-file format.

The salt is not the encryption password.

A salt helps password-based encryption avoid producing the same derived key/ciphertext pattern simply because the same password and plaintext are reused.

---

## Decrypting the File

The encrypted file was decrypted using:

```bash
openssl enc -aes-256-cbc -d -salt -pbkdf2 -in secret.enc -out decrypted.txt
```

The `-d` option tells OpenSSL to decrypt rather than encrypt.

The decrypted file was then inspected:

```bash
cat decrypted.txt
```

Output:

```text
Username: john Password: Pass123
```

This proved that the complete encryption/decryption cycle worked.

---

## Encryption and Decryption Flow

The practical demonstrated:

```text
secret.txt
   |
   | OpenSSL encryption
   | AES-256-CBC
   | Password-derived key
   v
secret.enc
   |
   | OpenSSL decryption
   | Correct password
   v
decrypted.txt
```

The final contents matched the original plaintext.

---

## Does Ciphertext Alone Reveal the Plaintext?

Not normally.

Obtaining:

```text
secret.enc
```

does not automatically reveal:

```text
Username: john Password: Pass123
```

The attacker would still need to defeat the cryptographic protection, for example by obtaining the secret/key or successfully guessing a weak password.

This is why strong secret management remains important even when encryption is used.

---

## Encryption Does Not Solve Every Security Problem

Encryption protects information, but its effectiveness depends on how cryptographic secrets are managed.

For example, encryption may be undermined if:

- A password is weak
- A secret is exposed in a script
- A key is stored insecurely
- An endpoint is compromised
- Malware captures the secret
- Credentials are accidentally exposed
- A private key is stolen

Therefore, encryption must be combined with proper:

```text
Key management
Access control
File permissions
Authentication
System security
```

---

## Encryption Password vs Authentication Password

An important distinction from the lab is that an **encryption password** and an **authentication password** are not necessarily the same thing.

An encryption password may be used to derive the cryptographic key needed to decrypt data.

An authentication password is used to prove a user's identity to a system.

For example:

```text
File encryption password
        ↓
Used to derive encryption key
        ↓
Decrypt encrypted file
```

versus:

```text
Account password
        ↓
Authenticate user
        ↓
Allow login
```

These serve different purposes.

---

## Key Management

One of the major lessons from encryption is that protecting the cryptographic key or secret is extremely important.

If an attacker obtains both:

```text
Encrypted Data
+
Correct Secret/Key
```

then the attacker may be able to decrypt the information.

This creates an important security question:

> How can two systems securely obtain the cryptographic information required to communicate without exposing the secret?

This question leads into the difference between **symmetric and asymmetric cryptography**.

---

## Encryption in TLS

The file-encryption exercise should not be confused with exactly how HTTPS works.

A web browser does not normally encrypt an entire HTTP conversation using a manually entered OpenSSL file password.

Modern TLS combines different cryptographic mechanisms.

At a high level:

```text
Public-key / asymmetric mechanisms
              ↓
Authentication and key establishment
              ↓
Symmetric session keys
              ↓
Efficient encryption of application traffic
```

Symmetric encryption remains extremely important because it is efficient for protecting large amounts of data.

---

## Troubleshooting Lessons

The practical also reinforced a general DevOps troubleshooting principle.

When an expected encrypted file did not appear, the correct approach was not to assume the reason.

Instead:

```text
Run command
    ↓
Inspect result
    ↓
Check expected file
    ↓
Read error
    ↓
Identify problem
    ↓
Correct problem
    ↓
Verify again
```

This same evidence-based troubleshooting approach was later used when configuring Apache and TLS.

---

## Key Takeaways

- Plaintext is readable original information.
- Encryption transforms plaintext into ciphertext.
- Decryption transforms ciphertext back into plaintext.
- Cryptographic keys control encryption and decryption.
- Ciphertext should not reveal the original information without the required cryptographic secret.
- Encryption can protect data at rest and data in transit.
- Strong encryption still requires secure key management.
- Password-based encryption should use appropriate key-derivation mechanisms.
- OpenSSL can be used to perform and inspect cryptographic operations.
- AES is a symmetric encryption algorithm.
- A salt is not the encryption password.
- Encryption passwords and account authentication passwords serve different purposes.
- Encryption alone does not solve authentication, identity, trust, or endpoint-security problems.
- Modern TLS combines public-key mechanisms with symmetric encryption.
- Always verify that security-related commands produced the expected result.

---

## Next Topic

The next section explores the two major encryption models in more detail:

```text
02-symmetric-and-asymmetric-encryption.md
```

It compares how symmetric and asymmetric cryptography use keys and explains why modern secure systems often combine both approaches.
