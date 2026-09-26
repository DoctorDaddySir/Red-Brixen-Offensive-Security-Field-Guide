# Command verification standard

Readers should be able to copy a command after setting its documented inputs and know exactly what was tested. The guide remains a manual reference: the tester runs and interprets each step. Lab scripts are maintainer QA, not a required reader workflow. See the [field-guide standard](FIELD_GUIDE_STANDARD.md).

| Status | Evidence required | What it does not establish |
| --- | --- | --- |
| Reference-reviewed | Primary source, date, applicable release | Command execution or successful behavior |
| Syntax-checked | Parser/tool check and result | Runtime prerequisites or target behavior |
| Executed | Actual invocation, shell/platform/version, exit result | Correct security conclusion or full workflow |
| Lab-validated | Expected result, meaningful negative control, scope and cleanup evidence | Compatibility with untested platforms or versions |

Every new or substantially changed operational command must name the execution location (operator, target, or tool console), shell, required tools/versions, privilege requirements, input variables, expected result, and cleanup. Use fenced code without shell prompt prefixes. Avoid `<IP>` placeholders that the shell interprets as redirection. Define variables once and quote them where appropriate; never put real credentials in examples.

A guide must link its actual verification record before calling a command verified. Record timestamps, tool versions, the command or executable source, expected/actual outcomes, negative controls, and limitations. Tests must assert behavior rather than merely checking that help text exists. Do not label the whole guide verified because one command passed.

Maintain protocol/platform distinctions. A TCP loopback test does not verify DNS, UDP, remote routing, Windows agents or a privilege escalation. Use a disposable target and synthetic evidence for invasive steps. Preserve reviewed source versions and rerun relevant checks after command changes.

## Current coverage

The [SSH/SOCKS lab](../labs/pivoting/README.md) establishes a first narrow, reproducible baseline. The [recorded result](../labs/pivoting/ssh-socks-result.json) names tested versions and individual assertions.

All other command families retain their previous status; where no explicit execution record exists, treat them as **unverified**, even if the prose sounds authoritative. AD, Windows boundary validation and full remote pivoting remain pending. Track expansion in [RB-014](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/18); Ligolo has [RB-013](https://github.com/DoctorDaddySir/Red-Brixen-Offensive-Security-Field-Guide/issues/17).

## Release checklist

- [ ] All supported command families have an explicit version/platform and evidence record.
- [ ] No literal shell-redirection placeholders or embedded secrets occur in copyable commands.
- [ ] Setup and cleanup are reproducible and limited to test-created resources.
- [ ] Expected behavior and a useful failure case are recorded.
- [ ] Legacy examples without records are marked unverified rather than silently promoted.
