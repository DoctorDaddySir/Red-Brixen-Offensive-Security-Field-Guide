# Penetration Test Report — [engagement name]

**Status:** Draft — complete and review before delivery
**Client / assessor:** [organizations and named contacts]

**Assessment dates / time zone:** [start–end]

**Report date / version:** [date, version, reviewer]

**Classification / recipients:** [agreed handling and distribution]

## Executive summary

[Describe the agreed objective, tested environment and demonstrated business impact in terms the recipient can act on. State material limitations. Do not claim administrative access, data exposure or full compromise unless the evidence establishes it. If no issue was demonstrated, describe the coverage and limits rather than asserting that the environment is secure.]

[Summarize the most urgent corrective actions, responsible teams and proposed priorities. Link each conclusion to finding IDs below.]

## Authorization, scope and constraints

| Item | Agreed scope / source of authorization |
| --- | --- |
| Engagement owner and authorization reference | [reference; keep private agreements separate] |
| Included assets and environments | [explicit hosts, applications, ranges, tenants] |
| Accounts / roles / starting access | [approved identities and privileges; no secrets] |
| Exclusions | [assets, data, methods and changes excluded] |
| Windows and activity limits | [time, request rates, lockouts, approved changes] |
| Escalation and stop conditions | [contact and agreed triggers] |
| Evidence retention / delivery / disposal | [agreed handling and owner] |

## Methodology and coverage

Describe what was actually performed and why. Include tool versions when they affect reproduction; distinguish manual validation from tool observations. A methodology name or scanner run does not establish complete coverage.

| Asset / boundary | Method and vantage point | Result / evidence IDs | Untested area or limitation |
| --- | --- | --- | --- |
| [asset] | [account, method, date] | [observation] | [constraint and effect] |

Record unreachable assets, denied access, missing prerequisites and stopped tests. Explain how each affects conclusions; do not silently mark an unperformed test as passed.

## Findings summary

| ID | Finding | Affected assets | Severity and rationale | Remediation owner / priority |
| --- | --- | --- | --- | --- |
| [F-001] | [evidence-backed title] | [assets] | [method/version and context] | [owner, priority] |

[Reconcile totals with the detailed findings. Document the severity method and version; if using CVSS, include its vector, score and rationale for selected metrics. Separate technical severity from business priority and identify uncertain assumptions.]

## Detailed findings

Repeat the [standalone finding template](../exploited-vulns/_TEMPLATE/finding_template.md) for each confirmed finding. Each entry needs its ID, prerequisites, expected versus observed behavior, reproducible actions, evidence, demonstrated impact, limitations, actionable remediation and retest criteria.

Commands are historical evidence here: paste the exact executed commands, identify their shell/host/account and explain substitutions. Redact secret values in the client copy and retain a protected original under agreed handling. A redacted command must make the required input type clear without revealing a reusable credential.

## Demonstrated attack paths, if applicable

| Step | Starting identity / asset | Observed action and result | Supporting finding / evidence | Remaining assumption |
| --- | --- | --- | --- | --- |
| [1] | [starting state] | [actual result] | [F-/E- IDs] | [none or explicit limitation] |

Include only paths needed to explain demonstrated impact. If a later step was not tested, end the demonstrated path and label the additional consequence as unverified. A shell or domain takeover is not required for every finding.

## Remediation plan

| Finding IDs | Specific corrective action | Owner | Target date | Verification criteria |
| --- | --- | --- | --- | --- |
| [IDs] | [root cause and compensating measure if needed] | [team] | [agreed date] | [same lower-privileged action and expected result] |

## Cleanup and handoff

| Test change / artifact | Original state | Restoration action | Verification evidence | Status / owner |
| --- | --- | --- | --- | --- |
| [exact object] | [original] | [action] | [evidence ID] | [restored or unresolved] |

Preserve assessment logs. Document unresolved changes, active test access and client follow-up explicitly; do not mark cleanup complete merely because testing ended.

## Retest record

| Finding | Fix/version/date supplied | Retest scope and method | Actual result / evidence | Status / limitations |
| --- | --- | --- | --- | --- |
| [ID] | [change reference] | [original boundary] | [result] | [resolved, partial, unresolved, unable to retest] |

## Evidence register

| Evidence ID | Finding / asset / identity | Capture time and time zone | Protected original reference | Client copy / redaction / reviewer |
| --- | --- | --- | --- | --- |
| [E-001] | [context] | [timestamp] | [reference, no secret-bearing path] | [reviewed artifact] |

Include only the approved client artifacts. Record a digest if used by the engagement's integrity process. Do not embed private logs, session tokens, reusable credentials or unrestricted data dumps. Record separately delivered restricted material and its authorized recipients without copying its contents here.

## Final review

- [ ] Every conclusion is supported by evidence or explicitly marked untested.
- [ ] Commands, outputs and screenshots agree with the described identity and asset.
- [ ] Scope, exclusions, limitations and unsuccessful tests are represented accurately.
- [ ] Finding IDs, severity counts and remediation references agree.
- [ ] Text, images, attachments and document metadata have been reviewed for private content.
- [ ] Cleanup/retest status and outstanding owners are accurate.
- [ ] The rendered deliverable is readable and approved for the named recipients.
