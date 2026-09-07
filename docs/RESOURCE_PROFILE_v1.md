# Resource profile and Codex installation — ZYR v1.7.0

The active [execution profile](../boot/14_RESOURCE_PROPORTIONAL_EXECUTION_v1.md)
uses one primary skill, progressive references, and the current agent for
ordinary work. Explicit S660 research keeps its multi-agent contract; strict ZIP
startup keeps CONFIRM. Complete authorized deliverables and relevant checks.
Do not repeat passing checks or restart intake without a concrete reason.
Ordinary replies have no status banner. Status is shown on user request or
diagnostic opt-in, without repeating unchanged fields; strict ZIP confirmation
and the underlying safeguards still apply.

## Why these defaults

The [official GPT-6 Astra guide](https://developers.openai.com/api/docs/guides/latest-model)
recommends auditing skill instructions, making completion explicit, and
calibrating tests. Its delegation advice is configurable; the single-agent
default here is a local workflow choice. Model and reasoning settings remain
under user control.

Eric Provencher's [Rethinking skills and prompts for GPT-6 Astra](https://x.com/pvncher/status/2095991462416490862)
supports short capability descriptions, selective reference loading, and precise
approval boundaries. The September 7 review read the complete official Markdown
and the article text through a public mirror; two embedded images could not be
verified because browser policy enforcement was unavailable. The
[historical audit](https://github.com/ARC0127/ZIP-your-Research/blob/b290a2a650b2e0f4dab55ff613697ae1fdcfe86f/docs/ASTRA_INSTRUCTION_AUDIT_v1.md)
retains the detailed findings without adding another current instruction entry.

## Update an existing installation

The v2 installer requires the existing full ZYR installation. It preserves 153
entry identities, canonical protocols, and invocation policies. Detailed source
protocols remain in `references/source.md`; 150 mapped descriptions are maintained
in `manifests/codex_descriptions_v1.yaml`. The default changes ZYR files only.

Run from the repository root, replacing paths with your own. Each backup path
must be new and outside the corresponding target root.

```powershell
py -3 -B tools/install_codex_profile_v2.py --codex-home D:/codex/home --apply --backup D:/codex/backups/zyr-update-NEW
py -3 -B tools/prune_retired_docs_v1.py --root D:/codex/home/skills/zip-your-research/references/upstream/ZIP-your-Research-main --apply --backup D:/codex/backups/zyr-docs-NEW
py -3 -B tools/install_codex_profile_v2.py --codex-home D:/codex/home --check
py -3 -B tools/prune_retired_docs_v1.py --root D:/codex/home/skills/zip-your-research/references/upstream/ZIP-your-Research-main --check
```

The cleanup command only deletes exact, unchanged retired copies and saves their
original bytes. A changed copy is kept and reported for inspection. Older v1
installers remain compatibility tools; use v2 for current discovery metadata.
Reload Codex or start a new task to refresh already loaded instructions.

## Optional personal profile

`--include-user-instructions` also installs `templates/codex-home/` and the
existing Headroom / Theory Claim Audit entrypoints. Review those templates before
adopting this user's personal profile elsewhere. It moves conditional writing,
engineering, and archive rules into references; it retains human scientific
choices and real approval boundaries. It does not change model configuration,
Claim's coaching/fresh-literature contract, vendor caches, or automatic memories.

## Rollback

Restore the cleanup receipt first, then the installer receipt:

```powershell
py -3 -B tools/prune_retired_docs_v1.py --root D:/codex/home/skills/zip-your-research/references/upstream/ZIP-your-Research-main --restore D:/codex/backups/zyr-docs-NEW/receipt.json
py -3 -B tools/install_codex_profile_v2.py --codex-home D:/codex/home --restore D:/codex/backups/zyr-update-NEW/receipt.json
```

Restoration refuses later edits. Keep receipts outside the installation. Byte
counts measure packaging size; token use, latency, behavior quality and scientific
benefit require paired evaluations and are not established by file cleanup.
