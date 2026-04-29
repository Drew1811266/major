# hybrid_retrieval

## 目录

- 用途
- 触发场景
- 输入
- 输出
- 核心步骤
- 失败处理
- 与其他算法的关系

## 用途

`hybrid_retrieval` 是 major 的混合检索算法，用于把关键词检索、语义检索、多语言术语扩展、国家术语映射、官方来源过滤和 current/next-cycle 时间过滤结合起来，生成符合 `schemas/retrieval_result.schema.json` 的检索结果。2025-01-01 只是最低时效底线，不等于当前信息。

## 触发场景

- 用户使用中文宽泛词，例如“传媒”“商科”“AI”“医学”“设计”；
- 查询非英语国家的本科专业；
- 需要跨中国、韩国、日本、英国、美国、澳大利亚比较；
- 查询具体大学、招生专业、课程、录取、费用、截止日期、认证、就业数据、签证或政策；
- 初始检索结果重复、来源类型单一或缺少官方来源。

## 输入

- 用户问题；
- `time_aware_retrieval` 生成的时效关键词；
- `data/major_aliases.yaml`；
- `data/country_terms.yaml`；
- `data/official_sources.yaml`；
- 目标国家、大学、专业、事实类型；
- 候选检索结果。

## 输出

输出必须是 `retrieval_result`，符合 `schemas/retrieval_result.schema.json`。核心字段包括：

- `query`；
- `expanded_queries`；
- `target_country`；
- `target_university`；
- `target_major`；
- `minimum_freshness_date`；
- `retrieved_sources`；
- `ranked_sources`；
- `rejected_sources`；
- `source_scores`；
- `freshness_summary`；
- `verification_required`；
- `limitations`。

## 核心步骤

1. **关键词检索**
   - 使用用户原始关键词；
   - 加入大学名、专业名、国家名、当前/下一招生周期、当前/下一学年和最低时效词；
   - 中国大陆优先使用“2026 本科招生章程”“2026 招生专业目录”“2026 分省招生计划”等当前或下一周期词；2025 词只作为最低底线或历史对比线索。

2. **语义检索**
   - 对用户问题进行语义扩展；
   - 把“现在有哪些专业”“这个专业学什么”“是否认证”等转化为 programme availability、course structure、accreditation 等事实类型；
   - 保留语义相关但词面不完全一致的官方页面。

3. **多语言术语扩展**
   - 使用 `data/major_aliases.yaml` 扩展中文、英文、韩文、日文专业名；
   - 例如“传媒”扩展为 Communication、Media Studies、Journalism、미디어커뮤니케이션、メディア学等；
   - 别名只用于检索扩展，不直接证明项目等价。

4. **国家术语映射**
   - 使用 `data/country_terms.yaml` 加入各国体系词：
     - 中国：本科专业、招生专业、培养方案；
     - 韩国：학과、전공、학부；
     - 日本：学部、学科、専攻、コース；
     - 英国：course、programme、module；
     - 美国：major、undergraduate catalog、department；
     - 澳大利亚：course、degree、major、specialisation、handbook。

5. **官方来源优先过滤**
   - 优先大学官网、院系官网、课程目录、招生官网、政府、考试院、官方招生平台、专业认证机构、职业统计机构；
   - 媒体、论坛、博客、中介和教育平台只能作为线索或辅助背景。

6. **Current/next-cycle 时间过滤**
   - 优先保留满足当前/下一招生周期、当前/下一 academic year 或 active/current 官方页面规则的来源；
   - 仅满足 2025-01-01 最低底线但不能证明当前适用的来源必须标注 limited；
   - 标记 rejected sources 的拒绝原因，例如 pre_2025、archived、outdated、not_official、not_relevant。

7. **Reciprocal Rank Fusion, RRF**
   - 对关键词检索、语义检索、多语言检索和官方入口检索的排名进行融合；
   - 公式：

```text
RRF_score(d) = Σ 1 / (k + rank_i(d))
```

   - `d` 是候选来源；
   - `rank_i(d)` 是来源 `d` 在第 `i` 个检索列表中的名次；
   - `k` 默认可取 60，用于降低单个列表排名差异的极端影响；
   - RRF 只负责融合候选结果，最终是否可引用仍由 `source_scoring` 和 `claim_verification` 决定。

8. **MMR, Maximal Marginal Relevance**
   - 目标是在相关性和多样性之间平衡，避免全部来源来自同一所大学、同一平台或同一类型页面；
   - 优先保留：
     - 直接回答用户问题的来源；
     - 不同来源类型，例如大学官网、课程目录、招生平台、认证机构；
     - 不同国家或大学的代表性来源；
     - 能互相交叉验证的来源；
   - 对重复转载、同一聚合平台、同一页面模板的结果降权。

## 失败处理

- 如果多语言扩展产生歧义，先说明候选含义，再继续检索或请用户确认。
- 如果 RRF 高排名结果不是官方来源，不得直接引用，必须交给 `source_scoring`。
- 如果 MMR 后仍缺少来源多样性，说明来源集中限制。
- 如果没有当前/下一周期可靠来源，输出 `limitations` 并说明当前信息无法确认；如果连 2025-01-01 最低底线来源都没有，触发 fallback 文案。

## 与其他算法的关系

- 上游：`time_aware_retrieval`。
- 下游：`source_scoring`、`claim_verification`、`uncertainty_management`。
- 与 `cross_country_alignment` 配合处理多国家术语差异。
