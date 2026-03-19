# Linux Host Enumeration Worksheet

## Target Info

* IP:
* Hostname:
* Domain (if any):
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
* Shell Type:
* Stability (TTY?):
* Entry Vector:

---

## System Info

```bash
uname -a
cat /etc/os-release
id
```

* OS:
* Kernel:
* Architecture:
* Current User:
* Groups:

---

## Network Info

```bash
ip a
netstat -tulnp
```

* Interfaces:
* Internal Services:
* Pivot Opportunities:

---

## Users & Credentials

```bash
cat /etc/passwd
```

* Users:
* Interesting Accounts:
* Passwords Found:
* SSH Keys:

---

## Sudo

```bash
sudo -l
```

* Allowed Commands:
* Exploitable?:

---

## SUID / Capabilities

```bash
find / -perm -4000 2>/dev/null
getcap -r / 2>/dev/null
```

* SUID Findings:
* Capability Findings:

---

## File System

* Writable Directories:
* Writable Files:
* Sensitive Files:
* Backups:

---

## Cron Jobs

```bash
crontab -l
ls -la /etc/cron*
```

* Jobs:
* Writable Scripts:
* Execution Context:

---

## Processes

```bash
ps aux
```

* Interesting Processes:
* Custom Scripts:

---

## Applications / Services

* Web apps:
* Databases:
* Custom apps:

---

## Credential Hunting

* Config Files:
* Hardcoded Credentials:
* Reused Credentials:

---

## Privilege Escalation Paths

* Path 1:
* Path 2:
* Path 3:

---

## Loot

* Flags:
* Credentials:
* Sensitive Data:

---

## Proof

* user.txt:
* proof.txt:

---

## Notes

*
