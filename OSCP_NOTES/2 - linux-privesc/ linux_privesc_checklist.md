# Linux Privilege Escalation Checklist

## 0. Immediate Context (DO THIS FIRST)

```bash
id
whoami
hostname
uname -a
cat /etc/os-release
ip a
```

* Identify user
* Identify groups
* Identify OS + kernel version

---

## 1. Quick Wins (ALWAYS CHECK FIRST)

### Sudo permissions

```bash
sudo -l
```

Look for:

* NOPASSWD
* Misconfigured binaries

---

### SUID binaries

```bash
find / -perm -4000 2>/dev/null
```

---

### Writable files

```bash
find / -writable -type f 2>/dev/null
```

---

### Writable directories

```bash
find / -writable -type d 2>/dev/null
```

---

## 2. Credential Hunting

### Search for passwords

```bash
grep -Ri "password" / 2>/dev/null
```

### Check common locations

* /home/
* /var/www/
* /opt/
* /etc/
* /backup/

---

### Check config files

```bash
cat /etc/passwd
cat /etc/shadow
```

---

### SSH keys

```bash
ls -la ~/.ssh/
```

---

## 3. SUDO Exploitation

```bash
sudo -l
```

If allowed commands:

* Check GTFOBins
* Look for:

  * editors (vim, nano)
  * interpreters (python, perl)
  * system tools (tar, find)

---

## 4. SUID Exploitation

```bash
find / -perm -4000 2>/dev/null
```

Check each binary against:

* GTFOBins

Look for:

* uncommon binaries
* custom binaries

---

## 5. Capabilities

```bash
getcap -r / 2>/dev/null
```

Look for:

* cap_setuid
* cap_setgid

---

## 6. Cron Jobs

```bash
crontab -l
ls -la /etc/cron*
```

Check:

* scripts executed by root
* writable scripts

---

## 7. PATH Abuse

```bash
echo $PATH
```

Look for:

* writable directories in PATH

---

## 8. Running Processes

```bash
ps aux
```

Look for:

* root processes
* custom scripts

---

## 9. Network Enumeration

```bash
netstat -tulnp
```

Look for:

* internal services
* localhost-only ports

---

## 10. NFS / Mounts

```bash
mount
cat /etc/fstab
```

Look for:

* misconfigured mounts
* no_root_squash

---

## 11. Writable System Files

Check:

* /etc/passwd
* /etc/shadow

```bash
ls -l /etc/passwd
```

---

## 12. Kernel Exploits (LAST RESORT)

```bash
uname -a
```

Check:

* exploit-db
* searchsploit

Only if:

* no other vectors exist

---

## 13. File Transfers

Check tools available:

```bash
which wget
which curl
which nc
```

---

## 14. Automated Enumeration

Run:

* linpeas

```bash
./linpeas.sh
```

Review manually.

---

## 15. Always Think

* Can I write to something root executes?
* Can I hijack a binary?
* Can I reuse credentials?
* Can I escalate via sudo/SUID/capabilities?

---

## 16. If Stuck (RESET)

* Re-run enumeration
* Re-check writable paths
* Re-check cron jobs
* Re-check sudo
* Re-check credentials
* Re-check processes

---

## 17. Proof

```bash
id
```

Capture:

* proof.txt
* user.txt
