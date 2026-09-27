# Scope, evidence and cleanup — manual checklist

Use this checklist in your own notes. No RB binary, special directory layout, or database is required.

## Before a task

Record the approved asset and account, objective, permitted methods, time window, exclusions, and contact for an unexpected result. Record limits that affect the task: scan/request rate, authentication attempts and lockout, files permitted for collection, allowed configuration changes, and restoration expectations. Scope is a property of the engagement; a discovered host or credential does not extend it.

| Decision | Record before proceeding |
| --- | --- |
| Network scan | Exact hosts/ports, approved rate, availability constraints, exclusions |
| Web discovery | Approved origins/paths, account/role, request budget, sensitive actions to avoid |
| Credential validation | Identity, one approved destination/service, attempt limit and stop condition |
| File access | Permitted share/path and minimum content needed to establish impact |
| Configuration change | Original value/permissions, approved change, restoration method and service check |
| Pivot | Approved source, agent and destination; existing routes/listeners and cleanup owner |

If a limit is unspecified, resolve that limit before the affected action; continue independent permitted work. Stop that action on unexpected service degradation, lockout, unapproved data access, or inability to restore a change. Preserve observations and contact the engagement owner.

## Record evidence as you work

For each result, capture UTC time, host/account, exact command or request, relevant output, what it proves, limitations, and the next decision. Keep original evidence protected and use redacted copies for client reports. A failed test can mean a missing prerequisite or blocked path; it does not establish that the asset is secure.

Capture the minimum evidence needed. A listing or one agreed sample can establish a file-access issue without copying an entire share. Do not embed discovered passwords, private keys or session tokens in shared notes.

## Change and restoration ledger

| Change ID | Asset and exact object | Original state/evidence | Test change and time | Restore action | Verification/evidence | Status and owner |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | Planned/restored/unresolved |

Restore the actual original state, not a guessed default. Remove only test-created files, accounts, memberships, tasks, certificates, routes, listeners and processes. For issued credentials/certificates, coordinate revocation or rotation where needed; deleting the local copy alone may not revoke access. Verify the legitimate application/service still works.

Preserve logs. Clearing event/audit logs is not assessment cleanup. A cleanup failure belongs in the client handoff with its owner, impact and next action. Do not mark cleanup complete while unresolved changes remain.

## Manual closure

- [ ] Compare each test-created change with its restoration evidence.
- [ ] Confirm test listeners/processes and temporary access are removed.
- [ ] List inaccessible or untested assets/methods as limitations.
- [ ] Separate demonstrated results from proposed impact.
- [ ] Record remediation and retest responsibilities.
- [ ] Deliver only the intended report/evidence set using agreed handling.

This is a process reference, not a command verification claim. Technique-specific commands remain in their individual guides.
