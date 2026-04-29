# constraint_filtering

## 用途

`constraint_filtering` 用于在候选专业排序前识别硬约束和软约束，避免推荐看似匹配但实际不可行、风险过高或与用户明确偏好冲突的方向。

## 触发场景

- 用户要求推荐或适配判断；
- 用户表达“完全不能接受”“不想要”“必须”“只能”等强约束；
- 候选专业涉及作品集、长期编程、大量数学、临床、执照、长期读研、语言或预算压力；
- 用户有国家、城市、家庭、预算、选科或身体条件限制。

## 输入

- 候选专业池；
- `schemas/user_profile.schema.json`；
- `data/constraint_rules.yaml`；
- `data/major_task_profiles.yaml`；
- `schemas/recommendation_score.schema.json`。

## 输出

- 每个候选专业的 constraint_status；
- hard_constraint_flags；
- soft_constraint_notes；
- 降级或过滤原因；
- 推荐分组初步标签：recommended、alternative、cautious、not_recommended；
- 可替代专业。

## 硬约束示例

- 用户完全不能接受作品集；
- 用户完全不能接受大量编程；
- 用户完全不能接受大量数学；
- 用户预算无法支持目标国家；
- 用户不能接受长期读研，但目标职业通常需要研究生或执照；
- 用户目标国家没有合适本科路径；
- 用户不满足关键先修或选科要求。

## 软约束示例

- 希望高收入；
- 希望稳定；
- 希望创造性；
- 希望申请难度较低；
- 希望本科毕业后就业；
- 希望国际化；
- 希望少写论文；
- 希望少做实验。

## 算法流程

```text
候选专业池
→ 硬约束过滤或降级
→ 软约束加权
→ fit_score 排序
→ risk_score 调整
→ 输出 recommended / alternative / cautious / not_recommended
```

## 核心步骤

1. 从用户画像中提取 constraints、disliked_tasks、risk_tolerance、budget_level、language_profile、priority_factors。
2. 从 `major_task_profiles` 读取候选专业的真实学习任务和强度。
3. 匹配硬约束：
   - 如果冲突不可调和，标记 not_recommended；
   - 如果可通过国家、项目或方向规避，标记 cautious。
4. 匹配软约束：
   - 对 fit_score 和 ranking_score 做加权调整；
   - 不直接过滤，除非用户表达为硬约束。
5. 对受监管专业检查资格、执照、临床、实习或读研依赖。
6. 输出硬约束 flags、软约束 notes、降级理由和替代专业。

## 失败处理

- 约束不明确：标记 missing profile field，不直接过滤。
- 用户偏好冲突：解释冲突并给折中路径。
- 约束涉及签证、资格、认证：不得自行判断可行性，必须要求官方核验。
- 约束过多导致候选为空：输出“需要放宽条件或补充优先级”，并列出最小冲突方向。

## 与其他算法的关系

- 上游：`active_profile_completion`、`preference_learning`。
- 下游：`major_fit_scoring`、`risk_scoring`、`recommendation_ranking`。
