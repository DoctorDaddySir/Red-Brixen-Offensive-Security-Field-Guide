# Target Triage

## 0. First 5 Minutes (DO NOT SKIP)

- Run full TCP scan
- Identify open ports/services
- Take initial notes
- Start thinking: Linux / Windows / Web / AD?

---

## 1. Identify Target Type

### Linux Indicators
- SSH (22)
- Apache/Nginx
- Typical Linux paths (/etc, /var)

→ Go to:
- Enumeration → web.md
- Linux privesc checklist

---

### Windows Indicators
- SMB (445)
- RPC (135)
- WinRM (5985/5986)
- RDP (3389)

→ Go to:
- smb.md
- ldap.md / rpc.md
- Windows privesc checklist

---

### Active Directory Indicators
- Domain name present
- Kerberos (88)
- LDAP (389)
- SMB + domain users

→ Go to:
- ad_enum.md
- BloodHound
- AD attack flow

---

### Web-Heavy Target
- HTTP/HTTPS dominant
- Login pages
- APIs

→ Go to:
- web.md
- dirsearch / gobuster
- vuln classes (LFI, upload, sqli)

---

## 2. Port-Based Decision Tree

### 21 (FTP)
- Anonymous login?
- Writable directories?
- Download files

---

### 22 (SSH)
- Valid usernames?
- Password reuse?
- Keys available?

---

### 80 / 443 (Web)
- Directory brute force
- Check technologies
- Test:
  - LFI
  - File upload
  - Command injection
  - Auth bypass

---

### 139 / 445 (SMB)
- `smbclient -L`
- Null sessions?
- Shares?
- Writable paths?

---

### 88 / 389 (Kerberos / LDAP)
- Enumerate users
- AS-REP roasting
- Kerberoasting

---

### 3306 / 1433 (Databases)
- Default creds
- Local access only?
- Extract creds

---

### 5985 / 5986 (WinRM)
- Try creds immediately
- Evil-WinRM

---

### 3389 (RDP)
- Try creds
- Check for low-priv access

---

## 3. Initial Enumeration Priority

Always prioritize:

1. **Web (if present)**
2. **SMB / Shares**
3. **Credential reuse across services**
4. **AD enumeration (if domain)**

---

## 4. Quick Win Checklist

Look for:

- Default credentials
- Config files with creds
- Backup files
- Writable shares
- File upload → RCE
- Password reuse
- Scripts with hardcoded creds

---

## 5. When You Get a Shell

Immediately:

- `whoami`
- `hostname`
- `ip a` / `ipconfig`
- Check users
- Check groups
- Save proof

Then:

→ Go to privesc checklist immediately

---

## 6. If Stuck (Critical Reset)

DO NOT SPIRAL

Do this instead:

- Re-enumerate ALL services
- Try creds on ALL services
- Check:
  - New ports from inside
  - Config files
  - Scripts
  - Scheduled tasks / cron
- Look for:
  - Internal-only services
  - Alternate attack paths

---

## 7. Time Management Rule

- 20–30 min stuck → switch vector
- 60 min stuck → switch target (if exam allows)
- Come back later with fresh perspective

---

## 8. Mental Model

- Enumeration > Exploitation
- Credentials = keys to everything
- Misconfigurations > exploits
- Simplicity wins

---

## 9. Golden Rule

If you feel lost:

→ You missed something in enumeration