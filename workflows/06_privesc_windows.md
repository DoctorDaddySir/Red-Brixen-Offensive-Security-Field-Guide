# 06 — Windows privilege escalation workflow

Purpose: identify a demonstrable privilege boundary failure on an authorized Windows host and capture enough evidence to reproduce and remediate it.

Status: reference-reviewed 2026-09-25; Windows lab execution pending. Record the Windows build, shell, identity, and versions of any additional tools in the engagement notes. Commands below are observations, not proof of exploitation.

## 1. Establish identity and context

Run in cmd.exe on the assessed host:

```cmd
hostname
whoami /all
systeminfo
```

Record the host, current account, group membership, integrity level, enabled/disabled privileges, and timestamp. A local administrator running with a filtered token is different from a standard account. A listed privilege alone does not prove that SYSTEM access is possible. See Microsoft's [access token model](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-tokens) and [UAC behavior](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/how-it-works).

## 2. Collect candidates without changing configuration

Run in PowerShell:

```powershell
Get-CimInstance Win32_Service |
    Select-Object Name, StartName, State, StartMode, PathName
Get-ScheduledTask | Select-Object TaskPath, TaskName, State
```

Inspect only relevant files and service configurations. For a selected service in cmd.exe, substitute the actual service name and binary path:

```cmd
sc.exe qc "SERVICE_NAME"
sc.exe sdshow "SERVICE_NAME"
icacls "C:\Path\To\Service.exe"
icacls "C:\Path\To"
```

Record denied queries as coverage limitations. An unquoted path is only a candidate: establish that it contains spaces, an earlier candidate location is writable by the tested identity, and the service runs with greater privileges. A writable file alone does not prove it will be executed.

## 3. Choose a supported investigation

| Observation | Next investigation | Evidence needed before validation |
| --- | --- | --- |
| Service configuration or binary appears writable | [Service permissions](../privilege-escalation/windows/weak_service_permissions.md), [file permissions](../privilege-escalation/windows/insecure_file_permissions.md) | Effective permissions, service identity, execution trigger, original state |
| Unquoted service path with spaces | [Unquoted path](../privilege-escalation/windows/unquoted_service_path.md) | Writable candidate directory and actual path resolution |
| Task references writable content | [Scheduled tasks](../privilege-escalation/windows/scheduled_tasks.md) | Task principal, trigger, referenced file and effective ACL |
| Installer policy may allow elevation | [Installer policy](../privilege-escalation/windows/always_install_elevated.md) | Both applicable policy values and affected user context |
| Sensitive token privileges | [Token privileges](../privilege-escalation/windows/token_privileges.md) | Token state, applicable privilege semantics, access prerequisites |
| Accessible application secrets | [Stored credentials](../privilege-escalation/windows/stored_credentials.md) | Source, affected identity and approved validation target; redact secrets |
| Potential platform vulnerability | [Kernel applicability](../privilege-escalation/windows/kernel_exploits.md) | Exact build/patch applicability and a separate approved validation plan |

Linked references are existing material with their own verification needs. Review prerequisites rather than assuming a named technique works on every Windows build.

### Credential reuse check

Before assuming local-only escalation, check whether any credentials found on this host or
discovered elsewhere in the engagement can be reused. On Windows, inspect credential stores:

```cmd
cmdkey /list
```

```powershell
sekurlsa::logonpasswords
```

Cross-check any found domain credentials against other in-scope systems (SMB, WinRM, RDP).
Reuse is out-of-scope without explicit authorization and must be recorded as a finding with
redacted secrets.

## 4. Validate the smallest relevant boundary

Agree on the allowed change, interruption window, and restoration steps before changing services, tasks, files, or accounts. Preserve the original configuration and ACLs. Prefer a lab clone if validation could interrupt the host.

For a permitted test, demonstrate the resulting identity and one agreed access check. Capture before/after output with host and time. Do not infer domain compromise from local administration, or claim an exploitation path that was only enumerated. Stop after the agreed objective is demonstrated.

If the test fails, record the exact prerequisite that was absent or the error observed. Reassess the hypothesis instead of repeatedly running unrelated payloads.

## 5. Report, restore, and retest

The finding must identify the affected service/task/file, original and tested identity, effective permissions, reproduction steps, observed impact, evidence paths, and specific remediation. Reference the [finding template](../exploited-vulns/_TEMPLATE/finding_template.md).

Restore modified configuration and permissions, remove test artifacts/accounts, and verify the service or task still works. Preserve relevant logs. Record any outstanding cleanup with its owner.

Retest using the original lower-privileged context after remediation. Confirm both that the unauthorized action is blocked and that legitimate service operation remains functional. Mark outcomes fixed, partially fixed, not fixed, or unable to retest.

## Validation still required

On disposable Windows systems, exercise one allowed and one denied service/file permission case, a filtered administrator token, and a standard user. Record actual outputs, OS build, tool versions, and restoration evidence before promoting this workflow to lab-validated status.
