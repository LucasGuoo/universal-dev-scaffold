# 规则：文档生命周期

> 本文件定义文档的创建、维护与同步规则。
> 详见 `docs/doc-lifecycle.md`（完整规范），本文件为红线摘要。

## 硬约束

1. **改源代码 → 必须同 diff 补/更新对应 docstring**（如项目采用 docstring 机制）。
2. **引入外部依赖 / 接口对接 → 必须建 `docs/integration/` 契约**（写一次即可）。
3. **推翻旧架构决策 → 新增 ADR，标记旧 ADR Superseded，旧正文不改**。
4. **`docs/README.md` 索引 → 增删文档即更新**。

## 维护分层

| 层级 | 文档类型 | 维护力度 |
|------|---------|---------|
| Tier 0 | specs/*（过程文档）、reference（自动生成） | 不维护：specs 归档即终态 |
| Tier 1 | how-to、tutorial、integration、runbook | 写一次，行为变了才顺手改 |
| Tier 2 | explanation（含 ADR） | 动态维护，ADR 被推翻时必须同步 |

## Specs ↔ Docs 联动

唯一强制同步点：**verdict 阶段**。
- specs 过程中不触发 docs 同步义务
- verdict 通过前，必须检查 docs 是否需要同步更新

## 参考

- 完整规范：`docs/doc-lifecycle.md`
- 触发矩阵：`docs/doc-lifecycle.md` 第 3 节
- 闸门清单：`specs/template/verdict.md` 阶段三
