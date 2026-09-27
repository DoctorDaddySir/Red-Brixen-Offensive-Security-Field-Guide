# 13 — Active Directory cleanup and closure

Restore assessment changes while preserving evidence. Use the [manual change ledger](../methodology/scope-and-cleanup.md); no RB tooling is needed.

## 1. Inventory what this assessment changed

Record exact object identifiers and original state for accounts, group membership, ACLs, GPOs, services/tasks, files, issued certificates, authentication material and network tunnels. Distinguish test-created objects from pre-existing client configuration. An account or token discovered during testing is not automatically yours to delete or revoke.

## 2. Restore the recorded state

| Change | Restoration decision | Verification |
| --- | --- | --- |
| Added test account/membership | Remove the specific test-created object or membership | Compare identifiers and effective access with the baseline |
| Modified ACL/GPO/service/task | Restore the captured original configuration | Confirm intended application behavior and permissions |
| Issued certificate or temporary credential | Coordinate revocation/rotation with the owner | Check effective validity/access; deleting a file is insufficient |
| Uploaded file or listener | Remove the exact test artifact or stop its process | Confirm absence and that legitimate service remains available |
| Added route/interface | Remove only the test-created route/interface | Compare network state and confirm intended connectivity |

Use the relevant platform procedure for the identified object. There is no safe universal delete command for an unknown AD environment. If the original state was not captured or restoration needs the owner, document the unresolved item rather than guessing.

## 3. Preserve and hand off evidence

Keep timestamps, relevant logs, change history, before/after output and identity context. Do not clear event or audit logs. Redact client copies of evidence; retain protected originals according to the engagement's handling requirements.

For each unresolved change record its asset, impact, owner and next action. Retest remediation under the original lower-privileged identity and record fixed, partially fixed, not fixed, or unable to retest. A successful cleanup does not by itself prove a vulnerability is fixed.

Status: manual process reference; no destructive command or environment-specific restoration has been executed for this page.
