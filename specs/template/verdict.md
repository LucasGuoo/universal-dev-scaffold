# Verdict — <feature-name>

> 模板：实现完成后填写，结论「通过」后移入 `specs/archive/`。
> 双检闸门：先核对"做对了没"，再核对"做得好不好"。

## 阶段一：规格符合性自查
- [ ] 实现了 proposal 的全部目标？
- [ ] 满足了所有验收标准？
- [ ] 范围边界内，未做 proposal 明确不做的事（YAGNI）？

## 阶段二：代码质量自查
- [ ] 测试通过（推荐 TDD，红灯 → 绿灯）；有客观验证证据（验证非协商）
- [ ] 无占位符 / 模糊指示
- [ ] 符合 DRY / YAGNI（无预建未用能力）；DAMP > DRY
- [ ] 密钥 / 敏感信息未入 git、未打印日志
- [ ] 提交信息符合 Conventional Commits 且关联 spec
- [ ] 稳定性五板斧：可读性(意图优先) / 变更 ≤~100 行 / 函数 ≤~500 行 / 错误处理 Fail Fast / 可测试性(DI)
- [ ] 安全基线：输入校验 / 注入防护 / 密钥不裸奔（见 `docs/rules/quality-gates.md`）

## 阶段二·五：金线三问验收（唯一判准，见 `docs/constitution.md#0`）
- [ ] ① 意图可读：人 / AI 一眼能懂它做什么，不用猜
- [ ] ② 可验证：有测试 / 构建 / 运行证据，能客观判断做对没
- [ ] ③ 服务业务：它真解决了 proposal 里的实际问题
- [ ] 无"反理性化表"借口绕过闸门（见 `docs/rules/quality-gates.md`）

## 阶段三：文档同步自查（唯一强制同步点，详见 `docs/doc-lifecycle.md` 与 `docs/rules/doc-lifecycle.md`）
- [ ] 改动的函数/类已同 diff 更新 docstring（如项目采用 docstring 机制）
- [ ] 引入外部依赖 / 接口对接 → 已建 `docs/integration/` 契约（写一次即可）
- [ ] 推翻旧架构决策 → 新 ADR 标记旧 ADR `Superseded`（旧正文不改）
- [ ] 行为确实变更的功能 → 对应 how-to / tutorial 已机会式更新（无变更则不碰）
- [ ] `docs/README.md` 索引已同步（增删文档即更新）

## 结论
- [ ] 通过（移入 `specs/archive/`）
- [ ] 有条件通过（列出待补项：）
- [ ] 不通过（说明原因：）
