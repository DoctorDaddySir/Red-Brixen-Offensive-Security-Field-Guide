# Pentesting Tools & OSCP+ Field Guide

## Purpose

This repository is a **high-speed operational reference** for penetration testing.

It is designed for:
- OSCP+ exam use
- lab environments
- real-world engagements

---

## Core Philosophy

- Speed > completeness
- Enumeration > guessing
- Credentials > exploits
- Simple > clever

---

## Structure

```
.
├── enumeration/
├── privesc/
│   ├── linux/
│   └── windows/
├── ad/
├── pivoting/
├── snippets/
├── workflows/
├── mindset/
├── worksheets/
```

---

## How To Use (Exam Mode)

1. Start with:
   → workflows/01_initial_enum.md

2. Follow workflow progression:
   → web / smb / ad

3. Use:
   → snippets/ for commands
   → privesc/ for escalation
   → pivoting/ for internal access

4. If stuck:
   → mindset/

---

## Golden Loop

```
Scan → Enum → Exploit → Shell → Privesc → Pivot → Repeat
```

---

## Priority Order

1. Credentials
2. Misconfigurations
3. Known attack paths
4. Exploits

---

## Warning

Do NOT:
- skip enumeration
- tunnel on one idea
- overcomplicate solutions

---

## Goal

Turn this repo into:
→ instinct under pressure