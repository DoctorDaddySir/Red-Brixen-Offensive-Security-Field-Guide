# Exam working notes worksheet

Use during preparation to record your own observations. This worksheet feeds the [exam report outline](../6%20-%20reporting/oscp-report-template.md); client engagements use the separate [professional template](../../reporting/client-report-template.md). Verify current exam rules before an attempt. No RB command or generated workspace is needed.

## One observation or test

- Timestamp / time zone: [actual time]
- Target / IP / identity / shell: [context]
- Question and prerequisite: [what this test can establish]
- Exact command or request: [what you actually ran]
- Relevant output / artifact reference: [evidence]
- Interpretation: [what the result establishes and what it does not]
- Next decision: [continue, change hypothesis, stop, or record limitation]

## Credential observation, if applicable

- Protected credential reference: [identifier; keep reusable values out of general notes]
- Source and identity: [observed context]
- Use permitted by current scope/rules: [specific destination and method]
- Actual validation result: [success, failure or not tested; supporting evidence]
- Impact supported: [actual access; do not assume lateral movement]

## Privilege or identity transition

- Starting identity and target: [observed]
- Misconfiguration or prerequisite: [evidence]
- Actions and relevant output: [exact executed sequence]
- Resulting identity and rights: [observed, or not achieved]
- Proof/evidence reference: [artifact]

## Multi-host sequence

| Step | Starting identity / host | Actual action | Destination / resulting identity | Evidence / unresolved prerequisite |
| --- | --- | --- | --- | --- |
| [step] | [context] | [command reference] | [observed result] | [reference] |

A chain can end at a failed prerequisite. Do not prefill domain compromise or administrative access. Transfer confirmed results into the final report while preserving limitations. Follow the [exam template's official-source checklist](../6%20-%20reporting/oscp-report-template.md) for proof and submission requirements.
