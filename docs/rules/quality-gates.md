# 规则：质量闸门

> 本文件定义不可违背的代码与文档质量闸门规则。
> 具体工具可将本文件内容映射为各自的红线规则格式。

## 代码质量

1. **测试通过**：推荐 TDD（红灯 → 绿灯 → 提交）。
2. **无占位符**：代码中无 TBD / TODO / 待定 / 适当处理 等模糊词。
3. **DRY / YAGNI**：不重复、不预建未用能力。
4. **密钥安全**：密钥 / `.env` 不入 git、不打印日志。
5. **提交规范**：Conventional Commits（`type(scope): description`），`type ∈ feat / fix / docs / spec / refactor / chore`。
6. **Lint 通过**：项目配置的 linter / formatter 无新增违规。
7. **类型检查通过**（如项目启用）：type checker 无新增错误。

## 文档质量

1. **改代码 → 同 diff 补 docstring**（如项目采用 docstring → reference 机制）。
2. **引入外部依赖 / 接口对接** → 必须建 `docs/integration/` 契约文档。
3. **推翻旧架构决策** → 新增 ADR 标记旧 ADR `Superseded`（旧正文不改）。
4. **行为变更的功能** → 对应 how-to / tutorial 机会式更新。
5. **`docs/README.md` 索引已同步**（增删文档即更新）。

## Verdict 双检

实现完成后，verdict 阶段做两检：
- **阶段一**：规格符合性（proposal 目标是否全部达成）
- **阶段二**：代码质量 + 文档同步

## 参考

- 闸门清单模板：`specs/template/verdict.md`
- 文档生命周期：`docs/doc-lifecycle.md`
