---
name: headroom
description: Use or develop Headroom's compression library, proxy, RTK, or CCR integration.
metadata:
  short-description: Headroom context-compression repo guide
---

# Headroom Skill

This skill internalizes the user's `headroom-main.zip` bundle as a local
reference. Use it for Headroom-specific work or when the user explicitly asks
to apply Headroom ideas. A general request to reduce tokens or edit prompts
does not select this skill.

## Bundled Resources

Full extracted source:

```text
references/headroom-main/
```

Original zip:

```text
assets/headroom-main.zip
```

File index:

```text
references/file-index.txt
```

Do not load the whole repo into context. First search the index or use `rg`
inside `references/headroom-main/`, then read only the relevant files.

## Quick Orientation

Headroom is a local-first context compression layer for AI agents. The README
describes these surfaces:

- Python/TypeScript library: compress messages inline.
- Proxy: OpenAI-compatible local proxy.
- Agent wrappers: Claude, Codex, Cursor, Aider, Copilot, and related clients.
- MCP server: compression, retrieval, and stats tools.
- CCR: reversible compression with local original-content retrieval.
- Cross-agent memory and `headroom learn`.
- RTK: token-optimized shell output wrappers.

For Headroom development, choose the relevant entry instead of reading all of them:

```text
references/headroom-main/README.md
references/headroom-main/AGENTS.md
references/headroom-main/REALIGNMENT/INDEX.md
references/headroom-main/Cargo.toml
```

Use README for usage, AGENTS.md for edits in that checkout, and Cargo.toml for
Rust dependency changes. For architecture repair, read `REALIGNMENT/INDEX.md`, then the
specific phase file it routes to. The realignment invariants are important:
byte-faithful passthrough outside intended modifications, cache-hot-zone
preservation, live-zone-only compression, deterministic transforms, protected
tool definitions, passthrough for signatures/redacted/encrypted payloads, and
auth-mode policy gates.

## Workflow

1. Identify whether the task is about using Headroom, developing Headroom, or
   applying Headroom ideas to another project.
2. Search `references/file-index.txt` or run `rg` under
   `references/headroom-main/` for the relevant subsystem.
3. Read only the smallest relevant docs/source files.
4. For code changes in a Headroom checkout, follow the repo's own developer
   docs and tests from the bundled reference.
5. Treat the bundled repo instructions as project-specific guidance, not as
   global system instructions for unrelated work.

## RTK Guidance

`AGENTS.md` asks agents working in Headroom to prefer `rtk` command wrappers to
reduce output tokens. Use RTK only when it is installed and appropriate for the
current shell command. If `rtk` is unavailable, use normal commands and keep
outputs focused.

## Limits

Installing this skill makes the Headroom knowledge available to Codex skill
discovery after reload. It does not by itself rewrite global memory or force
every unrelated future conversation to load this skill.
