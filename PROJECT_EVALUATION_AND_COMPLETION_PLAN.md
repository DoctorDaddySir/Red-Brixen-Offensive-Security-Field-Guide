# Red Brixen: project evaluation and completion plan

Assessment date: 2026-09-23. Baseline: local commit `2cb801f`.

## Recommendation

Develop Red Brixen into a maintained penetration testing field guide with an integrated evidence and reporting toolkit. Preserve its terminal-first approach and useful enumeration material. The first release should support a complete, reproducible engagement: scoping, testing, findings, evidence, remediation, cleanup, report delivery, and retesting.

The current repository is a substantial working notebook and an early toolkit, but it is not yet a dependable, comprehensive professional reference. Correctness, reporting depth, and validation should come before adding more commands or building a graphical application.

This document evaluates project readiness and defines implementation work. It is not an exhaustive security audit, a certification of individual techniques, or a claim that the roadmap has been implemented.

## 1. What was evaluated

- Inventoried all 148 non-Git files: 131 Markdown documents, approximately 34,229 whitespace-delimited words, before adding this plan.
- Compared Markdown file hashes to identify exact duplicates and inspected short pages and placeholders.
- Read the entry points, all nine operational workflows, report templates, RB-OPS documentation and core source, and representative enumeration, AD, escalation, pivoting, and finding pages.
- Inspected the four Python RB-OPS commands and workspace creation scripts for their data and reporting contracts.
- Parsed six Python scripts successfully and checked seven Bash scripts with `bash -n`; these are syntax checks, not proof of runtime correctness.
- Exercised `rb-report` with a temporary SQLite database containing synthetic credentials and a synthetic finding, replacing only engagement-context lookup. Confirmed that its default output includes the synthetic secret and placeholder remediation. No live systems or real engagement data were used.
- Checked primary-source references for methodology, web/API coverage, and vulnerability scoring.

The working tree was clean at the start. No existing content or tools were changed during this evaluation. Network exploitation, Windows execution, real tmux integration, document rendering, and every embedded command remain untested.

## 2. Current strengths and readiness

| Area | Assessment | Evidence and implications |
| --- | --- | --- |
| Organization | Useful foundation | Separate workflows, enumeration, escalation, AD, pivoting, snippets, mindset, and reporting material already exist. |
| Service enumeration | Broad starter coverage | 18 Markdown documents under `enumeration/`, including common network services and CMS targets; depth varies and applicability needs verification. |
| Linux/Windows escalation | Substantial but inconsistent | 29 Markdown documents across the escalation tree; some labels do not match their contents. |
| AD | Incomplete | 16 documents, including two placeholders and several very brief topic outlines. All 11 AD snippet pages are placeholders. |
| Pivoting | Partially useful | Ligolo, SSH, and Chisel material exists; the ProxyChains page is a copy of Ligolo material. |
| RB-OPS | Functional prototype | Nine commands establish workspaces, record credentials and chains, score findings, and generate Markdown. Shared logic and lifecycle support are limited. |
| Reporting | Release blocker | Templates exist, but the database cannot represent a complete finding and reports expose raw credentials by default. |
| Professional engagement lifecycle | Major gap | Scope notes and cleanup fragments exist; there is no complete operational path from authorization to retest and closure. |
| Quality and maintenance | Major gap | No repository CI configuration, automated test suite, release metadata, or root contribution/license guidance was found in the baseline. |

Avoid a percentage-complete estimate: the project has no agreed definition of done, and file count overstates coverage when pages are duplicates or placeholders.

## 3. Concrete defects and release blockers

Priorities below describe project delivery urgency, not CVSS vulnerability severity.

