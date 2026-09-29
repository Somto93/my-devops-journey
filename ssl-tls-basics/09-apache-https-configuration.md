# Apache HTTPS Configuration

This practical configured the Apache web server to serve HTTPS using the certificate and private key created during the SSL/TLS labs.

The exercise connected several concepts:

```text
Apache
Port 443
SSL/TLS Module
Virtual Hosts
Certificates
Private Keys
HTTPS
OpenSSL Verification
```

The final goal was:

```text
Client
   |
   | HTTPS / TLS
   v
Apache :443
   |
   +-- Certificate
   |
   +-- Private Key
```

---

# Starting Point

Apache was already installed and running.

The service was checked using:

```bash
sudo systemctl status apache2
```

Apache reported:

```text
Active: active (running)
```

Before configuring HTTPS, Apache was serving normal HTTP traffic.

The listening ports were inspected using:

```bash
sudo ss -ltnp | grep apache2
```

Initially, Apache was listening on:

```text
*:80
```

Port 80 is the standard port for:

```text
HTTP
```

The goal was to add:

```text
*:443
```

for:

```text
HTTPS
```

---

# HTTP vs HTTPS

HTTP normally uses:

```text
TCP Port 80
```

HTTPS normally uses:

```text
TCP Port 443
```

The difference is not simply the port number.

HTTPS means:

```text
HTTP
+
TLS
```

Conceptually:

```text
HTTP
  |
  v
Application Data
```

compared with:

```text
HTTPS
  |
  v
HTTP
  |
  v
TLS
  |
  v
TCP
```

TLS provides cryptographic protection for the HTTP communication.

---

# Checking the Apache SSL Module

Apache requires SSL/TLS support to provide HTTPS.

The loaded modules were checked using:

```bash
apache2ctl -M | grep ssl
```

Initially, no output was returned.

This indicated that the Apache SSL module was not currently enabled.

---

# Enabling the SSL Module

The SSL module was enabled using:

```bash
sudo a2enmod ssl
```

Apache reported that it enabled:

```text
socache_shmcb
ssl
```

The command also indicated that Apache needed to be restarted for the change to take effect.

---

# Validate Before Restarting

Before restarting Apache, the configuration was checked using:

```bash
sudo apache2ctl configtest
```

The result was:

```text
Syntax OK
```

This became an important operational habit throughout the practical:

```text
Change
   |
   v
Config Test
   |
   v
Apply Change
   |
   v
Verify
```

---

# Restarting Apache

After the configuration passed validation, Apache was restarted:

```bash
sudo systemctl restart apache2
```

The service status was then checked to confirm that Apache remained:

```text
active (running)
```

---

# Checking Port 443

After enabling SSL support, the listening sockets were inspected:

```bash
sudo ss -ltnp | grep apache2
```

Apache now showed listeners for:

```text
*:80
```

and:

```text
*:443
```

This demonstrated that Apache was listening for connections on both the normal HTTP and HTTPS ports.

However, this led to an important lesson.

---

# Listening on Port 443 Does Not Prove an SSL VirtualHost Is Configured

Seeing:

```text
*:443
```

means that Apache has a listening socket on TCP port 443.

It does not, by itself, prove that the expected SSL VirtualHost has been enabled and configured correctly.

This distinction was investigated using:

```bash
sudo apache2ctl -S
```

At that stage, the VirtualHost information showed the existing port 80 VirtualHosts but did not show the expected SSL VirtualHost.

Therefore:

```text
Port 443 Listening
```

and:

```text
SSL VirtualHost Enabled
```

are related but separate configuration questions.

---

# Apache Virtual Hosts

Apache uses VirtualHosts to determine how requests should be handled.

Conceptually:

```text
Apache
  |
  +-- :80 VirtualHost
  |
  +-- :443 SSL VirtualHost
```

An HTTPS VirtualHost normally contains SSL-related configuration such as:

```apache
SSLEngine on
SSLCertificateFile ...
SSLCertificateKeyFile ...
```

---

# Finding the Default SSL VirtualHost

The available Apache sites were inspected using:

```bash
ls -l /etc/apache2/sites-available/ | grep ssl
```

The output showed:

```text
default-ssl.conf
```

This was Apache's available default SSL VirtualHost configuration.

---

# Inspecting the SSL Certificate Configuration

