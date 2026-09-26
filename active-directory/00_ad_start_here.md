# Active Directory: start here

Status: planning workflow; live AD command verification is pending. Use the [coverage register](README.md) to distinguish usable planning material from deferred command references.

## Before collecting data

Record the authorized forest/domains, domain controllers, test accounts, permitted collection methods, excluded systems, time window, and stop conditions. Keep secret values in the engagement's protected store; use credential reference IDs in notes.

Start a [reconnaissance map](01_ad_recon_map.md). Keep observed facts, hypotheses, validated access, and untested assumptions separate. A graph edge or group name does not prove that a complete access path works.

## Choose the next step

| Current information | Next action | Required record |
| --- | --- | --- |
| Scope only | Confirm the supplied domain/DC/DNS inventory with the owner | Approved asset list and exclusions |
| Approved authenticated context | Plan limited directory collection for that identity | Identity, method, versions, collection scope |
| Relationship data | Build a candidate path to a scoped objective | Source principal, target, prerequisites, evidence |
| Candidate path | Validate the smallest allowed access change | Before/after identity and access, limitations |
| Confirmed finding | Document root cause and remediation | Reproduction, evidence IDs, impact and retest |
| Testing finished | Restore changes and confirm closure | Change log, cleanup results, outstanding items |

Existing [domain enumeration notes](02_domain_enum.md) and the [domain worksheet](AD_WORKSHEET.md) are study references. Their commands are not a verified execution baseline. Do not paste credentials into shared worksheets or run broad collection merely because a sample says “All.”

## Ready for reporting

For each candidate, record confirmed, rejected, blocked, or not tested. Describe demonstrated access separately from potential impact. Attach sanitized outputs with identity, host, UTC time, tool version and collection method. Use the [finding template](../exploited-vulns/_TEMPLATE/finding_template.md); avoid static severity claims without an assessment-specific rationale.

Remove test artifacts and restore account/object changes while preserving assessment logs. Retest with the original lower-privileged identity after remediation. Any unverified command family remains deferred until its lab record is available.
