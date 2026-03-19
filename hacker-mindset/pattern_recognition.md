# Pattern Recognition

## Purpose

Recognize recurring vulnerabilities and exploitation paths.

---

## Common Patterns

### Web

- login → weak creds
- upload → RCE
- LFI → file access → creds

---

### SMB

- share → files → creds → reuse

---

### AD

- user list → roasting → creds → lateral movement

---

### Linux

- SUID → privilege escalation
- sudo → misconfig

---

### Windows

- SeImpersonate → SYSTEM
- services → misconfig
- scheduled tasks → writable

---

## Skill Development

- note repeated patterns
- compare machines
- reuse successful approaches

---

## When To Use

- after initial enumeration
- when seeing familiar services

---

## Golden Rule

Most boxes are variations of known patterns