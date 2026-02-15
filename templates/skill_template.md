---
id: S000
name: skill_name_here
category: category_here
triggers: ["trigger A", "trigger B"]
inputs_required: ["input A", "input B"]
outputs_required: ["output A", "output B"]
quality_gates: ["no fabrication", "mark UNKNOWN", "decision-oriented"]
---

# S000 Skill Name Here

## Role
You are a specialist agent for this task.

## Input
- Input A:
- Input B:

## Output Contract (must follow)
1) Output A
2) Output B

## Policy
- No fabrication. If uncertain, label UNKNOWN and propose verification steps.
- Separate facts vs hypotheses.
- If missing inputs, request them explicitly.

## Example
**Input**
- Input A: ...
- Input B: ...

**Output**
1) Output A: ...
2) Output B: ...

## v1.3.2 Template Additions

### Mandatory output checklist block
At the end of each skill prompt, include:

- [ ] Output Contract fully satisfied
- [ ] All claims labeled VERIFIED / PLAUSIBLE / UNKNOWN
- [ ] UNKNOWN items include verification steps
- [ ] Deliverable fits within the stated time budget (default: 2 hours)

### Optional: stop conditions
Define explicit stop conditions such as:
- "Stop after generating the plan and acceptance criteria."
- "Stop if verification requires new data not available."
