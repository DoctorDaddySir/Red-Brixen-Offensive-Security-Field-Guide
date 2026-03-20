#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="${OSCP_EXAM_BASE:-$HOME/oscp/exams}"

read -rp "Engagement name: " ENGAGEMENT_NAME
if [[ -z "${ENGAGEMENT_NAME// }" ]]; then
  echo "[-] Engagement name cannot be empty."
  exit 1
fi

slugify() {
  echo "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/_/g; s/^_+//; s/_+$//'
}

SESSION_NAME="$(slugify "$ENGAGEMENT_NAME")"
ENGAGEMENT_DIR="$BASE_DIR/$SESSION_NAME"

if [[ -e "$ENGAGEMENT_DIR" ]]; then
  echo "[-] Directory already exists: $ENGAGEMENT_DIR"
  exit 1
fi

mkdir -p "$ENGAGEMENT_DIR"

mkdir -p \
  "$ENGAGEMENT_DIR/Active_Directory/hosts/host1"/{post_exploitation,privesc,proof,recon,screenshots} \
  "$ENGAGEMENT_DIR/Active_Directory/hosts/host2"/{post_exploitation,privesc,proof,recon,screenshots} \
  "$ENGAGEMENT_DIR/Active_Directory/hosts/host3"/{post_exploitation,privesc,proof,recon,screenshots} \
  "$ENGAGEMENT_DIR/00-reporting"/{images,notes,proofs} \
  "$ENGAGEMENT_DIR/Standalone_1"/{post_exploitation,privesc,proof,recon,screenshots} \
  "$ENGAGEMENT_DIR/Standalone_2"/{post_exploitation,privesc,proof,recon,screenshots} \
  "$ENGAGEMENT_DIR/Standalone_3"/{post_exploitation,privesc,proof,recon,screenshots} \
  "$ENGAGEMENT_DIR/zz-worksheets/privesc" \
  "$ENGAGEMENT_DIR/zz-worksheets/reporting"

cat > "$ENGAGEMENT_DIR/progress.md" <<'EOF_PROGRESS'
# OSCP+ Points Tracker

**Target:** 70 Points  
**Current Total:** 0  

---

# 🖥️ Standalone Targets

| Target        | IP | Local (10) | Proof (10) | Points |
|--------------|----|------------|------------|--------|
| standalone_1 |    | ❌         | ❌         | 0      |
| standalone_2 |    | ❌         | ❌         | 0      |
| standalone_3 |    | ❌         | ❌         | 0      |

**Standalone Subtotal:** 0 / 60

---

# 🌐 Active Directory Environment

## 🧑‍💻 Domain Machines (10 pts each)

| Target     | IP | Local (10) | Points |
|------------|----|------------|--------|
| domain_1   |    | ❌         | 0      |
| domain_2   |    | ❌         | 0      |

**Domain Machines Subtotal:** 0 / 20

---

## 🏰 Domain Controller (20 pts)

| Target | IP | Proof (20) | Points |
|--------|----|------------|--------|
| DC     |    | ❌         | 0      |

**DC Subtotal:** 0 / 20

---

# 🔢 TOTAL

**Standalone:** 0  
**AD Domain Machines:** 0  
**Domain Controller:** 0  

## ➡️ GRAND TOTAL: 0 / 100

---

# ⚡ Quick Update Guide

- Local flag → mark ✅ and add points  
- Proof flag → mark ✅ and add points  
- Update subtotal immediately (no mental math later)

---

# 🚨 Pass Condition

- [ ] 70+ points reached  
- [ ] All obtained flags have proof + screenshots
EOF_PROGRESS

cat > "$ENGAGEMENT_DIR/Active_Directory/AD_WORKSHEET.md" <<'EOF_AD'
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
EOF_AD

cat > "$ENGAGEMENT_DIR/zz-worksheets/privesc/linux_enum_worksheet.md" <<'EOF_LINUX'
# Linux Host Enumeration Worksheet

## Target Info

* IP:
* Hostname:
* Domain (if any):
* Initial Access Method:

---

## Port Scan Results

### Open Ports

*

### Service Versions

*

### Notes

*

---

## Initial Foothold

* User:
* Shell Type:
* Stability (TTY?):
* Entry Vector:

---

## System Info

