# Active Directory reconnaissance map

Status: planning template, not a verified command collection. Begin with the [starting workflow](00_ad_start_here.md).

## Engagement context

- Engagement ID and scope version:
- Authorized domains/forests and excluded trusts:
- Testing identity and credential reference (no secret value):
- Permitted methods and collection limits:
- Start/end time and escalation contact:

## Observed environment

| Asset/object ID | Name/domain | Type | Source/evidence ID | Collection UTC | Confidence/limitations |
| --- | --- | --- | --- | --- | --- |
| | | Domain/DC/DNS/host/user/group/CA | | | |

Capture the resolver and time source used. Record inaccessible services as coverage gaps rather than inferring absence. A trust relationship does not extend engagement scope.

## Candidate relationships

| Starting principal | Target object | Observed relationship | Required prerequisites | Evidence IDs | Status |
| --- | --- | --- | --- | --- | --- |
| | | Membership/permission/delegation/enrollment | | | Hypothesis/confirmed/rejected/blocked/not tested |

For a multi-step path, identify the input access and output access of each step. Verify each edge before claiming the end result. Preserve the original observations when a hypothesis is rejected.

## Validation and restoration ledger

| Test ID | Approved objective | Procedure/tool version | Baseline | Observed result | Evidence | Change/rollback | Retest |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

Use synthetic or minimal agreed proof. Reference protected credentials and original evidence by ID; redact derivatives for reporting. Record whether cleanup succeeded and who owns any unresolved action.

## Handoff checklist

- [ ] In-scope assets and identities are explicit.
- [ ] Confirmed results are distinguishable from proposed paths.
- [ ] Each finding has reproducible steps, actual impact and evidence.
- [ ] Untested domains, methods and blocked queries are listed.
- [ ] All changes have restoration results and retest status.
