# SSL/TLS Troubleshooting

SSL/TLS problems can occur at several different layers.

A useful DevOps troubleshooting approach is not to immediately assume:

```text
"The certificate is broken."
```

Instead, inspect the system layer by layer and use evidence to identify where the failure actually occurs.

This practical troubleshooting exercise deliberately introduced an Apache certificate configuration error and then diagnosed it without causing an unnecessary outage.

The workflow demonstrated:

```text
Observe
   |
   v
Inspect
   |
   v
Identify Failing Layer
   |
   v
Fix
   |
   v
Validate
   |
   v
Apply
   |
   v
Verify
```

---

# Troubleshooting Mindset

When someone reports:

```text
HTTP works but HTTPS does not work correctly
```

there are many possible causes.

Examples include:

```text
Apache service stopped
Port 443 not listening
SSL module disabled
SSL VirtualHost disabled
Invalid Apache configuration
Certificate file missing
Private key file missing
Certificate/key mismatch
TLS handshake failure
Certificate trust failure
Expired certificate
Hostname mismatch
```

Do not guess which one is responsible.

Collect evidence.

---

# Troubleshoot by Layer

A useful sequence is:

```text
1. Service
      |
      v
2. Network / Port
      |
      v
3. Apache VirtualHost
      |
      v
4. Apache Configuration
      |
      v
5. Certificate and Key Files
      |
      v
6. TLS Handshake
      |
      v
7. Certificate Presented
      |
      v
8. Trust
      |
      v
9. Hostname Identity
```

Each command should answer a specific question.

---

# Layer 1: Is Apache Running?

Check:

```bash
sudo systemctl status apache2
```

This answers:

```text
Is the Apache service running?
```

If Apache is not running, investigate the service before focusing on certificate trust or hostname verification.

Useful supporting commands can include:

```bash
sudo journalctl -u apache2
```

and:

```bash
sudo apache2ctl configtest
```

---

# Layer 2: Is Port 443 Listening?

Check:

```bash
sudo ss -ltnp | grep ':443'
```

This answers:

```text
Is a process listening on TCP port 443?
```

During the lab, the output showed Apache listening on:

```text
*:443
```

This provided evidence that:

```text
Port 443 was open locally
Apache owned the listener
```

Therefore, the investigation could move to the next layer.

---

# Listening Does Not Prove HTTPS Is Correct

A listener on:

```text
:443
```

does not prove:

```text
Correct certificate
Correct hostname
Trusted certificate
Correct SSL VirtualHost
```

It only proves that something is listening on the TCP port.

This distinction is important.

---

# Layer 3: Check Apache VirtualHosts

Use:

```bash
sudo apache2ctl -S
```

This shows the VirtualHosts Apache recognizes.

For HTTPS, look for a VirtualHost associated with:

```text
*:443
```

This helps answer:

```text
Does Apache have an SSL VirtualHost configured?
```

---

# Layer 4: Test the Live TLS Endpoint

A TLS connection can be tested using:

```bash
openssl s_client -connect localhost:443 -servername localhost
```

During the baseline troubleshooting check, the command successfully connected.

The output showed:

```text
TLSv1.3
```

and:

```text
TLS_AES_256_GCM_SHA384
```

It also showed the lab certificate.

The verification result was:

```text
Verify return code: 18 (self-signed certificate)
```

---

# Interpreting the Baseline Test

From this evidence we could conclude:

```text
Port 443 reachable        → Yes
Apache responding         → Yes
TLS handshake             → Successful
Encryption                → Established
Certificate presented     → Yes
Automatic certificate trust → Failed
```

The self-signed verification result was already expected from the lab.

Therefore, it was important not to interpret:

```text
Verify return code: 18
```

as meaning that the TLS service itself was unavailable.

---

# Layer 5: Validate Apache Configuration

Before modifying or reloading Apache, use:

```bash
sudo apache2ctl configtest
```

The healthy baseline returned:

```text
Syntax OK
```

This established that Apache's current configuration passed validation.

---

# Creating a Configuration Backup

Before deliberately introducing the troubleshooting fault, the SSL configuration was backed up:

