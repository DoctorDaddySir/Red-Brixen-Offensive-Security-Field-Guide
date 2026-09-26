# 08 – Passwords & Credentials

## Goal

Find and reuse credentials

---

## 1. Search Files

### Linux

```bash
grep -Ri password / 2>/dev/null
grep -Ri pass / 2>/dev/null
```

### Windows

```cmd
findstr /S /I password *.txt *.config
findstr /S /I pass *.txt
```

---

## 2. Stored Credentials

### Linux

```bash
# SSH agent identities
ssh-add -l
# SSH key files
ls -la ~/.ssh/
```

### Windows

```cmd
cmdkey /list
```

---

## 3. Config Files

Look in:

- Web apps
- Backups
- Scripts
- Environment files (`.env`, `*.conf`, `*.config`)

---

## 4. Reuse Everywhere

- ssh
- smb
- winrm
- rdp
- ldap

---

## 5. Crack Hashes

```bash
john hash.txt
hashcat -m 1000 hash.txt wordlist.txt
```

Use the appropriate mode number:

- NT / NTLM (Windows): `-m 1000`
- SHA-512 (Linux): `-m 1800`
- SHA-256 (Linux): `-m 1400`

---

## 6. Golden Rules

- credentials > exploits
- reuse everywhere
- always try default creds
- redact secrets before sharing
