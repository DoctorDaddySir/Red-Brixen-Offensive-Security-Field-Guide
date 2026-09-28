# Engagement selection, migrations and lifecycle (RB-011)

These are optional local operator tools. They do not automate an assessment or replace the manual guide. RB-011 builds on RB-006's private file handling and explicit credential encryption/recovery. Install all four Python commands, the four helper modules and the complete `rb_ops` package using [the installation instructions](README.md#installation). Supported verification environments are Linux with Python 3.11–3.14.

## Select an existing engagement

Use a single global selector **before** the subcommand:

```bash
rb-findings --engagement example list
rb-chain --engagement example list
rb-creds --engagement example list
rb-report --engagement example
```

The selector names one existing directory under `PENTEST_BASE` (default `~/pentest/engagements`). It takes precedence over tmux, so it also works outside tmux. Without it, the active tmux session name selects the directory as before. There is no current-directory guessing, prefix matching or automatic creation; create a workspace explicitly with `rb-start` first.

Names are 1–128 characters, begin with an ASCII letter/digit, and contain only letters, digits, underscores, dots or hyphens. Paths, traversal components, whitespace, symbolic-link paths, duplicate selectors and nonexistent engagements fail. Matching is exact and case-sensitive on the tested Linux filesystem. Storage ancestry must satisfy RB-006's ownership and replacement restrictions. One invocation resolves the name and base directory once and closes its database connections when it finishes, including on errors.

## Schema migration

All four commands open databases through `rb_ops.database`. Any database operation, including listing, reporting or backup, adopts a legacy database transactionally:

1. Schema version 1 creates missing original tables and the encrypted-secret companion table, preserving existing rows and columns. Missing finding detail records receive the existing model-version-1 empty draft. Credential secrets are **not** decrypted or converted.
2. Schema version 2 adds private `record_history` and append-only update/delete guards. It starts with no historical events; past activity is not invented.

`rb_schema` records the installed schema version. Migration uses a write transaction; a failed step rolls back the whole upgrade and version change. Repeated opens do not repeat migration steps. Unknown future versions fail rather than being rewritten. Keep all command/package versions together; mixed older writers can bypass history and compatibility checks.

Two commands opening the same database serialize their migrations and writes through SQLite. Busy/locked operations fail with a nonzero result after SQLite's normal timeout; retry only after checking the outcome. Nested operations use savepoints so a failure does not commit unrelated caller work. The implementation does not promise distributed/network-filesystem locking or repair arbitrary corrupted schemas.

## Edit records

Findings support title, description, host and complete CVSS v3.1 base-vector edits:

```bash
rb-findings --engagement example update 1 --title 'Reviewed title' --host 'lab-host'
rb-findings --engagement example update 1 --vector 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N'
rb-chain --engagement example update 1 --order 2 --outcome 'Confirmed result'
```

Finding titles/descriptions must be nonempty; the host may be cleared with `--host ''`. A complete vector derives score and severity using the existing scoring routine; detached score/severity edits and incomplete, duplicate or unsupported vector metrics are rejected. See [severity scoring](../../../reporting/severity-scoring.md) for evidence and scoring limitations. Chain titles must be nonempty and order must be a positive integer. Other chain text fields may be cleared explicitly; omitted fields retain their values. Record IDs remain stable and missing IDs fail.

Each creation or changed edit writes the record and its history event in the same transaction. A history insertion failure rolls back the data mutation too. Concurrent partial-field updates preserve each other's untouched fields. Identical updates are no-ops; they do not add duplicate events. Full finding-detail documents remain **whole-document replacements**: read the latest version before preparing a replacement to avoid overwriting another operator's edits.

## Record a retest

First add the evidence reference to the finding's existing complete detail document using `rb-findings details ID --file DOCUMENT`. Keep its other fields and current retest values. The [finding detail example](finding-details.example.json) shows the full format.

Save the following decision object in a protected local JSON file. It is the `retest` object itself, not a full detail document. Replace its synthetic values with the actual observed method, result and previously recorded evidence ID:

