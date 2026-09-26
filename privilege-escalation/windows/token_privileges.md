# Windows token privileges

Purpose: assess whether the tested process identity and token privileges create a demonstrable privilege-boundary failure. Token review is separate from searching for stored credentials.

Status: reference-reviewed 2026-09-25; Windows lab execution pending. Record the Windows build, account type, integrity level, and collection process.

## 1. Collect the current context

Run from cmd.exe on the authorized host:

```cmd
hostname
whoami /user
whoami /groups
whoami /priv
```

Record the host and time with output. Inspect the context in which the proposed action would execute; another process or thread may have a different token.

Windows uses primary tokens for process security context and impersonation tokens for a thread acting for a client. Group membership, integrity level, and privilege state matter. See Microsoft's [access tokens](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-tokens) and [impersonation tokens](https://learn.microsoft.com/en-us/windows/win32/secauthz/impersonation-tokens).

## 2. Interpret state before choosing a test

| Observation | Meaning for investigation |
| --- | --- |
| Privilege absent | Do not assume it can be enabled in this token. |
| Privilege present but disabled | Distinguish possession from enabled state; applicability depends on the operation and token access. |
| Privilege enabled | Establish its operation-specific prerequisites; this alone is not proof of higher-privileged access. |
| Administrators membership with restricted context | Review token filtering and integrity level before claiming a standard-user escalation. |
| Different process/thread identity | Capture the relevant context; shell output alone may not describe the service operation. |

[AdjustTokenPrivileges](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-adjusttokenprivileges) can enable or disable privileges already present; it cannot add missing privileges. Review [UAC token filtering](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/how-it-works) when comparing administrator sessions.

## 3. Prioritize applicable privilege boundaries

| Privilege | Investigation | Evidence needed |
| --- | --- | --- |
| `SeImpersonatePrivilege` | Whether a permitted service operation can actually impersonate an appropriately privileged client | Service identity, client/token provenance, impersonation level and resulting access |
| `SeAssignPrimaryTokenPrivilege` | Whether relevant token handles and process-creation prerequisites are available | Token access, required operation and actual created-process context |
| `SeBackupPrivilege` / `SeRestorePrivilege` | Whether backup/restore operations expose or alter resources beyond intended duties | Approved test resource, operation semantics and before/after authorization result |
| `SeDebugPrivilege` | Whether process access exceeds the role's intended boundary | Target protection, access requested and demonstrated result |
| `SeTakeOwnershipPrivilege` | Whether ownership changes could cross an intended resource boundary | Original ownership/ACL, permitted test object and restoration plan |

These are investigation categories, not guaranteed escalation paths. Service roles may legitimately possess some of these rights. Do not report the privilege name alone as a confirmed vulnerability or assume an old tool works on a current build.

Consult Microsoft's [privilege constants](https://learn.microsoft.com/en-us/windows/win32/secauthz/privilege-constants) for operation-specific semantics.

## 4. Validate in an approved environment

First reproduce prerequisites in a disposable system matching the target build. Define the original identity, the expected denied action, the permitted demonstration, and restoration. Use a benign test object or marker appropriate to the boundary; avoid collecting unrelated credentials or sensitive process memory.

Capture the denied baseline and resulting identity/access after the approved operation. A tool success message without a verified context or resource-access change is insufficient. Stop if the needed client, token handle, privilege, or platform behavior is absent; record the limitation.

## 5. Report and retest

A complete finding includes the affected service/account, assigned privilege, configuration source, prerequisite chain, baseline identity, observed impact, reproduction, and evidence IDs. Separate potential impact from actions actually demonstrated. Use the [finding template](../../exploited-vulns/_TEMPLATE/finding_template.md).

Recommend removing unnecessary rights from the affected account or changing its service design and isolation as appropriate. Validate legitimate service requirements before altering assignments. Retest with a newly created affected logon/service context after the approved policy change; an existing token may not reflect the new configuration.

Restore test-object ownership and ACLs, stop only test processes, remove artifacts, and preserve logs. Record cleanup and any unresolved changes.

## Lab acceptance checklist

- [ ] Record a standard-user context and an administrator's filtered/elevated contexts.
- [ ] Record a relevant service account and explain which privileges are expected for its role.
- [ ] Demonstrate one permitted benign boundary test with baseline and resulting access.
- [ ] Exercise a missing-prerequisite case and avoid classifying it as a confirmed exploit.
- [ ] Verify remediation in a new context and preserve restoration evidence.

Until this checklist has actual outputs, retain reference-reviewed status.
