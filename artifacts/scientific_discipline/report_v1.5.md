# Scientific discipline report (v1.5)

- corpus: `tests/scientific_discipline_v1_5/corpus_v1_5.jsonl`
- n_cases: 12

## Case 00
**Pattern**: `chinese_default_unless_override`  |  **Focus**: `boot/13`  |  **Heuristic**: `chinese_default_unless_override`

**User**: 如果用户没指定语言，请默认用中文输出这个科研审计结果，不要无故切成英文。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=chinese_default_unless_override]
LANGUAGE: zh
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: WHEN_NONTRIVIAL
HONESTY_POLICY: STRICT_HONESTY
TUNING_POLICY: FORBID_HEURISTIC_DOWNGRADE
LANGUAGE_DEFAULT_POLICY: ZH_UNLESS_OVERRIDDEN
```

**Check**: PASS

---
## Case 01
**Pattern**: `first_principles_before_tactics`  |  **Focus**: `boot/13`  |  **Heuristic**: `first_principles_before_tactics`

**User**: 先从目标、假设、机制和约束分析这个方法，再谈可执行策略，不要直接跳到 tricks。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=first_principles_before_tactics]
LANGUAGE: zh
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: WHEN_NONTRIVIAL
HONESTY_POLICY: STRICT_HONESTY
TUNING_POLICY: FORBID_HEURISTIC_DOWNGRADE
TACTICS_POLICY: FIRST_PRINCIPLES_BEFORE_TACTICS
```

**Check**: PASS

---
## Case 02
**Pattern**: `no_heuristic_tuning_downgrade`  |  **Focus**: `boot/11`  |  **Heuristic**: `no_heuristic_tuning_downgrade`

**User**: 这是一个科研问题，不要把它改写成拍脑袋调几个超参试试。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=no_heuristic_tuning_downgrade]
LANGUAGE: zh
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: WHEN_NONTRIVIAL
HONESTY_POLICY: STRICT_HONESTY
TUNING_POLICY: FORBID_HEURISTIC_DOWNGRADE
TUNING_DOWNGRADE_POLICY: FORBIDDEN
```

**Check**: PASS

---
## Case 03
**Pattern**: `fact_inference_verification_split`  |  **Focus**: `boot/13`  |  **Heuristic**: `fact_inference_verification_split`

**User**: 回答里要明确区分哪些是已确认事实，哪些是合理推断，哪些还待验证。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=fact_inference_verification_split]
LANGUAGE: zh
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: REQUIRED
HONESTY_POLICY: STRICT_HONESTY
TUNING_POLICY: N_A
FACT_INFERENCE_SPLIT_POLICY: REQUIRED
```

**Check**: PASS

---
## Case 04
**Pattern**: `honest_unexecuted_check`  |  **Focus**: `S431`  |  **Heuristic**: `honest_unexecuted_check`

**User**: 如果测试没跑，就明确说没跑，不要写成已经验证通过。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=honest_unexecuted_check]
LANGUAGE: zh
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: WHEN_NONTRIVIAL
HONESTY_POLICY: STRICT_HONESTY
TUNING_POLICY: N_A
EXECUTION_CLAIM_POLICY: NO_UNEXECUTED_CHECKS
```

**Check**: PASS

---
## Case 05
**Pattern**: `tool_failure_disclosure`  |  **Focus**: `boot/13`  |  **Heuristic**: `tool_failure_disclosure`

**User**: 一旦工具或流程失败，要明确说明失败点和影响范围，再给当前最优替代方案。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=tool_failure_disclosure]
LANGUAGE: zh
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: WHEN_NONTRIVIAL
HONESTY_POLICY: DISCLOSE_FAILURE
TUNING_POLICY: N_A
TOOL_FAILURE_POLICY: DISCLOSE_FAILURE_AND_IMPACT
```

**Check**: PASS

---
## Case 06
**Pattern**: `do_not_reask_known_info`  |  **Focus**: `S430`  |  **Heuristic**: `do_not_reask_known_info`

