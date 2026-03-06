# Secrets in Configuration Files

## Detection

grep -R "password" /etc /opt /home 2>/dev/null

Look for:

- database credentials
- SSH keys
- API keys

## Exploitation

Reuse credentials:

su <user>
ssh <user>@localhost
