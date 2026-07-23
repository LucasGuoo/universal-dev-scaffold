# 通用软件工程脚手架（Spec-Driven + 轻量技能化）

一套**通用**的、可套用到任意软件工程项目的治理骨架。纯 Markdown、零脚本依赖、方法论下沉到模板、多代理入口、YAGNI。

> 任何 AI Agent（CodeBuddy / Claude Code / Codex / Copilot / Gemini / Trae 等）进入你的项目，先读 `AGENTS.md`，再读 `docs/constitution.md`，最后按需读 `specs/active/`。

## 为什么有这套脚手架

设计来源取两家之长、弃其重处：

| 来源 | 借鉴 | 弃用 |
|------|------|------|
| dgcio `spec-driven-project-template` | spec 流程（proposal/design/tasks/verdict）、变更决策树、Handoff | `project-init.sh`、外部 `agent-scaffold` 依赖、强制 CI、ADR 膨胀 |
| obra `superpowers` | brainstorming 需求澄清、writing-plans 细粒度任务、双检质量闸门、YAGNI、技能即 Markdown、多代理入口 | 插件自动触发体系（我们用 git 约定 + rules 等价实现） |

结论：**零工具依赖的轻框架**——不绑定任何 IDE 专属技能包，不引入初始化脚本，不强制 CI。

## 核心原则

1. **纯 Markdown**：所有规则、流程、模板都是 `.md`，人可读、Agent 可解析。
2. **零脚本依赖**：没有 `project-init.sh` / `agent-scaffold` / 强制 CI。
3. **方法论下沉到模板**：brainstorming / writing-plans / 双检就写在 `specs/template/` 里，读模板即获得，无需记忆命令。
4. **多代理入口**：`AGENTS.md` 为单一真相源，`CLAUDE.md` / `COPILOT.md` / `GEMINI.md` 重定向到它，换 IDE 不用重写。
5. **YAGNI**：不预建未用能力；脚手架本身保持最小。

## 文件树

```
<project>/
├── AGENTS.md                      # Agent 入口（单一真相源）
├── CLAUDE.md / COPILOT.md / GEMINI.md  # 多代理重定向入口
├── README.md                      # 本文（仓库首页）
├── docs/
│   ├── constitution.md            # 硬约束（通用 10 条，不可违背）
│   ├── scaffold-setup-guide.md    # 搭建指南（设计理念 / 文件树 / 复用清单）
│   └── README.md                  # 文档索引
├── specs/
│   ├── template/                  # 6 个技能化模板（复制后填入具体 spec）
│   │   ├── proposal.md            # + brainstorming 需求澄清
│   │   ├── design.md
│   │   ├── tasks.md               # + writing-plans 结构
│   │   ├── verdict.md             # + 双检闸门
│   │   ├── change-proposal.md
│   │   └── context.md
│   ├── active/                    # 进行中（.gitkeep）
│   └── archive/                   # 已验收（.gitkeep）
└── .codebuddy/rules/              # CodeBuddy 自动加载的强制规则（其他 IDE 用各自入口）
    ├── 01-spec-driven/RULE.mdc
    ├── 02-quality-gates/RULE.mdc
    └── 03-architecture-invariants/RULE.mdc
└── scripts/                       # 文档工具链（可选，仅标准库）
    ├── gen-refs.py                # docstring → docs/reference/_generated/
    ├── check-docs.py              # docs↔src 一致性校验（可 --require-docstrings）
    └── ci-template/check-docs.yml # opt-in CI 模板（按需复制到 .github/workflows/）
```

## 快速开始（复制即用）

1. 复制 `AGENTS.md` + 三个重定向入口到你的项目根。
2. 复制 `docs/constitution.md`，填 `<日期>`，按需增删条款（业务专属约束加到第 10 条之后）。
3. 复制 `specs/` 三目录 + `template/` 6 模板（已含 brainstorming / writing-plans / 双检）。
4. 复制 `.codebuddy/rules/` 3 条，按项目改 `03-architecture-invariants` 的不可变约束。
5. 在 `AGENTS.md` 顶部「项目一句话」填项目定位。
6. **不要**引入任何外部初始化脚本 / agent-scaffold / 强制 CI（YAGNI）。

完整搭建步骤见 [`docs/scaffold-setup-guide.md`](docs/scaffold-setup-guide.md)。

## 三层结构与冲突优先级

```
硬约束层  ── docs/constitution.md        （不可违背的通用原则）
              │
流程层   ── AGENTS.md                     （Agent 入口 + 变更决策树 + 5步确认制）
              ├── specs/{template,active,archive}/  （Spec 流程载体 = 技能化模板）
              └── .codebuddy/rules/*.mdc           （IDE 自动加载的强制规则）
多代理入口 ── CLAUDE.md / COPILOT.md / GEMINI.md → AGENTS.md（重定向）
```

冲突优先级：`constitution.md` > `AGENTS.md` / `specs/*` > `rules/*`。

## 与业务专属脚手架的关系

本仓库是**母版**。业务专属项目（如运维 receiver）在其基础上：
- 保留通用 `specs/template/*` 与 `01-spec-driven` 规则不变；
- 在 `constitution.md` 追加业务硬约束（如触发权分离、HMAC 验签）；
- 在 `03-architecture-invariants` 填本项目不可变项；
- 额外 `docs/` 放架构基线 / 协议规范等业务文档。

## 文档工具链（可选）

脚手架附带一套**零依赖**（仅 Python 标准库）的文档工具链，把 docstring 当作 reference 文档的唯一真相源：

- `scripts/gen-refs.py` — 扫描 `src/`，把每个函数/类的 docstring 渲染成 `docs/reference/_generated/*.md`。
- `scripts/check-docs.py` — 校验 `docs/` 与 `src/` 一致；`--require-docstrings` 可强制全员有 docstring。
- `scripts/ci-template/check-docs.yml` — opt-in 的 GitHub Actions 模板，需要 CI 把关时复制到 `.github/workflows/` 即可。

docstring 约定（中文、小节按需写）见 `docs/constitution.md` #11；用法见 `AGENTS.md`「文档工具链」节。该工具链**非核心框架依赖**，符合 YAGNI，不默认开启 CI。

## License

[MIT](LICENSE)
