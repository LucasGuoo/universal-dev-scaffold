# Tasks — <feature-name>

> 模板：复制本文件到 `specs/active/YYYY-MM-DD-<slug>/tasks.md` 填写。
> 借鉴 writing-plans：把执行者当"零上下文"，所有路径 / 命令 / 代码写死，禁占位符。

## 任务清单

### Task 1: <组件名>
**Files:**（精确路径，创建 / 修改 / 测试）
- `src/...`
- `tests/...`

**Interfaces:**
- Consumes: `<依赖的精确签名，如 def foo(bar: int) -> str>`
- Produces: `<产出的精确签名>`

**Steps:**（每步 2–5 分钟，含 TDD 微循环）
- [ ] 1. 写失败测试（附代码块）
- [ ] 2. 运行验证失败（附命令与预期 FAIL）
- [ ] 3. 最小实现（附代码块）
- [ ] 4. 运行验证通过（附命令与预期 PASS）
- [ ] 5. 提交（附 `git add/commit` 命令）

### Task 2: ...

## Self-Review（全部任务完成后勾除）
- [ ] **覆盖**：每个 proposal 验收标准都有对应任务
- [ ] **占位符**：全文无 TBD / TODO / 待定 / 适当处理 等模糊词
- [ ] **类型一致**：Interfaces 的 Consumes / Produces 与实际代码签名一致
- [ ] **粒度**：每步可在 2–5 分钟内完成并可独立验证

## 接手上下文（跨 Agent 交接时填写）
- 当前阶段：
- 已完成：
- 未完成及阻塞：
- 关键决策：
- 建议下一步：
