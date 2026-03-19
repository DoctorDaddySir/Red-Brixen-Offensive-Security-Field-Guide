# Windows Privilege Escalation – Master Index

## Purpose

This file provides a structured, high-speed workflow for Windows privilege escalation.

Core rules:
- Follow the order (do not jump randomly)
- Prioritize high-probability techniques first
- Move fast and execute
- If stuck → reset and continue

---

# PHASE 1: INITIAL ENUMERATION (ALWAYS FIRST)

## System Info

```cmd
whoami
whoami /groups
whoami /priv
systeminfo
hostname
```

---

## Quick Wins Scan

```cmd
cmdkey /list
schtasks /query /fo LIST /v
wmic service get name,displayname,pathname,startmode
```

---

## Tools (if available)

- winPEAS.exe
- PowerUp.ps1

---

# PHASE 2: HIGHEST PROBABILITY WINS (DO THESE FIRST)

## 1. TOKEN PRIVILEGES (TOP PRIORITY)

File:
→ token_privileges.md

```cmd
whoami /priv
```

Look for:
- SeImpersonatePrivilege
- SeAssignPrimaryTokenPrivilege

---

## 2. STORED CREDENTIALS

File:
→ stored_credentials.md

```cmd
cmdkey /list
```

Also check:
- config files
- registry
- unattended files

---

## 3. ALWAYSINSTALLELEVATED

File:
→ always_install_elevated.md

```cmd
reg query HKLM\Software\Policies\Microsoft\Windows\Installer
reg query HKCU\Software\Policies\Microsoft\Windows\Installer
```

---

## 4. WEAK SERVICE PERMISSIONS

File:
→ weak_service_permissions.md

```cmd
accesschk.exe -uwcqv "Users" *
```

---

## 5. WRITABLE SERVICE FILES

File:
→ writable_service_files.md

```cmd
sc qc <service>
icacls <path>
```

---

# PHASE 3: VERY COMMON MISCONFIGS

## 6. UNQUOTED SERVICE PATHS

File:
→ unquoted_service_paths.md

```cmd
wmic service get name,displayname,pathname,startmode | findstr /i "Auto"
```

---

## 7. SCHEDULED TASKS

File:
→ scheduled_tasks.md

```cmd
schtasks /query /fo LIST /v
```

---

## 8. REGISTRY AUTORUNS

File:
→ registry_autoruns.md

```cmd
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
```

---

## 9. INSECURE FILE PERMISSIONS

File:
→ insecure_file_permissions.md

```cmd
icacls <path>
```

---

# PHASE 4: ADVANCED TECHNIQUES

## 10. DLL HIJACKING

File:
→ dll_hijacking.md

Use:
- Procmon
- missing DLL detection

---

## 11. UAC BYPASS (ADMIN ONLY)

File:
→ uac_bypass.md

```cmd
whoami /groups
```

---

## 12. KERNEL EXPLOITS (LAST RESORT)

File:
→ kernel_exploits.md

```cmd
systeminfo
```

---

# QUICK EXECUTION FLOW

Run in order:

1. whoami /priv  
2. cmdkey /list  
3. AlwaysInstallElevated  
4. service permissions (accesschk)  
5. writable service files  
6. unquoted paths  
7. scheduled tasks  
8. autoruns  
9. file permissions  
10. DLL hijacking  
11. kernel exploit (last)

---

# TIME MANAGEMENT STRATEGY

0–30 min:
- token privileges
- credentials
- AlwaysInstallElevated
- services

30–60 min:
- tasks
- autoruns
- unquoted paths

60+ min:
- DLL hijacking
- deeper enumeration
- kernel (only if needed)

---

# RESET STRATEGY (CRITICAL)

If stuck:

- re-run enumeration
- re-check token privileges
- re-check credentials
- re-check services
- re-check writable paths

Most failures come from:
→ missing something obvious

---

# MENTAL MODEL

You are not exploiting vulnerabilities first.

You are checking:
- permissions
- trust boundaries
- execution paths

---

# GOLDEN RULES

- Check whoami /priv immediately
- SeImpersonate = highest priority
- Always check credentials early
- Services are the most common win
- Directory permissions matter more than files
- Kernel exploits are last

---

# FINAL CHECKLIST

Before moving on:

- token privileges checked
- credentials searched
- services reviewed
- scheduled tasks checked
- autoruns checked
- writable paths tested

If anything missing:
→ go back