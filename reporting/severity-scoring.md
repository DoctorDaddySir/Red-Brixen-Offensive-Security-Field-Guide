# Manual severity scoring and remediation priority

A finding title does not determine its score. Establish the demonstrated boundary failure and record uncertainty before selecting a rating. Use this reference with the [finding template](../exploited-vulns/_TEMPLATE/finding_template.md); no RB binary is needed.

## Record a reproducible rating

1. Agree the scoring method/version for the engagement. Keep that choice visible beside every score.
2. Describe the attacker starting state, required access, affected component and demonstrated result. Separate a successful test from a suspected consequence.
3. Select each metric using the chosen specification. Record the evidence and reasoning for each choice; mark unresolved assumptions and keep the rating provisional when necessary.
4. Calculate with a calculator for that version. Save the complete vector, score, metric group, calculator/version or URL, date and reviewer together in your finding notes. Recalculate after changing any metric.
5. Set client remediation priority separately, explaining the asset importance, exposure, compensating controls, dependencies and operational urgency considered. Assign an owner and target date.

CVSS v3.1 uses Base, Temporal and Environmental metrics. CVSS v4.0 has different metrics and score nomenclature; do not relabel a 3.1 vector as 4.0 or assume identical scores across versions. See the [FIRST v3.1 specification](https://www.first.org/cvss/v3.1/specification-document) and [v4.0 user guide](https://www.first.org/cvss/v4.0/user-guide). CVSS describes severity and is one input to prioritization; it is not a complete client risk assessment.

## Finding scoring worksheet

- Method and version: [for example, CVSS 3.1]
- Score type / metric group: [for example, Base]
- Full version-prefixed vector: [the actual vector]
- Calculated score and qualitative label: [actual result]
- Calculator/version or reference: [how the score was calculated]
- Assessor / reviewer / date: [names and date]
- Status: [provisional or reviewed, with remaining assumptions]
- Client remediation priority / owner / target date: [separate decision and rationale]

| Metric | Selected value | Supporting observation / evidence ID | Assumption or unresolved dependency |
| --- | --- | --- | --- |
| [metric for selected version] | [value] | [actual evidence] | [none or explicit uncertainty] |

Retain the previous rationale when revising a score. Explain whether the change reflects new evidence, a corrected metric, a different method/version, or changed environment. Never silently replace a historical score in a delivered report.

## Worked example — assumed local privilege escalation

This is a hypothetical scoring exercise, not proof that any listed sudo or SUID configuration is exploitable. Assume an attacker already has a low-privilege local account, exploitation needs no user interaction or additional complexity, the affected security authority stays the same, and exploitation gives complete confidentiality, integrity and availability impact on that component.

| CVSS 3.1 Base metric | Value | Explicit assumption |
| --- | --- | --- |
| Attack Vector | L | Local execution is required |
| Attack Complexity | L | No additional conditions beyond the stated access |
| Privileges Required | L | A low-privilege account is required |
| User Interaction | N | Another user need not act |
| Scope | U | Impact remains within the same security authority |
| Confidentiality | H | Complete confidentiality impact is assumed |
| Integrity | H | Complete integrity impact is assumed |
| Availability | H | Complete availability impact is assumed |

Vector: `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`

Base score: **7.8 (High)**.

The [FIRST v3.1 calculator](https://www.first.org/cvss/calculator/3.1) can be used without any repository tool. The score here was also recomputed using the repository's optional v3.1 arithmetic function on 2026-09-27 UTC. That arithmetic check does not validate these assumptions on a real host or certify the entire calculator implementation.

If the file is not writable, execution cannot be triggered, or the identity/result differs, revise the finding and its assumptions before assigning this vector. Do not copy the example score solely because the technique name matches. Client priority may differ between an isolated test host and a critical production service; record that distinction without rewriting the Base metrics to express urgency.

## Template and tool compatibility

The common finding templates intentionally leave ratings unset and identify evidence needed for scoring. Their prose and commands are starting material, not records of successful execution. Replace them with your actual observations before delivery. Existing report scores are not retroactively recalculated by this documentation change.

The optional `rb-findings` prompt currently calculates CVSS 3.1 Base scores and stores its version-prefixed vector. It does not calculate CVSS 4.0 or turn operator answers into verified facts. Keep other scoring methods and their rationale in your manual report; do not enter a 4.0 result under a 3.1 label.

Reference review: FIRST specification/user-guide pages checked 2026-09-27 UTC. No exploitation or assessment-wide scoring validation is claimed by this reference.
