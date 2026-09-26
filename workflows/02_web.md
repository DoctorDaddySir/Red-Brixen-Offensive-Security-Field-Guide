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

## 2. Subdirectory & Vhost Scanning

### 2.1 Subdirectory scanning

Brute-force directories and filenames. Request common extensions with `-x`/`-e` and filter
status codes with `-mc` to reduce noise:

```bash
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt -x php,txt,html,js
ffuf -u http://<IP>/FUZZ -w wordlist.txt -mc 200,301,302,403 -e .php,.html,.js,.txt
```

Save and triage results:

```bash
ffuf -u http://<IP>/FUZZ -w wordlist.txt -of json -o subdir_results.json -t 50
```

### 2.2 Vhost (virtual host) scanning

Virtual hosts reveal alternate sites and admin panels not served on the default host. Fuzz
the `Host` header against a wordlist:

```bash
ffuf -u http://<IP>/ -H "Host: FUZZ" -w /usr/share/wordlists/dirb/common.txt -mc 200,302,404
gobuster vhost -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
```

Re-test each discovered host with the full enumeration set above, overriding the Host header:

```bash
ffuf -u http://discovered.host/ -H "Host: discovered.host" -w wordlist.txt -mc 200,301,403
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