```bash
uname -a
cat /etc/os-release
id
```

* OS:
* Kernel:
* Architecture:
* Current User:
* Groups:

---

## Network Info

```bash
ip a
netstat -tulnp
```

* Interfaces:
* Internal Services:
* Pivot Opportunities:

---

## Users & Credentials

```bash
cat /etc/passwd
```

* Users:
* Interesting Accounts:
* Passwords Found:
* SSH Keys:

---

## Sudo

```bash
sudo -l
```

* Allowed Commands:
* Exploitable?:

---

## SUID / Capabilities

```bash
find / -perm -4000 2>/dev/null
getcap -r / 2>/dev/null
```

* SUID Findings:
* Capability Findings:

---

## File System

* Writable Directories:
* Writable Files:
* Sensitive Files:
* Backups:

---

## Cron Jobs

```bash
crontab -l
ls -la /etc/cron*
```

* Jobs:
* Writable Scripts:
* Execution Context:

---

## Processes

```bash
ps aux
```

* Interesting Processes:
* Custom Scripts:

---

## Applications / Services

* Web apps:
* Databases:
* Custom apps:

---

## Credential Hunting

* Config Files:
* Hardcoded Credentials:
* Reused Credentials:

---

## Privilege Escalation Paths

* Path 1:
* Path 2:
* Path 3:

---

## Loot

* Flags:
* Credentials:
* Sensitive Data:

---

## Proof

* user.txt:
* proof.txt:

---

## Notes

*
EOF_LINUX

cat > "$ENGAGEMENT_DIR/zz-worksheets/privesc/windows_enum_worksheet.md" <<'EOF_WINDOWS'
# Windows Host Enumeration Worksheet

## Target Info

* IP:
* Hostname:
* Domain:
* Initial Access Method:

---

## Port Scan Results

### Open Ports

*

### Service Versions

*

### Notes

*

---

## Initial Foothold

* User:
* Access Method (WinRM/RDP/Shell):
* Privilege Level:
* Entry Vector:

---

## System Info

```powershell
systeminfo
whoami
whoami /groups
whoami /priv
```

* OS Version:
* Hostname:
* Domain:
* Current User:
* Privileges:

---

## Network Info

```powershell
ipconfig /all
netstat -ano
```

* Interfaces:
* Internal Services:
* Pivot Opportunities:

---

## Users & Groups

```powershell
net user
net localgroup
```

* Users:
* Admins:
* Interesting Groups:

---

## Credentials

* Stored Credentials (`cmdkey /list`):
* Found Passwords:
* Config Files:
* Registry Findings:

---

## SMB / Shares

```powershell
net share
```

* Shares:
* Writable Shares:
* Interesting Files:

---

## Services

```powershell
sc query
Get-WmiObject Win32_Service
```

* Vulnerable Services:
* Writable Paths:
* SYSTEM Services:

---

## Scheduled Tasks

```powershell
schtasks /query /fo LIST /v
```

* Tasks:
* SYSTEM Tasks:
* Writable Scripts:

---

## File System

* Writable Directories:
* Writable Files:
* Sensitive Files:

---

## Installed Applications

```powershell
wmic product get name,version
```

* Interesting Software:
* Potential Vulns:

---

## Processes

```powershell
tasklist /v
```

* SYSTEM Processes:
* Interesting Targets:

---

## AD Enumeration (if applicable)

* Users:
* Groups:
* SPNs:
* Sessions:
* BloodHound Notes:

---

## Privilege Escalation Paths

* Path 1:
* Path 2:
* Path 3:

---

## Loot

* Flags:
* Credentials:
* Hashes:
* Tickets:

---

## Proof

* user.txt:
* proof.txt:

---

## Notes

*
EOF_WINDOWS

cat > "$ENGAGEMENT_DIR/zz-worksheets/reporting/oscp-report.md" <<'EOF_REPORT'
# OffSec Certified Professional (OSCP) Exam Report

**Student:** [perry.t.shelton@gmail.com](mailto:perry.t.shelton@gmail.com)
**OSID:** XXXXX

---

# 1. Introduction

This report documents the penetration testing activities conducted during the OffSec Certified Professional (OSCP) exam. The objective is to demonstrate a methodical approach to identifying and exploiting vulnerabilities within the target environment.

---

# 2. Objective

