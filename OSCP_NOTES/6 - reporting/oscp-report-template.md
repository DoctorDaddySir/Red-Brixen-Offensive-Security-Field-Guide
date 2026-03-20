# OffSec Certified Professional (OSCP) Exam Report

**Student:** [student@youremailaddress.com](mailto:student@youremailaddress.com)
**OSID:** XXXXX

---

# 1. Introduction

This report documents the penetration testing activities conducted during the OffSec Certified Professional (OSCP) exam. The objective is to demonstrate a methodical approach to identifying and exploiting vulnerabilities within the target environment.

---

# 2. Objective

Perform an internal penetration test against the provided exam network. Identify vulnerabilities, exploit them, and document the process in a clear and reproducible manner.

---

# 3. Requirements

This report includes:

* High-Level Summary
* Methodology
* Detailed findings per target
* Screenshots and proof files
* Step-by-step reproduction steps

---

# 4. High-Level Summary

A penetration test was conducted against the internal lab environment. Multiple vulnerabilities were identified and successfully exploited, leading to administrative-level access on several systems.

The primary issues identified include:

* Weak credentials
* Misconfigured services
* Outdated software

---

## 4.1 Recommendations

* Apply security patches regularly
* Enforce strong password policies
* Disable unnecessary services
* Restrict anonymous access

---

# 5. Methodology

## 5.1 Information Gathering

* Identified target IP ranges
* Performed host discovery

## 5.2 Service Enumeration

* Conducted port scans (Nmap)
* Identified running services and versions

## 5.3 Exploitation

* Identified vulnerabilities
* Developed and executed exploits

## 5.4 Privilege Escalation

* Enumerated system misconfigurations
* Leveraged privilege escalation techniques

## 5.5 Post Exploitation

* Retrieved proof files
* Maintained access where necessary

---

# 6. Independent Challenges

---

## 6.1 Target #1 – <IP ADDRESS>

### 6.1.1 Vulnerability Summary

**Description:**
Explain the vulnerability.

**Impact:**
Explain what access was gained.

**Severity:** Critical / High / Medium / Low

**Fix:**
Explain remediation steps.

---

### 6.1.2 Enumeration

```bash
nmap -sC -sV -oA initial <IP>
```

**Findings:**

* Port XX: Service
* Port XX: Service

---

### 6.1.3 Exploitation (Initial Access)

**Steps:**

1. Describe step
2. Describe step

```bash
# Commands used
```

---

### 6.1.4 Privilege Escalation

**Technique Used:**

* Example: AlwaysInstallElevated

```bash
# Commands used
```

---

### 6.1.5 Proof

**local.txt**

```
<value>
```

**proof.txt**

```
<value>
```

**Screenshots:**

* Include terminal showing proof.txt and IP

---

### 6.1.6 Steps to Reproduce

1. Run initial scan:

```bash
nmap -sC -sV <IP>
```

2. Access service:

```bash
<command>
```

3. Exploit vulnerability:

```bash
<command>
```

4. Escalate privileges:

```bash
<command>
```

---

# 7. Active Directory Set

---

## 7.1 <Machine Name> – <IP>

### 7.1.1 Initial Access

**Vulnerability:**

* Description

```bash
# Commands
```

---

### 7.1.2 Privilege Escalation

**Technique:**

* Description

```bash
# Commands
```

---

### 7.1.3 Post Exploitation

* Lateral movement
* Credential harvesting

---

## 7.2 <Next Machine>

(Repeat structure for each machine)

---

# 8. Conclusion

The assessment demonstrated multiple critical vulnerabilities that allowed full compromise of the environment. Proper patching, credential management, and system hardening are recommended.

---
