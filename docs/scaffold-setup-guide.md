# 通用软件工程脚手架搭建指南（轻框架 v3）

> 本脚手架是一套**通用**的、可套用到任意软件工程项目的治理骨架。
> 设计来源：dgcio `spec-driven-project-template`（SDD 理念）+ obra `superpowers`（轻量技能化理念），取其精华、弃其重处。
> 核心原则：**纯 Markdown、零工具绑定、方法论下沉到模板、多代理入口、YAGNI**。

## 0. 设计理念

| 来源 | 借鉴 | 弃用 |
|------|------|------|
| dgcio SDD | spec 流程（proposal/design/tasks/verdict）、变更决策树、Handoff | `project-init.sh`、外部 `agent-scaffold` 依赖、强制 CI、ADR 膨胀 |
| superpowers | brainstorming 需求澄清、writing-plans 细粒度任务、双检质量闸门、YAGNI、技能即 Markdown、多代理入口 | 插件自动触发体系（我们用 git 约定 + rules 等价实现） |
| GitHub Spec Kit | agent 无关化模板设计、工具适配层分离 | CLI 初始化脚本（我们用复制即用） |

## 1. 三层结构

```
硬约束层  ── docs/constitution.md          （不可违背的通用原则）
              │
流程层   ── AGENTS.md                       （Agent 入口 + 变更决策树 + 5步确认制）
              ├── docs/rules/               （通用规则文本，工具无关）
              ├── specs/{template,active,archive}/  （Spec 流程载体 = 技能化模板）
              └── skills/                   （可选 Agent Skills）
多代理入口 ── CLAUDE.md / COPILOT.md / GEMINI.md → AGENTS.md（重定向）
```

冲突优先级：`constitution.md` > `AGENTS.md` / `specs/*` > `docs/rules/*`。

## 2. 完整文件树（搭建产物）

```
<project>/
├── AGENTS.md                      # Agent 入口（工具无关，单一真相源）
├── CLAUDE.md / COPILOT.md / GEMINI.md  # 多代理重定向入口
├── README.md
├── .editorconfig                  # 编辑器统一配置
├── .gitattributes                 # Git 行为配置
├── .gitignore                     # 忽略规则
├── docs/
│   ├── OVERVIEW.md                # 文档总览 / 导航地图（全局入口）
│   ├── constitution.md            # 硬约束（13 条通用原则）
│   ├── scaffold-setup-guide.md    # 本文
│   ├── doc-lifecycle.md           # 文档生命周期规范
│   ├── rules/                     # 通用规则文本（工具无关）
│   │   ├── spec-driven.md         #   Spec-Driven 流程规则
│   │   ├── quality-gates.md       #   质量闸门规则
│   │   ├── doc-lifecycle.md       #   文档生命周期红线
│   │   └── code-management.md     #   代码管理规则
│   ├── tutorials/                 # Diátaxis: 学习导向
│   ├── how-to/                    # Diátaxis: 问题导向（含 runbook）
│   ├── reference/                 # Diátaxis: 信息导向（API 文档）
│   ├── explanation/               # Diátaxis: 理解导向（含 ADR）
│   ├── integration/               # 外部接口/依赖契约
│   ├── operations/                # 运维手册
│   ├── product/                   # PRD / 产品文档
│   └── README.md                  # 文档索引
├── specs/
│   ├── template/                  # 6 个技能化模板
│   ├── active/                    # 进行中（.gitkeep）
│   └── archive/                   # 已验收（.gitkeep）
└── skills/                        # 通用 Agent Skills（可选）
    ├── using-scaffold/             #   脚手架全流程引导（决策树 + spec + verdict + 文档分类）
    ├── scaffold-handoff/           #   跨 Agent 交接协议
    └── references/                #   详细参考文档
```

## 3. 搭建步骤（复用清单）

- [ ] 复制 `AGENTS.md` + 重定向入口（CLAUDE.md / COPILOT.md / GEMINI.md）到项目根。
- [ ] 复制 `docs/constitution.md`，填 `<日期>`，按需增删条款（业务专属约束加到第 10 条之后）。
- [ ] 复制 `docs/rules/` 4 个规则文件，按项目定制 `code-management.md` 的工具链。
- [ ] 复制 `specs/` 三目录 + `template/` 6 模板。
- [ ] 复制 `.editorconfig` + `.gitattributes`，按项目语言惯例调整。
- [ ] 复制 `docs/` 子目录骨架（Diátaxis 四象限 + integration / operations / product）。
- [ ] （可选）复制 `skills/` 目录，安装到项目作用域。
- [ ] 在 `AGENTS.md` 顶部「项目一句话」填项目定位。
- [ ] 在 `docs/README.md` 登记项目文档索引。
- [ ] **不要**引入任何外部初始化脚本 / agent-scaffold / 强制 CI（YAGNI）。

