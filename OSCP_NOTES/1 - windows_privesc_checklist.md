# Windows Privilege Escalation Checklist

## 0. Immediate Context (DO THIS FIRST)

```powershell
whoami
whoami /priv
whoami /groups
hostname
systeminfo
ipconfig /all
```

* Save output
* Identify OS version
* Identify user privileges

---

## 1. Quick Wins (ALWAYS CHECK FIRST)

### Stored credentials

```powershell
cmdkey /list
```

### AlwaysInstallElevated

```powershell
reg query HKCU\Software\Policies\Microsoft\Windows\Installer
reg query HKLM\Software\Policies\Microsoft\Windows\Installer
```

### Shares

```powershell
net share
```

### Privileges

```powershell
whoami /priv
```

Look for:

* SeImpersonatePrivilege
* SeBackupPrivilege
* SeDebugPrivilege

---

## 2. Credential Hunting

### File search

```powershell
findstr /si password *.txt *.xml *.ini *.config
```

### Check common locations

* Desktop
* Documents
* Downloads
* C:\inetpub\
* C:\xampp\
* C:\Program Files\

### Registry search

```powershell
reg query HKLM /f password /t REG_SZ /s
```

---

## 3. Services (HIGH VALUE — MULTIPLE METHODS)

### Method 1 — Basic

```powershell
sc query
```

### Method 2 — Extended

```powershell
sc queryex
```

### Method 3 — Config

```powershell
sc qc <service>
```

### Method 4 — PowerShell

```powershell
Get-Service
```

### Method 5 — WMI (detailed)

```powershell
Get-WmiObject Win32_Service | select Name,DisplayName,PathName,StartMode,State
```

### Method 6 — Running only

```powershell
Get-Service | Where-Object {$_.Status -eq "Running"}
```

### Method 7 — SYSTEM services

```powershell
Get-WmiObject Win32_Service | Where-Object {$_.StartName -eq "LocalSystem"}
```

### Permission check

```powershell
sc qc <service>
icacls "<service_binary_path>"
```

### What to look for

* Unquoted service paths
* Writable service binaries
* Services running as SYSTEM
* Weak permissions

---

## 4. Scheduled Tasks (MULTIPLE METHODS)

### Method 1 — Basic

```powershell
schtasks /query
```

### Method 2 — Verbose

```powershell
schtasks /query /fo LIST /v
```

### Method 3 — PowerShell

```powershell
Get-ScheduledTask
```

### Method 4 — Detailed

```powershell
Get-ScheduledTask | Get-ScheduledTaskInfo
```

### Method 5 — SYSTEM tasks

```powershell
Get-ScheduledTask | Where-Object {$_.Principal.UserId -eq "SYSTEM"}
```

### Method 6 — Actions

```powershell
Get-ScheduledTask | Select TaskName,Actions
```

### What to look for

* Tasks running as SYSTEM
* Writable scripts/binaries
* Misconfigured permissions

---

## 5. File System Permissions

### Check common directories

```powershell
icacls "C:\Program Files" /t
icacls "C:\Program Files (x86)" /t
```

Look for:

* Writable directories
* Writable executables

---

## 6. Token Impersonation (VERY HIGH VALUE)

Check:

```powershell
whoami /priv
```

If present:

* SeImpersonatePrivilege

→ Try:

* PrintSpoofer
* RoguePotato / JuicyPotato

---

## 7. Installed Applications

```powershell
wmic product get name,version
```

Look for:

* Vulnerable versions
* Misconfigurations

---

## 8. Running Processes

```powershell
tasklist /v
```

Look for:

* SYSTEM processes
* Interesting services

---

## 9. Network Enumeration

```powershell
netstat -ano
```

Look for:

* Internal-only services
* Localhost-bound ports

---

## 10. Automated Enumeration

Run:

* winPEAS

```powershell
.\winPEAS.exe
```

Review output manually.

---

## 11. Special Privileges

### SeBackupPrivilege

* Dump SAM / SYSTEM
* Extract hashes

### SeDebugPrivilege

* Process injection

---

## 12. DLL Hijacking

Look for:

* Missing DLLs
* Writable directories in PATH

---

## 13. Alternate Enumeration (WMI / CIM)

```powershell
Get-CimInstance Win32_Service
Get-CimInstance Win32_ScheduledJob
```

---

## 14. Always Think

* Can I write to something executed by SYSTEM?
* Can I replace a binary or script?
* Can I reuse credentials?
* Can I impersonate a token?

---

## 15. If Stuck (RESET)

* Re-enumerate everything
* Re-check services
* Re-check scheduled tasks
* Re-check writable files
* Re-check credentials
* Try another method for each check

---

## 16. Proof

Once SYSTEM:

```powershell
whoami
```

Capture:

* proof.txt
* user.txt
* screenshots
