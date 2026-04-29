# source_scoring

## 目录

- 用途
- 触发场景
- 输入
- 输出
- 核心步骤
- 评分公式
- 分数定义
- 可靠性等级
- 失败处理
- 与其他算法的关系

## 用途

`source_scoring` 是 major 的来源评分算法，用于判断一个来源是否足够权威、及时、相关、具体并可被引用。它不替代人工判断，但为 `claim_verification` 和 `uncertainty_management` 提供结构化依据。

## 触发场景

- 任何需要引用来源的回答；
- 查询大学专业、招生专业、课程设置、录取要求、学费、截止日期；
- 查询专业认证、执照路径、就业数据、签证、工签、政策变化；
- 核查中介、媒体、论坛、聚合平台说法；
- 比较不同来源是否冲突。

## 输入

- 候选来源记录；
- 用户问题和目标事实类型；
- 目标国家、大学、专业、年份；
- `data/scoring_weights.yaml`；
- `data/authority_source_rules.yaml`；
- `schemas/source_record.schema.json`。

## 输出

- 每条来源的分项评分；
- `source_score`；
- `reliability_level`；
- 可引用来源、辅助来源和拒绝来源列表；
- 来源支持的 claim 列表。

## 核心步骤

1. 为来源识别 `source_type`、国家、大学、专业、年份和页面状态。
2. 按 `data/authority_source_rules.yaml` 计算 `authority_score`。
3. 按 current/next-cycle 当前性和 2025 最低底线计算 `freshness_score`。
4. 判断来源是否直接回答用户问题，计算 `relevance_score`。
5. 判断来源是否具体到大学、院系、专业、招生年度、入学年份或课程目录，计算 `specificity_score`。
6. 判断是否有两个以上可靠来源交叉验证，计算 `corroboration_score`。
7. 判断来源是否匹配目标国家和该国教育体系术语，计算 `country_match_score`。
8. 应用 outdated_penalty。
9. 按公式计算 `source_score`，并分配 `reliability_level`。
10. 把 high/medium 来源交给 `claim_verification`，把 low/unknown 来源标注为辅助或不可用。

## 评分公式

```text
source_score =
  0.30 * authority_score
+ 0.25 * freshness_score
+ 0.20 * relevance_score
+ 0.10 * specificity_score
+ 0.10 * corroboration_score
+ 0.05 * country_match_score
- outdated_penalty
```

总分限制在 0 到 1 之间。

## 分数定义

### authority_score

- 大学官网、招生网、教务处、教育部、省级考试院、阳光高考、专业认证机构等最高；
- 院系官网较高；
- 职业统计机构、行业协会中高；
- 教育平台、媒体中等；
- 论坛、博客、无来源内容低。
- `ranking_reference` 可作为专业实力参考，中等权威，不得作为招生事实依据。
- `local_repository_record` 只能作为候选或本地参考，除非有官方 current/next-cycle source_id 支撑，否则权威性低。

### freshness_score

- 当前/下一招生周期、当前/下一 academic year 或 active/current 官方页面：高；
- 仅满足 2025 最低底线但不明确当前：中或中低，并标注 limited；
- official current page 但无明确日期：中；
- 2024 或更早且不适用于 2025+：低或排除。

### relevance_score

判断来源是否直接回答用户问题：

- 是否包含目标专业；
- 是否包含目标大学；
- 是否匹配目标国家；
- 是否匹配目标年份、招生周期、entry year 或 academic year；
- 是否覆盖用户要问的事实类型。

### specificity_score

判断来源是否具体到：

- 大学；
- 院系；
- 专业；
- 招生年度；
- 入学年份；
- 课程目录；
- 认证项目；
- 学费或截止日期页面。

门户首页、新闻列表页和聚合搜索页 specificity 较低。

### corroboration_score

- 两个以上可靠来源交叉验证：高；
- 单一高权威官方来源直接支持：中高；
- 单一非官方来源：低；
- 没有可交叉验证：低。

### country_match_score

- 来源国家和用户目标国家一致：高；
- 来源使用该国教育体系术语并与问题匹配：高；
- 来源是跨国背景信息但非目标国家：低。

### outdated_penalty

以下情况扣分或排除：

- 早于 2025 且不适用于 2025+；
- archived page；
- 旧版招生页面；
- 聚合平台引用旧数据；
- 没有发布日期且无法判断 current。
- 把第三方排名当作招生事实；
- 把本地库记录当作官方 current/next-cycle 事实。

## 可靠性等级

- `high`: source_score >= 0.80，且来源类型为官方/高权威，满足 current/next-cycle 或 active/current official page 要求，并且页面不是 archived/outdated/historical；
- `medium`: 0.60 <= source_score < 0.80；
- `low`: 0.30 <= source_score < 0.60；
- `unknown`: source_score < 0.30 或关键字段缺失。

## 失败处理

- 没有 high 或 medium 来源：不得输出确定结论。
- 高分来源之间冲突：交给 `claim_verification`，输出 conflicting。
- 只有教育平台、媒体、论坛、博客来源：只能作为线索，不得作为当前事实证据。
- 来源不满足 current/next-cycle：必须降级或标注 limited；连 2025-01-01 最低底线也不满足时，除非用户要求历史背景，否则不得用于当前结论。

## 与其他算法的关系

- 上游：`time_aware_retrieval`、`hybrid_retrieval`。
- 下游：`claim_verification`、`uncertainty_management`。
- 评分权重来自 `data/scoring_weights.yaml`，权威性规则来自 `data/authority_source_rules.yaml`。
