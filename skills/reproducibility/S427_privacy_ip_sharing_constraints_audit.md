---
id: S427
name: privacy_ip_sharing_constraints_audit
category: reproducibility
triggers:
- privacy audit
- IP audit
- sharing constraints
- license constraints
- data rights
inputs_required:
- data_sources
- ownership_info
- sharing_target
outputs_required:
- constraint_map
- risk_register
- verification_record
quality_gates:
- no_fabrication
- mark_UNKNOWN
- audit_first
- copy_paste_ready
---

> **Global invariant (ZIP your Research):** Truthfulness • Trustworthiness • Deep logical reasoning. If required info is missing → mark **UNKNOWN** and ask minimal questions.

# S427 Privacy / IP / Sharing Constraints Audit

## Role
Identify constraints that affect data/code sharing: privacy, IP, licenses, contractual limits.

## Input
- Data sources and ownership
- Any agreements (if any)
- Intended sharing target (open / controlled / internal)

## Output Contract
1) Constraint map: privacy, IP, contractual, security.
2) Risk register with severity and mitigations.
3) Recommended sharing tier (open/controlled) with justification.
4) Verification record (UNKNOWN items + whom to ask / documents needed).

## Rules
- Do not give legal advice; output a checklist and risk map.