Perform an internal penetration test against the provided exam network. Identify vulnerabilities, exploit them, and document the process in a clear and reproducible manner.

---

# 3. Requirements

This report includes:

* High-Level Summary
* Methodology
* Detailed findings per target
* Screenshots and proof files
* Step-by-step reproduction steps

---

# 4. High-Level Summary

A penetration test was conducted against the internal lab environment. Multiple vulnerabilities were identified and successfully exploited, leading to administrative-level access on several systems.

The primary issues identified include:

* Weak credentials
* Misconfigured services
* Outdated software

---

## 4.1 Recommendations

* Apply security patches regularly
* Enforce strong password policies
* Disable unnecessary services
* Restrict anonymous access

---

# 5. Methodology

## 5.1 Information Gathering

* Identified target IP ranges
* Performed host discovery

## 5.2 Service Enumeration

* Conducted port scans (Nmap)
* Identified running services and versions

## 5.3 Exploitation

* Identified vulnerabilities
* Developed and executed exploits

## 5.4 Privilege Escalation

* Enumerated system misconfigurations
* Leveraged privilege escalation techniques

## 5.5 Post Exploitation

* Retrieved proof files
* Maintained access where necessary

---

# 6. Independent Challenges

---

## 6.1 Target #1 – <IP ADDRESS>

### 6.1.1 Vulnerability Summary

**Description:**
Explain the vulnerability.

**Impact:**
Explain what access was gained.

**Severity:** Critical / High / Medium / Low

**Fix:**
Explain remediation steps.

---

### 6.1.2 Enumeration

```bash
nmap -sC -sV -oA initial <IP>
```

**Findings:**

* Port XX: Service
* Port XX: Service

---

### 6.1.3 Exploitation (Initial Access)

**Steps:**

1. Describe step
2. Describe step

```bash
# Commands used
```

---

### 6.1.4 Privilege Escalation

**Technique Used:**

* Example: AlwaysInstallElevated

```bash
# Commands used
```

---

### 6.1.5 Proof

**local.txt**

```text
<value>
```

**proof.txt**

```text
<value>
```

**Screenshots:**

* Include terminal showing proof.txt and IP

---

### 6.1.6 Steps to Reproduce

1. Run initial scan:

```bash
nmap -sC -sV <IP>
```

2. Access service:

```bash
<command>
```

3. Exploit vulnerability:

```bash
<command>
```

4. Escalate privileges:

```bash
<command>
```

---

# 7. Active Directory Set

---

## 7.1 <Machine Name> – <IP>

### 7.1.1 Initial Access

**Vulnerability:**

* Description

```bash
# Commands
```

---

### 7.1.2 Privilege Escalation

**Technique:**

* Description

```bash
# Commands
```

---

### 7.1.3 Post Exploitation

* Lateral movement
* Credential harvesting

---

## 7.2 <Next Machine>

(Repeat structure for each machine)

---

# 8. Conclusion

The assessment demonstrated multiple critical vulnerabilities that allowed full compromise of the environment. Proper patching, credential management, and system hardening are recommended.

---
EOF_REPORT

cp "$ENGAGEMENT_DIR/zz-worksheets/privesc/windows_enum_worksheet.md" "$ENGAGEMENT_DIR/Active_Directory/hosts/host1/windows_enum_worksheet.md"
cp "$ENGAGEMENT_DIR/zz-worksheets/privesc/windows_enum_worksheet.md" "$ENGAGEMENT_DIR/Active_Directory/hosts/host2/windows_enum_worksheet.md"
cp "$ENGAGEMENT_DIR/zz-worksheets/privesc/windows_enum_worksheet.md" "$ENGAGEMENT_DIR/Active_Directory/hosts/host3/windows_enum_worksheet.md"
# Copy privesc worksheets into Standalone targets (both Linux and Windows)
cp "$ENGAGEMENT_DIR/zz-worksheets/privesc/linux_enum_worksheet.md" "$ENGAGEMENT_DIR/Standalone_1/linux_enum_worksheet.md"
cp "$ENGAGEMENT_DIR/zz-worksheets/privesc/windows_enum_worksheet.md" "$ENGAGEMENT_DIR/Standalone_1/windows_enum_worksheet.md"

