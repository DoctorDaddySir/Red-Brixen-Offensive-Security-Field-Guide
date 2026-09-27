# Verification coverage and release acceptance

Status snapshot: 2026-09-27. This is the maintained acceptance checklist for the manual guide and optional tools. The [completion plan](../PROJECT_EVALUATION_AND_COMPLETION_PLAN.md) retains the historical baseline and broader roadmap. RB-012 introduces repeatable checks and gates; it does not declare a v1 release.

## Checks on every pull request

Run `python tests/validate.py` after installing [requirements-dev.txt](../requirements-dev.txt). The [workflow](../.github/workflows/validate.yml) runs that command on pull requests targeting master, pushes to master and manual dispatch, using Ubuntu 24.04 with Python 3.11 and 3.14. Actions are pinned to commit revisions and the workflow requests only read access to repository contents.

| Check | What a pass establishes | Limits |
| --- | --- | --- |
| Synthetic export tests | Default outputs exclude seeded private text and secrets; restricted exports are explicit; output permissions and write failures are covered | No real engagement data, tmux session or complete installation lifecycle is exercised |
| Finding-model tests | Repeatable migration, rollback on failed backfill, validation, CLI updates and rendering preserve synthetic records | Not a full credential migration or multi-engagement lifecycle test |
| Internal Markdown links | Parsed local links/images resolve within the repository | No external URLs, fragments, raw HTML links, malformed text that never renders as a link, or editorial correctness check |
| Saved lab records | Both registered records and their fixture sources exist; timestamps, tool metadata, assertions and limitations are present | Structural checks do not rerun a fixture, verify the truth of its assertions or prove it matches a changed command |
| Python/Bash parsing | Repository Python sources, extensionless Python commands and Bash scripts parse | Does not execute embedded guide commands or prove runtime correctness |

No assessment target is contacted by these checks. Dependency installation uses the package registry. CI is deliberately separate from privileged/container labs, which have additional prerequisites and explicit scope.

Require both `Python 3.11 checks` and `Python 3.14 checks` in the owner's branch protection/ruleset before relying on them as merge enforcement. The workflow alone cannot prevent a privileged owner from merging or publishing. RB-012 does not change repository rules or publish releases. GitHub documents [workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow) and [required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

## Recorded execution evidence

These are historical runs, not results of the validation command above.

| Fixture and record | Recorded environment/date | Assertions and limits |
| --- | --- | --- |
| [SSH/SOCKS lab](../labs/pivoting/README.md), [result](../labs/pivoting/ssh-socks-result.json) | 2026-09-26; Linux, OpenSSH 10.4p1, curl 8.21.0, ProxyChains 4.17 | Local forward/SOCKS/proxied proof, stopped-proxy failure, live direct control and cleanup; loopback TCP only |
| [Ligolo lab](../labs/ligolo/README.md), [result](../labs/ligolo/result.json) | 2026-09-26; Ligolo 0.9.2, Linux amd64, Docker 28.5.2; archive digests and image ID in record | Isolated routed HTTP proof, direct-path negative control, stopped tunnel, live agent control and resource cleanup; no Windows/DNS/UDP/listener/multi-hop validation |

When changing a fixture or a command it substantiates, rerun the relevant lab and review the new result with the code change. If execution is unavailable, leave the historical record dated, label the changed behavior unverified and keep the PR draft until required evidence is obtained. Never update only a timestamp or version to imply a new run. Add new record formats to `tests/check_lab_records.py` with failure-case coverage. Follow the [command verification standard](COMMAND_VERIFICATION.md).

## Manual guide release gate — open

Create a copy of this checklist for the proposed release and record its exact commit, reviewer, date and evidence links. A checked box needs reviewable evidence, not only a CI badge.

- [ ] Both CI jobs pass for the proposed release commit, and the reviewer inspects the rendered navigation and changed prose/code fences.
- [ ] Every supported domain/procedure is mapped to its prerequisites, versions, source references and actual execution evidence; deferred and untested coverage is explicitly labeled.
- [ ] Changed procedures include expected results, meaningful negative controls, evidence, cleanup and remediation/retest guidance. Duplicates, mislabeled headings and unsupported claims have been reviewed.
- [ ] External references on the release path have been checked and dated; transient failures have a recorded review outcome. Until a scheduled external-link checker is added, the maintainer records a monthly manual review and another before release.
- [ ] An independent reader completes both fictional pilot engagements from the completion plan (internal AD/Linux/Windows with a pivot, and web/API with multiple roles/tenants) without RB tools. Record confirmed/rejected findings, benign/blocked tests, cleanup, remediation and retest.
- [ ] Two complete manually editable synthetic client reports pass technical/editorial review, contain no unresolved placeholders or unintended private data, and distinguish observed from untested impact. Exam material remains separate.
- [ ] The release names a maintenance owner, records provenance/license review, versions, known limitations, release notes and an offline/navigation check.
- [ ] The repository owner reviews the evidence and approves publication. Record the release tag/commit and a rollback plan to the previous reviewed version.

None of the unchecked requirements above is implied complete by the merged correction tickets. Existing templates and partial lab evidence are inputs to this review, not substitutes for it.

## Optional RB-OPS release gate — open

RB-006 and RB-011 remain open in the 2026-09-27 snapshot. Their release gate is independent of the manual guide.

- [ ] Credential entry, storage, key handling, backup/recovery and explicit secret export meet RB-006 acceptance criteria with migration/restore fixtures.
- [ ] Engagement selection, shared migrations, editable records/history and lifecycle behavior meet RB-011 acceptance criteria.
- [ ] Clean install/help/diagnostics and actual tmux integration are exercised on documented supported platforms.
- [ ] Two simultaneous engagements, invalid/colliding paths, repeated/interrupted initialization and concurrent writes are covered.
- [ ] Finding/evidence integrity, scoring reference vectors, history/retests, missing artifacts, output collisions and deterministic exports are checked.
- [ ] Seeded private data remains absent from default exports; restricted artifacts, permissions, backup and recovery receive a documented review.
- [ ] Migration and rollback instructions are rehearsed on copies of synthetic legacy data; the owner approves a versioned utility release.

## Compatibility and rollback for RB-012

This ticket adds maintainer-only checks and documentation. It changes no engagement database, command interface or saved lab result. Remove/revert the RB-012 change to restore the earlier maintainer workflow; no data migration is needed. If these jobs have become required checks, update the ruleset when reverting so pull requests are not left waiting for removed jobs. Preserve any failed run evidence in the PR and fix the check or code before treating validation as passed.