```bash
sudo cp /etc/apache2/sites-available/default-ssl.conf \
        /etc/apache2/sites-available/default-ssl.conf.bak
```

The files were checked using:

```bash
ls -l /etc/apache2/sites-available/default-ssl.conf*
```

Both the active configuration and backup were present.

Creating a backup before modifying an important configuration file provides a simple recovery option.

---

# The Working Certificate Configuration

Before the incident, Apache used:

```apache
SSLCertificateFile /etc/ssl/certs/somto-lab-san.crt
SSLCertificateKeyFile /etc/ssl/private/somto-lab.key
```

The certificate existed at:

```text
/etc/ssl/certs/somto-lab-san.crt
```

and the private key existed at:

```text
/etc/ssl/private/somto-lab.key
```

HTTPS was working.

---

# Troubleshooting Incident

For the lab, a configuration fault was deliberately introduced.

The working certificate path:

```apache
SSLCertificateFile /etc/ssl/certs/somto-lab-san.crt
```

was changed to:

```apache
SSLCertificateFile /etc/ssl/certs/somto-lab-broken.crt
```

The file:

```text
/etc/ssl/certs/somto-lab-broken.crt
```

did not exist.

Importantly, Apache was **not immediately reloaded**.

This allowed the problem to be diagnosed safely.

---

# Do Not Immediately Reload

After editing a configuration file, avoid blindly running:

```bash
sudo systemctl reload apache2
```

or:

```bash
sudo systemctl restart apache2
```

First validate the configuration.

The safer sequence is:

```text
Edit
  |
  v
Config Test
  |
  +---- Failure ----> Diagnose
  |
  +---- Success ----> Apply
```

---

# Diagnosing the Fault

The next diagnostic command was:

```bash
sudo apache2ctl configtest
```

Apache returned:

```text
AH00526: Syntax error on line 31 of /etc/apache2/sites-enabled/default-ssl.conf:
SSLCertificateFile: file '/etc/ssl/certs/somto-lab-broken.crt' does not exist or is empty
```

This output was highly useful because it identified:

```text
Configuration file
Line number
Directive
Certificate path
Nature of failure
```

---

# What the Error Told Us

The error specifically identified:

```text
SSLCertificateFile
```

and:

```text
/etc/ssl/certs/somto-lab-broken.crt
```

with:

```text
does not exist or is empty
```

Therefore, there was no reason to begin changing:

```text
Firewall rules
DNS
TLS versions
Cipher suites
Private-key permissions
Hostname verification
```

The evidence had already narrowed the failure to the certificate file path.

---

# Why `configtest` Was Important

At this point:

```text
Apache running process
```

was still using the previously loaded working configuration.

The broken configuration existed on disk, but it had not been successfully applied.

Conceptually:

```text
Configuration on Disk
        |
        | BROKEN
        v
default-ssl.conf

Running Apache
        |
        | Still has previous configuration
        v
HTTPS remains available
```

This is why configuration validation before reload is such an important operational habit.

---

# Configuration on Disk vs Runtime State

A service can have:

```text
Current configuration file on disk
```

that differs from:

```text
Configuration currently loaded by running process
```

Changing a file does not necessarily mean the running service has already loaded that change.

Therefore:

```text
Edited file
    ≠
Active runtime configuration
```

until the service successfully reloads or restarts.

---

# Inspecting the Available Certificate Files

The next step was to inspect the certificate directory.

A correct command was:

```bash
ls -lh /etc/ssl/certs/ | grep somto
```

The output showed:

```text
somto-lab-san.crt
somto-lab.crt
```

There was no:

```text
somto-lab-broken.crt
```

This confirmed the Apache error using filesystem evidence.

---

# Command Syntax Lesson

During troubleshooting, a command was initially considered using backticks around the directory:

```bash
ls -lh `/etc/ssl/certs/`
```

This is not appropriate here.

In the shell, backticks mean:

```text
Command substitution
```

The shell would try to execute:

```text
/etc/ssl/certs/
```

as a command.

The correct form is simply:

```bash
ls -lh /etc/ssl/certs/
```

