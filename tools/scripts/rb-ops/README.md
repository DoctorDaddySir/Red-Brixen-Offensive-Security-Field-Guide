# Red Brixen Security - RB-OPS

RB-OPS is an optional terminal-first engagement workspace toolkit. The field guide, manual procedures, and standalone reporting templates do not require these commands, tmux, SQLite, or the generated directory structure. The dependencies below apply only when a tester chooses to use RB-OPS.

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

Run from this directory with Python 3 available. Keep the shared module beside the installed commands:

```bash
mkdir -p ~/bin
install -m 644 rb_exports.py ~/bin/rb_exports.py
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

- Secrets are currently stored in plaintext in SQLite; credential storage protections are tracked separately in RB-006.
- `rb-findings` uses CVSS v3.1 base metrics to calculate a score and severity.
- `rb-report` generates a client draft with record references; operator prose is available only in explicitly restricted exports.


## Client drafts and restricted appendices

The four export commands (`rb-report`, `rb-creds export`, `rb-chain export`, `rb-findings export`) default to a **manual client draft**. Existing database text has no reviewed/public classification. Defaults therefore include only record IDs, validated numeric finding scores and recorded credential-validation status, plus placeholders for your reviewed prose. Names, assets, descriptions, vectors, commands, outcomes, sources, notes, timestamps and attachment references are omitted, including the engagement/session name. This avoids guessing whether arbitrary text or an embedded image contains a secret. The database is unchanged.

Fill in the draft using the [standalone finding template](../../../exploited-vulns/_TEMPLATE/finding_template.md), review the actual results and add separately reviewed/redacted evidence. A recorded validation flag is an operator assertion, not a fresh authentication test. A stored score is not revalidated against its vector by the exporter. No export copies attachment files or sanitizes their contents. The guide and templates remain usable without RB tools.

When operator detail is necessary, explicitly select a restricted appendix:

```bash
rb-report --restricted
rb-creds export --restricted
rb-chain export --restricted
rb-findings export --restricted
```

Default restricted filenames end in `.restricted.md` (for example `engagement_report.restricted.md`) and carry a restricted-data banner. `--output` remains supported; restricted exports require that suffix, while client drafts reject it. Restricted output includes the legacy free text and raw secrets, and the combined report includes scope/engagement notes. Treat embedded links and images as private too; render only in an appropriately controlled environment and distribute the appendix separately under agreed handling.

All newly written export files use POSIX owner-read/write permissions (0600), including replacements, and are replaced atomically. Symbolic-link output destinations are rejected. Protect the parent directory and backups too; file permissions do not encrypt content. Export failures preserve an existing destination when replacement has not occurred.

### Upgrade and verification

Reinstall all four scripts **and** `rb_exports.py` together. Existing default output names and database schemas remain unchanged. Earlier exports are not retroactively scrubbed: review or regenerate them before delivery. To recover the former detailed output, use `--restricted`; do not downgrade to restore unsafe defaults. If reverting code is necessary, keep export use suspended until the safe version is restored. Existing add/list/update/validate operations retain their behavior and are local operator views, not client exports.

Maintainer checks use synthetic SQLite data and mocked engagement resolution (no live client system):

```bash
python3 -m unittest discover -s tests -p 'test_rb_exports.py'
```

Run that command from the repository root. Tests exercise each exporter, unknown secrets in every text field, embedded attachment markup, private files, restricted detail, filename separation, permissions, malformed metadata, failure cleanup and copied/symlinked installation imports. POSIX/Linux behavior is tested; Windows ACL behavior and real tmux integration are not validated by this suite.
