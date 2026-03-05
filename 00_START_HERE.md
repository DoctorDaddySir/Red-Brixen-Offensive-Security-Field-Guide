# Start Here (OSCP KB)

## Flow
1. Triage ports (Nmap)
2. Pick service workflow
3. Foothold
4. Local enum
5. PrivEsc loop
6. Proof + move on

## Port → Workflow
- 80/443 → workflows/02_web.md
- 445 → workflows/03_smb.md
- 389/636/88 → workflows/04_ad.md
- 22 → services/ssh.md
- 21 → services/ftp.md
- 25/465/587 → services/smtp.md
- 5985/5986 → services/winrm.md
- 1433 → services/mssql.md
- 2049 → services/nfs.md
- 161 → services/snmp.md

## Jump Table
- Initial enum: workflows/01_initial_enum.md
- Web: workflows/02_web.md
- SMB: workflows/03_smb.md
- Linux PrivEsc: workflows/05_privesc_linux.md
- Windows PrivEsc: workflows/06_privesc_windows.md
- Pivoting/Tunneling: workflows/07_pivoting_tunneling.md

## Snippets
- Nmap: snippets/nmap.md
- Reverse shells: snippets/reverse_shells.md
- File transfer: snippets/file_transfer.md
- TTY stabilization: snippets/tty_stabilization.md

## Active Directory (Jump Table)
- AD start: active-directory/00_ad_start_here.md
- Recon map: active-directory/01_ad_recon_map.md
- Domain enum: active-directory/02_domain_enum.md
- Cred access: active-directory/03_credential_access.md
- Lateral: active-directory/04_lateral_movement.md
- PrivEsc: active-directory/05_privilege_escalation.md
- ACL abuse: active-directory/06_acl_abuse.md
- Kerberos: active-directory/08_kerberos_attacks.md
- ADCS: active-directory/09_adcs.md
- Coercion: active-directory/10_coercion_ntlm.md
- Relay: active-directory/11_relays.md

### AD Snippets
- snippets/ad/ad_command_map.md
- snippets/ad/netexec_cme.md
- snippets/ad/impacket.md
- snippets/ad/bloodhound.md
- snippets/ad/powerview.md
- snippets/ad/adcs_certipy.md
- snippets/ad/relay.md

### AD Checklists
- checklists/ad/ad_quick_triage.md
- checklists/ad/domain_enum_checklist.md
- checklists/ad/kerberos_checklist.md
- checklists/ad/adcs_checklist.md
- checklists/ad/relay_coercion_checklist.md
