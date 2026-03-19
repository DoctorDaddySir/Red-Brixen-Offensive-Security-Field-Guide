# Reporting Templates (OSCP+)

## Purpose

These templates allow fast, consistent documentation during and after the exam.

Write findings as you go.

---

# 1. Standard Finding Template

## Title

[Short descriptive name]

## Target

* IP:
* Hostname:

## Description

Brief explanation of the vulnerability.

## Enumeration

Commands used:

```
[commands]
```

Output summary:

```
[key output]
```

## Exploitation

Steps:

1. Step one
2. Step two
3. Step three

Commands:

```
[commands]
```

## Proof

```
[proof.txt output]
```

## Impact

* What access was gained
* Why it matters

## Remediation

* Fix misconfiguration
* Patch vulnerability
* Restrict permissions

---

# 2. Local Privilege Escalation

## Title

Local Privilege Escalation via [method]

## Target

* IP:
* User:

## Enumeration

* Findings:
* Misconfiguration:

## Exploitation

Steps:
1.
2.
3.

Commands:

```
[commands]
```

## Proof

```
whoami
```

## Impact

* SYSTEM/root access obtained

## Remediation

* Fix permissions
* Remove misconfiguration

---

# 3. Credential Discovery

## Title

Credential Disclosure

## Target

* IP:

## Source

* File / service / registry / share

## Details

* Username:
* Password:

## Usage

* Where credentials worked

## Impact

* Lateral movement possible

## Remediation

* Remove stored credentials
* Secure config files

---

# 4. AD Attack Chain

## Title

Active Directory Compromise Chain

## Summary

Brief overview of full chain.

## Steps

1. Initial access
2. Enumeration
3. Credential discovery
4. Lateral movement
5. Privilege escalation

## Commands

```
[commands]
```

## Proof

* Domain admin access evidence

## Impact

* Full domain compromise

## Remediation

* Fix each step in chain

---

# 5. Quick Notes Section

Use during exam:

* Commands:
* Creds:
* Paths:
* Observations:

---

# 6. Reporting Reminders

* Be concise
* Show commands clearly
* Show proof clearly
* Ensure steps are reproducible
* Avoid unnecessary theory
