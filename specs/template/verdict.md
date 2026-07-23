# Verdict — <feature-name>

> 模板：实现完成后填写，结论「通过」后移入 `specs/archive/`。
> 双检闸门：先核对"做对了没"，再核对"做得好不好"。

## 阶段一：规格符合性自查
- [ ] 实现了 proposal 的全部目标？
- [ ] 满足了所有验收标准？
- [ ] 范围边界内，未做 proposal 明确不做的事（YAGNI）？

## 阶段二：代码质量自查
- [ ] 测试通过（推荐 TDD，红灯 → 绿灯）
- [ ] 无占位符 / 模糊指示
- [ ] 符合 DRY / YAGNI（无预建未用能力）
- [ ] 密钥 / 敏感信息未入 git、未打印日志
- [ ] 提交信息符合 Conventional Commits 且关联 spec

## 阶段三：文档闸门自查（详见 `docs/doc-lifecycle.md` 与 `.codebuddy/rules/04-doc-lifecycle`）
- [ ] 改动的函数/类已同 diff 更新中文 docstring（`gen-refs.py` 渲染的 reference 已重生成）
- [ ] 引入外部依赖 / 接口对接 → 已建 `docs/integration/` 契约（写一次即可）
- [ ] 本次是否推翻了某条旧 ADR？是 → 新 ADR 标记旧 ADR `Superseded` 且旧正文不改；否 → 跳过
- [ ] 行为确实变更的功能 → 对应 `how-to` / `tutorial` 已机会式更新（无变更则不碰）
- [ ] `docs/README.md` 索引已同步（增删文档即更新）
- [ ] 本地跑 `python scripts/check-docs.py` 无 docstring 缺失 / 索引错误

## 结论
- [ ] 通过（移入 `specs/archive/`）
- [ ] 有条件通过（列出待补项：）
- [ ] 不通过（说明原因：）