The relevant SSL directives were inspected using:

```bash
grep -E 'SSLEngine|SSLCertificateFile|SSLCertificateKeyFile' \
  /etc/apache2/sites-available/default-ssl.conf
```

The configuration contained:

```apache
SSLEngine on
SSLCertificateFile /etc/ssl/certs/ssl-cert-snakeoil.pem
SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key
```

Apache therefore already had a default certificate and private key configured in the available SSL site.

---

# Apache Snakeoil Certificate

The default configuration referenced:

```text
/etc/ssl/certs/ssl-cert-snakeoil.pem
```

and:

```text
/etc/ssl/private/ssl-cert-snakeoil.key
```

These were not the certificate and key created during our lab.

The practical goal was eventually to replace these references with:

```text
Somto DevOps Lab certificate
```

and its corresponding:

```text
private key
```

---

# Checking Enabled Sites

The enabled Apache sites were inspected:

```bash
ls -l /etc/apache2/sites-enabled/
```

At that point, the enabled sites included:

```text
000-default.conf
houses.conf
oranges.conf
```

but:

```text
default-ssl.conf
```

was not enabled.

This explained why the SSL VirtualHost did not appear as expected in:

```bash
sudo apache2ctl -S
```

---

# Enabling the SSL Site

The default SSL site was enabled using:

```bash
sudo a2ensite default-ssl
```

Apache indicated that the site had been enabled and that the configuration should be reloaded.

---

# Validate the Configuration

Before applying the new configuration:

```bash
sudo apache2ctl configtest
```

was run again.

The result was:

```text
Syntax OK
```

This confirmed that Apache accepted the configuration syntax and referenced configuration at that point.

---

# Reloading Apache

Because Apache was already running, the configuration was applied using:

```bash
sudo systemctl reload apache2
```

A reload allows Apache to reread its configuration without performing a full service restart.

---

# Confirming the SSL VirtualHost

The VirtualHost configuration was inspected again:

```bash
sudo apache2ctl -S
```

This time Apache showed a port 443 VirtualHost similar to:

```text
*:443 Somto.localdomain
```

associated with:

```text
/etc/apache2/sites-enabled/default-ssl.conf
```

The important result was that Apache now had an enabled:

```text
:443 SSL VirtualHost
```

---

# First TLS Test

The HTTPS endpoint was tested using:

```bash
openssl s_client -connect localhost:443 -servername localhost
```

This command opened a TLS connection to:

```text
localhost:443
```

---

# Understanding `openssl s_client`

The command:

```bash
openssl s_client -connect localhost:443 -servername localhost
```

contains several important parts.

### `openssl s_client`

Runs OpenSSL's TLS client diagnostic functionality.

### `-connect localhost:443`

Connects to:

```text
localhost
```

on:

```text
TCP port 443
```

### `-servername localhost`

Sends:

```text
localhost
```

as the Server Name Indication, or SNI, value.

SNI helps a web server determine which TLS VirtualHost/certificate should be used when multiple names share an address.

---

# Initial Certificate Presented by Apache

The first TLS test showed a certificate with:

```text
CN=Somto.localdomain
```

This indicated that Apache was still presenting its default certificate rather than the certificate created in our lab.

The TLS connection itself successfully negotiated:

```text
TLSv1.3
```

with the cipher:

```text
TLS_AES_256_GCM_SHA384
```

This proved that HTTPS/TLS was functioning before replacing the certificate.

---

# Installing the Lab Certificate

The original self-signed lab certificate was copied into Apache's certificate area:

```bash
sudo cp server.crt /etc/ssl/certs/somto-lab.crt
```

The resulting file was:

```text
/etc/ssl/certs/somto-lab.crt
```

Its permissions allowed the certificate to be read as required.

---

# Installing the Private Key

The corresponding private key was copied using:

```bash
sudo cp server.key /etc/ssl/private/somto-lab.key
```

The resulting file was:

```text
/etc/ssl/private/somto-lab.key
```

Its permissions were restrictive:

```text
-rw-------
```

and it was owned by:

```text
root
```

This is important because the private key is sensitive.

---

# Certificate and Private-Key Locations

The configuration now had two separate types of files:

```text
Certificate:
 /etc/ssl/certs/somto-lab.crt

Private Key:
 /etc/ssl/private/somto-lab.key
```

