# Windows Host Enumeration Worksheet

## Target Info

* IP:
* Hostname:
* Domain:
* Initial Access Method:

---

## Port Scan Results

### Open Ports

*

### Service Versions

*

### Notes

*

---

## Initial Foothold

* User:
* Access Method (WinRM/RDP/Shell):
* Privilege Level:
* Entry Vector:

---

## System Info

```powershell
systeminfo
whoami
whoami /groups
whoami /priv
```

* OS Version:
* Hostname:
* Domain:
* Current User:
* Privileges:

---

## Network Info

```powershell
ipconfig /all
netstat -ano
```

* Interfaces:
* Internal Services:
* Pivot Opportunities:

---

## Users & Groups

```powershell
net user
net localgroup
```

* Users:
* Admins:
* Interesting Groups:

---

## Credentials

* Stored Credentials (`cmdkey /list`):
* Found Passwords:
* Config Files:
* Registry Findings:

---

## SMB / Shares

```powershell
net share
```

* Shares:
* Writable Shares:
* Interesting Files:

---

## Services

```powershell
sc query
Get-WmiObject Win32_Service
```

* Vulnerable Services:
* Writable Paths:
* SYSTEM Services:

---

## Scheduled Tasks

```powershell
schtasks /query /fo LIST /v
```

* Tasks:
* SYSTEM Tasks:
* Writable Scripts:

---

## File System

* Writable Directories:
* Writable Files:
* Sensitive Files:

---

## Installed Applications

```powershell
wmic product get name,version
```

* Interesting Software:
* Potential Vulns:

---

## Processes

```powershell
tasklist /v
```

* SYSTEM Processes:
* Interesting Targets:

---

## AD Enumeration (if applicable)

* Users:
* Groups:
* SPNs:
* Sessions:
* BloodHound Notes:

---

## Privilege Escalation Paths

* Path 1:
* Path 2:
* Path 3:

---

## Loot

* Flags:
* Credentials:
* Hashes:
* Tickets:

---

## Proof

* user.txt:
* proof.txt:

---

## Notes

*
