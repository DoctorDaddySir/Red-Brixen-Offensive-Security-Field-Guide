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

## 9. Golden Rules

- sudo -l first
- SUID is high probability
- credentials > exploits