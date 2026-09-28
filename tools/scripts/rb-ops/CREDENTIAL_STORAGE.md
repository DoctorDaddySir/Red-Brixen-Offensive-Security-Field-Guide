# Credential storage, migration and recovery (RB-006)

This optional utility is separate from the manual guide. Supported storage is a local POSIX/Linux filesystem with Python 3.11–3.14 and the pinned [dependency](requirements.txt). Use an owner-controlled engagement directory with no symbolic links or group/other write permission. Ancestors must be owned by the operator or system and must not permit another user to replace the path; sticky shared parents such as `/tmp` are allowed only when they protect an operator-owned child. All four Python commands secure `.redbrixen` to 0700 and the database/existing SQLite sidecars to 0600 before opening; new SQLite files inherit a private umask. Unsafe ownership, symlinks and multiply linked files are rejected. `rb-start` creates new workspace files with a private umask. Existing notes, artifacts and directories outside `.redbrixen` need their own review.

## Key and disclosure boundary

`RB_CREDENTIAL_KEY_FILE` contains a **path**, never key bytes. Create its parent as an owner-controlled directory (recommended 0700), keep the key outside the engagement directory, and run `rb-creds init-key` once from the engagement session. This creates a random 0600 key without overwriting existing files. Keep a separate protected key backup; never commit or bundle it with an engagement backup. Missing, unsafe, malformed or wrong keys fail closed and are never silently replaced. Losing the key loses access to protected secrets and backups. A compromised operator account can read the key and process memory; encryption does not defend against that account or root.

Secrets use the maintained library's [Fernet authenticated encryption](https://cryptography.io/en/latest/fernet/). Version-1 tokens include the credential ID and secret; decryption checks the ID to reject swapped rows. The original `credentials` columns and IDs remain, with `secret` empty after conversion; `credential_secrets` holds the version and token. Tokens expose their creation time. Metadata, arbitrary notes, findings, commands, external artifacts and terminal displays are **not** encrypted. Do not duplicate secrets into those fields.

`rb-creds add USERNAME` reads a hidden terminal prompt. The positional-secret interface is removed; invalid arguments are rejected without echoing their values. Hidden-input failure aborts. Do not pipe a secret or place it in argv or environment variables. `list` omits secrets; `list --show-secrets` decrypts deliberately. Client drafts and ordinary restricted exports need no key and never decrypt credential secrets. To disclose them into an owner-only restricted appendix, supply **both** `--restricted --include-secrets` to `rb-creds export` or `rb-report`. This does not scrub secret-looking text from notes. Old plaintext exports and shell history remain sensitive.

## Upgrade and migration

