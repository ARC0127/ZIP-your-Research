# Rewrite (portable): src/skills/loadSkillsDir.ts

**Source (Claude Code snapshot):** `claude-code-sourcemap-main/restored-src/src/skills/loadSkillsDir.ts`  
**Snapshot:** sha256 `d66e37fd2db4404b75330223831c5fd7f278afef58a92bc660fb86d002833744` - 34415 bytes - mtime(UTC) `2026-03-31 08:30:12`  
**Rewrite date:** 2026-03-31

## 1. Source role

Loads skills from layered directories, parses shared frontmatter fields, deduplicates them, and activates path-conditional skills.

## 2. Ground truth extracted from source

- Skill frontmatter includes description, tool permissions, model, effort, hooks, and path activation.
- Discovery happens across managed, user, project, and explicit additional roots.
- Dedup uses resolved file identity, not just skill name.

## 3. What ZYR should absorb

- Shared skill frontmatter schema.
- Deterministic layered discovery.
- Conditional activation by touched paths.

## 4. ZYR-native rewrite / interface shape

Create a ZYR `skill_loader` that:

- parses a stable frontmatter schema
- resolves roots in order
- deduplicates by file identity
- separates unconditional and conditional skill activation

## 5. What must not be copied

- Claude-specific policy-setting names.
- Directory rules that only make sense inside Claude Code.

## 6. Cross-links to compact topic docs

- [`SKILL_DISCOVERY_AND_FRONTMATTER_REWRITE_ZYR.md`](../../../claude_code_runtime_rw_20260331/SKILL_DISCOVERY_AND_FRONTMATTER_REWRITE_ZYR.md)

## 7. Maintenance note

If new frontmatter fields become important, update the compact summary and ZYR schema docs in the same change.
