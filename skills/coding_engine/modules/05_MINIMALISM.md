## 5) Minimalism & anti-scaffolding (v1.3)

Goal: raise code quality by **doing less, but verifiably correct**.

### Rules
- Prefer **one working path** over many knobs.
- New flags/features are allowed only if:
  1) they are exercised by a reproduction command, and
  2) they change output in a measurable way, and
  3) they do not create additional failure modes without tests.

### Anti-patterns (MUST NOT)
- “Future-proof” abstractions that are unused in the current acceptance criteria.
- Adding optional parameters “just in case”.
- Creating new files when a small diff suffices.

### Required output when proposing any refactor
- `minimal viable diff` (what is the smallest change that fixes the issue)
- `cleanup plan` (what will be deleted later if you must add scaffolding)
- `regression command(s)` proving no behavior change (unless desired)

