# 08 – Passwords & Credentials

## Goal

Find and reuse credentials

---

## 1. Search Files

```bash
grep -Ri password / 2>/dev/null
```

```cmd
findstr /S /I password *.txt *.config
```

---

## 2. Stored Credentials

```cmd
cmdkey /list
```

---

## 3. Config Files

Look in:
- web apps
- backups
- scripts

---

## 4. Reuse Everywhere

- ssh
- smb
- winrm
- rdp

---

## 5. Crack Hashes

```bash
john hash.txt
hashcat -m 1000 hash.txt wordlist.txt
```

---

## 6. Golden Rules

- credentials > exploits
- reuse everywhere
- always try default creds