# Proof verification report (v1.5)

- corpus: `tests/proof_verification_v1_5/corpus_v1_5.jsonl`
- n_cases: 24

## Case 00
**Pattern**: `majority_single_negative_fatal`  |  **Focus**: `proof_engine`  |  **Heuristic**: `majority_single_negative_fatal`

**Shape**: family=`analysis` | length=`long` | budget=`high` | chunk_policy=`progressive` | anchor=`line_anchor`

**User**: 三份 review 里两份说整体看起来没问题，但第三份指出第 7 行把单调收敛误用成主导收敛，属于致命错误。不要用 majority 盖过去。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=majority_single_negative_fatal]
PROOF_VERDICT: verified_false
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 01
**Pattern**: `theorem_condition_mismatch`  |  **Focus**: `S237`  |  **Heuristic**: `theorem_condition_mismatch`

**Shape**: family=`analysis` | length=`medium` | budget=`medium` | chunk_policy=`whole_only` | anchor=`assumption_anchor`

**User**: 定理只要求 f 连续，但证明里直接用了可微且导数有界。请把隐藏条件 mismatch 标成 fatal。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=theorem_condition_mismatch]
PROOF_VERDICT: verified_false
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 02
**Pattern**: `long_proof_local_derivation_error`  |  **Focus**: `S326`  |  **Heuristic**: `long_proof_local_derivation_error`

**Shape**: family=`algebra` | length=`long` | budget=`high` | chunk_policy=`progressive` | anchor=`line_anchor`

**User**: 这个长证明大部分成立，但第 19 到 21 行的矩阵乘法和求和换序有局部 derivation error。需要给出 first failing line。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=long_proof_local_derivation_error]
PROOF_VERDICT: verified_false
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 03
**Pattern**: `counterexample_required_for_derivation_failure`  |  **Focus**: `S326`  |  **Heuristic**: `counterexample_required_for_derivation_failure`

**Shape**: family=`algebra` | length=`medium` | budget=`medium` | chunk_policy=`whole_only` | anchor=`line_anchor`

**User**: 若你判这段多项式恒等变形为错，请给出局部反例或代入检验，不能只说‘看起来不对’。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=counterexample_required_for_derivation_failure]
PROOF_VERDICT: verified_false
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 04
**Pattern**: `pruning_multiple_failing_branches`  |  **Focus**: `S241`  |  **Heuristic**: `pruning_multiple_failing_branches`

**Shape**: family=`combinatorics` | length=`long` | budget=`high` | chunk_policy=`progressive_pruning` | anchor=`multi_anchor`

**User**: 这个组合证明有两个分支都各自含 fatal flaw；progressive verification 应 prune 掉已失败分支，而不是继续平均分配预算。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=pruning_multiple_failing_branches]
PROOF_VERDICT: verified_false
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 05
**Pattern**: `line_anchor_consistency_failure`  |  **Focus**: `S241`  |  **Heuristic**: `line_anchor_consistency_failure`

**Shape**: family=`probability` | length=`medium` | budget=`medium` | chunk_policy=`progressive` | anchor=`line_anchor`

**User**: 请检查这份概率证明的 line anchors 是否一致；如果第 11 行马尔可夫不等式用错了，就把 line anchor 固定到那一行。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=line_anchor_consistency_failure]
PROOF_VERDICT: verified_false
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 06
**Pattern**: `lemma_anchor_fatal_gap`  |  **Focus**: `S235`  |  **Heuristic**: `lemma_anchor_fatal_gap`

**Shape**: family=`combinatorics` | length=`medium` | budget=`medium` | chunk_policy=`lemma_aware` | anchor=`lemma_anchor`

**User**: 第 3 个引理本身就是错的，后面所有推导都依赖它。请用 lemma anchor 明确锁定 fatal gap。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=lemma_anchor_fatal_gap]
PROOF_VERDICT: verified_false
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 07
**Pattern**: `review_budget_sufficient_detects_hidden_flaw`  |  **Focus**: `S240`  |  **Heuristic**: `review_budget_sufficient_detects_hidden_flaw`

