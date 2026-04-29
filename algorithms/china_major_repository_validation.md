# china_major_repository_validation

## 用途

`china_major_repository_validation` 用于验证中国大陆大学专业数据存储库的数据质量、来源授权、ID 追踪、scope 完整性和“不能替代官方招生事实”的安全边界。

## 触发场景

- 导入中国专业库数据之后；
- 更新 `data/china_major_repository/` 目录之后；
- 在 CI 或 `validate_skill.py` 中做结构验证；
- 用户请求使用本地库生成院校专业候选池之前。

## 输入

- `schemas/china_major_repository_dataset.schema.json`；
- `schemas/china_university_major_record.schema.json`；
- `schemas/china_ranking_reference.schema.json`；
- `schemas/source_record.schema.json`；
- `data/china_major_repository/metadata.yaml`；
- `data/china_major_repository/sample_records.yaml`；
- `data/china_major_repository/sources.yaml`；
- `data/id_rules.yaml`。

## 输出

- validation status；
- missing required fields；
- invalid source IDs；
- records unsafe for user-facing factual use；
- records requiring official verification；
- authorization warnings。

## 核心步骤

1. 校验数据集 metadata：
   - dataset name；
   - version；
   - data year；
   - authorization status；
   - source list；
   - update date；
   - limitations。
2. 校验 source records：
   - `source_id` 格式；
   - source type；
   - publisher；
   - URL；
   - access date；
   - source freshness；
   - ranking/reference/admissions source 边界。
3. 校验专业记录：
   - 院校名、专业名、本科层级、年份、来源 ID；
   - 专业代码保留字符串；
   - `record_usage` 不得与来源类型冲突；
   - `currently_admitting = true` 必须有官方 current/next-cycle source_id。
4. 校验软科排名参考：
   - ranking year；
   - publisher；
   - ranking name；
   - methodology URL；
   - limitations；
   - `not_admissions_evidence = true`。
5. 校验 cross-reference：
   - 专业记录引用的 source_id 必须存在；
   - ranking_reference 引用的 source_id 必须存在；
   - claim_id 必须符合 `id_rules`。
6. 标记不可用于最终事实的记录：
   - 仅样例；
   - 授权未知；
   - 只有 ranking_reference；
   - 只有 local_repository_record；
   - 缺少 official current/next-cycle 来源。

## 失败处理

- 结构错误：验证失败。
- 授权未知：允许保留文件，但禁止作为用户可见事实引用。
- source_id 缺失：验证失败。
- 排名参考被错误标为招生依据：验证失败。
- 当前招生字段缺少官方来源：验证失败或降级为候选记录。

## 与其他算法的关系

- 上游：`china_major_repository_import`。
- 下游：`china_major_repository_lookup`、`source_scoring`、`claim_verification`。
- 被 `scripts/validate_skill.py` 和 `scripts/china_major_repository_import.py --validate-only` 调用。
