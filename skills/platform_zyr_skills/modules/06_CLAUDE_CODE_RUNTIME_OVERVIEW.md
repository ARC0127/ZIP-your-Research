# 06 — Claude Code runtime overview

This module family captures what ZYR can learn from the Claude Code runtime architecture without importing Anthropic-private product behavior.

## What this source family is

- Source family: `claude-code-sourcemap-main/restored-src/**`
- Nature: public-package reconstruction plus source-map recovery
- Use case inside ZYR: runtime architecture reference, not product cloning

## Why it belongs here

Claude Code contributes strong operational patterns in areas where ZYR benefits from more runtime structure:

- tool contracts
- permission boundaries
- query/session lifecycle separation
- skill discovery and frontmatter loading
- plugin packaging
- remote permission bridging

These are execution-substrate concerns, which fit `platform_zyr_skills` better than `research_core` or `proof_engine`.

## What the rewrite set contains

- A compact topic layer:
  - [../rewrites/claude_code_runtime_rw_20260331/README.md](../rewrites/claude_code_runtime_rw_20260331/README.md)
- A full source-mapped layer:
  - [../rewrites/claude_code_runtime_rw_20260331_f15/INDEX.md](../rewrites/claude_code_runtime_rw_20260331_f15/INDEX.md)

## What ZYR should extract

- portable interface shapes
- runtime layering choices
- durable transcript/state patterns
- skill/plugin packaging rules
- explicit non-goal boundaries around private auth and backend glue

## What ZYR must not do

- copy Anthropic-specific OAuth logic
- copy subscription or entitlement checks
- copy private remote-control backend contracts
- treat the source snapshot as authoritative product source