## 4. 工具适配（Agent 无关化）

脚手架本身**不绑定任何特定 IDE 或 Agent 工具**。`docs/rules/` 中的规则是纯 Markdown 文本，具体项目按工具选型做适配：

| 工具 | 适配方式 |
|------|---------|
| CodeBuddy / Qoder | 将 `docs/rules/` 内容映射为 `.codebuddy/rules/*.mdc` |
| Cursor | 将规则写入 `.cursorrules` |
| GitHub Copilot | 将规则写入 `.github/copilot-instructions.md` |
| Claude Code | 将规则写入 `.claude/CLAUDE.md`（重定向到 AGENTS.md） |
| Windsurf | 将规则写入 `.windsurfrules` |
| Gemini CLI | 通过 `.gemini/settings.json` 指向 AGENTS.md |
| 其他 | 读 AGENTS.md + 手动参考 docs/rules/ |

**适配原则**：
- AGENTS.md 是单一真相源，各工具入口文件只做重定向或内容映射
- 规则文本在 `docs/rules/` 中维护，工具特定格式从它生成/复制
- 不因为某个工具的特性而在脚手架中写死工具专属路径

## 5. 代码管理适配

脚手架不预置具体语言的工具链，但要求具体项目**必须配置以下能力**：

| 能力 | Python | JS/TS | Go | Java | Rust |
|------|--------|-------|-----|------|------|
| Linter | ruff | eslint | golangci-lint | checkstyle | clippy |
| Formatter | ruff format | prettier | gofmt | google-java-format | rustfmt |
| Type Checker | mypy（可选） | tsc | — | javac | — |
| Lockfile | poetry.lock | package-lock.json | go.sum | — | Cargo.lock |

**搭建步骤**：
1. 复制 `.editorconfig`，按项目语言调整缩进和行尾规则
2. 复制 `.gitattributes`，按项目文件类型调整
3. 配置项目级 Linter + Formatter
4. （推荐）配置 pre-commit hooks 自动运行 lint/format
5. 确保 Lockfile 入 git

## 6. 文档架构说明

`docs/` 采用 **Diátaxis 四象限** 分类 + 业务扩展目录：

| 目录 | 类型 | 维护力度 |
|------|------|---------|
| `tutorials/` | 学习导向，引导新人 | Tier 1：写一次，按需更新 |
| `how-to/` | 问题导向，解决特定问题 | Tier 1：写一次，按需更新 |
| `reference/` | 信息导向，精确描述 API | Tier 0：自动生成或手写 |
| `explanation/` | 理解导向，解释"为什么" | Tier 2：动态维护（含 ADR） |
| `integration/` | 外部接口契约 | Tier 1：引入时写一次 |
| `operations/` | 运维手册 | Tier 1：按需更新 |
| `product/` | PRD / 产品文档 | Tier 1：按需更新 |
| `rules/` | 项目规则 | 随项目演进 |

**关键区分**：`specs/` 是过程文档（时效性，归档即冻结），`docs/` 是活文档（持久性，与时俱进）。联动点在 verdict 阶段。

## 7. Agent Skills（可选）

脚手架包含 2 个通用 Skill，安装到项目作用域后 Agent 会自动按脚手架流程工作：

| Skill | 触发场景 | 核心职责 |
|-------|---------|----------|
| **using-scaffold** | 开始任何项目动作时 | 决策树路由 → spec 5 步确认制 → verdict 双检 → 文档分类指引（含 references/ 详细参考） |
| **scaffold-handoff** | 跨 Agent / 跨工具交接时 | 撰写接手上下文 + 恢复流程引导 |

**安装方式**：将 `skills/` 目录复制到项目的 skill 作用域（具体路径按工具不同，见第 4 节工具适配表）。

## 8. 与业务专属脚手架的关系

本脚手架是**母版**。业务专属项目在其基础上：
- 保留通用 `specs/template/*` 与 `docs/rules/spec-driven.md` 不变；
- 在 `constitution.md` 追加业务硬约束；
- 在 `docs/rules/code-management.md` 填入项目具体工具链；
- 按需填充 `docs/` 各子目录的业务文档；
- 按需安装 `skills/` 到项目作用域。
