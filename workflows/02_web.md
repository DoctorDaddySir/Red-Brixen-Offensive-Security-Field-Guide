# 02 – Web Enumeration

## Goal

Find:
- directories
- functionality
- vulnerabilities
- upload points

---

## 1. Basic Recon

```bash
whatweb http://<IP>
curl -I http://<IP>
```

---

## 2. Directory Bruteforce

```bash
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
ffuf -u http://<IP>/FUZZ -w wordlist.txt
```

---

## 3. Check Manually

- login pages
- file uploads
- admin panels
- APIs

---

## 4. Technology Identification

- PHP / ASPX / Node
- CMS (WordPress, Drupal, Joomla)

---

## 5. Common Attacks

- LFI / RFI
- command injection
- file upload → RCE
- SQLi

---

## 6. If Upload Exists

- try web shell
- bypass filters (extension, MIME)

---

## 7. If Auth Exists

- default creds
- brute force
- password reuse

---

## 8. Golden Rules

- Always fuzz directories
- Always check uploads
- Always try basic injection