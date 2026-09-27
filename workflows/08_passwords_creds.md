# 08 — Credential discovery, handling and validation

Purpose: determine whether an exposed credential enables a specific unauthorized action, without assuming that it can be tested everywhere. Use ordinary protected notes and the [scope checklist](../methodology/scope-and-cleanup.md); RB utilities are optional.

## 1. Search the approved location

On an authorized Linux host in Bash, choose a specific application/configuration directory:

```bash
read -r -p 'Approved configuration directory to inspect: ' CONFIG_DIR
grep -RIl --exclude-dir=.git -E 'password|passwd|api[_-]?key|secret' -- "$CONFIG_DIR"
```

This lists matching filenames rather than printing secret values. Review relevant files individually using the approved evidence-handling process. A keyword match is a candidate, not proof of a usable secret. Avoid filesystem-wide searches unless explicitly needed and scoped. Unreadable files and binary files can create coverage limitations.

For Windows stored-credential metadata, run in cmd.exe on the tested host:

```cmd
cmdkey /list
```

This is inventory, not a password dump or proof that the listed identity can be used. Windows behavior remains reference-reviewed, not lab-validated here.

## 2. Decide whether to validate

| Question | Required decision |
| --- | --- |
| What is it? | Password, token, hash, key, certificate, or sample/obsolete value |
| Who owns it? | Identity, source, environment, privilege assumptions |
| Is use permitted? | Approved destination/service and method, not “all reachable hosts” |
| What limits apply? | Attempt budget, lockout policy, timing, MFA and stop conditions |
| What would establish impact? | One minimal agreed access action, not blanket data retrieval |

Do not test a discovered production identity against an unapproved destination or assume a cloud/API token is interchangeable with a login password. Stop on lockout indications, unexpected MFA prompts or evidence that the identity belongs outside scope.

## 3. Perform the selected manual check

Use the service's native client with interactive secret entry when available; the [SMB guide](03_smb.md) shows one such path. Record the identity reference, destination, method, time, result and evidence ID. Keep secret values out of shell history and report screenshots.

A failed authentication can reflect format, domain, time, MFA, expiry or routing problems. Do not infer “invalid password” from every error or retry without regard to the agreed attempt limit. A successful login establishes that authentication worked, not that administrative access or lateral movement was demonstrated.

## 4. Offline material

Identify the actual format before choosing a cracking mode. Raw SHA-256, sha256crypt, sha512crypt, NTLM and Kerberos material are different formats; a hash length alone is not enough. Consult the installed tool's documented format list. Offline analysis is a separately scoped task with its own material-handling rules, not an automatic follow-up to every discovery.

## 5. Report, clean up and retest

Capture source, access conditions, affected identity and demonstrated impact. Reference protected artifacts instead of embedding reusable secret values. Recommend removal of the exposure and appropriate owner-coordinated rotation/revocation; deleting the discovered file alone may leave a credential usable elsewhere.

Record sessions or files created by validation and close/remove only those artifacts. Retest exposure and effective invalidation after remediation. Record unable to retest rather than assuming a rotation succeeded.

Verification: the bounded filename-only search is exercised against synthetic files in [the RB-007 record](../methodology/rb-007-verification.md). Authentication and Windows commands are not represented as executed by that record.