**Shape**: family=`probability` | length=`long` | budget=`high` | chunk_policy=`progressive` | anchor=`assumption_anchor`

**User**: 低预算时这份随机过程证明可能被放过，但在足够 review budget 下应发现它偷偷引入了独立性假设。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=review_budget_sufficient_detects_hidden_flaw]
PROOF_VERDICT: verified_false
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 08
**Pattern**: `missing_lemma_or_unjustified_step`  |  **Focus**: `S235`  |  **Heuristic**: `missing_lemma_or_unjustified_step`

**Shape**: family=`analysis` | length=`medium` | budget=`medium` | chunk_policy=`lemma_aware` | anchor=`lemma_anchor`

**User**: 证明第 4 步直接调用一个并未给出的紧性引理，也没有前文结果可代替。这种 missing lemma 不能直接放行。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=missing_lemma_or_unjustified_step]
PROOF_VERDICT: verification_incomplete
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 09
**Pattern**: `annotation_or_rigor_mismatch`  |  **Focus**: `S240`  |  **Heuristic**: `annotation_or_rigor_mismatch`

**Shape**: family=`analysis` | length=`short` | budget=`low` | chunk_policy=`whole_only` | anchor=`assumption_anchor`

**User**: 数据集打分会接受‘显然成立’，但当前目标是论文级严格证明。请标注 annotation/rigor mismatch，而不是强行判 true。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=annotation_or_rigor_mismatch]
PROOF_VERDICT: verification_incomplete
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 10
**Pattern**: `formal_adapter_requested_unavailable`  |  **Focus**: `S433`  |  **Heuristic**: `formal_adapter_requested_unavailable`

**Shape**: family=`algebra` | length=`medium` | budget=`low` | chunk_policy=`whole_only` | anchor=`lemma_anchor`

**User**: 用户要求附一个 Lean sketch，但当前缺少目标库和 notation 对齐信息。formal adapter 失败不能阻塞主 proof audit。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=formal_adapter_requested_unavailable]
PROOF_VERDICT: verification_incomplete
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: OPTIONAL_NON_BLOCKING
```

**Check**: PASS

---
## Case 11
**Pattern**: `review_budget_too_small`  |  **Focus**: `proof_engine`  |  **Heuristic**: `review_budget_too_small`

**Shape**: family=`probability` | length=`long` | budget=`low` | chunk_policy=`progressive` | anchor=`line_anchor`

**User**: 这份长概率证明在 review budget 太小时只能做粗检，当前证据不足以通过，应返回 incomplete 而不是假阳性。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=review_budget_too_small]
PROOF_VERDICT: verification_incomplete
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 12
**Pattern**: `repair_proposal_without_reverify`  |  **Focus**: `proof_engine`  |  **Heuristic**: `refinement_then_reverify`

**Shape**: family=`combinatorics` | length=`long` | budget=`medium` | chunk_policy=`progressive` | anchor=`lemma_anchor`

**User**: 已经有 repair proposal 了，但 corrected proof 还没 re-verify。不要把修订建议直接算成 verified。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=repair_proposal_without_reverify]
PROOF_VERDICT: verification_incomplete
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: REVERIFY_REQUIRED
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 13
**Pattern**: `dataset_rigor_paper_rigor_mismatch`  |  **Focus**: `S240`  |  **Heuristic**: `dataset_rigor_paper_rigor_mismatch`

**Shape**: family=`probability` | length=`medium` | budget=`medium` | chunk_policy=`whole_only` | anchor=`assumption_anchor`

**User**: 竞赛风格答案可能会过，但论文风格需要把 dominated convergence 的使用条件写全。请按 paper rigor 记为 incomplete。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=dataset_rigor_paper_rigor_mismatch]
PROOF_VERDICT: verification_incomplete
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 14
**Pattern**: `unknown_assumption_blocks_verification`  |  **Focus**: `S237`  |  **Heuristic**: `unknown_assumption_blocks_verification`

**Shape**: family=`combinatorics` | length=`short` | budget=`low` | chunk_policy=`whole_only` | anchor=`assumption_anchor`

**User**: 证明里一直用到图是简单图，但 theorem statement 没说，前文也没定义。未知假设应阻断通过。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=unknown_assumption_blocks_verification]
PROOF_VERDICT: verification_incomplete
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 15
**Pattern**: `formal_success_auxiliary_only`  |  **Focus**: `S433`  |  **Heuristic**: `formal_success_auxiliary_only`

**Shape**: family=`combinatorics` | length=`medium` | budget=`high` | chunk_policy=`lemma_aware` | anchor=`lemma_anchor`

**User**: 即便 autoformalization 某个子引理成功了，只要自然语言主证明还有未解释跳步，也不能直接判 true。formal success 只能算辅助证据。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=formal_success_auxiliary_only]
PROOF_VERDICT: verification_incomplete
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: OPTIONAL_NON_BLOCKING
```

