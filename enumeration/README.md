# Enumeration

## Purpose

Systematically identify:
- services
- users
- credentials
- attack surface

---

## Critical Concept

Enumeration is NOT a phase.

It is:
→ continuous

---

## When To Enumerate

- initial access
- after shell
- after privilege escalation
- after pivoting

---

## Structure

Each file represents a service or protocol. Active Directory enumeration ([ad_enum.md](ad_enum.md)) covers LDAP, Kerberos, and BloodHound collection — there is no standalone `ldap.md` here.

- [web.md](web.md)
- [smb.md](smb.md)
- [ad_enum.md](ad_enum.md)
- [rpc.md](rpc.md)
- [dns.md](dns.md)
- [ftp.md](ftp.md)
- [ssh.md](ssh.md)
- [winrm.md](winrm.md)
- [mssql.md](mssql.md)
- [snmp.md](snmp.md)
- [smtp.md](smtp.md)
- [nfs.md](nfs.md)
- [webdav.md](webdav.md)
- [wordpress.md](wordpress.md)
- [drupal.md](drupal.md)
- [jenkins.md](jenkins.md)
- [github.md](github.md)

---

## Usage

1. identify service
2. open corresponding file
3. execute commands
4. record findings

---

## Golden Rule

If you are stuck:
→ you missed something