or, to narrow the output:

```bash
ls -lh /etc/ssl/certs/ | grep somto
```

---

# Identifying the Correct Certificate

The filesystem evidence showed the valid SAN certificate:

```text
/etc/ssl/certs/somto-lab-san.crt
```

Therefore, Apache's configuration was corrected back to:

```apache
SSLCertificateFile /etc/ssl/certs/somto-lab-san.crt
```

The private-key directive remained:

```apache
SSLCertificateKeyFile /etc/ssl/private/somto-lab.key
```

---

# Validate the Fix

After correcting the certificate path, the next step was **not** to immediately reload Apache.

The configuration was tested again:

```bash
sudo apache2ctl configtest
```

The result was:

```text
Syntax OK
```

This provided evidence that the configuration was now valid enough for Apache to accept it.

---

# Apply the Fix

After successful validation, Apache was reloaded:

```bash
sudo systemctl reload apache2
```

Using a reload allowed the running service to reread the corrected configuration without an unnecessary full restart.

---

# Verify Port 443

After applying the configuration, the listener was checked again:

```bash
sudo ss -ltnp | grep 443
```

The output showed Apache listening on:

```text
*:443
```

This confirmed that the HTTPS listener remained available.

---

# Verify the TLS Endpoint

The live TLS service was then tested:

```bash
openssl s_client -connect localhost:443 -servername localhost
```

This was important because:

```text
Config Test Success
```

does not by itself prove:

```text
Live HTTPS Behaviour Is Correct
```

The running endpoint still needs to be verified.

---

# Focused TLS Verification

To make the output easier to interpret, the important TLS fields were filtered:

```bash
openssl s_client -connect localhost:443 -servername localhost \
  </dev/null 2>&1 |
  grep -E 'subject=|issuer=|Protocol|Cipher|Verify return code'
```

The output included:

```text
subject=C=AU, ST=South Australia, L=Adelaide, O=Somto DevOps Lab, OU=DevOps, CN=localhost

issuer=C=AU, ST=South Australia, L=Adelaide, O=Somto DevOps Lab, OU=DevOps, CN=localhost

New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384

Protocol: TLSv1.3

Verify return code: 18 (self-signed certificate)
```

---

# Interpreting the Final Verification

The evidence showed:

```text
Apache listener        → Working
TLS handshake          → Working
TLS version            → TLSv1.3
Cipher                 → TLS_AES_256_GCM_SHA384
Expected certificate   → Presented
Certificate trust      → Self-signed warning
```

The:

```text
Verify return code: 18
```

was expected because the certificate remained self-signed.

It did not indicate that the certificate-path incident was still unresolved.

---

# Incident Timeline

The entire troubleshooting incident can be represented as:

```text
HTTPS Working
     |
     v
Create Config Backup
     |
     v
Change Certificate Path
     |
     v
Path References Missing File
     |
     v
DO NOT RELOAD
     |
     v
Run apache2ctl configtest
     |
     v
Exact Certificate Path Error
     |
     v
Inspect /etc/ssl/certs/
     |
     v
Find Correct Certificate
     |
     v
Correct Apache Configuration
     |
     v
Run configtest Again
     |
     v
Syntax OK
     |
     v
Reload Apache
     |
     v
Check Port 443
     |
     v
Test TLS Endpoint
     |
     v
Service Verified
```

---

# Why the Incident Did Not Become an Outage

The most important operational lesson was the sequence:

```text
Edit
  |
  v
Validate
  |
  v
Apply
```

rather than:

```text
Edit
  |
  v
Immediately Restart/Reload
```

Because the broken certificate path was detected by:

```bash
sudo apache2ctl configtest
```

before it was applied, the running Apache process could continue using its previously loaded working configuration.

---

# Troubleshooting Principle: Inspect Before Changing

When a service fails, avoid making several unrelated changes at once.

For example, if HTTPS fails, do not immediately:

```text
Change firewall
Change certificate
Change private key
Change DNS
Change TLS versions
Restart Apache
Reinstall Apache
```

Doing so can destroy useful evidence and introduce additional problems.

Instead:

