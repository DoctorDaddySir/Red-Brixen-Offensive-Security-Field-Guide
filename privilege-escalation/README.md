# Privilege Escalation

## Purpose

Escalate from:
- low user → root (Linux)
- user → SYSTEM (Windows)

---

## Structure

```
linux/
windows/
```

---

## Strategy

1. quick wins first
2. misconfigurations
3. credentials
4. exploits (last)

---

## Golden Rules

- sudo -l first (Linux)
- whoami /priv (Windows)
- credentials > exploits