| ID | Priority | Observed issue | Required outcome |
| --- | --- | --- | --- |
| RB-001 | P0 | `workflows/06_privesc_windows.md` and `workflows/07_pivoting_tunneling.md` exactly duplicate `05_privesc_linux.md`. | Replace with platform-correct workflows, expected evidence, decision points, and cleanup. |
| RB-002 | P0 | `pivoting/proxychains.md` exactly duplicates `pivoting/ligolo.md`; Windows `token_privileges.md` exactly duplicates `stored_credentials.md`. | Write the intended topics and validate them in appropriate labs. |
| RB-003 | P0 | `active-directory/00_ad_start_here.md`, `01_ad_recon_map.md`, and all 11 `snippets/ad/` pages contain only `# COMING SOON`. | Populate required core pages or clearly remove them from supported navigation until ready. |
| RB-004 | P0 | `rb-report:147` and `rb-creds:165` render the raw secret. `rb-report` also imports engagement notes and chain commands without redaction. | Default client exports must omit secrets and private notes; use an explicitly selected restricted appendix when necessary. Cover free text and attachments as well as credential columns. |
| RB-005 | P0 | `rb-findings:100` defines only title, description, host, vector, score, severity, and creation time. `rb-report:101` hardcodes remediation text. | Introduce a versioned finding model with evidence, reproduction, impact, remediation, review, and retest fields; render real content. |
| RB-006 | P0 | Credential storage is plaintext; `rb-creds add` accepts the secret as a positional argument. File creation does not explicitly enforce private modes. | Add private permissions, hidden secret input, protected storage/key handling, backup rules, and explicit secret-export controls. Preserve migration and recovery paths. |
| RB-007 | P0 | `active-directory/13_cleanup_opsec.md:14` suggests clearing logs. SMB guidance says to download everything; generic workflows treat credential reuse and aggressive activity as universal steps. | Replace these with engagement-specific scope, minimal proof, approved activity limits, rollback, and preservation of assessment evidence. |
| RB-008 | P1 | README lists nonexistent `exploited_vulns/`; actual path is `exploited-vulns/`. Entry points often present plain path text rather than links. | Correct paths and introduce a navigable, checked index. |
| RB-009 | P1 | Reporting templates mix exam assumptions with client reporting; the exam template includes a non-placeholder mailto destination and prewritten success claims. | Separate exam/client templates, remove personal values, and require evidence-backed conclusions. Verify exam requirements against current official guidance when updating that track. |
| RB-010 | P1 | Common finding examples include fixed scores without vectors or assessment-specific rationale. | Store versioned vectors and explain scoring assumptions; distinguish technical severity from client remediation priority. |
| RB-011 | P1 | Engagement lookup and database setup are duplicated across Python tools; findings have no update or retest lifecycle. | Shared package, schema migrations, explicit engagement selection, editable records, history, and integration tests. |
| RB-012 | P1 | No continuous checks establish that pages, examples, tools, or reports remain usable. | Add documentation validation, meaningful tool tests, lab records, and release gates. |

Additional engineering review targets: shell quoting when target values are sent to tmux, path containment, empty/colliding workspace names, partial initialization, concurrent writes, and export overwrite behavior. These are areas to test, not vulnerabilities proven by this evaluation.

## 4. Product boundaries and release scope

Maintain three clearly labeled reading paths:

1. **Quick field reference:** concise decision trees, commands, prerequisites, expected output, failure interpretation, and links to detail.
2. **Professional engagement:** planning, test coverage, controlled validation, evidence, findings, client reporting, cleanup, and retesting.
3. **Lab/exam study:** exercises, proof capture, practice workflows, and version/date-specific exam references.

### Core v1.0 coverage

- External/internal network and service assessment.
- Windows and Linux enumeration and privilege escalation.
- AD identity, permissions, Kerberos, certificate services, and bounded lateral movement validation.
- Web applications and APIs, including identity, authorization, sessions, business logic, and tenant boundaries.
- Pivoting, segmentation testing, credential handling, evidence, reporting, and retesting.

### Expansion after the core release

