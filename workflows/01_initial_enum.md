# 01 – Initial Enumeration

## Goal

Identify:
- open ports
- services
- entry points

---

## 1. Host Discovery

```bash
nmap -sn <subnet>
```

---

## 2. Full TCP Scan (FIRST STEP)

```bash
nmap -p- --min-rate 1000 -T4 <target> -oA initial
```

---

## 3. Service Scan

```bash
nmap -p <ports> -sC -sV -oA services <target>
```

---

## 4. UDP Quick Check

```bash
nmap -sU --top-ports 20 <target>
```

---

## 5. Identify Attack Surface

Map:
- web → 80/443/8080
- smb → 445
- ldap → 389
- ssh → 22
- ftp → 21
- rdp → 3389
- winrm → 5985/5986

---

## 6. Immediate Actions

- open browser (web)
- smb enum
- ldap/ad enum
- ftp login test

---

## 7. Golden Rules

- Always run full port scan
- Do not skip UDP basics
- Start attacking while scanning continues