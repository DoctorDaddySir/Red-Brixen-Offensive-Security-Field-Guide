# 03 — SMB enumeration and minimal evidence

Purpose: determine the tested identity's permitted share/file access. Set the scope, authentication-attempt limit and collection permissions using the [manual checklist](../methodology/scope-and-cleanup.md). Share visibility, file read, file write and code execution are distinct results.

## 1. Inspect approved shares

Operator Bash, with Samba smbclient installed:

```bash
read -r -p 'Approved SMB host: ' SMB_HOST
read -r -p 'Approved identity, such as DOMAIN/user: ' SMB_ID
smbclient --version
smbclient -L "$SMB_HOST" -U "$SMB_ID"
```

Enter the password at the tool prompt. Do not embed it in the command or shared transcript. If a null-session check is explicitly part of the test, use this separate unauthenticated request:

```bash
smbclient -L "$SMB_HOST" -U '%' -N
```

An authenticated share listing does not prove a null session works. Record the actual identity and response; access denied is a result, not a reason to repeat attempts across accounts. A guest mapping is also different from a true anonymous session.

## 2. Open one selected share

```bash
read -r -p 'Approved share name from the listing: ' SHARE
smbclient "//$SMB_HOST/$SHARE" -U "$SMB_ID"
```

At the smbclient prompt, start with:

```text
pwd
ls
```

Review the listing before retrieving anything. Enter `cd` with the actual approved subdirectory if needed. Capture a listing or one agreed sample; do not default to recursive wildcard download.

For an agreed lab file named `approved-proof.txt`, these are smbclient console commands:

```text
get approved-proof.txt evidence-copy.txt
quit
```

For a real assessment, substitute the exact approved remote/local filenames. Do not execute that example unless the remote file exists and collection is allowed. Record the source path, local artifact ID, timestamp and why that sample establishes the issue. Handle sensitive samples in the approved protected location.

## 3. Validate write access separately

Only if write validation is authorized, select an unused filename in an agreed test directory and upload a benign marker containing no executable content. Confirm the file exists, then remove that exact marker and verify removal. Preserve proof of creation/removal. A listing marked writable is a hypothesis until the relevant access is tested; a successful write does not prove execution.

## 4. Assess credentials and impact

If a credential is discovered, reference it in protected notes and use the [credential-validation decision path](08_passwords_creds.md). Scope one destination/service and its attempt limit before testing it. Do not automatically spray a target list or try every protocol.

Report the identity, share/path, expected versus observed access, minimal evidence and effect on confidentiality/integrity. Recommend the relevant share/filesystem permission or credential-storage correction and retest the same access boundary after remediation. Restore test-created artifacts; preserve server logs.

Verification: commands are reference-reviewed against the [Samba manual](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html); parser/help checks do not establish SMB server behavior. An authenticated Windows/Samba target execution record remains pending.
