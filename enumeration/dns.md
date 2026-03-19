# DNS Enumeration & Exploitation

## Purpose

This file provides a structured workflow for enumerating DNS services and extracting domain, host, and network information.

Core rules:

* DNS reveals the network structure
* Always attempt zone transfer
* Use DNS to expand attack surface
* Feed results into SMB, LDAP, and AD enumeration

---

## 0. Identify DNS

Common port:

* 53 (TCP/UDP)

Confirm:

```bash id="a1x9u3"
nmap -p 53 -sV <IP>
```

---

## 1. Basic Queries

### Domain lookup

```bash id="n7y2c5"
nslookup <IP>
```

### Reverse lookup

```bash id="p3v8m1"
nslookup <IP>
```

### Specific domain

```bash id="c4k2r6"
nslookup domain.local <IP>
```

---

## 2. Host Discovery

```bash id="f8t1b9"
host <IP>
```

```bash id="z6x4j2"
dig <IP>
```

---

## 3. Zone Transfer (CRITICAL CHECK)

```bash id="m9q3w7"
dig axfr domain.local @<IP>
```

If successful:
→ full domain dump

Extract:

* hostnames
* internal services
* domain structure

---

## 4. Subdomain Enumeration

### Using wordlist

```bash id="u2k5z8"
gobuster dns -d domain.local -w wordlist.txt
```

```bash id="q8n3l6"
ffuf -u http://FUZZ.domain.local -w wordlist.txt
```

---

## 5. Reverse DNS Sweep

```bash id="r1j7h4"
for i in {1..254}; do host 192.168.1.$i; done
```

Look for:

* hostnames
* domain naming patterns

---

## 6. Record Types

### A Records

```bash id="s3c9p2"
dig domain.local A
```

### MX Records

```bash id="x5w8v1"
dig domain.local MX
```

### NS Records

```bash id="d2k4t7"
dig domain.local NS
```

### TXT Records

```bash id="y7m1q8"
dig domain.local TXT
```

Look for:

* mail servers
* domain controllers
* service endpoints
* configuration info

---

## 7. AD-Specific DNS

Look for:

* _ldap._tcp.domain.local
* _kerberos._tcp.domain.local

```bash id="b4n8c6"
dig _ldap._tcp.domain.local SRV
```

```bash id="k9z2f5"
dig _kerberos._tcp.domain.local SRV
```

These reveal:

* domain controllers
* authentication services

---

## 8. DNS + AD Integration

Use DNS to:

* identify DC
* identify internal hosts
* map network

Feed into:

* LDAP
* SMB
* Kerberos attacks

---

## 9. Pivot Opportunities

DNS may reveal:

* internal hostnames
* hidden services
* alternate domains
* staging servers

---

## 10. If Zone Transfer Fails

Try:

* other DNS servers
* subdomain brute force
* reverse lookups

---

## 11. If Stuck

RESET:

* rerun reverse sweep
* enumerate subdomains
* check SRV records
* verify domain name

---

## 12. Mental Model

* DNS = map of the network
* Hostnames = targets
* Domain = attack scope

---

## 13. Golden Rules

* Always attempt zone transfer
* Always enumerate subdomains
* Always extract hostnames
* Always feed into other services