cp "$ENGAGEMENT_DIR/zz-worksheets/privesc/linux_enum_worksheet.md" "$ENGAGEMENT_DIR/Standalone_2/linux_enum_worksheet.md"
cp "$ENGAGEMENT_DIR/zz-worksheets/privesc/windows_enum_worksheet.md" "$ENGAGEMENT_DIR/Standalone_2/windows_enum_worksheet.md"

cp "$ENGAGEMENT_DIR/zz-worksheets/privesc/linux_enum_worksheet.md" "$ENGAGEMENT_DIR/Standalone_3/linux_enum_worksheet.md"
cp "$ENGAGEMENT_DIR/zz-worksheets/privesc/windows_enum_worksheet.md" "$ENGAGEMENT_DIR/Standalone_3/windows_enum_worksheet.md"


if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "[-] tmux session already exists: $SESSION_NAME"
  exit 1
fi

# Build tmux environment
# command  -> engagement root
# AD-base  -> Active_Directory
# AD1-3    -> Active_Directory/hosts/host1-3
# SA1-3    -> Standalone_1-3

tmux start-server

tmux new-session -d -s "$SESSION_NAME" -n "command" -c "$ENGAGEMENT_DIR"
tmux set-option -t "$SESSION_NAME" -g mouse on
tmux set-option -t "$SESSION_NAME" -g history-limit 200000
tmux set-option -t "$SESSION_NAME" -g remain-on-exit on
tmux set-option -t "$SESSION_NAME" -g base-index 1
tmux set-option -t "$SESSION_NAME" -g pane-base-index 1
tmux set-option -t "$SESSION_NAME" -g renumber-windows on

tmux set-environment -t "$SESSION_NAME" ENGAGEMENT_NAME "$ENGAGEMENT_NAME"
tmux set-environment -t "$SESSION_NAME" ENGAGEMENT_DIR "$ENGAGEMENT_DIR"

tmux new-window -t "$SESSION_NAME" -n "AD-base" -c "$ENGAGEMENT_DIR/Active_Directory"
tmux new-window -t "$SESSION_NAME" -n "AD1" -c "$ENGAGEMENT_DIR/Active_Directory/hosts/host1"
tmux new-window -t "$SESSION_NAME" -n "AD2" -c "$ENGAGEMENT_DIR/Active_Directory/hosts/host2"
tmux new-window -t "$SESSION_NAME" -n "AD3" -c "$ENGAGEMENT_DIR/Active_Directory/hosts/host3"
tmux new-window -t "$SESSION_NAME" -n "SA1" -c "$ENGAGEMENT_DIR/Standalone_1"
tmux new-window -t "$SESSION_NAME" -n "SA2" -c "$ENGAGEMENT_DIR/Standalone_2"
tmux new-window -t "$SESSION_NAME" -n "SA3" -c "$ENGAGEMENT_DIR/Standalone_3"

# Seed each window with a clean prompt in the correct directory
for window in command AD-base AD1 AD2 AD3 SA1 SA2 SA3; do
  tmux send-keys -t "$SESSION_NAME:$window" "clear" C-m
  tmux send-keys -t "$SESSION_NAME:$window" "pwd" C-m
  tmux send-keys -t "$SESSION_NAME:$window" "clear" C-m
done

# Put useful files in front of you immediately
# command window -> root tracker
# AD-base window -> AD worksheet

tmux send-keys -t "$SESSION_NAME:command" "echo '[*] Engagement: $ENGAGEMENT_NAME'" C-m
tmux send-keys -t "$SESSION_NAME:command" "echo '[*] Root: $ENGAGEMENT_DIR'" C-m
tmux send-keys -t "$SESSION_NAME:command" "echo '[*] Tracker: $ENGAGEMENT_DIR/progress.md'" C-m

tmux send-keys -t "$SESSION_NAME:AD-base" "echo '[*] AD worksheet: $ENGAGEMENT_DIR/Active_Directory/AD_WORKSHEET.md'" C-m

tmux select-window -t "$SESSION_NAME:command"

echo "[+] Engagement directory created: $ENGAGEMENT_DIR"
echo "[+] tmux session created: $SESSION_NAME"
echo "[+] Windows: command, AD-base, AD1, AD2, AD3, SA1, SA2, SA3"
exec tmux attach-session -t "$SESSION_NAME"