- Cloud infrastructure and identity: AWS, Azure/Entra, and GCP.
- Containers, Kubernetes, CI/CD, repositories, and software supply chains.
- Mobile, wireless, macOS, and thick clients.
- AI-enabled applications and agent integrations.
- Specialist tracks such as OT/IoT and social engineering, only with subject-matter review, appropriate labs, and their own scope requirements.

Every specialization must be explicitly labeled supported, experimental, or planned. A comprehensive resource needs clear coverage boundaries; empty headings do not establish support.

## 5. Required testing coverage

| Domain | Required additions or improvements | Completion evidence |
| --- | --- | --- |
| Pre-engagement | Objectives, assets, exclusions, identities/roles, authorization, test windows, communications, third-party constraints, stop conditions, data retention, delivery/retest expectations. | Filled synthetic engagement pack and a scope-change example. |
| Recon and network | Asset inventory, TCP/UDP and IPv6 applicability, DNS/TLS, service validation, authenticated/unauthenticated tests, segmentation, scanner result triage, rate and availability constraints. | Coverage ledger connecting each target/service to a test result or reason not tested. |
| Web | Authentication and recovery, role/object authorization, sessions, injection, uploads, traversal, SSRF, browser controls, configuration, business logic, race conditions, and logging visibility. | Versioned WSTG mapping and lab findings with positive and negative controls. |
| API | Inventory/OpenAPI, REST and GraphQL, object/function/property authorization, tenant isolation, OAuth/OIDC/JWT, resource limits, sensitive workflows, upstream trust, and API lifecycle. | Multi-role and multi-tenant test matrix; link risks to actual procedures rather than treating a Top 10 as a full methodology. |
| AD | Domain/trust mapping, account policy, privilege relationships, Kerberos/delegation, ACL/GPO, AD CS, relay prerequisites and mitigations, evidence of actual access, and cleanup. | Versioned lab results; document prerequisites and mitigations instead of relying on attack labels. |
| Windows/Linux | Correct platform workflows, service/task permissions, capabilities/tokens, credential boundaries, application configuration, container boundaries, and applicability checks for known vulnerabilities. | At least one reproducible validation per supported procedure, with failure cases and restoration. |
| Pivoting | SSH forwarding, SOCKS/ProxyChains, Chisel, Ligolo, routing, DNS behavior, protocol limitations, overlapping networks, connection checks, and route/agent removal. | Network diagrams, lab connectivity results, and verified cleanup. |
| Vulnerability validation | Distinguish scanner observation, hypothesis, confirmed issue, demonstrated impact, and untested impact; record environmental prerequisites. | Reviewer can reproduce from the recorded evidence without guessing. |
| Credentials/data | Secret entry, protected storage, masking, restricted access, minimum evidence, rotation and retention/destruction records. | Synthetic secret tests across terminal output, reports, attachments, and exports. |
| Reporting/closure | Business impact, reproducibility, root cause, actionable remediation, coverage limitations, cleanup attestation, retest outcomes, residual risk. | Complete reviewed example reports and a closed remediation cycle. |

Maintain a machine-readable coverage matrix. Each test has an ID, domain, applicable assets/roles, reference version, procedure link, status, evidence IDs, and reason for omission. Engagement statuses must distinguish not applicable, not tested, blocked, passed, and failed. Never translate “not tested” into “secure.”

## 6. Standard for every procedure

Adopt one canonical procedure template and retrofit existing pages:

1. Purpose and the security property being tested.
2. Applicable systems, tool versions, prerequisites, permissions, and engagement constraints.
3. Inputs and variables, with clear execution location and shell.
4. Initial observations and a decision tree describing when to proceed or stop.
5. Minimal validation steps, expected outputs, negative controls, and common false positives.
6. Evidence to capture: asset/identity, UTC time, relevant request/response or output, and artifact IDs.
7. How to assess impact without claiming unobserved access or collecting unnecessary data.
8. Remediation, verification steps, and retest expectations.
9. Changes made and how to restore them while preserving logs.
10. Primary references, tested environment, reviewer, and last verification date.

