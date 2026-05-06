# External Skill Attribution for v1.6.0

ZIP-your-Research v1.6.0 integrates external writing and figure-making materials as source-preserved references and ZYR-native routing wrappers. These integrations are used with attribution and without claiming the upstream materials as original ZYR inventions.

## Integrated upstream sources

| Source | Upstream repository | Integrated location | Role in v1.6 |
|---|---|---|---|
| Research-Paper-Writing-Skills | [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | `ext/src/rpws/` | Reviewer-facing paper structure, section guides, and claim-evidence writing discipline. |
| Prof. Peng Sida open research notes | [pengsida/learning_research](https://github.com/pengsida/learning_research) | Acknowledged through Research-Paper-Writing-Skills upstream attribution | Original writing methodology source credited by Research-Paper-Writing-Skills. |
| awesome-ai-research-writing | [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) | `ext/src/awesome/` | Academic writing prompts, bilingual rewriting, logic checking, and prompt examples. |
| figures4papers | [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers) | `ext/src/figures/` | Publication-quality figure design principles, plotting scripts, and scientific-figure examples. |
| S340 v4.2 ruleset | user-authored local bundle maintained with this release; not an external GitHub dependency | `ext/src/S340_v4.2_theory_global_skill_bundle/` | Hard logic, language, and paper-quality requirements used as the global writing-review gate. |

## Integration boundary

The external source trees are preserved as reference material. The new `skills/rwf_s340/` files are ZYR-native routing and execution wrappers that reorganize those materials into public-facing workflows: paper writing and review, figure production, style and logic review, and no-omission validation.


## S340 provenance note

`S340 v4.2` is authored by the maintainer/user of this release and is integrated as a local requirement layer. It should not be described as a third-party package, and the README should not claim that a public GitHub upstream exists. Its role is to harden ZYR writing behavior: structure before wording, evidence before claim strength, and explicit removal of unsupported transitions, mechanical slogans, and forbidden phrasing patterns.
