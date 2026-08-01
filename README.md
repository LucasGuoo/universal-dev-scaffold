# 通用软件工程脚手架（Spec-Driven + 轻量技能化）

一套**通用**的、可套用到任意软件工程项目的治理骨架。纯 Markdown、零工具绑定、方法论下沉到模板、多代理入口、YAGNI。

> 任何 AI Agent（CodeBuddy / Claude Code / Codex / Copilot / Gemini / Trae 等）进入你的项目，先读 `AGENTS.md`，再读 `docs/constitution.md`，最后按需读 `specs/active/`。

## 为什么有这套脚手架

设计来源取各家之长、弃其重处：

| 来源 | 借鉴 | 弃用 |
|------|------|------|
| dgcio `spec-driven-project-template` | spec 流程（proposal/design/tasks/verdict）、变更决策树、Handoff | `project-init.sh`、外部 `agent-scaffold` 依赖、强制 CI、ADR 膨胀 |
| obra `superpowers` | brainstorming 需求澄清、writing-plans 细粒度任务、双检质量闸门、YAGNI、技能即 Markdown、多代理入口 | 插件自动触发体系（我们用 git 约定 + rules 等价实现） |
| GitHub Spec Kit | agent 无关化模板设计、工具适配层分离 | CLI 初始化脚本（我们用复制即用） |
| Diátaxis | 四象限文档分类框架 | 无（直接采用） |

结论：**零工具绑定的轻框架**——不绑定任何 IDE 专属技能包，不引入初始化脚本，不强制 CI。

## 核心原则

1. **纯 Markdown**：所有规则、流程、模板都是 `.md`，人可读、Agent 可解析。
2. **零工具绑定**：不绑定特定 IDE / Agent / 语言工具链。`AGENTS.md` 为单一真相源，规则在 `docs/rules/` 以纯文本存在。
3. **方法论下沉到模板**：brainstorming / writing-plans / 双检就写在 `specs/template/` 里，读模板即获得，无需记忆命令。
4. **多代理入口**：`AGENTS.md` 为单一真相源，`CLAUDE.md` / `COPILOT.md` / `GEMINI.md` 重定向到它，换 IDE 不用重写。
5. **YAGNI**：不预建未用能力；脚手架本身保持最小。

## 文件树

```
<project>/
├── AGENTS.md                      # Agent 入口（工具无关，单一真相源）
├── CLAUDE.md / COPILOT.md / GEMINI.md  # 多代理重定向入口
├── README.md                      # 本文（仓库首页）
├── .editorconfig                  # 编辑器统一配置
├── .gitattributes                 # Git 行为配置
├── .gitignore                     # 忽略规则
├── docs/
│   ├── OVERVIEW.md                # 文档总览 / 导航地图（全局入口，先读它）
│   ├── constitution.md            # 硬约束（13 条通用原则）
│   ├── scaffold-setup-guide.md    # 搭建指南（含工具适配 / 代码管理适配）
│   ├── doc-lifecycle.md           # 文档生命周期规范
│   ├── rules/                     # 通用规则文本（工具无关）
│   ├── tutorials/                 # Diátaxis: 学习导向
│   ├── how-to/                    # Diátaxis: 问题导向（含 runbook）
│   ├── reference/                 # Diátaxis: 信息导向（API 文档）
│   ├── explanation/               # Diátaxis: 理解导向（含 ADR）
│   ├── integration/               # 外部接口/依赖契约
│   ├── operations/                # 运维手册
│   ├── product/                   # PRD / 产品文档
│   └── README.md                  # 文档索引
├── specs/
│   ├── template/                  # 6 个技能化模板（复制后填入具体 spec）
│   ├── active/                    # 进行中（.gitkeep）
│   └── archive/                   # 已验收（.gitkeep）
└── skills/                        # 通用 Agent Skills（可选）
    ├── using-scaffold/             #   脚手架全流程引导（决策树 + spec + verdict + 文档分类）
    ├── scaffold-handoff/           #   跨 Agent 交接协议
    └── references/                #   详细参考文档（diataxis / adr / file-paths）
```

## 快速开始（复制即用）

1. 复制 `AGENTS.md` + 重定向入口到你的项目根。
2. 复制 `docs/constitution.md`，填 `<日期>`，按需增删条款。
3. 复制 `docs/rules/` 4 个规则文件，按项目定制工具链。
4. 复制 `specs/` 三目录 + `template/` 6 模板。
5. 复制 `.editorconfig` + `.gitattributes`，按项目语言惯例调整。
6. 复制 `docs/` 子目录骨架（Diátaxis 四象限 + 扩展目录）。
7. （可选）复制 `skills/` 目录，安装到项目作用域。
8. 在 `AGENTS.md` 顶部「项目一句话」填项目定位。
9. **不要**引入任何外部初始化脚本 / agent-scaffold / 强制 CI（YAGNI）。

完整搭建步骤（含工具适配表 + 代码管理适配表）见 [`docs/scaffold-setup-guide.md`](docs/scaffold-setup-guide.md)。

## 三层结构与冲突优先级

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

## 文档架构

`docs/` 采用 **Diátaxis 四象限** + 业务扩展目录：

- **Tutorials**（`tutorials/`）— 学习导向，引导新人完成完整体验
- **How-to**（`how-to/`）— 问题导向，解决特定问题的步骤（含 runbook）
- **Reference**（`reference/`）— 信息导向，精确描述 API/接口/配置
- **Explanation**（`explanation/`）— 理解导向，解释"为什么"（含 ADR 架构决策记录）
- **Integration**（`integration/`）— 外部接口/依赖契约
- **Operations**（`operations/`）— 运维手册（部署/监控/应急）
- **Product**（`product/`）— PRD / MRD / 产品文档
- **Rules**（`rules/`）— 项目规则（工具无关的纯文本）

**关键区分**：`specs/` 是过程文档（时效性，归档即冻结），`docs/` 是活文档（持久性，与时俱进）。联动点在 verdict 阶段。

## Agent Skills（可选）

| Skill | 触发场景 | 核心职责 |
|-------|---------|----------|
| **using-scaffold** | 开始任何项目动作时 | 决策树路由 → spec 5 步确认制 → verdict 双检 → 文档分类指引（含 `references/` 详细参考） |
| **scaffold-handoff** | 跨 Agent / 跨工具交接时 | 撰写接手上下文 + 恢复流程引导 |

安装方式：将 `skills/` 复制到项目作用域（具体路径按工具不同，见 `docs/scaffold-setup-guide.md` §4 工具适配表）。

## 与业务专属脚手架的关系

本仓库是**母版**。业务专属项目在其基础上：
- 保留通用 `specs/template/*` 与 `docs/rules/spec-driven.md` 不变；
- 在 `constitution.md` 追加业务硬约束；
- 在 `docs/rules/code-management.md` 填入项目具体工具链；
- 按需填充 `docs/` 各子目录的业务文档；
- 按需安装 `skills/` 到项目作用域。

## License

[MIT](LICENSE)
