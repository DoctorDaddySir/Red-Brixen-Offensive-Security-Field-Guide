# Red Brixen Offensive Security Field Guide

A manual reference for penetration testers: practical procedures, copyable commands, result interpretation, evidence collection, remediation, and reporting.

The tester chooses and performs each task. Every guide must be usable independently of RB binaries, a database, a generated workspace, or an automated lab. Use your own notes, evidence folders, and preferred reporting tools.

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
