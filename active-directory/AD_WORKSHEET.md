# Active Directory Domain Worksheet

## Purpose

This worksheet is for **domain-wide** AD tracking during an engagement or exam.

Use it to capture:
- environment structure
- credentials
- attack paths
- lateral movement options
- escalation opportunities

Priority order:
1. Domain basics
2. Credentials and access
3. Users / groups / hosts
4. Kerberos / BloodHound paths
5. Lateral movement and escalation
6. Persistence / cleanup notes

---

# 00. DOMAIN OVERVIEW (HIGHEST PRIORITY)

## Domain Identity
- Domain Name:
- NetBIOS Name:
- Forest:
- Functional Level:
- Time Source / Clock Skew Notes:

## Domain Controllers
| Hostname | IP | OS | Notes |
|---|---:|---|---|
|  |  |  |  |

## DNS / AD Discovery
- DNS Server(s):
- LDAP Server(s):
- Kerberos Server(s):
- Global Catalog(s):
- ADCS Present?:
- Multiple Domains / Trusts?:

## Key Commands / Sources Used
- 
- 
- 

---

# 01. INITIAL ACCESS / KNOWN CREDENTIALS (TOP PRIORITY)

## Known Credentials
| Username | Domain | Password / Hash / Ticket | Source | Validated Against | Privilege Level | Notes |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Local Admin / Remote Access Wins
| Host | Account | Access Type (SMB/WinRM/RDP/SSH) | Confirmed? | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## High-Value Credential Sources Found
- SYSVOL / GPP:
- Shares:
- Config files:
- Scripts:
- DB credentials:
- Saved creds / cmdkey:
- Browser / history:
- LSASS / SAM / NTDS possibilities:
- Certificates / PFX / PEM:
- Notes:

---

# 02. USER ENUMERATION (VERY HIGH PRIORITY)

## User Summary
- Total Identified Users:
- Likely Admin Users:
- Service Accounts:
- Disabled Accounts:
- Stale / Old Accounts:
- Accounts with Descriptions:
- Accounts with "Password Never Expires":

## Important Users
| Username | Display Name | Description | Group Membership | Last Logon Clues | Notes |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Username Patterns
- Format observed:
- Email format:
- Naming conventions:
- Password spray candidate format:
- Notes:

---

# 03. GROUPS / PRIVILEGE MODEL (VERY HIGH PRIORITY)

## High-Value Groups
| Group | Members Identified | Why Important | Notes |
|---|---|---|---|
| Domain Admins |  |  |  |
| Enterprise Admins |  |  |  |
| Administrators |  |  |  |
| Account Operators |  |  |  |
| Server Operators |  |  |  |
| Backup Operators |  |  |  |
| Print Operators |  |  |  |
| Remote Desktop Users |  |  |  |
| DnsAdmins |  |  |  |
| Group Policy Creator Owners |  |  |  |

## Interesting Delegated / Custom Groups
| Group | Members | Rights / Relevance | Notes |
|---|---|---|---|
|  |  |  |  |

## Privilege Relationships
- Which groups appear to control others:
- Any nested group surprises:
- Any service accounts in privileged groups:
- Notes:

---

# 04. HOST / COMPUTER ENUMERATION (VERY HIGH PRIORITY)

## Host Summary
- Total Hosts Identified:
- Workstations:
- Servers:
- File Servers:
- SQL Servers:
- Web Servers:
- Management Hosts:
- Jump Hosts:
- Unknown / Custom Roles:

## Important Hosts
| Hostname | IP | Role | OS | Admin Access? | Interesting Services | Notes |
|---|---:|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Hosts with Confirmed Access
| Host | Account | Access Type | Current Privilege | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Internal Network Segments / Reachability
- Subnets discovered:
- Hosts only reachable through pivot:
- Management VLAN clues:
- Notes:

---

# 05. SMB / SHARE INTELLIGENCE (HIGH PRIORITY)

## High-Value Shares
| Host | Share | Access (R/W) | Interesting Contents | Credential Value | Notes |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## SYSVOL / NETLOGON Findings
- Login scripts:
- Batch / PowerShell scripts:
- Credentials:
- cpassword / GPP:
- GPO references:
- Notes:

## Other Useful File Findings
- Backups:
- Config files:
- Deployment files:
- Password lists:
- KeePass / vault files:
- Notes:

---

# 06. KERBEROS ATTACK SURFACE (HIGH PRIORITY)

## AS-REP Roastable Users
| Username | Confirmed? | Hash Captured? | Cracked? | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Kerberoast Targets (SPNs)
| Account | SPN | Privilege Clues | Hash Captured? | Cracked? | Notes |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Ticket / Kerberos Notes
- TGTs obtained:
- TGSs obtained:
- Pass-the-ticket options:
- Delegation issues identified:
- Clock skew problems:
- Notes:

---

# 07. BLOODHOUND / GRAPH PATHS (HIGH PRIORITY)

