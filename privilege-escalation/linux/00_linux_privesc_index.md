# Linux Privilege Escalation – Master Index

## Purpose

This file provides a structured, high-speed workflow for Linux privilege escalation.

Core rules:
- Follow order (don’t jump randomly)
- Prioritize high-probability wins
- Move fast, don’t overanalyze
- If stuck → reset and continue

---

# PHASE 1: INITIAL ENUMERATION (ALWAYS FIRST)

## Basic Info

```bash
id
whoami
uname -a
cat /etc/os-release
```

---

## Users & Access

```bash
cat /etc/passwd
ls /home
```

---

## Quick Wins Scan

```bash
sudo -l
find / -perm -4000 2>/dev/null
id | grep docker
```

---

# PHASE 2: HIGH-PROBABILITY PRIVESC (DO THESE FIRST)

## 1. SUDO MISCONFIG (TOP PRIORITY)

File:
→ sudo_misconfig.md

Command:
```bash
sudo -l
```

Look for:
- NOPASSWD
- allowed binaries
- ALL privileges

---

## 2. SUID BINARIES (VERY HIGH)

File:
→ suid_sgid_binaries.md

```bash
find / -perm -4000 2>/dev/null
```

---

## 3. CREDENTIALS / SSH KEYS

File:
→ ssh_keys_and_creds.md

```bash
find / -name "id_rsa" 2>/dev/null
cat ~/.bash_history
```

---

## 4. DOCKER / LXD GROUP

File:
→ docker_lxc_groups.md

```bash
id
docker ps
lxc list
```

---

## 5. CRON JOBS

File:
→ cron_jobs.md

```bash
cat /etc/crontab
ls -la /etc/cron.*
```

---

# PHASE 3: FILE & EXECUTION ABUSE

## 6. WRITABLE FILES / PATH HIJACK

File:
→ writeable_paths_path_hijack.md

```bash
echo $PATH
find / -writable -type d 2>/dev/null
```

---

## 7. SYSTEMD SERVICES

File:
→ systemd_units.md

```bash
systemctl list-units --type=service
systemctl cat <service>
```

---

## 8. NFS NO_ROOT_SQUASH

File:
→ nfs_no_root_squash.md

```bash
showmount -e <IP>
```

---

# PHASE 4: DEEPER ENUMERATION

## 9. CONFIG FILES / SECRETS

File:
→ config_secrets.md

```bash
grep -Ri "password" / 2>/dev/null
```

---

## 10. CAPABILITIES

File:
→ capabilities.md

```bash
getcap -r / 2>/dev/null
```

---

## 11. KERNEL EXPLOITS (LAST RESORT)

File:
→ kernel_exploits.md

```bash
uname -a
searchsploit linux kernel
```

---

# PHASE 5: SERVICE ENUMERATION (CROSSOVER)

Check:
- web services
- databases
- SMB / NFS
- internal services

Files:
- web.md
- smb.md
- ftp.md
- mssql.md
- ldap.md
- rpc.md
- dns.md

---

# QUICK ENUM SCRIPT (MENTAL FLOW)

Run in order:

1. sudo -l  
2. SUID scan  
3. check credentials / SSH  
4. check groups (docker/lxd)  
5. cron jobs  
6. writable paths / PATH  
7. systemd  
8. capabilities  
9. config secrets  
10. kernel exploit (last)

---

# TIME MANAGEMENT STRATEGY

0–30 min:
- enumeration
- sudo
- SUID
- creds

30–60 min:
- cron
- docker/lxd
- writable paths

60+ min:
- deeper enumeration
- kernel only if needed

---

# RESET STRATEGY (CRITICAL)

If stuck:

- re-run enumeration
- re-check sudo
- re-check SUID
- re-check credentials
- look for missed writable files

Most failures come from:
→ missing something obvious

---

# MENTAL MODEL

You are not guessing.

You are checking:

- permissions
- misconfigurations
- trust boundaries

---

# GOLDEN RULES

- Check sudo early
- Check SUID every time
- Always search for credentials
- Always test PATH hijacking
- Always verify writable files
- Do not jump to kernel exploits early

---

# FINAL CHECKLIST

Before moving on:

- sudo checked
- SUID checked
- credentials searched
- cron reviewed
- writable paths tested
- services inspected

If any missing:
→ go back