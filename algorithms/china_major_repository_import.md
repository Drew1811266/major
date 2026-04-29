# china_major_repository_import

## 用途

`china_major_repository_import` 用于把用户或部署方提供的合规授权 CSV/JSON 数据导入为 major 可读取的中国大陆大学专业数据集。该算法不抓取、不复制完整第三方排名网页内容，只处理用户明确提供且有使用权的数据文件。

## 触发场景

- 用户或部署方提供软科、教育部、阳光高考、省考试院、高校招生网或高校教务处来源的授权数据文件；
- 需要把外部 CSV/JSON 转换为 `china_major_repository_dataset.schema.json`；
- 需要更新本地中国专业库样例或私有部署数据；
- 需要在导入前检查字段、来源、年份、授权状态、source_id 和 scope。

## 输入

- 授权 CSV 或 JSON 文件；
- `data/china_major_repository/import_mapping.yaml`；
- `schemas/china_university_major_record.schema.json`；
- `schemas/china_major_repository_dataset.schema.json`；
- `schemas/china_ranking_reference.schema.json`；
- `data/id_rules.yaml`；
- `data/china_major_repository/sources.yaml`。

## 输出

- 标准化后的 dataset JSON；
- 导入报告；
- 被拒绝记录及原因；
- 需要官方核验字段；
- `source_id`、`record_id`、`ranking_reference_id`。

## 核心步骤

1. 确认数据文件不是从网页未授权复制的完整榜单；如果授权状态不明，停止导入或标记为 `authorization_status: unknown`。
2. 根据 `import_mapping.yaml` 识别字段：
   - 院校名称；
   - 专业名称；
   - 专业代码；
   - 专业类；
   - 学科门类；
   - 年份；
   - 来源；
   - 软科评级/排名字段；
   - 招生 scope 字段。
3. 标准化文本：
   - 去除多余空格；
   - 中文院校名、专业名保留原文；
   - 英文名仅作为辅助；
   - 专业代码保留前导零；
   - 年份统一为字符串。
4. 为每条来源、专业记录和排名参考生成稳定 ID。
5. 校验必填字段：
   - `record_id`;
   - `university_name_zh`;
   - `major_name_zh`;
   - `education_level`;
   - `data_year`;
   - `source_ids`;
   - `record_usage`;
   - `limitations`。
6. 将软科排名字段写入 `ranking_reference`，并强制包含：
   - ranking year；
   - publisher；
   - methodology URL；
   - limitations；
   - `not_admissions_evidence: true`。
7. 输出 dataset，并写明本地库不能替代官方招生核验。

## 失败处理

- 缺少授权声明：导入失败或只生成不可用于用户回答的测试数据集。
- 缺少来源、年份、院校、专业或 source_id：记录失败。
- 排名参考缺少方法链接或局限说明：排名参考失败。
- 记录声称“当前招生”但没有官方 current/next-cycle source_id：记录降级为 `candidate_only`。

## 与其他算法的关系

- 上游：用户或部署方提供数据文件。
- 下游：`china_major_repository_validation`、`china_major_repository_lookup`、`source_scoring`。
- 与 `china_major_repository_ranking_reference` 协作，确保第三方排名只作为参考信号。
