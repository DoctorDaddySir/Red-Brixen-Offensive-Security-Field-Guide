# 02 – Domain Enumeration

## Goal

Extract maximum domain information

---

## LDAP

```bash
ldapsearch -x -H ldap://<IP> -s base namingcontexts
```

---

## BloodHound (CRITICAL)

```bash
bloodhound-python -u user -p pass -ns <DC_IP> -d domain.local -c All
```

---

## SMB Enum

```bash
netexec smb <IP> --users
netexec smb <IP> --shares
```

---

## Identify

- high-value users
- admin groups
- service accounts

---

## Golden Rule

BloodHound reveals attack paths