```json
{
  "status": "resolved",
  "tester": "operator-name",
  "tested_at": "2026-09-28T12:00:00Z",
  "method": "Repeat the original action and its negative control",
  "result": "Original unauthorized action denied; authorized control succeeds",
  "evidence_ids": ["E-1"]
}
```

```bash
rb-findings --engagement example retest 1 --file /private/path/retest.json
rb-findings --engagement example history 1
```

Supported statuses are `not_tested`, `resolved`, `partial`, `unresolved` and `unable_to_retest`. A decision other than `not_tested` needs tester, timezone-qualified time and result/reason. Executed retests (`resolved`, `partial`, `unresolved`) also need a method and recorded evidence IDs. `unable_to_retest` records why execution was unavailable. Evidence files are references, not automatically opened or verified.

Once a decision has been recorded, it cannot be reset to `not_tested`, including through full detail replacement. A subsequent valid decision may change the result in any other direction, with its own supporting fields; the prior version remains in history. A later failure can therefore move a finding from `resolved` to `unresolved`. This validates the record, not whether a test was performed or the issue was actually fixed.

## Private history

```bash
rb-findings --engagement example history 1
rb-chain --engagement example history 1
```

History is displayed as JSON with event ID, action, local operating-system username, UTC timestamp and before/after content. A creation has a null `before`. Detail replacements that change the retest record receive action `retest`; other detail replacements receive `details`. Core field edits use `update`.

The application exposes no history update/delete command; database triggers reject ordinary updates/deletes. This is an operator change record, **not tamper-proof auditing** against the database owner/root, who can alter the database or drop triggers. Actor identity records the local account, not independent reviewer approval. History accepts finding/chain records only and never copies the credential tables or key material. Arbitrary finding/chain text can still contain sensitive information; keep terminal output and backups private.

Neither client drafts nor restricted reports include history. Restricted reports still show current private record detail, with credential secrets controlled separately by RB-006. Removed private text may remain in history; deleting it from the current record is not erasure.

## Upgrade and recovery

Before installing RB-011, stop all writers and use the installed RB-006 `rb-creds backup --output NEW_FILE` with the matching external key to make a consistent encrypted backup. Preserve the key separately. Also preserve external artifacts, which are not in the SQLite backup. Test recovery into a fresh workspace before replacing the old installation. See [credential recovery](CREDENTIAL_STORAGE.md) for the complete commands and key requirements.

After installing the complete RB-011 command/helper/package set, the next database command migrates the selected engagement. Verify current records and inspect history after a synthetic edit. There is no key prompt or secret conversion during generic migration. Legacy credentials still require RB-006's explicit `rb-creds migrate --backup NEW_FILE` before adding/revealing secrets.

If migration raises an error, preserve the database and pre-upgrade backup and resolve the reported incompatibility before retrying. The transaction tests cover an injected failure between steps; real process termination/power-loss recovery is delegated to SQLite and has not been fault-injected. Do not delete the schema version marker to force adoption.

For code rollback, suspend writes and retain the upgraded database and key. Restore the pre-upgrade encrypted backup into a fresh isolated engagement using the matching RB-006 tools/key. Never overwrite the current engagement: the old backup lacks later edits/history. Do not run older writers against an upgraded database because they do not append history or reject unknown versions. No destructive in-place downgrade is provided.

## Maintainer verification

Run `python3 tests/validate.py` after installing `requirements-dev.txt`. `tests/test_lifecycle.py` covers explicit selection/tmux fallback caching, rejected paths and duplicate selectors, concurrent independent engagements, concurrent initialization, version-1/legacy migration, unknown future versions, rollback after a failed schema step, finding/chain edits, retest transitions, history failure rollback, append-only guards, encrypted recovery preserving schema/history, and export isolation. Existing credential, finding model, link and export suites remain required. Installation checks exercise copied scripts and symbolic-link entry points with the package present.

On 2026-09-28, a separate real tmux session with user configuration disabled passed engagement discovery, populated chain/finding creation and edits, private history retrieval, and default report generation. The temporary server and records were removed afterward. Retest decisions and failure injection are covered by the automated tests, not that tmux smoke check.

All fixtures are synthetic. This suite does not establish a full engagement workflow, Windows support, network-filesystem behavior, production recovery, hostile same-account protection or guide-lab execution.