This separation reflects their different security requirements.

The certificate is public information.

The private key must remain protected.

---

# Finding the Apache Certificate Directives

The exact configuration lines were located using:

```bash
grep -nE 'SSLCertificateFile|SSLCertificateKeyFile' \
  /etc/apache2/sites-available/default-ssl.conf
```

The relevant directives were around:

```text
Line 31
Line 32
```

They originally referenced Apache's snakeoil certificate and key.

---

# Configuring Apache to Use the Lab Certificate

The configuration was changed from:

```apache
SSLCertificateFile /etc/ssl/certs/ssl-cert-snakeoil.pem
SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key
```

to:

```apache
SSLCertificateFile /etc/ssl/certs/somto-lab.crt
SSLCertificateKeyFile /etc/ssl/private/somto-lab.key
```

This paired the lab certificate with its corresponding private key.

---

# Validate Before Applying

After editing the SSL configuration, Apache was checked again:

```bash
sudo apache2ctl configtest
```

The expected result was:

```text
Syntax OK
```

Only after successful validation was the configuration applied.

---

# Reloading Apache with the Lab Certificate

The configuration was applied using:

```bash
sudo systemctl reload apache2
```

Apache then began presenting the lab certificate for new TLS connections.

---

# Verifying the New Certificate

The TLS endpoint was tested again:

```bash
openssl s_client -connect localhost:443 -servername localhost
```

This time the certificate Subject contained:

```text
C=AU
ST=South Australia
L=Adelaide
O=Somto DevOps Lab
OU=DevOps
CN=localhost
```

This confirmed that Apache was now presenting the certificate created during the lab.

---

# Self-Signed Verification Result

OpenSSL reported:

```text
Verify return code: 18 (self-signed certificate)
```

At the same time, TLS successfully negotiated:

```text
TLSv1.3
```

with:

```text
TLS_AES_256_GCM_SHA384
```

Therefore:

```text
Apache HTTPS        → Working
TLS Encryption      → Working
Certificate         → Correct lab certificate
Automatic Trust     → Failed because self-signed
```

This was expected.

---

# Upgrading to the SAN Certificate

The original certificate did not contain Subject Alternative Names.

A newer certificate had therefore been created:

```text
server-san.crt
```

with:

```text
DNS:localhost
IP Address:127.0.0.1
```

It was copied into the system certificate directory:

```bash
sudo cp server-san.crt /etc/ssl/certs/somto-lab-san.crt
```

The installed certificate became:

```text
/etc/ssl/certs/somto-lab-san.crt
```

---

# Updating Apache to the SAN Certificate

Only the certificate path needed to change.

Apache was updated to use:

```apache
SSLCertificateFile /etc/ssl/certs/somto-lab-san.crt
```

The private-key directive remained:

```apache
SSLCertificateKeyFile /etc/ssl/private/somto-lab.key
```

The same private key could be used because the SAN certificate contained the public key corresponding to that private key.

---

# Final SSL Certificate Configuration

The relevant configuration became:

```apache
SSLEngine on

SSLCertificateFile /etc/ssl/certs/somto-lab-san.crt

SSLCertificateKeyFile /etc/ssl/private/somto-lab.key
```

This provided Apache with:

```text
TLS enabled
+
Certificate
+
Corresponding private key
```

---

# Validate and Reload

After changing the certificate path:

```bash
sudo apache2ctl configtest
```

was used to validate the configuration.

After successful validation:

```bash
sudo systemctl reload apache2
```

applied the configuration.

The operational sequence remained:

```text
Edit
  |
  v
Config Test
  |
  v
Reload
  |
  v
Verify
```

---

# Verifying the SAN Certificate

The TLS endpoint was tested:

```bash
openssl s_client -connect localhost:443 -servername localhost
```

The server presented the new certificate.

The connection again successfully negotiated:

```text
TLSv1.3
```

using:

```text
TLS_AES_256_GCM_SHA384
```

The normal verification result remained:

```text
Verify return code: 18 (self-signed certificate)
```

because changing the SAN information did not turn the certificate into a publicly trusted CA-issued certificate.

---

# Testing Trust and Hostname Verification

The certificate was then explicitly trusted for a test:

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

This confirmed:

```text
TLS connection    → Working
Certificate trust → Explicitly supplied
Hostname          → Matches SAN
```

