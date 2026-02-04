# Workflow Chain Template (v1.0.1)

Use this when authoring a new workflow in `docs/WORKFLOWS.md`.

## Header
- Name:
- When to use:
- Inputs:
- Time budget:
- Deliverables:

## Steps (each step is a skill)
1) Skill ID:
   - Purpose:
   - Required inputs:
   - Output files (if any):
   - Stop condition:
2) ...

## Quality gates
- No fabrication, label UNKNOWN.
- Decision-oriented.
- 2-hour deliverable by default.

## Failure handling
- If any step fails: record the failure, then run the relevant debug skill (e.g., S309 error_analysis_playbook).
