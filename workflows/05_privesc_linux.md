# 05 – Linux Privilege Escalation

## Goal

Escalate to root

---

## 1. Quick Checks

```bash
id
sudo -l
```

---

## 2. SUID

```bash
find / -perm -4000 2>/dev/null
```

---

## 3. Capabilities

```bash
getcap -r / 2>/dev/null
```

---

## 4. Cron Jobs

```bash
cat /etc/crontab
ls -la /etc/cron.*
```

---

## 5. Writable Files

```bash
find / -writable -type d 2>/dev/null
```

---

## 6. Credentials

```bash
grep -Ri password / 2>/dev/null
```

---

## 7. SSH Keys

```bash
find / -name "id_rsa" 2>/dev/null
```

---

## 8. Kernel Exploits

```bash
uname -a
```

---

## 9. Credential Reuse

Check whether credentials found elsewhere on the network can be reused locally. Test any
domain, database, or application credentials discovered during the engagement against local
services first:
```bash
# Reuse discovered credentials
ssh user@<IP>
smbclient //<IP>/share -U 'DOMAIN\user%pass'
```

Look for local credential stores:

```bash
# SSH agents and keys
ssh-add -l
ls -la ~/.ssh/
find / -name "id_rsa" -o -name "id_ed25519" 2>/dev/null

# Application/env secrets
find / -name ".env" 2>/dev/null
```

If local reuse fails, prioritize the remaining local privesc paths above.

---

## 10. Golden Rules

- sudo -l first
- SUID is high probability
- credentials > exploits
