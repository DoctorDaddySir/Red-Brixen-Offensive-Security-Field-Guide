# Linux Privilege Escalation – Config & Secrets

## Purpose

This file provides a structured workflow for discovering credentials and sensitive data in configuration files.

Core rules:

* Credentials are often stored in plaintext
* Config files = fastest path to privilege escalation
* Always search broadly, then refine
* Reuse credentials across all services

---

## 0. Fast Keyword Search (CRITICAL FIRST STEP)

```bash
grep -Ri "pass" / 2>/dev/null
grep -Ri "password" / 2>/dev/null
grep -Ri "user" / 2>/dev/null
grep -Ri "key" / 2>/dev/null
grep -Ri "secret" / 2>/dev/null
```

---

## 1. High-Value Locations

Check:

```text
/home/
/var/www/
/etc/
/opt/
/srv/
/tmp/
```

---

## 2. Common Config Files

Look for:

```text
.env
config.php
settings.py
web.config
database.yml
wp-config.php
```

---

## 3. Web Application Configs

Common paths:

```bash
/var/www/html/
/var/www/
/opt/web/
```

Extract:

* DB credentials
* API keys
* admin credentials

---

## 4. Database Credentials

Look for:

```text
DB_USER
DB_PASS
DB_PASSWORD
DB_HOST
```

Test:

* SSH
* SMB
* WinRM

---

## 5. Backup Files (HIGH VALUE)

Search:

```bash
find / -name "*.bak" 2>/dev/null
find / -name "*.old" 2>/dev/null
find / -name "*.zip" 2>/dev/null
```

---

## 6. History Files

```bash
cat ~/.bash_history
cat ~/.mysql_history
cat ~/.nano_history
```

Look for:

* commands with passwords
* connections

---

## 7. Environment Variables

```bash
env
```

Look for:

* tokens
* passwords
* keys

---

## 8. SSH Keys

Search:

```bash
find / -name "id_rsa" 2>/dev/null
```

Use:

```bash
ssh -i id_rsa user@localhost
```

---

## 9. Cron Jobs & Scripts

Check:

```bash
cat /etc/crontab
```

Look for:

* scripts with credentials
* writable scripts

---

## 10. Application Logs

```bash
grep -Ri "pass" /var/log 2>/dev/null
```

---

## 11. Sudo Config

```bash
cat /etc/sudoers
```

Look for:

* stored credentials
* misconfigurations

---

## 12. Credential Reuse (CRITICAL)

Test everything on:

```bash
su user
ssh user@localhost
```

And:

```bash
crackmapexec smb <IP> -u user -p pass
crackmapexec winrm <IP> -u user -p pass
```

---

## 13. Automated Search (Optional)

```bash
linpeas.sh
```

---

## 14. Pivot Opportunities

Config files can reveal:

* credentials
* internal services
* file paths
* database access

---

## 15. If Stuck

RESET:

* search different directories
* refine grep terms
* check backups again
* revisit web configs

---

## 16. Mental Model

* Files = secrets
* Secrets = access
* Access = escalation

---

## 17. Golden Rules

* Always grep early
* Always check web configs
* Always check backups
* Always reuse credentials