```text
Observe
   |
   v
Form a question
   |
   v
Run a diagnostic command
   |
   v
Interpret evidence
   |
   v
Choose next action
```

---

# One Command Should Answer a Question

A useful troubleshooting habit is to know what question each command answers.

### Service

```bash
sudo systemctl status apache2
```

Question:

```text
Is Apache running?
```

### Listener

```bash
sudo ss -ltnp | grep ':443'
```

Question:

```text
Is something listening on TCP 443?
```

### VirtualHost

```bash
sudo apache2ctl -S
```

Question:

```text
Does Apache recognize the expected :443 VirtualHost?
```

### Configuration

```bash
sudo apache2ctl configtest
```

Question:

```text
Does Apache accept the current configuration?
```

### Certificate Files

```bash
ls -lh /etc/ssl/certs/ | grep somto
```

Question:

```text
Which expected certificate files actually exist?
```

### TLS Endpoint

```bash
openssl s_client -connect localhost:443 -servername localhost
```

Question:

```text
Can the live server negotiate TLS, and what certificate does it present?
```

---

# Trust Troubleshooting

If TLS successfully negotiates but OpenSSL reports:

```text
Verify return code: 18 (self-signed certificate)
```

the problem is different from:

```text
Connection refused
```

The first suggests:

```text
TLS endpoint reachable
TLS handshake successful
Certificate presented
Trust verification problem
```

The second may indicate a network/listener/service problem.

Different errors point to different layers.

---

# Hostname Troubleshooting

The lab also demonstrated:

```text
Verify return code: 62 (hostname mismatch)
```

when the certificate for:

```text
localhost
```

was verified against:

```text
www.example.com
```

This means the investigation should focus on certificate identity/SAN configuration rather than assuming TLS encryption failed.

---

# SAN Troubleshooting

To inspect SAN information:

```bash
openssl x509 -in server-san.crt -noout -text |
  grep -A2 "Subject Alternative Name"
```

The lab certificate showed:

```text
DNS:localhost
IP Address:127.0.0.1
```

If the requested hostname is not represented appropriately in the certificate, hostname verification can fail.

---

# Certificate Expiration Troubleshooting

Certificate dates can be inspected using:

```bash
openssl x509 -in server-san.crt -noout -dates
```

This shows:

```text
notBefore
notAfter
```

A certificate may fail verification if it is:

```text
Expired
```

or:

```text
Not yet valid
```

---

# Inspect Subject and Issuer

Use:

```bash
openssl x509 -in server-san.crt -noout -subject -issuer
```

This helps answer:

```text
Who does the certificate represent?
```

and:

```text
Who issued the certificate?
```

For the self-signed lab certificate, Subject and Issuer represent the same lab identity.

---

# Certificate and Private-Key Mismatch

Another possible HTTPS problem is configuring a certificate with the wrong private key.

The certificate contains a public key.

The configured private key must correspond to that public key.

A mismatch can prevent Apache from using the certificate/key pair correctly.

This was not the fault introduced in our incident, but it is an important certificate configuration failure to distinguish from a missing-file error.

---

# Private-Key Permissions

The lab private key was installed as:

```text
/etc/ssl/private/somto-lab.key
```

with restrictive permissions.

If a service cannot appropriately access a required private key, TLS configuration can fail.

However, permissions should only be investigated when the evidence points in that direction.

Do not weaken private-key permissions unnecessarily simply because HTTPS has a problem.

---

# Apache Logs

When configuration tests or service state do not provide enough information, Apache logs and the system journal can provide additional evidence.

For example:

```bash
sudo journalctl -u apache2
```

The exact log investigation should be driven by the failure being observed.

The troubleshooting principle remains:

```text
Use evidence to narrow the failing layer.
```

---

# Configuration Backup and Recovery

Before changing an important configuration file, creating a backup can provide a quick recovery option.

In the lab:

```bash
sudo cp /etc/apache2/sites-available/default-ssl.conf \
        /etc/apache2/sites-available/default-ssl.conf.bak
```

created:

```text
default-ssl.conf.bak
```

