# 03 – SMB Enumeration

## Goal

Find:
- shares
- users
- credentials
- writable locations

---

## 1. Anonymous / Guest Access

Try anonymous/guest access first. On many targets the guest account is enabled or anonymous
binding succeeds with an empty password — both are common initial footholds.

```bash
smbclient -L //<IP> -N
smbmap -H <IP>
```

### Guest account check

```bash
netexec smb <IP> --local-auth -u guest -p '' --shares
# null-session alternative:
smbclient -L //<IP> -U guest%
```

---

## 2. Enum4linux

```bash
enum4linux -a <IP>
```

---

## 3. NetExec (preferred)

NetExec is the maintained community successor to CrackMapExec. Prefer `netexec` for authenticated
SMB enumeration; `crackmapexec` is retained as a legacy alias where already installed.

```bash
netexec smb <IP> --shares
netexec smb <IP> --users
```

---

## 4. Access Shares

```bash
smbclient //<IP>/share -U user
```

---

## 5. Download (scoped)

```bash
recurse ON
prompt OFF
mget *
```

Scope downloads to relevant shares and preserve a file manifest for evidence.

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

## 8. Credential Reuse

Test any found creds across protocols:

```bash
netexec smb <targets.txt> -u user -p pass -d DOMAIN
netexec winrm <targets.txt> -u user -p pass -d DOMAIN
netexec rdp <targets.txt> -u user -p pass -d DOMAIN
```

---

## 9. Golden Rules

- Always check anonymous/guest first
- Always scope downloads and preserve evidence
- SMB = high-value target
