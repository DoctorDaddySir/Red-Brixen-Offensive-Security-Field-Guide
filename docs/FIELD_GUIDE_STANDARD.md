# Manual field-reference standard

Red Brixen helps a penetration tester perform and reason about a task manually. A guide is a reference, not an orchestrator, automated assessment, or instruction to run an RB wrapper.

## Required content

1. **Purpose and applicability:** the question being tested and when the technique is relevant.
2. **Prerequisites:** platform/tool versions, access, scope, dependencies, and changes the task may make.
3. **Execution location and inputs:** operator shell, target shell, or tool console; named variables and where to obtain their values.
4. **Copyable commands:** the underlying tool commands, grouped into small steps without prompt prefixes or shell-interpreted angle-bracket placeholders.
5. **Expected result:** representative output or an observable condition. Clearly label illustrative output versus recorded output.
6. **Interpretation:** what the result establishes, what it does not, false positives, and common failure causes.
7. **Next action:** branches based on observations, including when to stop or revisit prerequisites.
8. **Evidence:** what to capture in ordinary notes/files, how to identify assets and timestamps, and what to redact.
9. **Remediation and retest:** practical corrections and how a tester checks them.
10. **Cleanup:** restore only changes made for the task and preserve assessment logs.
11. **References and verification:** primary sources, tested environment/date, and precise limitations.

A tester must be able to follow the procedure with ordinary tools and their own notes. Do not require RB-OPS, SQLite, tmux, a generated engagement directory, fixture scripts, or a repo-specific runner. A technique's actual third-party tool dependencies, such as Ligolo or an SSH client, must still be documented.

## Reporting

Provide standalone templates and examples a tester can fill out by hand: observations, affected assets, reproduction, evidence, impact, severity rationale, remediation, cleanup, and retest status. The reader may use an editor, notebook, spreadsheet, or their existing reporting system. Optional exporters can help but cannot be the only way to complete a reporting step.

## Optional RB utilities

Document RB binaries in the tools section. If mentioned from a guide, describe them as optional convenience utilities after the full manual procedure. Never replace underlying commands or explanations with an RB invocation. Utility tests and release criteria are separate from field-guide completeness.

## Maintainer verification

Maintainers can use isolated labs and test scripts to validate instructions. These are supporting evidence, not assessment workflow steps. Keep them under `labs/` or `tests/`, label them maintainer-only QA, and link results from the guide without requiring the reader to execute the fixture.

Follow the [command verification standard](COMMAND_VERIFICATION.md). A guide's manual command is not validated merely because an unrelated wrapper, syntax check, or help command passed. Record what was actually exercised and distinguish unsupported platforms/protocols.

## Review question

Could a pentester use this page to perform the task, understand the outcome, record a finding, and clean up without installing any Red Brixen binary or running a verification fixture? If not, the guide is incomplete.
