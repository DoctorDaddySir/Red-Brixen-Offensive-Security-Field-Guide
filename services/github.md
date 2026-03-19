# GitHub Enumeration & Exploitation

## Purpose

This file provides a structured workflow for identifying and exploiting GitHub-based information leaks.

Core rules:

* Developers leak credentials constantly
* Git history is often more valuable than current code
* GitHub = recon goldmine
* Always search before exploiting

---

## 0. Identify GitHub Usage

Look for:

* links to GitHub repos
* developer usernames
* organization names
* commit emails

Sources:

* web pages
* source code comments
* error messages

---

## 1. Search GitHub (CRITICAL)

### Basic Search

Search for:

```text
company_name
domain.com
username
```

---

### Targeted Searches

```text
company_name password
company_name api_key
company_name secret
```

---

## 2. GitHub Dorks

Search:

```text
"password" "company_name"
"api_key" "company_name"
"secret" "company_name"
"db_password" "company_name"
```

---

## 3. Clone Repositories

```bash
git clone https://github.com/user/repo.git
```

---

## 4. Search for Secrets

```bash
grep -i "password" -r .
grep -i "key" -r .
grep -i "secret" -r .
```

---

## 5. Check .git Exposure (WEB TARGET)

```bash
wget -r http://<IP>/.git/
```

Recover repo:

```bash
git checkout .
```

---

## 6. Git History Analysis (CRITICAL)

```bash
git log
```

```bash
git show <commit>
```

Look for:

* removed passwords
* old credentials
* config changes

---

## 7. Automated Secret Scanning

```bash
trufflehog .
```

```bash
git-secrets --scan
```

---

## 8. Config Files (HIGH VALUE)

Check for:

* .env
* config.php
* settings.py
* database.yml

Look for:

* DB creds
* API keys
* tokens

---

## 9. SSH Keys

Look for:

```text
id_rsa
private keys
```

Use:

```bash
ssh -i id_rsa user@<IP>
```

---

## 10. API Keys

Look for:

* AWS keys
* tokens
* service credentials

---

## 11. Developer Patterns

Extract:

* usernames
* password patterns

Use for:

* password spraying

---

## 12. Credential Reuse

Test found creds on:

```bash
crackmapexec smb <IP> -u user -p pass
crackmapexec winrm <IP> -u user -p pass
ssh user@<IP>
```

---

## 13. Organization Recon

Check:

* employee repos
* forks
* public commits

---

## 14. Web App Integration

Check:

* source code leaks
* debug info
* exposed repos

---

## 15. Pivot Opportunities

GitHub can reveal:

* credentials
* infrastructure details
* internal endpoints
* service configs

---

## 16. If Stuck

RESET:

* search more keywords
* check commit history deeper
* expand org search
* scan repos with tools

---

## 17. Mental Model

* GitHub = developer mistakes
* History = secrets
* Code = credentials

---

## 18. Golden Rules

* Always search GitHub early
* Always check commit history
* Always scan for secrets
* Always reuse credentials