Stop all RB-OPS writers and other SQLite clients for the engagement. Install all four Python commands, the four shared modules, the complete `rb_ops` package and the dependency together as described in [installation](README.md#installation). Keep the activated virtual environment on PATH when running the installed commands. Do not mix old and new command versions: old commands can reintroduce plaintext.

For each engagement, inside its tmux session, in Bash:

```bash
install -d -m 700 ~/.config/redbrixen/keys ~/rb-private-backups
export RB_CREDENTIAL_KEY_FILE=~/.config/redbrixen/keys/example-engagement.key
rb-creds init-key
# Preserve this key separately in your approved encrypted/password-manager backup.
rb-creds migrate --backup ~/rb-private-backups/example-before-migration.rbbackup
rb-creds list
rb-creds list --show-secrets
```

Use new, engagement-specific key and backup filenames. If the key already exists, reuse the matching key and skip `init-key`. Never replace a missing key with a new one for an existing protected database.

Migration first validates any existing protected rows, then writes a consistent, encrypted, whole-database SQLite backup to a new 0600 file. It refuses to overwrite that backup. It encrypts legacy secrets in a transaction while preserving IDs, validation events and unrelated tables. A failed conversion rolls back. New credential addition refuses a database containing unmigrated legacy rows. Metadata views remain available during staged migration.

After conversion it runs SQLite secure deletion, VACUUM and WAL truncation. Repeated migration does not re-encrypt converted rows or overwrite the original backup, but retries the cleanup. A busy checkpoint is a failure: close other clients and rerun migration before treating cleanup as complete. A process interruption during conversion leaves either committed protected rows or the previous transaction state; inspect and rerun with a fresh backup filename if legacy rows remain. If only cleanup was interrupted, the existing backup filename is safe to reuse.

These checks remove the synthetic marker from the current tested database/WAL files. They cannot erase previously copied databases, old backups, snapshots, filesystem journals, SSD remnants, shell history, swap or secrets entered into free text. Retire those copies according to your storage policy. No claim of forensic erasure is made.

## Backup and recovery

From the stopped engagement, using its matching external key (take the pre-upgrade backup with the installed RB-006 version before upgrading to RB-011):

```bash
rb-creds backup --output ~/rb-private-backups/example-current.rbbackup
```

Backups encrypt the entire consistent database (including committed WAL state) and include a format marker. They contain all database tables, not external screenshots, notes or loot files. Back up those separately under appropriate protection. Keep keys separately. The backup implementation holds the database in memory; it is intended for modest local engagement databases, not large artifact stores. Backup/restore never accepts a plaintext backup file.

To rehearse recovery, create a **new** engagement with `rb-start`, select its tmux session and set `RB_CREDENTIAL_KEY_FILE` to the original matching key. Do not run database commands in that fresh engagement before restoring:

```bash
rb-creds restore --input ~/rb-private-backups/example-current.rbbackup
rb-creds list
rb-creds list --show-secrets
```

Restore authenticates the backup and validates database integrity before writing a new 0600 database. It refuses an existing database or SQLite sidecars, so it cannot overwrite later work. Wrong keys and damaged backups fail without creating a database. Restore interrupted while writing may leave an incomplete destination after a machine crash; keep the original backup and retry into another fresh engagement. Check expected IDs, validation history and finding details after recovery. Synthetic tests exercise both a protected backup and a pre-migration backup.

A pre-migration backup deliberately restores the original legacy state, including plaintext credential fields. Treat that recovered database as private and run migration with a new backup filename before further credential entry/disclosure. Do not downgrade current protected data: older commands cannot read the encrypted companion table. If code rollback is unavoidable, suspend credential writes/exports, retain current data and key, and restore the pre-migration backup only into an isolated fresh workspace. That backup does not contain later work; the original engagement remains untouched.

## Verification and limits

Run `python3 tests/validate.py` from the repository root after installing `requirements-dev.txt`. `tests/test_credentials.py` covers real-PTY hidden input without echo (with simulated tmux discovery), rejected positional values without secret echoes, real-file permissions under permissive umask across all four openers, symlink/hardlink and writable-ancestor rejection, missing/wrong keys, damaged/swapped tokens, migration rollback, plaintext-marker absence, preserved IDs/history/unrelated records, encrypted backup/recovery and explicit secret export. The existing export and finding-model regressions remain part of the suite.

On 2026-09-27, a separate isolated real tmux session also passed engagement discovery, external-key initialization, empty database initialization and encrypted backup/restore into a fresh engagement. Its temporary server used no user tmux configuration. That smoke check does not cover a complete populated tmux workflow; populated data and hidden entry are covered by the synthetic and PTY tests above.

Tests use synthetic local data. Windows ACLs, network filesystems, hostile processes running as the operator, full production backup infrastructure and power-loss fault injection are not validated. Real external assessments and guide labs are not run by these tests. Review these limitations before adopting the optional tools for sensitive work.

RB-011 adds explicit selection (`rb-creds --engagement NAME ...`) and generic schema migrations through the shared package. These migrations never decrypt or convert credential secrets. Credential conversion remains the explicit `migrate --backup` operation described above. See [lifecycle upgrade and recovery](LIFECYCLE.md#upgrade-and-recovery) before installing RB-011.