## BloodHound Collection Status
- Collected?:
- Scope:
- Any collection gaps:
- Notes:

## Top Attack Paths
| Path # | Starting Principal | Target | Technique / Relationship | Complexity | Notes |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |

## Key Relationships Found
- GenericAll:
- GenericWrite:
- WriteDACL:
- WriteOwner:
- AddMember:
- ForceChangePassword:
- AllowedToDelegate:
- Constrained Delegation:
- RBCD:
- DCSync rights:
- Notes:

---

# 08. CREDENTIAL ACCESS TRACKER (HIGH PRIORITY)

## Hashes / Secrets
| Type | Account | Source | Value Stored? | Cracked? | Notes |
|---|---|---|---|---|---|
| NTLM |  |  |  |  |  |
| Kerberos |  |  |  |  |  |
| SAM |  |  |  |  |  |
| LSA Secrets |  |  |  |  |  |
| GPP cpassword |  |  |  |  |  |
| Browser creds |  |  |  |  |  |

## Password Reuse Patterns
- Same password on multiple users:
- Local admin password reuse:
- Service password reuse:
- Domain-to-local reuse:
- Notes:

---

# 09. LATERAL MOVEMENT TRACKER (HIGH PRIORITY)

## Successful Movement
| From Host | To Host | Account Used | Method | Result | Notes |
|---|---|---|---|---|---|
|  |  |  | SMB / WinRM / RDP / PSExec / WMI / SSH |  |  |

## Candidate Next Moves
| Target Host | Reason It Matters | Likely Access Method | Required Creds / Conditions | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Sessions / Logged-On Users
| Host | User | Source | High Value? | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

---

# 10. DOMAIN PRIVILEGE ESCALATION (HIGH PRIORITY)

## Current Best Escalation Paths
| Path | Starting Point | End Goal | Technique | Confidence | Notes |
|---|---|---|---|---:|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |

## Common Escalation Categories
- Group membership abuse:
- ACL abuse:
- GPO abuse:
- Token abuse:
- Delegation abuse:
- Kerberos abuse:
- ADCS abuse:
- NTLM relay:
- DCSync:
- Notes:

---

# 11. ACL ABUSE TRACKER

## Writable / Controllable Objects
| Principal Controlled | Object | Right | Exploit Idea | Executed? | Notes |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Candidate Actions
- Reset password:
- Add user to group:
- Add SPN:
- Shadow credentials:
- WriteDACL escalation:
- Ownership change:
- Notes:

---

# 12. GPO ABUSE TRACKER

## Interesting GPOs
| GPO Name | Linked To | Writable? | Abuse Opportunity | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## GPO Findings
- Startup scripts:
- Scheduled tasks:
- Restricted groups:
- Local users/groups changes:
- Immediate task possibilities:
- Notes:

---

# 13. ADCS TRACKER

## ADCS Presence
- Found?:
- CA Name:
- Enrollment Web?:
- Vulnerable Templates?:
- ESC paths suspected:
- Notes:

## Certificates / Templates
| Template | Vulnerability Clue | Exploit Candidate | Notes |
|---|---|---|---|
|  |  |  |  |

---

# 14. COERCION / RELAY TRACKER

## Coercion Opportunities
| Source Host | Technique | Relay Target | Potential Result | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Relay Notes
- SMB signing status:
- LDAP relay candidates:
- HTTP relay candidates:
- ntlmrelayx usage:
- Results:
- Notes:

---

# 15. DCSYNC / DOMAIN DOMINANCE CHECK

## DCSync Candidates
| Principal | Why Candidate | Rights Confirmed? | Executed? | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Domain Dominance Indicators
- Domain Admin access:
- Enterprise Admin access:
- DCSync rights:
- KRBTGT material:
- Full DC code execution:
- Notes:

---

# 16. PERSISTENCE / CLEANUP (LOWER PRIORITY, BUT TRACK)

## Persistence Options Considered
| Method | Planted? | Scope | Risk | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Cleanup Needed
- Users added:
- Groups modified:
- Services changed:
- Scheduled tasks added:
- Files uploaded:
- Certs issued:
- GPOs modified:
- Notes:

---

# 17. PRIORITY BOARD (LIVE USE SECTION)

## Immediate Next 3 Actions
1. 
2. 
3. 

## Best Current Credential
- Account:
- Why it matters:
- Where to test next:

## Best Current Host Target
- Host:
- Why it matters:
- Access method:

## Best Current Escalation Path
- Path:
- Why it is best:
- Blocking issue:

---

# 18. NOTES / RAW OBSERVATIONS

- 
- 
- 
- 

---

# 19. ENGAGEMENT STATUS SNAPSHOT

## Current Access Level
- Initial foothold:
- Current best account:
- Current best host:
- Highest privilege obtained:
- Domain-wide control obtained?:

## Confidence
- Enumeration completeness: /10
- Credential picture: /10
- Lateral movement coverage: /10
- Escalation path clarity: /10

## Final Thoughts
- 