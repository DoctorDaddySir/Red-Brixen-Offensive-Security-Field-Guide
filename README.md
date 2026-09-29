# Red Brixen Offensive Security Field Guide

A manual reference for penetration testers: practical procedures, copyable commands, result interpretation, evidence collection, remediation, and reporting.

The tester chooses and performs each task. Every guide must be usable independently of RB binaries, a database, a generated workspace, or an automated lab. Use your own notes, evidence folders, and preferred reporting tools.

## Current status — 2026-09-28

The manual reference is under active development. Core corrections and reporting references have merged, but the comprehensive v1 release gates are still open. The completion plan describes the original assessment and future scope; it is not a current completion report.

| Area | Implemented | Remaining limits |
| --- | --- | --- |
| Guide structure | Manual-first entry points, canonical indexes and checked local links; corrected Windows, pivoting, ProxyChains and token-privilege material | Legacy pages still vary in depth and verification; an index does not establish validated coverage |
| Active Directory | Starting map and explicit coverage/deferred-topic labels | Deferred topics and broad AD/Windows lab verification remain incomplete |
| Scope and reporting | Scope-aware testing/cleanup, standalone client and exam templates, evidence-backed versioned severity guidance | Complete synthetic engagement reports and independent end-to-end review remain release requirements |
| Recorded command evidence | SSH/SOCKS/ProxyChains loopback TCP and Ligolo 0.9.2 Linux amd64 routed TCP fixtures with positive, negative and cleanup checks | Records cover only their named environments; they do not validate Windows, DNS, UDP, multi-hop pivoting or the rest of the guide |
| Optional RB-OPS | Private credential storage/recovery, default export confidentiality and a versioned finding model; RB-011 adds shared selection/migrations, editable findings/chains and private history | RB-011 awaits owner review on this branch; platform/pilot release checks remain open and default exports are reviewable drafts |
| Maintainer QA | Local validation command and pull-request CI for links, synthetic tool tests, lab-record structure and Python/Bash syntax (RB-012) | Passing checks do not establish procedure correctness or release readiness; see the acceptance gates below |

The merged ticket work includes RB-000–010 and RB-012–015. RB-011 is implemented on this branch with explicit engagement selection, transactional schema upgrades, record edits/retests and append-only application history; it remains subject to owner review. Check the [live open tickets](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues?q=is%3Aissue%20is%3Aopen) and [pull requests](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/pulls) for changes after this snapshot. Optional utility tickets do not block use of the manual guide.

See the [verification coverage and release gates](docs/RELEASE_ACCEPTANCE.md) for evidence, unresolved acceptance work and the distinction between guide and utility releases.

### Latest verification

The [merged RB-006 CI run](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/actions/runs/36371948957) passed on Python 3.11 and 3.14. RB-011 local validation passes 52 tests, 281 rendered local Markdown destinations, both saved lab-record structural checks, and parsing of 26 Python and 7 Bash sources. This includes concurrent engagement isolation, migration/history failure rollback and existing credential/export protections. A separate isolated real tmux smoke check passed populated finding/chain edits, history and default reporting. These checks do not rerun the guide labs or establish full release readiness.

Next steps are owner review of [RB-011 engagement lifecycle support](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/12) and the remaining manual-guide and optional-tool release evidence in the acceptance checklist. See the [lifecycle guide](tools/scripts/rb-ops/LIFECYCLE.md) for installation, compatibility and recovery.

## Start with the task

- [Start here](00_START_HERE.md): choose a reference for the current task.
- [Workflows](workflows/README.md): decision paths for enumeration, web, SMB, AD, escalation, and pivoting.
- [Service enumeration](enumeration/README.md): service-specific reference material.
- [Active Directory](active-directory/README.md): planning, reconnaissance, and current coverage status.
- [Privilege escalation](privilege-escalation/README.md): Linux and Windows references.
- [Pivoting](pivoting/README.md): SSH, ProxyChains, Chisel, and Ligolo.
- [Command snippets](snippets/README.md): short examples linked to their prerequisites.
- [Problem-solving references](hacker-mindset/README.md): hypotheses, interpretation, and next steps.
- [Finding template](exploited-vulns/_TEMPLATE/finding_template.md): document a finding manually.
- [Manual reporting hub](reporting/README.md): professional client reports, evidence handling and separate exam material.
- [Exam reporting template](OSCP_NOTES/6%20-%20reporting/oscp-report-template.md): separate study/exam material; check current exam requirements.

## How to use a procedure

Confirm the scope and prerequisites, set the documented inputs, and run the command in the named shell and location. Compare the actual output with the expected result, interpret what it proves, and choose the next step. Record evidence and limitations as you work. Restore any changes and document remediation and retest results.

A reference-reviewed command is not necessarily lab-validated. Check the verification status, tested versions, and limitations on each page. Older pages without a verification record remain unverified. The [reference-writing standard](docs/FIELD_GUIDE_STANDARD.md) defines what a complete guide should provide.

## Optional tools

[RB-OPS](tools/scripts/rb-ops/README.md) contains optional operator utilities for organizing engagement data. They are separate from the guide and are never prerequisites for its workflows or report templates. An individual utility can have its own runtime dependencies.

## Project maintenance

[Completion plan](PROJECT_EVALUATION_AND_COMPLETION_PLAN.md) · [Ticket queue](IMPLEMENTATION_QUEUE.md) · [Contributing](CONTRIBUTING.md)

Verification fixtures under `labs/` and tests are maintainer quality checks. They substantiate command claims; the pentester does not need to run them to use a guide. They do not automate an engagement.

Maintainers can run the same checks used by CI from the repository root on Linux with Python 3.11–3.14, Git and Bash:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tests/validate.py
```

CI exercises Python 3.11 and 3.14. Dependency installation needs network access; the checks use local files and synthetic data. This command does not run the SSH or Docker labs. Follow each lab's documented prerequisites when refreshing its evidence.