---

# SNI vs Hostname Verification

Two options in the command serve different purposes.

### `-servername localhost`

Provides the SNI value during the TLS handshake.

Conceptually:

```text
Which server name am I requesting?
```

This can influence which VirtualHost/certificate the server presents.

### `-verify_hostname localhost`

Performs certificate identity verification.

Conceptually:

```text
Is this certificate valid for localhost?
```

They should not be treated as the same operation.

---

# Wrong Hostname Test

The certificate was deliberately tested against the wrong hostname:

```bash
openssl s_client -connect localhost:443 \
  -servername localhost \
  -verify_hostname www.example.com \
  -CAfile server-san.crt
```

OpenSSL reported:

```text
verify error:num=62:hostname mismatch
```

and:

```text
Verify return code: 62 (hostname mismatch)
```

TLS itself still negotiated successfully.

This showed:

```text
Network Connection → Working
TLS Encryption     → Working
Trust              → Supplied
Hostname Identity  → Failed
```

---

# Apache Configuration Validation

One of the most important commands in this practical was:

```bash
sudo apache2ctl configtest
```

It should be used before applying important Apache configuration changes.

A successful result:

```text
Syntax OK
```

provides evidence that Apache accepts the configuration.

It does not prove every possible runtime behaviour is correct, so verification is still required after the reload.

---

# Reload vs Restart

Two commands were used during the practical.

### Restart

```bash
sudo systemctl restart apache2
```

This stops and starts the Apache service.

### Reload

```bash
sudo systemctl reload apache2
```

This tells the running Apache service to reread its configuration.

For ordinary valid configuration changes, a reload can avoid an unnecessary full restart.

In either case, configuration should be validated first.

---

# Checking Apache Service State

Apache's service state can be inspected with:

```bash
sudo systemctl status apache2
```

This answers:

```text
Is the Apache service running?
```

It does not by itself prove:

```text
HTTPS is correctly configured
```

Additional checks are required.

---

# Checking Listening Ports

The listening sockets can be inspected using:

```bash
sudo ss -ltnp | grep apache2
```

or specifically:

```bash
sudo ss -ltnp | grep ':443'
```

This answers:

```text
Is something listening on TCP port 443?
```

Again, this does not prove that the correct certificate is being presented.

---

# Checking VirtualHosts

Apache VirtualHost configuration can be inspected using:

```bash
sudo apache2ctl -S
```

This helps answer:

```text
Which VirtualHosts does Apache currently recognize?
```

and:

```text
Is there a :443 VirtualHost?
```

---

# Checking Certificate Configuration

The certificate paths can be inspected using:

```bash
grep -nE 'SSLCertificateFile|SSLCertificateKeyFile' \
  /etc/apache2/sites-available/default-ssl.conf
```

This answers:

```text
Which certificate file is configured?
```

and:

```text
Which private key file is configured?
```

---

# Testing the Actual TLS Endpoint

The most important final test is not simply reading the configuration file.

The actual server should be contacted:

```bash
openssl s_client -connect localhost:443 -servername localhost
```

This tests the live TLS endpoint and shows information including:

```text
Presented Certificate
Subject
Issuer
Protocol
Cipher
Verification Result
```

This distinguishes:

```text
What the configuration file says
```

from:

```text
What the running server actually presents
```

---

# Focused OpenSSL Output

Instead of reading the entire `s_client` output, useful information can be filtered:

```bash
openssl s_client -connect localhost:443 -servername localhost \
  </dev/null 2>&1 |
  grep -E 'subject=|issuer=|Protocol|Cipher|Verify return code'
```

During the lab, this produced information including:

```text
subject=C=AU, ST=South Australia, L=Adelaide,
O=Somto DevOps Lab, OU=DevOps, CN=localhost

issuer=C=AU, ST=South Australia, L=Adelaide,
O=Somto DevOps Lab, OU=DevOps, CN=localhost

New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384

Protocol: TLSv1.3

Verify return code: 18 (self-signed certificate)
```

This is a useful diagnostic summary.

---

# Apache HTTPS Troubleshooting Layers

When HTTPS has a problem, avoid immediately assuming that the certificate is the cause.

Investigate the system layer by layer.

A useful sequence is:

```text
1. Is Apache running?
        |
        v
2. Is port 443 listening?
        |
        v
3. Is a :443 VirtualHost enabled?
        |
        v
4. Is Apache configuration valid?
        |
        v
5. Are certificate/key paths correct?
        |
        v
6. Can TLS negotiate?
        |
        v
7. Which certificate is presented?
        |
        v
8. Is the certificate trusted?
        |
        v
9. Does the hostname match?
```

This prevents unrelated TLS problems from being grouped together as:

```text
HTTPS is broken
```

---

# Configuration Does Not Equal Runtime

An important DevOps principle from this practical is:

```text
Configuration File
        ≠
Verified Runtime Behaviour
```

For example, a configuration file might contain:

```apache
SSLCertificateFile /some/certificate.crt
```

but the running Apache process may still be using an older configuration if the new configuration has not been successfully reloaded.

Therefore:

```text
Inspect Configuration
        |
        v
Validate
        |
        v
Apply
        |
        v
Verify Runtime
```

---

# Private-Key Security

The private key installed for Apache was:

```text
/etc/ssl/private/somto-lab.key
```

It had restrictive permissions:

```text
-rw-------
```

The private key should never be:

```text
Published
Committed to Git
Sent to clients
Placed in public web content
```

The certificate and private key serve different purposes:

```text
Certificate → Public
Private Key → Secret
```

---

# Practical Apache HTTPS Flow

The complete practical can be summarized as:

```text
Apache HTTP working on :80
          |
          v
Check SSL module
          |
          v
Enable mod_ssl
          |
          v
Config test
          |
          v
Restart Apache
          |
          v
Port 443 listening
          |
          v
Inspect VirtualHosts
          |
          v
Find default-ssl.conf
          |
          v
Inspect snakeoil cert/key
          |
          v
Enable default-ssl
          |
          v
Config test
          |
          v
Reload Apache
          |
          v
Confirm :443 VirtualHost
          |
          v
Test with openssl s_client
          |
          v
Apache presents default certificate
          |
          v
Install lab certificate + private key
          |
          v
Update Apache certificate paths
          |
          v
Config test
          |
          v
Reload
          |
          v
Verify live certificate
          |
          v
Create/install SAN certificate
          |
          v
Config test + reload
          |
          v
Verify TLS + trust + hostname
```

---

# Key Takeaways

- Apache must have SSL/TLS support enabled to serve HTTPS.
- `a2enmod ssl` enables the Apache SSL module.
- HTTPS normally uses TCP port 443.
- HTTP normally uses TCP port 80.
- Listening on port 443 does not by itself prove the expected SSL VirtualHost is enabled.
- `apache2ctl -S` shows Apache's recognized VirtualHosts.
- `default-ssl.conf` provides an Apache SSL VirtualHost configuration.
- `a2ensite default-ssl` enables that site.
- Apache's default SSL configuration initially used a snakeoil certificate.
- `SSLCertificateFile` identifies the certificate.
- `SSLCertificateKeyFile` identifies the corresponding private key.
- The lab certificate was installed under `/etc/ssl/certs/`.
- The lab private key was installed under `/etc/ssl/private/`.
- Private-key permissions should be restrictive.
- `apache2ctl configtest` should be used before applying configuration changes.
- `systemctl reload apache2` can apply valid configuration changes without a full restart.
- `openssl s_client` tests the actual TLS endpoint.
- The server successfully negotiated TLS 1.3.
- The lab connection used `TLS_AES_256_GCM_SHA384`.
- A self-signed trust error does not mean TLS encryption failed.
- SAN information was added for `localhost` and `127.0.0.1`.
- Explicit trust and hostname verification are separate checks.
- SNI and hostname verification serve different purposes.
- A configuration file should not be assumed to represent current runtime behaviour until the live service is verified.
- HTTPS troubleshooting should proceed layer by layer.

---

# Next Topic

The final section is:

```text
10-ssl-tls-troubleshooting.md
```

It documents the troubleshooting incident where Apache was deliberately configured with a nonexistent certificate path.

The incident demonstrates the workflow:

```text
Observe
   |
   v
Diagnose
   |
   v
Identify the failing layer
   |
   v
Fix
   |
   v
Validate
   |
   v
Reload
   |
   v
Verify
```

It also demonstrates why running:

```bash
sudo apache2ctl configtest
```

before a reload can prevent a configuration mistake from becoming a service outage.