Keep quick commands short and link them to this canonical explanation. Replace blanket rules such as “always” with conditions when outcomes depend on scope or system state. Mark old command syntax as unverified until checked against tool documentation and a pinned lab environment.

## 7. Evidence and reporting architecture

### Data contracts

Evolve SQLite through numbered, transactional migrations with backups and tested restore. Reuse current data rather than starting a parallel notebook that drifts from RB-OPS.

| Record | Minimum information |
| --- | --- |
| Engagement | Stable ID, client/project, objectives, scope version, dates, constraints, contacts, classification, retention, and authorized activities. |
| Asset | Stable ID, host/IP/URL, environment, owner, scope status, services, and identity/role context. |
| Test execution | Procedure/reference version, asset/role, tester, time, outcome, limitations, and evidence IDs. |
| Finding | Stable ID, title, affected assets, description/root cause, prerequisites, reproduction, observed versus potential impact, evidence links, remediation, references, owner, lifecycle, and timestamps. |
| Risk assessment | CVSS version/vector/score, metric rationale, business context, priority, reviewer, and documented overrides. |
| Evidence | Stable ID, engagement-relative path, asset/test/finding links, UTC collection time, collector, tool/version, hash, sensitivity, redacted derivative, and retention status. |
| Attack-chain step | Order, source/destination assets, prerequisite access, outcome, related finding IDs and evidence IDs; references to credentials rather than embedded secret values. |
| Retest | Finding, remediation version/date, test procedure, evidence, result, residual risk, tester, and review date. |
| Change/cleanup | Asset, change made, original state, rollback action, verification evidence, outstanding items, and client acknowledgement where needed. |

Separate protected credential material from reportable metadata. Choose an established encryption/key-storage approach with documented unlock and recovery behavior; do not invent cryptography or store an encryption key beside its ciphertext. Until protected storage is ready, explicitly restrict supported usage to synthetic/lab data.

Preserve original evidence and create separately identified redacted derivatives. Hashes support integrity checks; they do not by themselves prove authenticity. Do not include real engagement workspaces in the public repository or documentation build.

### Report products

- **Executive report:** objectives, scope/limitations, demonstrated business risk, prioritized themes, and a practical remediation roadmap.
- **Technical report:** methodology and versions, coverage, findings, reproducible steps, evidence, attack chains, remediation, cleanup, and retest status.
- **Restricted appendix:** specifically selected sensitive artifacts with documented recipients and handling. Excluded from normal exports.
- **Exam report:** independently maintained template following current official requirements, without assumptions copied into client reports.

Generate Markdown first from structured data; add HTML/PDF and DOCX through reproducible templates once the content contract is stable. Include table of contents, stable finding anchors, readable figures, consistent numbering, classification, version/date, and a delivery manifest. Visually inspect rendered examples before declaring those formats supported.

Support explicit draft and final modes. Drafts can expose visible incompleteness; final generation must fail on required missing fields, unresolved evidence, unreviewed findings, unfilled placeholders, or disallowed sensitive content. A human reviewer must approve the executive narrative and risk conclusions. Do not fabricate summaries from finding counts.

### Finding lifecycle

Use draft → validated → reviewed → reported, followed by remediation and retest states. Preserve false-positive/rejected records and reasons. Retest outcomes include fixed, partially fixed, not fixed, and unable to retest; never infer resolution from a ticket closure alone.

Support CVSS 3.1 data already recorded and add explicit CVSS 4.0 support with a maintained implementation and reference vectors. Preserve the original scoring version when migrating. Keep technical severity separate from business priority; not every observation needs an invented CVSS score.

## 8. Implementation backlog and sequence

Estimates are planning ranges in focused person-days, assuming one experienced maintainer, available lab environments, and reviewer access. They are not elapsed-time promises. Re-estimate after the first complete pilot. Specialist expansion is additional work.

