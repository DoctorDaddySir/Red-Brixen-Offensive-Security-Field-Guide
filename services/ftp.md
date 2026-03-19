# FTP Enumeration & Exploitation

## Purpose

This file provides a structured workflow for enumerating FTP services and identifying access, credentials, and exploitation opportunities.

Core rules:

* Always try anonymous login first
* FTP often exposes files and credentials
* Writable FTP can lead directly to RCE
* Always check where files are stored

---

## 0. Identify FTP

Common port:

* 21

Confirm:

```bash id="f9x2k3"
nmap -p 21 -sV <IP>
```

---

## 1. Anonymous Login (FIRST STEP)

```bash id="x8k4j1"
ftp <IP>
```

Login:

```
username: anonymous
password: anonymous
```

If successful:
→ high-value access

---

## 2. Basic Enumeration

Inside FTP:

```bash id="z7p3l6"
ls
pwd
cd <dir>
```

Download files:

```bash id="q5r2v8"
get file
mget *
```

---

## 3. What to Look For (CRITICAL)

### Credentials

* config files
* scripts
* backups
* .txt / .ini / .xml

### Sensitive Files

* database dumps
* source code
* deployment files

### Keys

* SSH keys
* API keys

---

## 4. Writable Directories (HIGH VALUE)

Test:

```bash id="y3m9t2"
put test.txt
```

If successful:
→ writable FTP

---

## 5. FTP → Web Exploitation

If web server exists:

* Upload:

```bash id="p4k7n1"
put shell.php
```

Access:

```bash id="h2q8r6"
http://<IP>/shell.php
```

---

## 6. FTP → Reverse Shell

Upload:

* webshell
* reverse shell script

Trigger via:

* browser
* command execution

---

## 7. Credential Reuse

Test FTP creds on:

```bash id="d6v3c9"
crackmapexec smb <IP> -u user -p pass
crackmapexec winrm <IP> -u user -p pass
```

Also test:

* SSH
* web login
* database

---

## 8. Brute Force (If Needed)

```bash id="m1k8z5"
hydra -L users.txt -P passwords.txt ftp://<IP>
```

---

## 9. Anonymous Write (Rare but Critical)

If anonymous write allowed:

* upload payload
* check execution paths

---

## 10. Check File Paths

Try to determine:

* where FTP root maps to
* web root overlap

Common paths:

* /var/www/html
* /htdocs
* /www

---

## 11. FTP Bounce (Rare)

Check:

* misconfigured FTP for scanning

(Not common in OSCP)

---

## 12. Pivot Opportunities

FTP can reveal:

* credentials
* internal scripts
* config files
* hostnames

---

## 13. If Anonymous Fails

Try:

* known creds
* password spraying
* brute force

---

## 14. If Stuck

RESET:

* download ALL files
* search for credentials
* test uploads again
* check web integration

---

## 15. Mental Model

* FTP = file access
* Files = credentials or execution
* Write access = potential RCE

---

## 16. Golden Rules

* Always try anonymous
* Always download everything
* Always test write access
* Always check web integration
