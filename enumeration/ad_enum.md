# Active Directory Enumeration

## Purpose

This file provides a structured, command-driven workflow for enumerating Active Directory environments.

Core rules:

* Extract as much data as possible early
* Save outputs for reuse
* Feed all results into attack flow and credential testing

---

## 0. Pre-Checks (CRITICAL)

### DNS

```bash
nslookup domain.local <DC_IP>
```

### Hosts file (if needed)

```bash
echo "<IP> dc.domain.local dc" | sudo tee -a /etc/hosts
```

### Time sync (Kerberos requirement)

```bash
sudo ntpdate <DC_IP>
```

If Kerberos fails:

* check DNS
* check time
* check domain spelling

---

## 1. Initial Nmap Scan

```bash
nmap -sC -sV -Pn -p 53,88,135,139,389,445,464,593,636,3268,5985 <IP>
```

```bash
nmap -Pn -p- --min-rate 1000 <IP>
```

Capture:

* domain name
* hostnames
* services

---

## 2. SMB Enumeration

Anonymous:

```bash
smbclient -L //<IP> -N
smbmap -H <IP>
```

With creds:

```bash
smbclient -L //<IP> -U 'DOMAIN\user%pass'
smbmap -H <IP> -u user -p pass -d DOMAIN
crackmapexec smb <IP> -u user -p pass -d DOMAIN
```

Dump shares:

```bash
smbclient //<IP>/share -U user
```

Look for:

* SYSVOL
* NETLOGON
* scripts
* credentials
* backups

---

## 3. LDAP Enumeration

Get base:

```bash
ldapsearch -x -H ldap://<IP> -s base namingcontexts
```

Full dump:

```bash
ldapsearch -x -H ldap://<IP> -b "DC=domain,DC=local"
```

With creds:

```bash
ldapsearch -x -H ldap://<IP> -D 'DOMAIN\user' -w 'pass' -b "DC=domain,DC=local"
```

Extract:

* users
* groups
* SPNs
* descriptions

---

## 4. CrackMapExec Enumeration

```bash
crackmapexec smb <targets.txt> -u user -p pass -d DOMAIN
```

```bash
crackmapexec ldap <IP> -u user -p pass -d DOMAIN
```

```bash
crackmapexec winrm <targets.txt> -u user -p pass -d DOMAIN
```

---

## 5. User Enumeration

Sources:

* LDAP
* RPC
* SMB files
* BloodHound

Save:

```text
users.txt
```

---

## 6. Kerberos Enumeration

### AS-REP Roast

```bash
GetNPUsers.py DOMAIN.LOCAL/ -dc-ip <IP> -usersfile users.txt -no-pass
```

---

### Kerberoast

```bash
GetUserSPNs.py DOMAIN.LOCAL/user:pass -dc-ip <IP> -request
```

---

## 7. BloodHound Collection

```bash
bloodhound-python -u user -p pass -ns <DC_IP> -d domain.local -c All
```

Upload to BloodHound.

---

## 8. What to Extract (CHECKLIST)

### Users

* usernames
* descriptions
* admin accounts

### Groups

* Domain Admins
* privileged groups

### Computers

* hostnames
* roles

### Shares

* readable
* writable

### Credentials

* passwords
* hashes
* tickets

### SPNs

* service accounts

---

## 9. Credential Validation Loop

Test creds on:

```bash
crackmapexec smb <targets.txt> -u user -p pass -d DOMAIN
crackmapexec winrm <targets.txt> -u user -p pass -d DOMAIN
crackmapexec rdp <targets.txt> -u use
```
