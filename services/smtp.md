# SMTP Enumeration & Exploitation

## Purpose

This file provides a structured workflow for enumerating SMTP services and extracting usernames, credentials, and pivot opportunities.

Core rules:

* SMTP = user enumeration engine
* Build username lists early
* Feed results into password attacks
* Look for misconfigurations and open relay

---

## 0. Identify SMTP

Common ports:

* 25 (SMTP)
* 465 (SMTPS)
* 587 (Submission)

Confirm:

```bash id="q2m8v1"
nmap -p 25,465,587 -sV <IP>
```

---

## 1. Banner Grabbing

```bash id="x7c4n9"
nc <IP> 25
```

or:

```bash id="z3k6r2"
telnet <IP> 25
```

Look for:

* server type (Postfix, Exim, Sendmail)
* domain name
* version info

---

## 2. Basic SMTP Interaction

```bash id="n5p2j8"
HELO test
```

```bash id="c8v4t1"
EHLO test
```

---

## 3. User Enumeration (CRITICAL)

### VRFY Command

```bash id="k1y7q3"
VRFY username
```

Responses:

* 250 → user exists
* 550 → user does not exist

---

### EXPN Command

```bash id="r9f3w6"
EXPN username
```

---

### RCPT TO Method

```bash id="m4d8x2"
MAIL FROM:test@test.com
RCPT TO:user@domain.local
```

---

## 4. Automated User Enumeration

### smtp-user-enum

```bash id="p6j1n5"
smtp-user-enum -M VRFY -U users.txt -t <IP>
```

```bash id="v8c2r7"
smtp-user-enum -M RCPT -U users.txt -t <IP>
```

---

## 5. Extract Domain Info

Look for:

* domain name
* user naming format
* internal email structure

---

## 6. Credential Discovery

Check for:

* emails with passwords (rare but possible)
* exposed mailboxes
* config leaks

---

## 7. Open Relay Check

```bash id="s2k9z4"
nmap --script smtp-open-relay -p 25 <IP>
```

If open relay:
→ can send spoofed emails (rarely needed in OSCP)

---

## 8. SMTP Auth (If Enabled)

```bash id="f7x3v9"
nmap --script smtp-brute -p 25 <IP>
```

---

## 9. Combine with Other Attacks

SMTP users → feed into:

* SMB login attempts
* LDAP enumeration
* Kerberos attacks
* password spraying

---

## 10. Password Spraying

```bash id="t5m1c8"
crackmapexec smb <IP> -u users.txt -p passwords.txt
```

---

## 11. Pivot Opportunities

SMTP can reveal:

* valid usernames
* domain structure
* email patterns

---

## 12. If VRFY Disabled

Try:

* RCPT TO method
* smtp-user-enum alternate modes
* username guessing

---

## 13. If Stuck

RESET:

* rerun user enumeration
* expand username list
* test creds on other services
* revisit domain naming patterns

---

## 14. Mental Model

* SMTP = user discovery
* Users = attack surface
* More users = more chances for creds

---

## 15. Golden Rules

* Always attempt user enumeration
* Always build username list
* Always reuse usernames across services
* Always combine with SMB/LDAP
