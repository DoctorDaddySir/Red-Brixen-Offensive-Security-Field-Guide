# Exam Workflow (OSCP+)

## Purpose

This file defines the exact process to follow during the exam.

If you feel lost → return here.

---

## 0. Global Rules

* Enumeration > Exploitation
* Credentials are priority #1
* Misconfigurations > exploits
* Always document everything
* Always test credentials across all services

---

## 1. Start of Exam

### Setup

* Start notes for each target
* Open:

  * target worksheet
  * quick commands
  * privesc checklist
* Start logging commands

---

### Initial Scans (ALL TARGETS)

```bash id="b6x8u4"
nmap -p- -T4 <IP>
```

```bash id="xk8y2r"
nmap -sC -sV -p <PORTS> <IP>
```

---

## 2. Target Triage

For each host:

* Identify:

  * Linux / Windows / AD / Web
* Choose initial attack path:

  * Web first if present
  * SMB if Windows
  * AD if domain present

---

## 3. Enumeration Phase (CRITICAL)

### Always:

* Enumerate ALL services
* Take structured notes (worksheet)
* Do NOT exploit immediately

---

### Priority Order

1. Web
2. SMB / Shares
3. Credentials
4. AD enumeration

---

## 4. Foothold Phase

Once access is gained:

### Immediately:

```bash id="jq5s3r"
whoami
hostname
ip a
```

or

```powershell id="m4z7qa"
whoami
hostname
ipconfig
```

* Save proof
* Identify context

---

## 5. Stabilize Shell

* Upgrade TTY (Linux)
* Ensure reliable access
* Prepare for file transfer

---

## 6. Privilege Escalation

### Immediately run checklist:

* Windows → windows_privesc_checklist.md
* Linux → linux_privesc_checklist.md

### Do NOT:

* Skip steps
* Assume something was checked

---

## 7. Credential Reuse Loop

Every time you find creds:

* Test on:

  * SMB
  * WinRM
  * RDP
  * SSH
  * LDAP
  * Web logins

This is one of the highest success paths.

---

## 8. Pivot / Lateral Movement

If multiple hosts:

* Check:

  * internal services
  * new hosts
  * reused credentials

---

## 9. Active Directory Flow

If AD present:

* Follow ad_attack_flow.md
* Focus on:

  * creds
  * Kerberos attacks
  * BloodHound paths

---

## 10. Time Management

* 20–30 min stuck → switch approach
* 60 min stuck → switch target
* Return later with fresh perspective

---

## 11. If Stuck (RESET)

* Re-enumerate everything
* Re-check credentials
* Re-check services
* Re-check writable files
* Revisit assumptions

---

## 12. Documentation Discipline

Always record:

* commands used
* credentials found
* exploitation steps
* privesc path

---

## 13. Proof Collection

For each host:

* user.txt
* proof.txt
* screenshots
* command history

---

## 14. Endgame

Before finishing:

* verify all flags
* verify all steps reproducible
* organize notes for reporting

---

## 15. Mental Model

* Slow is smooth, smooth is fast
* Enumeration reveals the path
* Credentials unlock the network
* Simplicity wins

---

## 16. Golden Rule

If you feel stuck:

→ You missed something in enumeration
