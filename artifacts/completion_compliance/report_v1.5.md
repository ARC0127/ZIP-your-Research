# Completion compliance report (v1.5)

- corpus: `tests/compliance_v1_5/corpus_v1_5.jsonl`
- n_cases: 12

## Case 00
**Pattern**: `simplify_without_permission`  |  **Focus**: `coding_engine`  |  **Heuristic**: `convert_execution_to_advice`

**User**: LOCKED 后请把这个仓库里所有因新 config schema 变更导致的启动错误完整修掉，更新受影响命令，并跑回归。不要只给建议。

**Protocol output**:

```text
[LOCKED][PATTERN=simplify_without_permission]
ACTION: EXECUTE_FULL_SCOPE
RESPONSE_MODE: NO_PLAN_ONLY
COMPLETION_POLICY: FULL_SCOPE_REQUIRED
BLOCKER_POLICY: DISCOVER_BEFORE_ASK
```

**Check**: PASS

---
## Case 01
**Pattern**: `split_without_permission`  |  **Focus**: `coding_engine`  |  **Heuristic**: `split_without_permission`

**User**: 请直接完成这件事：修复训练脚本、评估脚本、以及 README 里的过时命令；不要擅自拆成只修其中一部分。

**Protocol output**:

```text
[LOCKED][PATTERN=split_without_permission]
ACTION: EXECUTE_ALL_COMPONENTS
RESPONSE_MODE: NO_PLAN_ONLY
COMPLETION_POLICY: NO_PARTIAL_AS_DONE
BLOCKER_POLICY: DISCOVER_BEFORE_ASK
```

**Check**: PASS

---
## Case 02
**Pattern**: `premature_stop`  |  **Focus**: `writing_engine`  |  **Heuristic**: `premature_stop`

**User**: 把摘要、引言和 related work 全部改到可投稿状态；如果中途只做了一部分，必须明确说没做完，不能提前收尾。

**Protocol output**:

```text
[LOCKED][PATTERN=premature_stop]
ACTION: EXECUTE_FULL_SCOPE
RESPONSE_MODE: EXECUTION_REQUIRED
COMPLETION_POLICY: LABEL_PARTIAL_IF_STOPPING
BLOCKER_POLICY: ASK_MINIMAL_IF_BLOCKED
```

**Check**: PASS

---
## Case 03
**Pattern**: `convert_execution_to_advice`  |  **Focus**: `writing_engine`  |  **Heuristic**: `simplify_without_permission`

**User**: 下面 12 句请直接重写，不要告诉我怎么改，也不要给原则总结。

**Protocol output**:

```text
[LOCKED][PATTERN=convert_execution_to_advice]
ACTION: EXECUTE_FULL_SCOPE
RESPONSE_MODE: NO_ADVICE_ONLY
COMPLETION_POLICY: FULL_SCOPE_REQUIRED
BLOCKER_POLICY: ASK_MINIMAL_IF_BLOCKED
```

**Check**: PASS

---
## Case 04
**Pattern**: `over_ask_when_discoverable`  |  **Focus**: `S430`  |  **Heuristic**: `over_ask_when_discoverable`

**User**: zip 里已经有 repo、日志和报错截图。你先自己定位 root cause 并修复，只有真正缺关键输入时再问我。

**Protocol output**:

```text
[LOCKED][PATTERN=over_ask_when_discoverable]
ACTION: DISCOVER_THEN_EXECUTE
RESPONSE_MODE: NO_PLAN_ONLY
COMPLETION_POLICY: NO_PARTIAL_AS_DONE
BLOCKER_POLICY: DISCOVER_BEFORE_ASK
```

**Check**: PASS

---
## Case 05
**Pattern**: `under_deliver_on_lawful_scope`  |  **Focus**: `S430`  |  **Heuristic**: `under_deliver_on_lawful_scope`

**User**: 请同时完成 patch、验证命令、回归矩阵和风险说明。这四项都要，不能只做最容易的一项。

**Protocol output**:

```text
[LOCKED][PATTERN=under_deliver_on_lawful_scope]
ACTION: EXECUTE_ALL_COMPONENTS
RESPONSE_MODE: EXECUTION_REQUIRED
COMPLETION_POLICY: NO_PARTIAL_AS_DONE
BLOCKER_POLICY: DISCOVER_BEFORE_ASK
```

**Check**: PASS

---
## Case 06
**Pattern**: `mixed_request_easy_part_only`  |  **Focus**: `writing_engine`  |  **Heuristic**: `mixed_request_easy_part_only`