A backup should not replace proper version control and configuration management in larger environments, but it is useful during a local learning exercise.

---

# Safe Change Workflow

A strong operational workflow is:

```text
1. Inspect current state

2. Back up important configuration when appropriate

3. Make one controlled change

4. Validate configuration

5. Do not apply invalid configuration

6. Apply valid configuration

7. Verify service state

8. Verify network listener

9. Test actual application/TLS behaviour

10. Confirm expected certificate and identity
```

This is safer than making multiple changes and hoping the problem disappears.

---

# Troubleshooting Decision Flow

A simplified HTTPS troubleshooting flow is:

```text
HTTPS Problem
     |
     v
Is Apache running?
     |
     +-- No --> Investigate service
     |
     +-- Yes
           |
           v
Is :443 listening?
           |
           +-- No --> Investigate listener/SSL config
           |
           +-- Yes
                 |
                 v
Does Apache recognize :443 VirtualHost?
                 |
                 +-- No --> Investigate site/vhost config
                 |
                 +-- Yes
                       |
                       v
Does configtest pass?
                       |
                       +-- No --> Fix reported config error
                       |
                       +-- Yes
                             |
                             v
Can TLS negotiate?
                             |
                             +-- No --> Investigate TLS config
                             |
                             +-- Yes
                                   |
                                   v
Correct certificate presented?
                                   |
                                   +-- No --> Inspect certificate config
                                   |
                                   +-- Yes
                                         |
                                         v
Certificate trusted?
                                         |
                                         +-- No --> Investigate trust chain
                                         |
                                         +-- Yes
                                               |
                                               v
Hostname matches?
                                               |
                                               +-- No --> Inspect SAN/identity
                                               |
                                               +-- Yes --> TLS verification healthy
```

---

# Common Error Categories

It is useful to classify failures rather than simply saying:

```text
SSL is not working
```

Possible categories include:

| Symptom | Likely Layer to Investigate |
|---|---|
| Apache inactive | Service |
| Nothing listening on 443 | Listener / Apache SSL configuration |
| No `:443` VirtualHost | Apache site configuration |
| `configtest` failure | Apache configuration |
| Certificate file does not exist | Filesystem / configuration path |
| TLS cannot negotiate | TLS configuration |
| Wrong certificate presented | VirtualHost / certificate configuration |
| Self-signed verification error | Trust |
| Hostname mismatch | Certificate identity / SAN |
| Certificate expired | Certificate lifecycle |
| Private key inaccessible | File permissions / service access |
| Certificate/key mismatch | Key-pair configuration |

The table is a starting point for investigation, not a substitute for collecting evidence.

---

# DevOps Lesson: Prevent the Outage

Troubleshooting is not only about repairing failed systems.

Good operational practice also prevents failures from reaching production.

In this incident:

```text
Broken configuration
```

was caught before:

```text
Service reload
```

Therefore the diagnostic command acted as a safety check.

This pattern applies beyond Apache.

Many services provide some form of:

```text
Configuration validation
Syntax check
Dry run
Test mode
```

Using those capabilities before applying changes can reduce avoidable outages.

---

# DevOps Lesson: Verify After the Fix

A successful command such as:

```text
Syntax OK
```

is not the end of troubleshooting.

After applying the fix, verify the actual service.

For this lab:

```text
Config test
    |
    v
Reload Apache
    |
    v
Check :443
    |
    v
Connect with OpenSSL
    |
    v
Inspect certificate/protocol/cipher
```

This confirms that the system is working from the client's perspective as well as from the configuration parser's perspective.

---

# Final SSL/TLS Troubleshooting Checklist

When troubleshooting an Apache HTTPS service, consider:

```text
[ ] Is Apache running?

[ ] Is TCP 443 listening?

[ ] Is the SSL module enabled?

[ ] Is the expected :443 VirtualHost enabled?

[ ] Does apache2ctl configtest succeed?

[ ] Does the configured certificate file exist?

[ ] Does the configured private key exist?

[ ] Are private-key permissions appropriate?

[ ] Do the certificate and private key correspond?

[ ] Can openssl s_client establish TLS?

[ ] Which certificate is actually presented?

[ ] What TLS version is negotiated?

[ ] What cipher is negotiated?

[ ] Is the certificate trusted?

[ ] Is the certificate currently valid?

[ ] Does the hostname match the certificate SAN?

[ ] Was the service verified after the change?
```

