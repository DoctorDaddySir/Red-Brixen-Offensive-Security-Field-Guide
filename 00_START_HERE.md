# Start here — manual field reference

Choose the task you need. These references are not an automated sequence: the tester decides what to run and how to interpret the result. No RB utility or special workspace is required.

| Current task | Reference |
| --- | --- |
| Establish services and entry points | [Initial enumeration](workflows/01_initial_enum.md) |
| Assess an HTTP application | [Web workflow](workflows/02_web.md) |
| Investigate SMB | [SMB workflow](workflows/03_smb.md) |
| Map a domain and access relationships | [AD start](active-directory/00_ad_start_here.md) |
| Investigate Linux local privileges | [Linux escalation](workflows/05_privesc_linux.md) |
| Investigate Windows local privileges | [Windows escalation](workflows/06_privesc_windows.md) |
| Reach an approved internal service | [Pivoting workflow](workflows/07_pivoting_tunneling.md) |
| Write up a demonstrated issue | [Finding template](exploited-vulns/_TEMPLATE/finding_template.md) |
| Reassess a stalled hypothesis | [Problem-solving references](hacker-mindset/README.md) |

Before executing a command, confirm the applicable platform, tool version, required access, scope, execution location, inputs, and expected result. Read any verification limitations. A listed attack path is a hypothesis until the required conditions and result are established.

Keep ordinary notes and evidence files in your preferred system. Record the host/account, timestamp, command, relevant output, interpretation, and next action. Use the [manual reporting references](reporting/README.md) and complete a standalone finding template when warranted; no database or report generator is needed.
