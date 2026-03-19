# Pivoting – SSH Tunneling

## Purpose

This file provides a structured workflow for using SSH tunneling to pivot into internal networks.

Core rules:
- SSH is stable and widely available
- Supports local, remote, and dynamic (SOCKS) tunnels
- Often bypasses firewall restrictions
- Excellent fallback when other tools fail

---

## 0. Mental Model

SSH creates encrypted tunnels.

You can:
- forward ports
- create SOCKS proxies
- expose internal services

---

# =========================
# 1. LOCAL PORT FORWARDING
# =========================

## Use Case

Access internal service from attacker

---

## Command

ssh -L <local_port>:<target_ip>:<target_port> user@<pivot_host>

---

## Example (RDP)

ssh -L 3389:10.10.10.5:3389 user@<pivot>

Then connect:

xfreerdp /v:127.0.0.1

---

## Flow

[ATTACKER:local_port] → [SSH] → [PIVOT] → [TARGET]

---

# =========================
# 2. REMOTE PORT FORWARDING
# =========================

## Use Case

Expose attacker service to target

---

## Command

ssh -R <remote_port>:<attacker_ip>:<attacker_port> user@<pivot_host>

---

## Example

ssh -R 4444:127.0.0.1:4444 user@<pivot>

Target connects to pivot:4444 → attacker

---

## Flow

[TARGET] → [PIVOT] → [ATTACKER]

---

# =========================
# 3. DYNAMIC PORT FORWARDING (SOCKS)
# =========================

## MOST IMPORTANT MODE

Creates SOCKS proxy

---

## Command

ssh -D 1080 user@<pivot_host>

---

## Result

SOCKS proxy on:

127.0.0.1:1080

---

## Use with Proxychains

proxychains nmap -sT -Pn <target>

---

## Flow

[TOOL] → [SOCKS] → [SSH] → [PIVOT] → [TARGET]

---

# =========================
# 4. BACKGROUND TUNNEL
# =========================

## Run without blocking shell

ssh -f -N -D 1080 user@<pivot>

---

# =========================
# 5. MULTIPLE FORWARDS
# =========================

ssh -L 8080:10.10.10.5:80 -L 3389:10.10.10.5:3389 user@<pivot>

---

# =========================
# 6. VERIFY CONNECTION
# =========================

netstat -an | grep 1080

---

# =========================
# 7. COMMON USE CASES
# =========================

- access internal web apps
- RDP pivoting
- SMB enumeration
- database access
- internal scanning via SOCKS

---

# =========================
# 8. COMMON FAILURE POINTS
# =========================

- wrong IP (use internal IPs)
- port already in use
- firewall blocking SSH
- proxychains misconfigured
- forgetting -Pn in nmap

---

# =========================
# 9. IF STUCK
# =========================

- test basic SSH connection
- verify tunnel is listening
- try different port
- check routing
- switch to chisel/ligolo

---

# =========================
# 10. QUICK EXPLOIT PATTERN
# =========================

1. gain SSH access to pivot host
2. choose tunnel type
3. start tunnel
4. verify connection
5. use tools through tunnel

---

# =========================
# 11. MENTAL MODEL
# =========================

SSH = tunnel  
Tunnel = path  
Pivot = gateway  
Target = internal network  

---

# =========================
# 12. GOLDEN RULES
# =========================

- Use dynamic (-D) for flexibility
- Use -f -N for background tunnels
- Always verify ports are open
- Prefer SOCKS + proxychains for scanning
- SSH is your most reliable fallback