Do not necessarily run every check for every incident.

Use the observed evidence to determine the next relevant check.

---

# Commands Used During Troubleshooting

### Check Apache

```bash
sudo systemctl status apache2
```

### Check port 443

```bash
sudo ss -ltnp | grep ':443'
```

### Check VirtualHosts

```bash
sudo apache2ctl -S
```

### Validate Apache configuration

```bash
sudo apache2ctl configtest
```

### Inspect configured certificate paths

```bash
grep -nE 'SSLCertificateFile|SSLCertificateKeyFile' \
  /etc/apache2/sites-available/default-ssl.conf
```

### Inspect certificate files

```bash
ls -lh /etc/ssl/certs/ | grep somto
```

### Test TLS

```bash
openssl s_client -connect localhost:443 -servername localhost
```

### Focus TLS output

```bash
openssl s_client -connect localhost:443 -servername localhost \
  </dev/null 2>&1 |
  grep -E 'subject=|issuer=|Protocol|Cipher|Verify return code'
```

### Inspect SAN

```bash
openssl x509 -in server-san.crt -noout -text |
  grep -A2 "Subject Alternative Name"
```

### Check certificate dates

```bash
openssl x509 -in server-san.crt -noout -dates
```

### Check Subject and Issuer

```bash
openssl x509 -in server-san.crt -noout -subject -issuer
```

### Inspect Apache journal

```bash
sudo journalctl -u apache2
```

---

# Key Takeaways

- Troubleshoot SSL/TLS problems layer by layer.
- Do not assume every HTTPS problem is a certificate problem.
- Check service state, listeners, VirtualHosts, configuration, files, TLS, trust, and identity separately.
- Know what question each diagnostic command is answering.
- Port 443 listening does not prove HTTPS is correctly configured.
- A successful TLS handshake does not prove certificate trust.
- Certificate trust does not prove hostname identity.
- A hostname mismatch does not mean TLS encryption failed.
- `apache2ctl configtest` is an important safety check before reload or restart.
- The troubleshooting lab deliberately configured a nonexistent certificate path.
- `configtest` identified the exact file and line responsible.
- Apache was not reloaded while the configuration was broken.
- The running service therefore continued using its previous working configuration.
- Inspecting `/etc/ssl/certs/` confirmed which certificate files actually existed.
- The correct SAN certificate path was restored.
- The configuration was tested again before reload.
- Apache was reloaded only after `Syntax OK`.
- Port 443 was checked after the change.
- The actual TLS endpoint was tested after the fix.
- The expected certificate, TLS version, and cipher were confirmed.
- The remaining self-signed verification warning was expected and was not confused with the original incident.
- Configuration on disk and runtime state are not always the same.
- Make controlled changes rather than changing several variables at once.
- Always verify the service after applying a fix.
- Good troubleshooting can prevent outages, not merely repair them.

---

# SSL/TLS Section Complete

This completes the SSL/TLS fundamentals section.

The learning progression was:

```text
Encryption Fundamentals
        |
        v
Symmetric Encryption
        |
        v
Asymmetric Encryption
        |
        v
Public and Private Keys
        |
        v
SSH Key Authentication
        |
        v
SSL/TLS Certificates
        |
        v
Certificate Authorities and PKI
        |
        v
Certificate Signing Requests
        |
        v
Self-Signed Certificates
        |
        v
Apache HTTPS Configuration
        |
        v
SSL/TLS Troubleshooting
```

The practical work demonstrated the complete relationship:

```text
Private Key
     |
     v
CSR
     |
     v
Certificate
     |
     v
Apache HTTPS
     |
     v
TLS Connection
     |
     v
Certificate Verification
     |
     v
Troubleshooting
```

The next repository task should be to review the generated lab files carefully before staging anything with Git.

In particular, private keys and plaintext lab secrets must not be committed.
