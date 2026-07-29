# 规则：代码管理

> 本文件定义通用的代码与工程管理规则。
> 具体工具链（linter / formatter / type checker）由项目按语言选型，本文件只规定"必须有"。

## 工程基础

1. **必须有 `.editorconfig`**：统一缩进、行尾、编码，确保跨编辑器一致性。
2. **必须有 `.gitignore`**：排除构建产物、依赖目录、IDE 配置、密钥文件。
3. **推荐有 `.gitattributes`**：标准化行尾、标记二进制文件、控制发布打包。

## 代码质量工具链（按语言选型）

脚手架不预置具体工具，但要求具体项目**必须配置以下能力**：

| 能力 | 作用 | 语言示例 |
|------|------|---------|
| Linter | 静态分析、风格检查 | Python: ruff · JS/TS: eslint · Go: golangci-lint · Java: checkstyle |
| Formatter | 自动格式化 | Python: ruff format · JS/TS: prettier · Go: gofmt · Rust: rustfmt |
| Type Checker | 类型安全（可选） | Python: mypy · JS/TS: tsc · Java: javac |

## 依赖管理

1. **Lockfile 必须入 git**：确保可复现构建（`package-lock.json` / `poetry.lock` / `go.sum` / `Cargo.lock` 等）。
2. **语义化版本（SemVer）**：依赖约束遵循 major.minor.patch。
3. **最小依赖（YAGNI）**：不引入未使用的依赖。
4. **依赖变更走 change-proposal**：引入新依赖或升级 major 版本需在 spec 流程中记录。
5. **安全扫描（推荐）**：Dependabot / Snyk / npm audit 等工具检测已知漏洞。

## 提交规范

- Conventional Commits：`type(scope): description`
- `type ∈ feat / fix / docs / spec / refactor / chore / test / build / ci`
- 关联 spec（如有）：在 commit message 的 body 中引用 `specs/active/<slug>/`

## 工程目录约定

脚手架推荐的通用目录结构（具体项目按需调整）：

```
<project>/
├── src/                 # 源代码
├── tests/               # 测试代码
├── docs/                # 文档（Diátaxis 四象限）
├── specs/               # 过程文档（spec-driven）
├── scripts/             # 工具脚本
├── skills/              # Agent Skills（可选）
├── .github/workflows/   # CI/CD（opt-in）
├── .editorconfig        # 编辑器配置
├── .gitattributes       # Git 行为配置
├── .gitignore           # 忽略规则
├── AGENTS.md            # Agent 入口
├── LICENSE
└── README.md
```

## 参考

- 编辑器配置模板：`.editorconfig`
- Git 配置模板：`.gitattributes`
- 搭建指南·代码管理适配：`docs/scaffold-setup-guide.md`
