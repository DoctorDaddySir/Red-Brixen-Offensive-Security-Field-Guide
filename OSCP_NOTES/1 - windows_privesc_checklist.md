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

### Check for stored credentials

```powershell
cmdkey /list
```

### Check for AlwaysInstallElevated

```powershell
reg query HKCU\Software\Policies\Microsoft\Windows\Installer
reg query HKLM\Software\Policies\Microsoft\Windows\Installer
```

### Check for writable shares

```powershell
net share
```

### Check current user privileges

```powershell
whoami /priv
```

Look for:

* SeImpersonatePrivilege
* SeBackupPrivilege
* SeDebugPrivilege

---

## 2. Credential Hunting

### Search for passwords in files

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

### Registry creds

```powershell
reg query HKLM /f password /t REG_SZ /s
```

---

## 3. Services (HIGH VALUE)

### List services

```powershell
sc query
```

### Check service configs

```powershell
sc qc <service>
```

Look for:

* Unquoted service paths
* Writable service binaries
* Weak permissions

---

## 4. Scheduled Tasks

```powershell
schtasks /query /fo LIST /v
```

Look for:

* Tasks running as SYSTEM
* Writable scripts/binaries

---

## 5. File System Permissions

### Find writable directories

```powershell
icacls "C:\Program Files" /t
```

Look for:

* Write access in privileged paths

---

## 6. Token Impersonation (VERY COMMON)

If you have:

* SeImpersonatePrivilege

→ Try:

* PrintSpoofer
* JuicyPotato / RoguePotato

---

## 7. Installed Applications

```powershell
wmic product get name,version
```

Look for:

* Known vulnerable software
* Misconfigurations

---

## 8. Running Processes

```powershell
tasklist /v
```

Look for:

* Processes running as SYSTEM
* Interesting services

---

## 9. Network Enumeration

```powershell
netstat -ano
```

Look for:

* Internal-only services
* Ports bound to localhost

---

## 10. Automated Enumeration

Run:

* winPEAS

Transfer and execute:

```powershell
.\winPEAS.exe
```

Review output carefully.

---

## 11. Special Privileges

### SeBackupPrivilege

* Dump SAM / SYSTEM
* Extract hashes

### SeDebugPrivilege

* Inject into processes

---

## 12. DLL Hijacking

Look for:

* Missing DLLs
* Writable directories in PATH

---

## 13. Always Think:

* Can I write to something executed by SYSTEM?
* Can I replace something?
* Can I reuse credentials?
* Can I impersonate?

---

## 14. If Stuck

RESET:

* Re-run enumeration
* Check ALL writable files
* Check ALL services again
* Check ALL tasks again
* Look for creds again
* Try different tools

---

## 15. Proof

Once SYSTEM:

```powershell
whoami
```

Capture:

* proof.txt
* user.txt
* screenshots
