# OSCP exam report worksheet

Exam preparation material, separate from the [professional client report](../../reporting/client-report-template.md). This is an unofficial editable outline, not a completed report or a guarantee of exam compliance. No RB tool is required. Replace bracketed instructions with your own observed results; remove unused entries without inventing outcomes.

**Student name / email:** [your details]

**OSID:** [your assigned ID]

**Exam dates / time zone:** [actual dates]

**Report version:** [version]

## Current official requirements

Reference check: 2026-09-27 UTC. Recheck the [OffSec exam guide](https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide) and [reporting requirements](https://help.offsec.com/hc/en-us/articles/360046787731-OSCP-Reporting-Requirements) before an attempt; the control panel and current official instructions govern. OffSec supplies recommended Word and LibreOffice templates on the reporting-requirements page.

The checked guide requires reproducible steps, commands and output. Proof must be captured from its original location using `cat` or `type` in an interactive target shell; screenshots must also show the target IP using the documented network command. Submit required proofs in the control panel before the exam ends. Modified exploits need their source URL, changes, explanation and applicable generation commands. Review current tool restrictions, including the prohibition on AI chatbot assistance.

For submission, the checked guide specifies PDF inside an unencrypted `.7z`, only PDFs in the archive, a 200 MB maximum and upload within 24 hours after completion. Follow its exact case-sensitive filename pattern using your OSID; verify the upload MD5 and complete the final submission action. Recheck these rules rather than relying on remembered packaging commands. [Source: official exam guide](https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide).

## Objective and actual coverage

[Record the assigned objectives and tested targets. Describe the access actually demonstrated, any partial results and missing evidence. Do not prewrite a success claim or infer domain control from local administration.]

| Target / IP | Assigned objective | Demonstrated result | Evidence reference | Uncompleted work |
| --- | --- | --- | --- | --- |
| [target] | [objective] | [actual result] | [screenshot/section] | [limitation] |

## Per-target record — repeat for each assigned target

### Target and starting context

- Host / IP / environment: [actual target]
- Starting access / identity: [actual state; distinguish supplied access from access you obtained]
- Relevant versions and prerequisites: [observed evidence]
- Objective and outcome: [actual result, including partial or unsuccessful]

### Enumeration and interpretation

[Paste the commands actually run, shell/vantage point, relevant output and why the observations led to the selected test. Do not substitute a stock scan command for your evidence.]

### Initial access or tested boundary

1. [Reproducible action, prerequisite and actual input.]
2. [Observed output and interpretation.]
3. [Result and evidence reference; distinguish failure from success.]

[Include exploit source and any modifications according to the current official requirements. Record paths, parameters and dependencies required to reproduce your work.]

### Privilege change, if demonstrated

[Record before/after identity, exact actions and evidence. If not attempted or not achieved, state that and why; do not leave an assumed SYSTEM/root outcome.]

### Proof and screenshots

| Required proof/objective | Target and identity | Capture / screenshot reference | Control-panel submission record |
| --- | --- | --- | --- |
| [as assigned] | [actual context] | [legible evidence] | [actual status/time] |

[Insert the required evidence from your attempt. Check that screenshots satisfy the official proof and target-IP requirements. A placeholder or typed claim is not proof.]

### Reproduction and limitations

[Confirm a technically competent reader can follow the sequence from the documented starting state. Identify retries, environmental dependencies and steps whose outcome could not be confirmed.]

## AD sequence, when assigned

| Sequence | Source identity / host | Action and destination | Observed privilege / result | Evidence |
| --- | --- | --- | --- | --- |
| [step] | [starting context] | [actual action] | [demonstrated result] | [reference] |

[Document the transitions actually performed, including the supplied starting context. Do not assume every transition or final objective succeeded.]

## Conclusion

[Summarize only demonstrated results, linked to target sections. State incomplete objectives and evidence gaps honestly. Any recommendations should address the observed causes rather than a prefilled list of generic fixes.]

## Final manual review

- [ ] Personal placeholders replaced with your own details; no template author's contact remains.
- [ ] Every claimed result maps to reproducible steps and legible evidence.
- [ ] Current official instructions and target-specific objectives checked.
- [ ] All required screenshots, exploit details and console output are present.
- [ ] Final PDF visually reviewed for clipping, missing images and unreadable text.
- [ ] Package, naming, deadline and upload confirmation checked against current guidance.

Verification: official-source review and Markdown checks only. No exam target, actual submission, archive command or PDF export was exercised for this template update.
