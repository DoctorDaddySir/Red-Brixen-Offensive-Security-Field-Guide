# Red Brixen Offensive Security Field Guide
A structured penetration testing system designed for OSCP+ preparation and real-world engagements.

## Intended Audience

- OSCP candidates
- aspiring penetration testers
- security engineers building practical workflows

## Highlights

- End-to-end attack workflows
- Active Directory attack framework
- Privilege escalation playbooks (Linux + Windows)
- Pivoting strategies (Ligolo, tunnels)
- Reporting templates

## Purpose

This repository is a **high-speed operational system** for penetration testing.

It is optimized for:
- OSCP+ exam execution
- lab environments
- real-world engagements

---

## Core Philosophy

- Enumeration is continuous
- Credentials are king
- Misconfigurations beat exploits
- Simplicity beats cleverness

---

## Structure

```
.
├── enumeration/
├── privilege-escalation/
│   ├── linux/
│   └── windows/
├── active-directory/
├── pivoting/
├── snippets/
├── workflows/
├── hacker-mindset/
├── exploited_vulns/
```

---

## How To Use (Exam Mode)

1. Start here:
   → workflows/01_initial_enum.md

2. Follow the workflow:
   → web → smb → active-directory

3. Use:
   → snippets/ for commands  
   → privilege-escalation/ for escalation  
   → pivoting/ for internal access  

4. If stuck:
   → hacker-mindset/

---

## Core Loop

```
Scan → Enum → Exploit → Shell → Privesc → Pivot → Repeat
```

---

## Priority Order

1. Credentials
2. Misconfigurations
3. Known attack paths
4. Exploits (last)

---

## Warning

Do NOT:
- skip enumeration
- tunnel on one idea
- overcomplicate solutions

---

## Goal

Turn this repo into instinct under pressure
