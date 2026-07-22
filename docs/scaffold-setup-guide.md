# 通用软件工程脚手架搭建指南（轻框架 v2）

> 本脚手架是一套**通用**的、可套用到任意软件工程项目的治理骨架。
> 设计来源：dgcio `spec-driven-project-template`（SDD 理念）+ obra `superpowers`（轻量技能化理念），取其精华、弃其重处。
> 核心原则：**纯 Markdown、零脚本依赖、方法论下沉到模板、多代理入口、YAGNI**。

## 0. 设计理念

| 来源 | 借鉴 | 弃用 |
|------|------|------|
| dgcio SDD | spec 流程（proposal/design/tasks/verdict）、变更决策树、Handoff | `project-init.sh`、外部 `agent-scaffold` 依赖、强制 CI、ADR 膨胀 |
| superpowers | brainstorming 需求澄清、writing-plans 细粒度任务、双检质量闸门、YAGNI、技能即 Markdown、多代理入口 | 插件自动触发体系（我们用 git 约定 + rules 等价实现） |

## 1. 三层结构

```
硬约束层  ── docs/constitution.md        （不可违背的通用原则）
              │
流程层   ── AGENTS.md                     （Agent 入口 + 变更决策树 + 5步确认制）
              ├── specs/{template,active,archive}/  （Spec 流程载体 = 技能化模板）
              └── .codebuddy/rules/*.mdc           （IDE 自动加载的强制规则）
多代理入口 ── CLAUDE.md / COPILOT.md / GEMINI.md → AGENTS.md（重定向）
```

冲突优先级：`constitution.md` > `AGENTS.md` / `specs/*` > `rules/*`。

## 2. 完整文件树（搭建产物）

```
<project>/
├── AGENTS.md                      # Agent 入口
├── CLAUDE.md / COPILOT.md / GEMINI.md  # 多代理重定向入口
├── docs/
│   ├── constitution.md            # 硬约束（通用 10 条）
│   ├── scaffold-setup-guide.md    # 本文
│   └── README.md                  # 文档索引（可选）
├── specs/
│   ├── template/                  # 6 模板（技能化）
│   │   ├── proposal.md            # + brainstorming 需求澄清
│   │   ├── design.md
│   │   ├── tasks.md               # + writing-plans 结构
│   │   ├── verdict.md             # + 双检闸门
│   │   ├── change-proposal.md
│   │   └── context.md
│   ├── active/                    # 进行中（.gitkeep）
│   └── archive/                   # 已验收（.gitkeep）
└── .codebuddy/rules/
    ├── 01-spec-driven/RULE.mdc          # Spec-Driven 流程
    ├── 02-quality-gates/RULE.mdc        # 质量闸门（TDD/双检/YAGNI）
    └── 03-architecture-invariants/RULE.mdc # 架构不可变约束（按项目填）
```

## 3. 搭建步骤（复用清单）

- [ ] 复制 `AGENTS.md` + 三个重定向入口到项目根。
- [ ] 复制 `docs/constitution.md`，填 `<日期>`，按需增删条款（业务专属约束加到第 10 条之后）。
- [ ] 复制 `specs/` 三目录 + `template/` 6 模板（已含 brainstorming / writing-plans / 双检）。
- [ ] 复制 `.codebuddy/rules/` 3 条，按项目改 `03-architecture-invariants` 的不可变约束。
- [ ] 在 `AGENTS.md` 顶部「项目一句话」填项目定位。
- [ ] **不要**引入任何外部初始化脚本 / agent-scaffold / 强制 CI（YAGNI）。

## 4. 与业务专属脚手架的关系

本脚手架是**母版**。业务专属项目（如运维 receiver）在其基础上：
- 保留通用 `specs/template/*` 与 `01-spec-driven` 规则不变；
- 在 `constitution.md` 追加业务硬约束（如触发权分离、HMAC 验签）；
- 在 `03-architecture-invariants` 填本项目不可变项；
- 额外 `docs/` 放架构基线 / 协议规范等业务文档。
