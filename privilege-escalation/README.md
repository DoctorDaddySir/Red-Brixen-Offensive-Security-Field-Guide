# Privilege Escalation

## Purpose

Escalate privileges on compromised systems

---

## Structure

```
linux/
windows/
```

---

## Strategy

1. quick wins
2. misconfigurations
3. credentials
4. exploits (last)

---

## Workflow

After gaining a shell:

- enumerate system
- check privileges
- identify misconfigurations
- escalate

---

## Golden Rules

- Linux: sudo -l first
- Windows: whoami /priv first
- credentials > exploits