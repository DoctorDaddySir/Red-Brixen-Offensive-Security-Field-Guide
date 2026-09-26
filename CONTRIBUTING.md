# Contributing to Red Brixen

Every implementation ticket uses its own branch and pull request. Start from the current `origin/master`, name the branch `ticket/rb-NNN`, and limit its changes to that ticket. Link the issue in the PR and explain the behavior change, verification, remaining limitations, and dependencies.

The repository owner approves and merges pull requests. Contributors must not merge their own work or enable automatic merging on the owner's behalf. Do not mark an issue complete until its acceptance criteria are met. Use a draft PR when required verification is outstanding.

For dependent work, wait for the prerequisite to merge, then branch from updated master. Independently reviewable tickets may proceed on separate branches. Do not mix unrelated fixes into the same PR.

## Documentation verification

Check local links, heading/content agreement, fenced code blocks, and whitespace. Cite primary documentation for platform-dependent claims. State the tested environment and date; distinguish reference review from commands actually executed in a lab. Never claim an unperformed test passed.

## Tool verification

Use synthetic data in temporary workspaces. Exercise changed behavior and important failure cases, and record the exact checks in the PR. Never commit real credentials, client data, private reports, or collected evidence.

## Release readiness

Use the acceptance gates in [the completion plan](PROJECT_EVALUATION_AND_COMPLETION_PLAN.md). A merged content correction does not by itself establish lab validation or release readiness. Preserve unresolved validation work in the relevant issue or follow-up ticket.

## Copyable commands

Follow the [command verification standard](docs/COMMAND_VERIFICATION.md). Record actual runs and relevant failure cases before labeling examples verified. The [pivoting smoke lab](labs/pivoting/README.md) provides the first executable baseline; it does not validate other command families.
