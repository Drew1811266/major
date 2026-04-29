# uncertainty_management

## 用途

`uncertainty_management` 用于为 major 的每个关键结论标注确定性等级，并规定不同等级在最终回答中的表达方式。它确保 major 不把缺乏来源支持、来源过旧或用户画像不足的内容包装成确定事实。

## 触发场景

- 所有涉及来源和当前事实的回答；
- 个性化推荐和适配判断；
- 受监管专业、签证、移民、资格路径；
- 来源冲突或来源不足；
- 找不到 current/next-cycle 可靠来源；
- 只找到 current page 但缺少发布日期或更新日期。

## 输入

- `claim_verification` 结果；
- `source_scoring` 分数；
- 用户画像完整度；
- 来源时效摘要；
- `data/scoring_weights.yaml` 中的 certainty_levels；
- `schemas/uncertainty_record.schema.json`。

## 输出

符合 `schemas/uncertainty_record.schema.json` 的记录：

- claim_id；
- subject；
- certainty_level；
- reasons；
- missing_information；
- source_limitations；
- output_rule；
- user_visible_note；
- next_verification_step。

## certainty_level 定义

### high

current/next-cycle 官方来源直接支持，并且信息与问题高度相关。仅满足 2025 最低底线但不明确当前的来源通常不能标为 high。

输出规则：可以作为当前结论输出，但仍需标注来源。

### medium

来源可靠，但缺少部分关键字段，例如明确更新日期、招生年份或交叉验证。

输出规则：可以输出，但必须提示限制。

### low

来源不够官方，或只能间接支持结论。

输出规则：只能作为参考，不得作为强结论。

### unknown

没有找到可靠来源支持。

输出规则：必须说明无法确认，不得编造或推断。

## 核心步骤

1. 读取每条 claim 的 verification_status。
2. 结合 source_score、freshness_score、source_type 和支持来源数量判断 certainty_level。
3. 对 `supported` 且来源直接、官方、current/next-cycle 的 claim 标为 high。
4. 对 `partially_supported` 或缺少更新日期、招生年份、交叉验证的 claim 标为 medium。
5. 对非官方或间接来源支持的 claim 标为 low。
6. 对 `not_found`、无法核验、无可靠来源的 claim 标为 unknown。
7. 对 `outdated` claim 标为 low 或 unknown，并禁止作为当前结论。
8. 生成用户可见说明。

## 失败处理

- 无法判断确定性：使用 `unknown`。
- 用户要求确定答案但证据不足：说明不能严肃确认。
- 高风险领域缺少官方来源：降为 unknown 或 low，并提示官方核验。
- 推荐类结论画像不足：标注“基于当前信息的初步判断”。

## 与其他算法的关系

- 上游：`source_scoring`、`claim_verification`、`active_profile_completion`。
- 下游：最终回答。
- 与 `safety_and_uncertainty.md` 的不承诺规则共同生效。