**Check**: PASS

---
## Case 16
**Pattern**: `harmless_typo_nonfatal`  |  **Focus**: `S240`  |  **Heuristic**: `harmless_typo_nonfatal`

**Shape**: family=`analysis` | length=`short` | budget=`low` | chunk_policy=`whole_only` | anchor=`line_anchor`

**User**: 证明里只有一个符号笔误，把 x_i 写成 x_j，但上下文唯一可恢复且不影响逻辑。不要把 harmless typo 升格成 fatal flaw。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=harmless_typo_nonfatal]
PROOF_VERDICT: verified_true
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 17
**Pattern**: `refinement_then_reverify`  |  **Focus**: `proof_engine`  |  **Heuristic**: `review_budget_sufficient_clean_proof`

**Shape**: family=`algebra` | length=`medium` | budget=`medium` | chunk_policy=`progressive` | anchor=`line_anchor`

**User**: reviewer 已指出 fatal flaw，之后给出的 corrected proof 也已经重新验证通过。这时才允许把 verdict 记成 true。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=refinement_then_reverify]
PROOF_VERDICT: verified_true
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: REVERIFY_REQUIRED
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 18
**Pattern**: `long_true_proof_clean`  |  **Focus**: `proof_engine`  |  **Heuristic**: `long_true_proof_clean`

**Shape**: family=`analysis` | length=`long` | budget=`high` | chunk_policy=`progressive_pruning` | anchor=`lemma_anchor`

**User**: 这是一个很长的泛函分析证明，但所有 lemma anchors、条件使用和局部 derivation 都一致，没有 fatal flaw。不要因为它长就偏向 false。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=long_true_proof_clean]
PROOF_VERDICT: verified_true
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 19
**Pattern**: `algebra_true_with_line_anchor`  |  **Focus**: `S326`  |  **Heuristic**: `line_anchor_consistency_failure`

**Shape**: family=`algebra` | length=`medium` | budget=`medium` | chunk_policy=`whole_only` | anchor=`line_anchor`

**User**: 这段代数证明每一行都可复算，line anchor 应保持一致且最终 verdict 为 true。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=algebra_true_with_line_anchor]
PROOF_VERDICT: verified_true
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 20
**Pattern**: `probability_true_progressive_chunk`  |  **Focus**: `S241`  |  **Heuristic**: `long_proof_local_derivation_error`

**Shape**: family=`probability` | length=`long` | budget=`high` | chunk_policy=`progressive` | anchor=`line_anchor`

**User**: 对这个长概率证明做 progressive chunk review 时，不应凭长度默认怀疑；若所有 chunk 都通过，最终应记为 verified true。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=probability_true_progressive_chunk]
PROOF_VERDICT: verified_true
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 21
**Pattern**: `combinatorics_true_lemma_anchor`  |  **Focus**: `S235`  |  **Heuristic**: `combinatorics_true_lemma_anchor`

