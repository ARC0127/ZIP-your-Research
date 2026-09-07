# ZYR resource profile v1

Suite release remains **v1.6.6**. This is a maintenance profile, not a claim
that scientific capability or measured end-to-end token efficiency improved.

## GPT-6 Astra alignment (verified 2026-09-07)

The [official model guide](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)
describes sensitivity to skill instructions, clarification pauses, detailed
formatting, configurable delegation, and overly broad tests on small changes.
This profile maps those observations to the following defaults:

| Officially described behavior | ZYR behavior |
|---|---|
| Greater sensitivity to skills and AGENTS.md | One applicable contract, progressive references, explicit precedence over retained blanket defaults |
| Clarification can interrupt expected follow-through | Reuse current authorization; finish independent work while required input is pending |
| Detailed formatted responses | Lead with the result and decisive evidence; avoid repeated deliberation and unnecessary status artifacts |
| Delegation depends on prompting and host needs | Single-agent default; preserve explicitly requested S660, independent review, and named skills |
| Small changes can trigger excessive testing | Relevant checks, completion criteria, and no repeat without new evidence |

The guide says Astra can delegate less often than desired. It does not establish
that over-delegation is an intrinsic model defect. ZYR's former broad triggers
are local evidence for this user's reported overhead. Neither a smaller entry
file nor a deterministic routing test establishes end-to-end token savings.

Model/API features such as asynchronous tools and mid-turn steering do not
require extra worker agents. Existing host tools provide those capabilities;
this patch does not add an API integration or change reasoning settings. The
user's GPT-6 Astra / xhigh choice and the claim skill's search rules are retained.

## Behavior

The active policy is [resource-proportional execution](../boot/14_RESOURCE_PROPORTIONAL_EXECUTION_v1.md).
It scopes old unconditional companion rules while preserving complete requested
outputs, evidence requirements, explicit approvals, and strict ZIP boot.
Same-objective steering does not restart intake. Default execution uses the
current agent. The separate claim coaching/fresh-literature contract is unchanged.

`python tools/zyr.py route "query"` uses `router/route_v1_8.py`. Ordinary
authoritative search selects S204; explicitly requested multi-agent research
retains S660. Explicit named-skill requests take precedence over a shorter
default route. Merely discussing S660 does not launch it, and refusing a team
while requesting ordinary search is not a routing conflict. Related skills
appear in `optional_companions` instead of forcing
every workflow to run. Negation, ambiguous requests, untrusted source boundaries,
and unavailable capabilities retain the v1_7 checks. `route-test` retains the
33-case v1_7 compatibility suite; active routing has separate regression tests.

## Installed skills

The current follow-up uses `tools/install_codex_profile_v2.py` for concise
discovery descriptions and an opt-in personal instruction profile. See the
[Astra instruction audit](ASTRA_INSTRUCTION_AUDIT_v1.md) for source coverage,
specific edits, current installation commands, and authority boundaries.
The v1 commands below describe the retained initial profile.

`tools/install_codex_profile_v1.py` updates an existing complete ZYR installation.
It creates short SKILL.md entrypoints, preserves full protocols in references,
and synchronizes the listed active source files to the packaged suite. Historical
writing modules remain verbatim. Existing names, version, and invocation-policy
files are retained. The research-evolution workflow distinguishes maintenance,
agent-behavior evidence, and scientific-capability promotion.

```powershell
py -3 -B tools/zyr.py build
py -3 -B tools/zyr.py build --check
py -3 -B tools/validate_v7_2.py
py -3 -B tools/zyr.py route-test
py -3 -B -m unittest tests.integrity.test_resource_profile_v1
py -3 -B tools/install_codex_profile_v1.py --skills-root D:/codex/home/skills --apply --backup D:/codex/home/skill-backups/CHOOSE-NEW-DIRECTORY
py -3 -B tools/install_codex_profile_v1.py --skills-root D:/codex/home/skills --check
```

Rollback uses the exact receipt from the apply command:

```powershell
py -3 -B tools/install_codex_profile_v1.py --skills-root D:/codex/home/skills --restore D:/codex/home/skill-backups/CHOOSE-NEW-DIRECTORY/receipt.json
```

The installer rejects paths outside the installation and refuses rollback over
later edits. It does not touch model settings, the claim skill, plugin caches,
automatic memories, or other projects. Restart Codex or use a new task to refresh
skill discovery; already loaded instructions cannot be removed from a running
conversation by changing a file.

## Evidence and acceptance

The 2026-09-07 user approved review items 1-6 and chose to retain GPT-6 Astra
with xhigh. The baseline was preserved before editing. Acceptance requires:
all 153 ZYR entries remain; all 150 mapped source protocols match the current
repository; untouched modules and non-ZYR skills remain byte-identical;
active routing preserves explicit multi-agent work and trust boundaries;
installation check and rollback tests pass. Entry bytes and description bytes
are packaging metrics. Agent-behavior tokens, time, and scientific benefit remain
UNKNOWN until measured on paired real tasks with equal settings and quality gates.

The design follows official guidance on instruction sensitivity, proportional
testing, and outcome-focused prompting: [GPT-6 Astra guide](https://developers.openai.com/api/docs/guides/latest-model).
Progressive loading follows [OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills).
Published model evaluations and launch commentary are context, not evidence for
this installation's measured improvement.