**User**: 用户已经给了路径、日志和任务背景时，不要重复索取同样的信息，先 best effort 继续。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=do_not_reask_known_info]
LANGUAGE: zh
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: WHEN_NONTRIVIAL
HONESTY_POLICY: STRICT_HONESTY
TUNING_POLICY: N_A
INFO_REUSE_POLICY: RECOVER_BEFORE_ASK
```

**Check**: PASS

---
## Case 07
**Pattern**: `clickable_file_reference`  |  **Focus**: `boot/13`  |  **Heuristic**: `clickable_file_reference`

**User**: 如果要引用 sandbox 里的文件，请给可点击格式，不要只丢一个裸路径。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=clickable_file_reference]
LANGUAGE: zh
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: WHEN_NONTRIVIAL
HONESTY_POLICY: STRICT_HONESTY
TUNING_POLICY: N_A
FILE_REFERENCE_POLICY: CLICKABLE_REQUIRED
```

**Check**: PASS

---
## Case 08
**Pattern**: `concise_no_filler`  |  **Focus**: `boot/13`  |  **Heuristic**: `concise_no_filler`

**User**: 不要废话堆砌，不要低质量分很多小点，直接给高信号结果。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=concise_no_filler]
LANGUAGE: zh
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: WHEN_NONTRIVIAL
HONESTY_POLICY: STRICT_HONESTY
TUNING_POLICY: N_A
STYLE_POLICY: CONCISE_HIGH_SIGNAL
```

**Check**: PASS

---
## Case 09
**Pattern**: `migration_prompt_lossless_english`  |  **Focus**: `migration`  |  **Heuristic**: `migration_prompt_lossless_english`

**User**: 如果我要迁移到下个对话，请输出英文 migration prompt，并尽量无损恢复目标、约束、路径、进度和未决问题。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=migration_prompt_lossless_english]
LANGUAGE: en
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: WHEN_NONTRIVIAL
HONESTY_POLICY: STRICT_HONESTY
TUNING_POLICY: N_A
MIGRATION_POLICY: LOSS_MINIMIZING_ENGLISH
```

**Check**: PASS

---
## Case 10
**Pattern**: `bounded_search_cost_disclosure`  |  **Focus**: `boot/13`  |  **Heuristic**: `bounded_search_cost_disclosure`

**User**: 如果需要调参或搜实验范围，优先小范围、有依据、可解释的搜索，并明确成本和风险。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=bounded_search_cost_disclosure]
LANGUAGE: zh
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: WHEN_NONTRIVIAL
HONESTY_POLICY: STRICT_HONESTY
TUNING_POLICY: BOUNDED_EXPLAINED_SEARCH
SEARCH_COST_POLICY: BOUNDED_AND_EXPLICIT
```

**Check**: PASS

---
## Case 11
**Pattern**: `zyr_protocol_authority`  |  **Focus**: `protocol`  |  **Heuristic**: `zyr_protocol_authority`

**User**: 如果检测到 ZIP your Research 或 zyr 协议，就把它当成权威流程约束执行，不要当可选建议。

**Protocol output**:

```text
[LOCKED][SCIENTIFIC_PATTERN=zyr_protocol_authority]
LANGUAGE: zh
ANALYSIS_BASIS: FIRST_PRINCIPLES
FACT_INFERENCE_SPLIT: WHEN_NONTRIVIAL
HONESTY_POLICY: STRICT_HONESTY
TUNING_POLICY: N_A
PROTOCOL_AUTHORITY_POLICY: STRICT
```

**Check**: PASS

---

## Summary
- protocol_stability: PASS
- heuristic_pattern_alignment: 1.000
- language_counts:
  - en: 1
  - zh: 11
- pattern_counts:
  - bounded_search_cost_disclosure: 1
  - chinese_default_unless_override: 1
  - clickable_file_reference: 1
  - concise_no_filler: 1
  - do_not_reask_known_info: 1
  - fact_inference_verification_split: 1
  - first_principles_before_tactics: 1
  - honest_unexecuted_check: 1
  - migration_prompt_lossless_english: 1
  - no_heuristic_tuning_downgrade: 1
  - tool_failure_disclosure: 1
  - zyr_protocol_authority: 1
