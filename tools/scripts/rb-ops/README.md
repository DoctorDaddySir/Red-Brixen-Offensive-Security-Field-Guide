# Red Brixen Security - RB-OPS

RB-OPS is a terminal-first engagement workspace toolkit for penetration testing workflows.

## Current Commands

- `rb-start` - initialize a new engagement workspace and tmux session
- `rb-host` - create a host-specific workspace
- `rb-web` - create a web-target workspace
- `rb-resume` - resume a detached tmux session and reopen VS Code
- `rb-stop` - detach from the current tmux session
- `rb-creds` - store and validate credentials in an engagement-local SQLite database
- `rb-chain` - track exploit-chain steps in an engagement-local SQLite database
- `rb-findings` - record findings with interactive CVSS scoring in an engagement-local SQLite database
- `rb-report` - generate a markdown report from engagement data

## Design Rules

- `rb-creds`, `rb-chain`, `rb-findings`, and `rb-report` must be run **inside an active tmux session**.
- The current tmux session name is treated as the engagement name.
- Each engagement uses its own SQLite database:

```text
~/pentest/engagements/<engagement>/.redbrixen/opskit.db
```

This keeps credentials, findings, and exploit-chain data isolated per engagement.

## Installation

```bash
install -m 755 rb-start ~/bin/rb-start
install -m 755 rb-host ~/bin/rb-host
install -m 755 rb-web ~/bin/rb-web
install -m 755 rb-resume ~/bin/rb-resume
install -m 755 rb-stop ~/bin/rb-stop
install -m 755 rb-creds ~/bin/rb-creds
install -m 755 rb-chain ~/bin/rb-chain
install -m 755 rb-findings ~/bin/rb-findings
install -m 755 rb-report ~/bin/rb-report
```

## Usage Examples

### Credentials

```bash
rb-creds add svc_sql 'Summer2026!' --host db01 --service mssql --source 'manual review'
rb-creds list --show-secrets
rb-creds validate 1 --host app01 --service winrm --notes 'validated over Evil-WinRM'
rb-creds export
```

### Attack Chain

```bash
rb-chain add 'Initial foothold via Jenkins Script Console' \
  --tactic exploit \
  --host jenkins01 \
  --command 'spawn reverse shell via console' \
  --outcome 'obtained www-data shell' \
  --evidence '06-evidence/jenkins_console.png'

rb-chain list
rb-chain export
```

### Findings

```bash
rb-findings add
rb-findings list
rb-findings export
```

### Reporting

```bash
rb-report
```

The generated report is written by default to:

```text
~/pentest/engagements/<engagement>/07-reporting/engagement_report.md
```

## Notes

- Secrets are currently stored in plaintext in SQLite. That is acceptable for a first local operator workflow, but not the final state.
- `rb-findings` uses CVSS v3.1 base metrics to calculate a score and severity.
- `rb-report` assembles findings, exploit-chain steps, credentials, and engagement notes into one markdown report.
