# Quickstart — ZYR v1.7.0

For first use, [the homepage walkthrough](../README.md#quick-start) provides
copy/paste, local Codex, and ZIP startup steps with task inputs and expected outputs.

## Use one skill

Choose the task in [the skills guide](SKILLS.md) or search [INDEX.md](../INDEX.md)
for its Sxxx identifier. With Codex skills installed, invoke that skill and give
it the material to work on. For copy/paste use, copy the selected source prompt
and fill its required inputs. Load another workflow only for a distinct need.

Examples: S204 for literature triage, S203 for claim/evidence review, S603 for
local prose, S235 for proof gaps, and S301 for a decisive experiment. A full
manuscript review can select the writing engine and its applicable global checks.

## Start an explicitly strict ZIP session

Upload the ZIP, request ZIP startup, and follow
[the bootstrap protocol](../boot/00_BOOTSTRAP_PROTOCOL_v1.7.0.md). Complete intake
and confirm the Mode Lock before locked work. These stage rules apply to that
selected workflow; ordinary repository work and atomic skill use do not restart
intake. Corrections within the existing objective reuse its authorization.

## Local tools

Run from the repository root:

```bash
python -m pip install -r requirements.txt
python -B tools/zyr.py build --check
python -B tools/validate_v7_3.py
python -B tools/zyr.py route "summarize this paper and extract claims" --json
```

For an existing Codex installation, follow [installation and cleanup](RESOURCE_PROFILE_v1.md).
For a release archive, use [the release guide](RELEASE.md).
