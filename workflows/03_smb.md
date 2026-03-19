# 03 – SMB Enumeration

## Goal

Find:
- shares
- users
- credentials
- writable locations

---

## 1. Anonymous Access

```bash
smbclient -L //<IP> -N
```

---

## 2. Enum4linux

```bash
enum4linux -a <IP>
```

---

## 3. CrackMapExec

```bash
crackmapexec smb <IP> --shares
crackmapexec smb <IP> --users
```

---

## 4. Access Shares

```bash
smbclient //<IP>/share -U user
```

---

## 5. Download Everything

```bash
recurse ON
prompt OFF
mget *
```

---

## 6. Look For

- passwords
- config files
- scripts
- backups

---

## 7. Writable Shares

Upload payload:

```bash
put shell.exe
```

---

## 8. Golden Rules

- Always check anonymous first
- Always download everything
- SMB = high-value target