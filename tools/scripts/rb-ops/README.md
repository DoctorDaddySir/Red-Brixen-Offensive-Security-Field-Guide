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

- `rb-creds`, `rb-chain`, `rb-findings`, and `rb-report` accept `--engagement NAME` before any subcommand, or use the active tmux session when no selector is supplied. The selected engagement must already exist.
- The current tmux session name is treated as the engagement name.
- Each engagement uses its own SQLite database:

```text
~/pentest/engagements/<engagement>/.redbrixen/opskit.db
```

This keeps credentials, findings, and exploit-chain data isolated per engagement.

## Installation

Run from this directory on Linux with Python 3.11–3.14, using an activated virtual environment. Credential encryption requires the pinned `cryptography` dependency. Keep all shared modules and the `rb_ops` package beside the installed commands:

```bash
python3 -m pip install -r requirements.txt
mkdir -p ~/bin
install -m 644 rb_exports.py ~/bin/rb_exports.py
install -m 644 rb_finding_model.py ~/bin/rb_finding_model.py
install -m 644 rb_private.py ~/bin/rb_private.py
install -m 644 rb_credentials.py ~/bin/rb_credentials.py
install -d -m 755 ~/bin/rb_ops
install -m 644 rb_ops/*.py ~/bin/rb_ops/
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
# Inside the engagement tmux session; use a separate key for each engagement.
install -d -m 700 ~/.config/redbrixen/keys
export RB_CREDENTIAL_KEY_FILE=~/.config/redbrixen/keys/example-engagement.key
rb-creds init-key
# Back up that key separately before storing secrets. Never put it in the repo.
rb-creds add svc_sql --host db01 --service mssql --source 'manual review'
# Enter the secret only at the hidden prompt. No positional secret is accepted.
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

- New credential secrets use authenticated encryption with a separate key. Existing plaintext records require explicit migration; see [credential migration and recovery](CREDENTIAL_STORAGE.md). Notes and other free text are not encrypted.
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

Default restricted filenames end in `.restricted.md` (for example `engagement_report.restricted.md`) and carry a restricted-data banner. `--output` remains supported; restricted exports require that suffix, while client drafts reject it. Restricted output includes legacy free text, and the combined report includes scope/engagement notes. Credential secrets are omitted unless `rb-creds export --restricted --include-secrets` or `rb-report --restricted --include-secrets` is used with the matching key. Free-text fields may still contain secrets entered there; this is not a text scrubber. Treat embedded links and images as private too; render only in an appropriately controlled environment and distribute the appendix separately under agreed handling.

All newly written export files use POSIX owner-read/write permissions (0600), including replacements, and are replaced atomically. Symbolic-link output destinations are rejected. Protect the parent directory and backups too; file permissions do not encrypt content. Export failures preserve an existing destination when replacement has not occurred.

### Upgrade and verification

Reinstall all four Python scripts, all four shared Python modules and the complete `rb_ops` package together, plus the credential dependency. Existing default output names remain unchanged. RB-006 adds a companion encrypted-secret table and changes secret entry/disclosure; follow [credential migration and recovery](CREDENTIAL_STORAGE.md) before upgrading existing engagements. Earlier exports are not retroactively scrubbed: review or regenerate them before delivery. To recover the former detailed output, use `--restricted`; do not downgrade to restore unsafe defaults. If reverting code is necessary, keep export use suspended until the safe version is restored. Metadata listing and validation remain local operator views. Credential addition now prompts invisibly; `list --show-secrets` requires the external key and migrated records.

Maintainer checks use synthetic SQLite data and mocked engagement resolution (no live client system):

```bash
python3 -m unittest discover -s tests -p 'test_rb_exports.py'
```

Run that command from the repository root. Tests exercise each exporter, unknown secrets in every text field, embedded attachment markup, private files, restricted detail, filename separation, permissions, malformed metadata, failure cleanup and copied/symlinked installation imports. POSIX/Linux behavior is tested; Windows ACL behavior and real tmux integration are not validated by this suite.


## Complete finding details (model version 1)

The optional findings tool can retain prerequisites, reproduction, expected/observed behavior, impact, remediation, limitations, scoring rationale, client priority, evidence references, review and retest records. These remain private operator data. A `reviewed` label records your review; it does not release any text into a default client export.

Start with [the editable JSON example](finding-details.example.json). Save a protected working copy in your own notes directory and fill in the actual observations. Inside the selected tmux engagement, obtain the finding ID from `rb-findings list`, then run in Bash:

```bash
read -r -p 'Existing finding ID: ' FINDING_ID
read -r -p 'Path to complete private finding-detail JSON: ' DETAIL_FILE
rb-findings details "$FINDING_ID" --file "$DETAIL_FILE"
rb-findings details "$FINDING_ID"
```

Expected: a save confirmation, followed by the stored JSON in the terminal. Treat the display and source file as private; they can contain secrets. The command replaces the **whole detail document**, not individual fields. Each changed document now records its previous and new state in private history. Use `rb-findings history ID` to inspect it. A recorded retest cannot be reset to `not_tested`; record a new supported decision instead. See [engagement selection, migrations and lifecycle](LIFECYCLE.md). Invalid documents and unknown finding IDs are rejected. Use `rb-findings export --restricted` or `rb-report --restricted` to include the actual detail in a restricted appendix. Default client drafts remain unchanged.

The top-level `model_version` must be integer `1`; unknown versions, duplicate JSON keys, missing/unknown fields and incorrect types fail validation. Empty draft fields mean “not recorded,” not an inferred success. Review status is `draft` or `reviewed`; reviewed records require a reviewer and a timezone-qualified timestamp.

Evidence is a list of objects containing `id`, `path`, `caption`, `captured_at`, `sha256`, and `redaction_status`. IDs must be unique; the path/reference is required. Timestamps, when recorded, require a time zone. An optional SHA-256 is 64 hexadecimal characters. Redaction status is `unreviewed`, `redacted`, or `no_redaction_needed`. References and hashes are operator supplied: these commands do not open attachments, verify their existence, compute digests, sanitize images or prove redaction.

Retest status is `not_tested`, `resolved`, `partial`, `unresolved`, or `unable_to_retest`. A recorded decision needs tester, timestamp and result/reason. Executed retests additionally require a method and `evidence_ids` referencing entries in the evidence list. This checks completeness of the record, not whether the conclusion is correct. Keep demonstrated impact separate from hypotheses and client priority separate from technical severity.

### Migration and recovery

Before upgrading, stop all writers and preserve a protected, consistent backup of the engagement database and any SQLite journal/WAL state using your normal SQLite backup procedure. Keep it under the same restricted handling as credentials. Installing files does not itself alter a database. RB-011 migrates the selected database transactionally on the first database command (including list/report/backup), adopting existing tables and backfilling version-1 empty finding details; repeated initialization preserves existing details. Original `findings` columns, IDs and values are unchanged. Newly saved findings receive an empty draft.

`rb-report` now uses the same schema migration entry point as the other commands; absent legacy details become empty drafts and render as “Not recorded.” An unsupported or malformed stored detail document fails restricted rendering instead of silently discarding fields. Default client exports never read these private documents. Do not mix older writers with RB-011: they do not record edit history or enforce schema compatibility. Keep the current database and any encrypted backup/key; the [lifecycle recovery procedure](LIFECYCLE.md#upgrade-and-recovery) describes safe rollback into an isolated workspace. Retain the database and JSON source copies; restore the full consistent backup only when intentionally rolling back data, since restoration discards later work.

Verification: synthetic legacy/new SQLite records, repeated/failed backfill, interactive add, JSON save/show, rejected malformed documents and unknown IDs, real-content restricted rendering, and default export isolation are exercised by `tests/test_finding_model.py`. Run `python3 -m unittest discover -s tests` from the repository root. Engagement resolution is mocked; live tmux, production backups and external evidence artifacts are not validated by these tests.


## Engagement selection and record lifecycle (RB-011)

The shared `rb_ops` package handles one selected engagement per invocation, private database opening, ordered transactional migrations, record edits and private history. `--engagement NAME` overrides tmux and must precede the subcommand; it never creates a missing engagement.

```bash
rb-chain --engagement example list
rb-findings --engagement example update 1 --title 'Reviewed finding title'
rb-findings --engagement example history 1
rb-chain --engagement example update 1 --outcome 'Confirmed with a negative control'
rb-chain --engagement example history 1
rb-report --engagement example
```

Follow [the lifecycle guide](LIFECYCLE.md) for retest JSON, migration/recovery, validation evidence and compatibility limits. History is private operator data and is not included in either default or restricted report exports. It begins when this version starts recording edits; it does not reconstruct earlier activity.
