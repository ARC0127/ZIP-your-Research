# Astra instruction audit — 2026-09-07

This follow-up applies the two requested readings to the actual Codex instruction
stack. Suite version stays **1.6.6**; the active router stays **v1.8**. No historical
research module is removed. The user authorized edits, local installation, and
GitHub synchronization, and previously chose to retain **GPT-6 Astra / xhigh**.

## Sources and reading coverage

- OpenAI, [Using GPT-6 Astra](https://developers.openai.com/api/docs/guides/latest-model):
  fetched the complete Markdown through the official documentation connector,
  including introduction, new features, prompting guidance, and migration.
- Eric Provencher (@pvncher), [Rethinking skills and prompts for GPT-6 Astra](https://x.com/pvncher/status/2095991462416490862),
  September 4, 2026 UTC: read all text blocks, headings, captions, and the closing
  paragraph from the public FxTwitter representation of that exact post. Its
  article identity is `2095989703967125509`; author, title, post identity and
  article identity matched. This was author text delivered through a third-party
  mirror, not a secondary summary. Direct X requests returned HTTP 403. The two
  embedded example images were **not inspected**: the browser could not verify
  its admin-enforced access policy. No image-only details are asserted here.

The official guide supports auditing persistent instructions, making completion
explicit, calibrating verification, and retaining effective reasoning effort.
Its delegation advice is configurable: it says Astra may delegate less than a
workflow wants. It does not establish that excessive agents are an intrinsic
model defect. The single-agent default is this user's local operating choice.

Eric emphasizes concise discovery descriptions, selective reference loading,
removing excessive step-by-step prescriptions, and defining completion and
approval boundaries precisely. His discussion of description truncation matches
the actual session catalog: many entries began with repeated ZYR identifiers
and were shortened before the distinguishing task appeared.

## Effective stack inspected

1. Codex host instructions and the injected skills catalog: runtime-owned and
   not editable through repository files.
2. `$CODEX_HOME/AGENTS.md`: the user's global file. No home override was found.
3. Repository `AGENTS.md`: the only AGENTS file found on the workspace's ancestor
   chain and in the relevant source tree.
4. `$CODEX_HOME/config.toml`: reasoning/model and instruction-path settings only;
   no additional instruction file was configured. No credentials were copied.
5. ZYR discovery metadata, installed wrappers, active resource policy, source
   generator, and selected writing, evolution, memory, and theory entries.
6. The adjacent user-maintained Headroom, Theory Claim Audit, and Claim entrypoints;
   the current OpenAI Docs and Skill Creator instructions. Full scientific or
   vendor reference trees were not all loaded or treated as global instructions.

Automatic memories are navigation supplied by the host, not configuration to
rewrite. The project experience INDEX was read; the pre-existing untracked
`.codex/` directory is outside this commit. Vendor plugin caches and invocation
policies are unchanged.

## Findings and implemented edits

| Priority / file | Previous instruction or pattern | Practical effect | Implemented edit |
|---|---|---|---|
| High — global AGENTS | “全程保持高度逻辑化思考” plus repeated final checklists and universal S340 scanning | Routine answers inherit formal research ceremony | Keep evidence discipline in a compact root; load formal-writing detail for its actual task |
| High — global AGENTS §3 | Full archive templates and lock procedure in every context | Storage mechanics consume context even without a storage operation | Preserve the complete protocol in `instructions/archive-protocol.md`; retain startup/index, write, consent, privacy, and concurrency boundaries |
| High — ZYR installer | `ZYR {title}: {purpose}. Use for ... or an explicit {sid} request.` | Repeats identity before usefulness; broad triggers and truncated descriptions impair selection | Add 150 concise capability-first descriptions; preserve IDs, names, protocols, and invocation policies |
| High — Headroom SKILL | “context compression, token reduction ... cross-agent memory” | Generic token questions can pull in an unrelated tool repository | Trigger on Headroom use/development or explicit application of its ideas; choose relevant orientation documents |
| High — Theory Claim Audit SKILL | “For an early discussion round, stop after the first two protocol steps” | A requested complete audit can stop because the project is early-stage | Bind the checkpoint to explicitly iterative discussion; complete requested audits with provisional branches/UNKNOWN while retaining human ownership of assumptions and claims |
| Medium — repository AGENTS | “PRE-LOCK: intake / mode lock / usage clarification only” | The retained sentence can look unconditional even with the active profile above | Put the existing strict-workflow qualifier beside the stage rule; reuse current maintenance authorization |
| Medium — global testing rule | “优先添加…最小确定性测试” without a task qualifier | Encourages tests for text-only changes | Apply differential tests to defects/executable contracts, keep required checks, stop after passing relevant checks |
| Medium — global NO_CHANGE | “问题无法复现…NO_CHANGE” | Lack of reproduction may prematurely close a valid diagnostic task | Distinguish evidence of no change needed from inability to reproduce |

The root global file now defines delivery as the authorized result plus relevant
verification, and says that a first implementation is not necessarily completion.
Same-objective steering retains accepted facts and work. Instructions that cause
a pause must be identified by file and exact rule.

## Authority and safeguards

The edits expand routine follow-through and permit provisional analysis when a
complete audit is requested. They do **not** grant new authority over publication,
deployment, external messages, credentials, real money, devices, production data,
security settings, or protected memory activation. Explicit review-only requests,
action-time confirmations, scientific acceptance by the researcher, strict ZIP
CONFIRM, and S661 consent/attestation gates remain in force. Existing approval for
the same action is reused where the governing policy allows it.

Claim's coaching, formula-clarity, fresh-literature and challenge rules remain
byte-identical. Those are intentional user contracts, not generic overhead to
remove. Reading archived advice does not authorize executing historical plans.

## Installation and rollback

The versioned installer reuses v1's backup/hash/restore mechanism. Default mode
changes ZYR only. The personal profile is explicitly opted into; it is this
user's profile, not a required global policy for every ZYR contributor.

```powershell
py -3 -B tools/install_codex_profile_v2.py --codex-home D:/codex/home --include-user-instructions --apply --backup D:/codex/backups/CHOOSE-NEW-DIRECTORY
py -3 -B tools/install_codex_profile_v2.py --codex-home D:/codex/home --include-user-instructions --check
py -3 -B tools/install_codex_profile_v2.py --codex-home D:/codex/home --restore D:/codex/backups/CHOOSE-NEW-DIRECTORY/receipt.json
```

The actual backup directory for this run is
`D:/codex/backups/astra-instructions-20260907/`; the installation receipt is under
`install/`. Additional refinement receipts, if needed, must be restored newest
first. Restore refuses to overwrite a later user edit. The original global file
is also preserved locally. No original article text or private configuration is
published with this repository.

Use v2 for the current description profile; v1 intentionally remains a historical
installer and can restore the earlier description layout. Start a new task or
reload Codex to refresh global instructions and skill discovery. Files already
injected into a running conversation cannot be retroactively removed.

## Verification boundary

Check description/manifest closure, metadata preservation, opt-in target scope,
existing routing and installation regressions, generated artifacts and the
required repository validation. Inspect the final install and preserved Claim /
configuration hashes. File and description byte counts measure context packaging;
actual token use, latency, and task-quality changes remain **UNKNOWN** without
paired measurements. No scientific capability gain is claimed.

Local checks on 2026-09-07: 77 Python tests ran (76 passed, one platform-specific
skip); 33 compatibility routing cases passed; generated build check,
`validate_v7_2.py`, and `zyr.py check --ci` passed. Description coverage includes
all 150 mapped identities. The remaining three ZYR entries are suite routers.

| Local packaging measure | Before this follow-up | Candidate |
|---|---:|---:|
| Global AGENTS bytes | 25,448 | 5,652 |
| ZYR description bytes | 16,364 | 7,463 |
| ZYR SKILL.md bytes | 165,819 | 156,322 |
| ZYR entries | 153 | 153 |

The README now has a single dated latest-update section. Future updates replace
that section; detailed provenance remains in linked audits and Git history.