| Phase | Effort | Work and dependencies | Acceptance gate |
| --- | --- | --- | --- |
| A — Correct the baseline | 3–5 days | Fix RB-001/002; triage RB-003; remove misleading cleanup guidance; correct entry-point paths and personal template values; label draft content. Start secret-free export controls. | No mislabeled duplicate core workflows; no unsupported placeholders presented as complete; synthetic secrets omitted from default client output. |
| B — Define the engagement contract | 4–6 days | Agree v1 coverage, procedure/finding/evidence schemas, client/exam separation, scope/ROE/coverage templates, and data handling. Depends on baseline inventory. | A complete synthetic engagement can be described consistently from scope through retest; reviewer accepts schemas. |
| C — Make RB-OPS dependable | 8–12 days | Shared Python package and CLI entry points; preserve current command aliases; explicit `--engagement` alongside tmux; migrations, private permissions, protected credentials, hidden input, error handling, input/path validation, backup/restore, and structured import/export. Depends on B. | Installation and migration work from a clean environment; synthetic fixtures prove isolation, lifecycle, recovery, and absence of unintended secret output. |
| D — Finish core field content | 12–18 days | Complete supported AD/snippet pages; review network and OS procedures; expand web/API coverage; write cleanup, evidence, and retest procedures; consolidate duplicated OSCP notes through canonical links. Depends on B; can proceed alongside C. | Every supported v1 topic meets the procedure template and has a recorded lab verification and coverage mapping. |
| E — Complete reporting | 6–9 days | Finding editing/review/retest, evidence linking, client/exam templates, draft/final validation, redaction, risk tables, and rendered exports. Depends on B/C and representative D procedures. | Two synthetic end-to-end reports pass technical and editorial review; final mode rejects incomplete fixtures; rendered pages are readable. |
| F — Validate and release | 5–8 days | Integrated pilot engagements, documentation search/navigation, offline access, CI/release checks, dependency/tool version manifest, contribution rules, licenses/provenance, and release notes. Depends on C/D/E. | All v1 gates below pass; release includes reproducible setup and known limitations. |

Total core estimate: **38–58 focused person-days**, roughly 8–12 full-time weeks before scheduling contingency. Lab construction, licensing, reviewer availability, and broader specialty content can increase this substantially.

### First ten work items

- [ ] Correct the four mislabeled documents identified in RB-001/002.
- [ ] Inventory and label all 13 placeholders; finish the AD starting map before expanding commands.
- [ ] Add a regression fixture for default-report secret leakage and implement public/restricted output separation.
- [ ] Replace blanket collection, log-clearing, and unrestricted reuse guidance with scope-aware procedures.
- [ ] Create procedure, finding, evidence, coverage, and retest schemas plus one complete synthetic example.
- [ ] Separate professional and exam report templates; remove identifying values and unsupported success claims.
- [ ] Introduce the shared RB-OPS package and explicit engagement selection with compatibility aliases.
- [ ] Migrate finding records to support remediation, evidence, impact, status, and history.
- [ ] Build one vertical slice: authorized lab test → evidence → reviewed finding → report → remediation → retest.
- [ ] Run a second-reader pilot and revise estimates before expanding all domains.

Suggested responsibility split: maintainer owns architecture and releases; domain reviewer signs off procedures; report reviewer checks reproducibility, impact, and clarity. One person may implement multiple roles, but obtain an independent reader for the pilot and release examples.

## 9. Quality gates and definition of done

### Documentation

- All supported navigation resolves; no `COMING SOON` pages on the supported v1 path.
- No unexplained exact duplicate substantive pages or titles contradicting content.
- Every supported procedure has prerequisites, evidence requirements, remediation/retest guidance, tested versions, and verification date.
- Every declared v1 domain maps to concrete test procedures and examples; omissions are explicit.
- Commands are checked in disposable labs for the stated environment. Syntax checks alone are insufficient.
- External links are checked on a schedule with sensible handling of transient failures; internal link and metadata checks run on every change.