**User**: 先查 3 篇最相关工作，再改写摘要，并指出最大的方法风险。不要只做摘要改写。

**Protocol output**:

```text
[LOCKED][PATTERN=mixed_request_easy_part_only]
ACTION: EXECUTE_ALL_COMPONENTS
RESPONSE_MODE: EXECUTION_REQUIRED
COMPLETION_POLICY: NO_PARTIAL_AS_DONE
BLOCKER_POLICY: DISCOVER_BEFORE_ASK
```

**Check**: PASS

---
## Case 07
**Pattern**: `large_scope_downgrade_to_mvp`  |  **Focus**: `S503`  |  **Heuristic**: `large_scope_downgrade_to_mvp`

**User**: 对整套论文材料做 submission readiness gate，我没有要求最小版，也没有要求 sample output。

**Protocol output**:

```text
[LOCKED][PATTERN=large_scope_downgrade_to_mvp]
ACTION: EXECUTE_FULL_SCOPE
RESPONSE_MODE: NO_MVP_DOWNGRADE
COMPLETION_POLICY: FULL_SCOPE_REQUIRED
BLOCKER_POLICY: ASK_MINIMAL_IF_BLOCKED
```

**Check**: PASS

---
## Case 08
**Pattern**: `plan_only_without_permission`  |  **Focus**: `coding_engine`  |  **Heuristic**: `plan_only_without_permission`

**User**: 这个 PR 里的 failing tests 直接修到 pass，不要先给我一个计划书。

**Protocol output**:

```text
[LOCKED][PATTERN=plan_only_without_permission]
ACTION: EXECUTE_FULL_SCOPE
RESPONSE_MODE: NO_PLAN_ONLY
COMPLETION_POLICY: FULL_SCOPE_REQUIRED
BLOCKER_POLICY: DISCOVER_BEFORE_ASK
```

**Check**: PASS

---
## Case 09
**Pattern**: `partial_as_done`  |  **Focus**: `S431`  |  **Heuristic**: `partial_as_done`

**User**: 修 serialization bug 后还要验证 save/reload。只改代码但没验证，不算完成。

**Protocol output**:

```text
[LOCKED][PATTERN=partial_as_done]
ACTION: EXECUTE_FULL_SCOPE
RESPONSE_MODE: EXECUTION_REQUIRED
COMPLETION_POLICY: LABEL_PARTIAL_IF_STOPPING
BLOCKER_POLICY: ASK_MINIMAL_IF_BLOCKED
```

**Check**: PASS

---
## Case 10
**Pattern**: `blocker_question_overreach`  |  **Focus**: `S432`  |  **Heuristic**: `blocker_question_overreach`

**User**: 如果你被阻塞，只问最少的问题；不要把整个需求重新问我一遍。

**Protocol output**:

```text
[LOCKED][PATTERN=blocker_question_overreach]
ACTION: ASK_MINIMAL_BLOCKER
RESPONSE_MODE: EXECUTION_REQUIRED
COMPLETION_POLICY: LABEL_PARTIAL_IF_STOPPING
BLOCKER_POLICY: ASK_MINIMAL_IF_BLOCKED
```

**Check**: PASS

---
## Case 11
**Pattern**: `discoverable_local_context`  |  **Focus**: `S430`  |  **Heuristic**: `discoverable_local_context`

**User**: 不要问我 entrypoint，先自己从仓库脚本、Makefile、README 和日志里找。

**Protocol output**:

```text
[LOCKED][PATTERN=discoverable_local_context]
ACTION: DISCOVER_THEN_EXECUTE
RESPONSE_MODE: NO_PLAN_ONLY
COMPLETION_POLICY: FULL_SCOPE_REQUIRED
BLOCKER_POLICY: DISCOVER_BEFORE_ASK
```

**Check**: PASS

---

## Summary
- protocol_stability: PASS
- heuristic_pattern_alignment: 0.833
- pattern_counts:
  - blocker_question_overreach: 1
  - convert_execution_to_advice: 1
  - discoverable_local_context: 1
  - large_scope_downgrade_to_mvp: 1
  - mixed_request_easy_part_only: 1
  - over_ask_when_discoverable: 1
  - partial_as_done: 1
  - plan_only_without_permission: 1
  - premature_stop: 1
  - simplify_without_permission: 1
  - split_without_permission: 1
  - under_deliver_on_lawful_scope: 1
