# DNS and Name Resolution

This section documents what I learned about hostname resolution, `/etc/hosts`, DNS, `/etc/resolv.conf`, `/etc/nsswitch.conf`, search domains, DNS record types, and DNS troubleshooting.

## 1. What Is Name Resolution?

Humans normally prefer names such as:

```text
app1.local
google.com
```

rather than remembering IP addresses.

Computers ultimately need an IP address to communicate with a destination.

Name resolution is the process of translating a name into an IP address.

A simple way I think about it is:

```text
Hostname
   ↓
Name Resolution
   ↓
IP Address
```

For example, in my networking lab:

```text
app1.local
      ↓
172.23.210.163
```

Once the system determines the IP address, networking can continue towards that destination.

---

## 2. `/etc/hosts`

Linux can resolve names using the local:

```text
/etc/hosts
```

file.

In my lab, I added:

```text
172.23.210.163 app1.local
```

This created a local mapping:

```text
app1.local → 172.23.210.163
```

I could then run:

```bash
getent hosts app1.local
```

and receive:

```text
172.23.210.163 app1.local
```

This allowed me to access my Flask application using:

```bash
curl http://app1.local:5000
```

instead of:

```bash
curl http://172.23.210.163:5000
```

---

## 3. `/etc/hosts` Is Not a DNS Server

One distinction I learned is that `/etc/hosts` and DNS can both help resolve names, but they are not the same thing.

`/etc/hosts` provides local static mappings.

For example:

```text
172.23.210.163 app1.local
```

DNS provides a system for resolving names using DNS servers.

Therefore:

```text
/etc/hosts
→ Local static hostname mapping

DNS
→ Name resolution using DNS infrastructure
```

---

## 4. DNS

DNS stands for:

```text
Domain Name System
```

DNS helps translate domain names into information such as IP addresses.

For example:

```text
example.com
     ↓
DNS lookup
     ↓
IP address
```

An important lesson for me was that DNS does not carry the application's actual HTTP traffic.

DNS helps determine the destination.

After resolution, the system still needs to communicate with that destination using the appropriate networking path and service port.

So:

```text
DNS
 ↓
Find destination IP
 ↓
Routing / Reachability
 ↓
Port
 ↓
Application
```

---

## 5. `/etc/resolv.conf`

Linux uses resolver configuration to determine which DNS server or servers should be queried.

I can inspect this using:

```bash
cat /etc/resolv.conf
```

The file can contain entries such as:

```text
nameserver 8.8.8.8
```

The `nameserver` entry identifies a DNS resolver that can be queried.

I can inspect nameserver entries with:

```bash
grep nameserver /etc/resolv.conf
```

One important lesson is that:

```text
/etc/resolv.conf
```

does not contain all DNS records.

Instead, it provides resolver configuration, including which DNS server the system should use.

---

## 6. `/etc/nsswitch.conf`

Linux can use more than one source for name resolution.

The configuration file:

```text
/etc/nsswitch.conf
```

controls which sources are consulted and their order.

A simplified example is:

```text
hosts: files dns
```

This means hostname resolution can consult:

```text
files
 ↓
Local files such as /etc/hosts

dns
 ↓
DNS
```

This helped me understand why an `/etc/hosts` entry can affect the result even though DNS is also configured.

---

## 7. `getent hosts`

I used:

```bash
getent hosts app1.local
```

frequently during my lab.

This command helped answer:

> What address does my system currently resolve this hostname to?

For example:

```text
172.23.210.163 app1.local
```

showed that the name resolved to the expected address.

This was especially useful because I could compare the result with:

```bash
ip addr
```

For example:

```text
getent hosts app1.local
        ↓
172.23.210.163

ip addr
        ↓
eth0 = 172.23.210.163
```

The two matched.

---

## 8. Name Resolution Failure

Before configuring `app1.local`, I tried:

```bash
getent hosts app1.local
```

and received no useful result.

Then:

```bash
curl http://app1.local:5000
```

returned an error similar to:

```text
Could not resolve host: app1.local
```

This was an important troubleshooting lesson.

The connection had not yet reached the stage where port `5000` or Flask was the main issue.

The system first needed to resolve:

```text
app1.local
```

to an IP address.

So:

```text
Could not resolve host
        ↓
Investigate name resolution
```

rather than immediately investigating the application port.

---

## 9. My Wrong-IP Incident

I deliberately created a name-resolution problem by changing the `/etc/hosts` mapping from:

```text
172.23.210.163 app1.local
```

to:

```text
172.23.210.200 app1.local
```

Then I ran:

```bash
curl --connect-timeout 3 http://app1.local:5000
```

and the request timed out.

At first, this could look like a general network failure.

Instead of immediately changing the application, I investigated.

### Step 1 — Check name resolution

I ran:

```bash
getent hosts app1.local
```

and found:

```text
172.23.210.200 app1.local
```

Name resolution was technically succeeding.

However, it was returning the wrong destination for my application.

This taught me an important lesson:

> Successful name resolution does not necessarily mean that the resolved IP address is correct.

---

## 10. Comparing the Resolved IP With My Interface

I then used:

```bash
ip addr
```

and saw that my `eth0` address was:

```text
172.23.210.163
```

Now I had:

```text
app1.local → 172.23.210.200

eth0       → 172.23.210.163
```

The values did not match.

This gave me evidence that the hostname was pointing to the wrong destination.

---

## 11. Checking Routing Before Blaming Routing

I also examined:

```bash
ip route
```

My system had:

```text
172.23.208.0/20 dev eth0
```

The incorrect destination:

```text
172.23.210.200
```

was still within that directly connected network.

Therefore, Linux still knew how to attempt to reach that IP.

The main problem was the incorrect hostname-to-IP mapping, not the absence of a route.

---

## 12. Fixing the Mapping

I corrected `/etc/hosts` so that:

```text
app1.local
```

again pointed to:

```text
172.23.210.163
```

Then I verified:

```bash
getent hosts app1.local
```

and tested:

```bash
curl --connect-timeout 3 http://app1.local:5000
```

I also checked the health endpoint:

```bash
curl http://app1.local:5000/health
```

The application returned:

```json
{"status":"healthy"}
```

This completed the troubleshooting cycle:

```text
Detect
  ↓
Investigate
  ↓
Identify root cause
  ↓
Fix
  ↓
Verify
```

---

## 13. DNS Search Domains

I also learned about DNS search domains.

A search domain can allow a shorter hostname to be expanded during name resolution.

For example, instead of always entering a fully qualified name, a resolver may append a configured search domain to a short name.

Search-domain configuration can appear in:

```text
/etc/resolv.conf
```

I can inspect it using:

```bash
grep '^search' /etc/resolv.conf
```

The general idea is:

```text
Short name
   ↓
Search domain appended
   ↓
Longer domain name
   ↓
DNS lookup
```

This can be useful in environments where systems regularly communicate using internal hostnames.

---

## 14. DNS Record Types

I learned about several common DNS record types.

### A Record

An `A` record maps a name to an IPv4 address.

```text
Name
 ↓
IPv4 address
```

Example concept:

```text
app.example.com → 192.0.2.10
```

### AAAA Record

An `AAAA` record maps a name to an IPv6 address.

```text
Name
 ↓
IPv6 address
```

### CNAME Record

A `CNAME` record provides an alias from one name to another name.

Conceptually:

```text
Alias
  ↓
Canonical hostname
```

These record types helped me understand that DNS can store different kinds of information and does more than simply provide IPv4 addresses.

---

## 15. `nslookup`

I can use:

```bash
nslookup <hostname>
```

to query DNS information.

For example:

```bash
nslookup google.com
```

can help me inspect DNS resolution for that name.

This is useful when I specifically want to investigate DNS.

---

## 16. `dig`

Another DNS troubleshooting tool is:

```bash
dig
```

For example:

```bash
dig google.com
```

`dig` provides more detailed DNS query information.