**Shape**: family=`combinatorics` | length=`medium` | budget=`medium` | chunk_policy=`lemma_aware` | anchor=`lemma_anchor`

**User**: 这个组合证明主要靠两个引理，lemma anchors 都齐全且依赖关系闭合，最终应给 true 而不是无端保留。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=combinatorics_true_lemma_anchor]
PROOF_VERDICT: verified_true
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---
## Case 22
**Pattern**: `formal_adapter_success_nonblocking_true`  |  **Focus**: `S433`  |  **Heuristic**: `formal_adapter_success_nonblocking_true`

**Shape**: family=`algebra` | length=`long` | budget=`high` | chunk_policy=`progressive` | anchor=`lemma_anchor`

**User**: 自然语言主证明已经通过，同时 Lean sketch 也顺利产出。formal adapter 的成功只是辅助证据，不应改变主 verdict 的判定逻辑。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=formal_adapter_success_nonblocking_true]
PROOF_VERDICT: verified_true
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: OPTIONAL_NON_BLOCKING
```

**Check**: PASS

---
## Case 23
**Pattern**: `review_budget_sufficient_clean_proof`  |  **Focus**: `proof_engine`  |  **Heuristic**: `review_budget_sufficient_clean_proof`

**Shape**: family=`probability` | length=`short` | budget=`medium` | chunk_policy=`whole_only` | anchor=`multi_anchor`

**User**: 在足够但不过量的 review budget 下，这个短证明应稳定通过，不需要被过度怀疑或无限扩展检查。

**Protocol output**:

```text
[LOCKED][PROOF_PATTERN=review_budget_sufficient_clean_proof]
PROOF_VERDICT: verified_true
FATAL_POLICY: FIRST_ERROR_WINS
MAJORITY_POLICY: DIAGNOSTIC_ONLY
REFINEMENT_POLICY: NO_REFINEMENT
FORMAL_ADAPTER_POLICY: NOT_REQUESTED
```

**Check**: PASS

---

## Summary
- protocol_stability: PASS
- heuristic_pattern_alignment: 0.833
- verdict_counts:
  - verification_incomplete: 8
  - verified_false: 8
  - verified_true: 8
- theorem_family_counts:
  - algebra: 6
  - analysis: 6
  - combinatorics: 6
  - probability: 6
- proof_length_bucket_counts:
  - long: 9
  - medium: 11
  - short: 4
- anchor_kind_counts:
  - assumption_anchor: 5
  - lemma_anchor: 8
  - line_anchor: 9
  - multi_anchor: 2
- budget_policy_coverage:
  - high: 8
  - low: 5
  - medium: 11
- pattern_counts:
  - algebra_true_with_line_anchor: 1
  - annotation_or_rigor_mismatch: 1
  - combinatorics_true_lemma_anchor: 1
  - counterexample_required_for_derivation_failure: 1
  - dataset_rigor_paper_rigor_mismatch: 1
  - formal_adapter_requested_unavailable: 1
  - formal_adapter_success_nonblocking_true: 1
  - formal_success_auxiliary_only: 1
  - harmless_typo_nonfatal: 1
  - lemma_anchor_fatal_gap: 1
  - line_anchor_consistency_failure: 1
  - long_proof_local_derivation_error: 1
  - long_true_proof_clean: 1
  - majority_single_negative_fatal: 1
  - missing_lemma_or_unjustified_step: 1
  - probability_true_progressive_chunk: 1
  - pruning_multiple_failing_branches: 1
  - refinement_then_reverify: 1
  - repair_proposal_without_reverify: 1
  - review_budget_sufficient_clean_proof: 1
  - review_budget_sufficient_detects_hidden_flaw: 1
  - review_budget_too_small: 1
  - theorem_condition_mismatch: 1
  - unknown_assumption_blocks_verification: 1
