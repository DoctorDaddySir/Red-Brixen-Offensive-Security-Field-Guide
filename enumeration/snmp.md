# SNMP Enumeration & Exploitation

## Purpose

This file provides a structured workflow for enumerating SNMP services and extracting system, user, and network information.

Core rules:

* SNMP can expose massive system data
* Always try default community strings
* Dump everything and parse later
* Use SNMP to discover users and services

---

## 0. Identify SNMP

Common port:

* 161 (UDP)

Confirm:

```bash
nmap -sU -p 161 <IP>
```

Service detection:

```bash
nmap -sU -p 161 -sV <IP>
```

---

## 1. Test Community Strings

Common:

* public
* private

```bash
snmpwalk -v2c -c public <IP>
```

```bash
snmpwalk -v2c -c private <IP>
```

If successful:
→ full data access

---

## 2. Human-Readable Enumeration (FAST INSIGHT)

```bash
snmp-check <IP> -c public
```

This provides:

* system info
* users
* network info
* running services

Use this FIRST for quick understanding, then dump everything.

---

## 3. Full SNMP Dump (CRITICAL)

```bash
snmpwalk -v2c -c public <IP> > snmp_dump.txt
```

---

## 4. System Information

```bash
snmpwalk -v2c -c public <IP> 1.3.6.1.2.1.1
```

Extract:

* hostname
* OS version
* system description

---

## 5. User Enumeration (HIGH VALUE)

```bash
snmpwalk -v2c -c public <IP> 1.3.6.1.4.1.77.1.2.25
```

Save:

* usernames → users.txt

---

## 6. Running Processes

```bash
snmpwalk -v2c -c public <IP> 1.3.6.1.2.1.25.4.2.1.2
```

Look for:

* services
* scripts
* unusual processes

---

## 7. Installed Software

```bash
snmpwalk -v2c -c public <IP> 1.3.6.1.2.1.25.6.3.1.2
```

---

## 8. Network Interfaces

```bash
snmpwalk -v2c -c public <IP> 1.3.6.1.2.1.2.2.1.2
```

---

## 9. Credential Discovery

Search dump:

```bash
grep -i "pass" snmp_dump.txt
grep -i "user" snmp_dump.txt
```

---

## 10. Combine with Other Services

SNMP findings → feed into:

* SMB
* SSH
* FTP
* LDAP
* MSSQL

---

## 11. Brute Force Community Strings

```bash
onesixtyone -c community.txt <IP>
```

---

## 12. Pivot Opportunities

SNMP can reveal:

* usernames
* running services
* internal structure
* software versions

---

## 13. If Default Strings Fail

Try:

* brute forcing
* custom wordlists
* alternate SNMP versions

---

## 14. If Stuck

RESET:

* dump again
* search for credentials
* extract usernames
* map services

---

## 15. Mental Model

* SNMP = system visibility
* Data = attack surface
* Users + services = entry points

---

## 16. Golden Rules

* Always try public/private
* Always run snmp-check for quick insight
* Always dump everything
* Always extract usernames
* Always search for credentials