I can use it when I need to investigate DNS responses and records in more detail.

---

## 17. `getent` vs `nslookup` / `dig`

An important distinction I learned is that these tools do not necessarily answer exactly the same troubleshooting question.

### `getent`

```bash
getent hosts app1.local
```

helps me understand what the system's configured name-resolution mechanism returns.

This is useful when `/etc/hosts`, DNS, and system resolution configuration may all be relevant.

### `nslookup` and `dig`

```bash
nslookup example.com
dig example.com
```

are useful for investigating DNS queries and DNS records specifically.

So during troubleshooting, I should choose the tool based on the question I am trying to answer.

---

## 18. DNS vs Routing

I initially needed to separate DNS and routing clearly.

DNS answers:

> What IP address belongs to this name?

Routing answers:

> How should packets reach that IP address?

For example:

```text
app1.local
     ↓
Name resolution
     ↓
172.23.210.163
     ↓
Routing decision
     ↓
Destination
```

If name resolution returns the wrong IP, routing may work perfectly but send traffic towards the wrong destination.

---

## 19. DNS vs Ports

I also learned not to confuse DNS problems with port problems.

Consider:

```bash
curl http://app1.local:5000
```

There are several stages:

```text
app1.local
   ↓
Resolve hostname
   ↓
Destination IP
   ↓
Connect to TCP port 5000
```

If I receive:

```text
Could not resolve host
```

I should investigate name resolution.

If the hostname resolves successfully but the connection to port `5000` fails, I should continue investigating the networking/service path rather than assuming DNS is still the problem.

---

## 20. My Name-Resolution Troubleshooting Flow

When I suspect a hostname problem, I can work through:

```text
1. What does the hostname resolve to?
              ↓
   getent hosts app1.local

2. Is that the destination I expect?
              ↓
   Compare with ip addr or known service IP

3. What local resolution configuration exists?
              ↓
   /etc/hosts
   /etc/nsswitch.conf

4. What resolver configuration exists?
              ↓
   /etc/resolv.conf

5. If investigating DNS specifically:
              ↓
   nslookup
   dig

6. After correcting the problem:
              ↓
   getent hosts

7. Verify the application:
              ↓
   curl
```

---

## Commands I Practised

| Command | Purpose |
|---|---|
| `getent hosts <hostname>` | Check how the system resolves a hostname |
| `cat /etc/hosts` | View local static hostname mappings |
| `cat /etc/resolv.conf` | View resolver configuration |
| `grep nameserver /etc/resolv.conf` | View configured DNS resolver entries |
| `grep '^search' /etc/resolv.conf` | View configured search domains |
| `cat /etc/nsswitch.conf` | Inspect name-service lookup configuration |
| `nslookup <hostname>` | Query DNS information |
| `dig <hostname>` | Perform a detailed DNS query |
| `ip addr` | Compare a resolved address with local interface addresses |
| `ip route` | Determine how Linux would route towards a destination |
| `curl <URL>` | Verify application connectivity after resolution |

---

## Key Lessons

From learning DNS and name resolution, I learned that:

- Hostnames must be resolved to addresses before applications can communicate using those names.
- `/etc/hosts` provides local static hostname mappings.
- `/etc/hosts` is not itself a DNS server.
- `/etc/resolv.conf` contains resolver configuration such as nameservers and search domains.
- `/etc/nsswitch.conf` influences which name-resolution sources the system uses and their order.
- `getent hosts` is useful for checking the result of the system's name-resolution process.
- `nslookup` and `dig` are useful when investigating DNS specifically.
- An `A` record maps a name to an IPv4 address.
- An `AAAA` record maps a name to an IPv6 address.
- A `CNAME` record provides an alias to another hostname.
- Successful resolution can still return the wrong destination.
- DNS/name resolution and routing are separate concepts.
- DNS/name resolution and application ports are also separate concepts.

My biggest troubleshooting lesson was:

> Do not stop at "the hostname resolves." Always check whether it resolves to the destination I actually expect.