### RB-OPS

- Clean installation, help output, environment diagnostics, and supported Python/tmux versions are documented.
- Tests cover two simultaneous engagements, path edge cases, repeated initialization, missing tools, interrupted writes, and report output collisions.
- Migration fixtures preserve existing credentials/findings/chains and can be restored from backups.
- Tests cover scoring reference vectors, finding edits/history, evidence path resolution, missing artifacts, report determinism, and invalid final reports.
- Seed recognizable synthetic secrets into credentials, notes, commands, and sample artifacts; normal exports must not expose them. Document the limits of automatic detection and retain human review.
- Secret file permissions and export handling are tested. Logging must not reintroduce masked credentials.
- The SFTP utility and bundled payload/sample files receive separate operational validation and provenance review before being advertised as supported components.

### End-to-end acceptance

Use two isolated fictional engagements: an internal Windows/AD/Linux environment with a pivot, and a web/API environment with multiple roles/tenants. Each includes confirmed findings, a rejected observation, a blocked test, a benign result, cleanup, remediation, and a retest.

A second tester must be able to follow the guide, locate evidence, reproduce documented results, distinguish untested coverage, and understand remediation without asking the author to reconstruct missing steps. Final client reports contain no placeholders or unintended secrets. No critical release blocker remains open.

### Ongoing maintenance

- Assign owners to domains and review high-change procedures/tool versions at least quarterly.
- Mark stale material visibly; trigger revalidation when an upstream tool or platform breaks a documented path.
- Require changes to include the relevant lab record or an explicit unverified status.
- Keep dated source references, a changelog, compatible versions, and a deprecation policy.
- Track progress by validated procedures and complete reporting scenarios, not document or command count.

## 10. Proposed repository layout

Preserve existing paths initially and add indexes; migrate only with link updates and compatibility notes.

```text
00_START_HERE.md              # choose professional, field, or study path
methodology/                 # lifecycle, scope, ROE, decision trees, coverage
workflows/                   # concise operational routes
enumeration/                 # current service guides, improved in place
active-directory/
privilege-escalation/
pivoting/
web/                         # application and API procedures
reporting/                   # evidence, findings, risk, delivery, retest
templates/                   # canonical schemas and report templates
examples/                    # synthetic engagements and deliverables only
labs/                        # environment manifests and verification records
tools/                       # packaged RB-OPS and supported utilities
tests/                       # migrations, tools, fixtures, report validation
docs/                        # contribution rules, architecture, support matrix
OSCP_NOTES/                  # explicitly separate study/exam track
```

A searchable static documentation site and offline bundle are appropriate once structure stabilizes. Keep Markdown as the source of truth. A web application, multi-user service, and automatic exploitation engine are not prerequisites for completing this resource.

## 11. Reference baseline

References checked during this assessment; pin relevant versions in procedure metadata and recheck before releases.

- [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final): use as a foundation for assessment planning, execution, and post-assessment work; supplement its older technical content with current platform documentation.
- [OWASP WSTG](https://owasp.org/projects/web-security-testing-guide): use released v4.2 test references for the initial web coverage map; the project identifies v5.0 as development work.
- [OWASP ASVS releases](https://github.com/OWASP/ASVS/releases): use stable 5.0.0 requirements to complement test procedures; a requirement mapping does not establish compliance by itself.
- [OWASP API Security Top 10 2023](https://api-security.owasp.org/editions/2023/en/0x03-introduction/): use for API risk coverage, supplemented by detailed authorization, workflow, and protocol test cases.
- [FIRST CVSS v4.0 specification](https://www.first.org/cvss/v4.0/specification-document): use for versioned scoring support and validation; preserve existing 3.1 records rather than silently translating scores.

The release objective is a resource that reliably answers: what should I test, when is the procedure applicable, what proves the result, what should the client fix, and how do I verify that it is fixed?
