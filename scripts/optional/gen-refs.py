#!/usr/bin/env python3
"""Generate Diátaxis Reference docs from ``src/`` docstrings (zero deps).

Reads docstrings via ``ast`` and renders one markdown per module under
``docs/reference/_generated/``, mirroring the hand-written reference template.
Because it reads the AST, ``**文件**：`src/x.py:NN`` and ``**签名**：`` are
always correct and never drift. Docstrings are the single source of truth.

Docstring convention — write in Chinese, all sections optional, add only
what a section actually needs (Google summary + custom ops sections, any order):
    '''一句话说明这段代码做什么（功能）。

    职责：做什么、在哪一步被调用。
    触发：谁/什么调用它（webhook POST / systemd timer / ...）。
    入参：参数含义与约束。
    处理顺序：核心步骤 1 → 2 → 3（把主流程讲清楚）。
    返回：成功 / 失败 / 边界各返回什么。
    关键分支：条件 -> 行为。
    关键副作用：写哪张表 / 外部调用 / 日志关键字。
    配置依赖：用到的 config 字段。
    设计原因：关键算法或决策为什么这么设计（取舍、坑）。
    运维注意：什么症状说明它出问题、去哪查。
    '''

Usage:
    python scripts/optional/gen-refs.py            # write docs/reference/_generated/*.md
    python scripts/optional/gen-refs.py --check    # fail if generated docs are stale
    python scripts/optional/gen-refs.py --dry-run  # print to stdout, write nothing
Exit: 0 success; 1 if --check finds stale docs.
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
OUT_DIR = REPO_ROOT / "docs" / "reference" / "_generated"

SECTION_RE = re.compile(
    r"^([\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_/\- ]{0,15})[：:]\s?(.*)$"
)

CANON = ["职责", "触发", "入参", "处理顺序", "执行顺序", "返回", "出参",
         "关键分支", "关键副作用", "副作用", "配置依赖", "调用链", "关联",
         "设计原因", "运维注意", "运维关注点", "说明"]


def parse_docstring(doc: str):
    if not doc:
        return "", []
    lines = doc.strip().splitlines()
    # Summary = first paragraph (up to the first blank line). Anything after the
    # first blank line is parsed into optional sections ("Title：body").
    summary_lines: list[str] = []
    i = 0
    while i < len(lines) and lines[i].strip():
        summary_lines.append(lines[i])
        i += 1
    summary = "\n".join(summary_lines).strip()
    sections: list[tuple[str, str]] = []
    cur_title: str | None = None
    cur_body: list[str] = []
    for line in lines[i:]:
        m = SECTION_RE.match(line)
        if m and not line[:1].isspace():
            if cur_title is not None:
                sections.append((cur_title, "\n".join(cur_body).rstrip()))
            cur_title = m.group(1)
            cur_body = [m.group(2)] if m.group(2).strip() else []
        elif cur_title is not None:
            cur_body.append(line)
    if cur_title is not None:
        sections.append((cur_title, "\n".join(cur_body).rstrip()))
    return summary, sections


def _order_key(title: str) -> int:
    return CANON.index(title) if title in CANON else len(CANON)


def _fmt_arg(a, default=None) -> str:
    s = a.arg
    if a.annotation is not None:
        s += ": " + ast.unparse(a.annotation)
    if default is not None:
        s += " = " + ast.unparse(default)
    return s


def signature_of(node: ast.AST) -> str:
    if isinstance(node, ast.ClassDef):
        bases = [ast.unparse(b) for b in node.bases]
        return "class " + node.name + ("(" + ", ".join(bases) + ")" if bases else "")
    kind = "async def " if isinstance(node, ast.AsyncFunctionDef) else "def "
    args = node.args
    parts: list[str] = []
    for a in args.posonlyargs:
        parts.append(_fmt_arg(a))
    if args.posonlyargs:
        parts.append("/")
    for a, d in zip(args.args, args.defaults):
        parts.append(_fmt_arg(a, d))
    if args.vararg:
        parts.append("*" + args.vararg.arg)
    elif args.kwonlyargs:
        parts.append("*")
    for a, d in zip(args.kwonlyargs, args.kw_defaults):
        parts.append(_fmt_arg(a, d))
    if args.kwarg:
        parts.append("**" + args.kwarg.arg)
    ret = " -> " + ast.unparse(node.returns) if node.returns is not None else ""
    return kind + node.name + "(" + ", ".join(parts) + ")" + ret


def render_callable(node: ast.AST, src_rel: str, h: int) -> str | None:
    doc = ast.get_docstring(node)
    if not doc:
        return None
    summary, sections = parse_docstring(doc)
    if isinstance(node, ast.ClassDef):
        heading = f"{'#' * h} `class {node.name}`"
    else:
        kw = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
        heading = f"{'#' * h} `{kw}{node.name}()`"
    lines = [heading]
    if summary:
        lines += ["", summary]
    lines += ["", f"**文件**：`{src_rel}:{node.lineno}`", "",
              f"**签名**：`{signature_of(node)}`"]
    for title, body in sorted(sections, key=lambda s: _order_key(s[0])):
        lines += ["", f"**{title}**："]
        if body:
            lines.append(body)
    return "\n".join(lines)


def render_module(mod_path: Path, tree: ast.Module) -> str:
    src_rel = "src/" + str(mod_path.relative_to(SRC_DIR)).replace("\\", "/")
    mod = mod_path.stem
    blocks: list[str] = []
    mdoc = ast.get_docstring(tree)
    title = f"# `{mod}.py`"
    if mdoc:
        s, secs = parse_docstring(mdoc)
        if s:
            title += " — " + s.splitlines()[0]
    blocks += [title, "",
               "> 参考类文档（Reference）。由 `scripts/optional/gen-refs.py` 从 docstring "
               "自动生成；改代码请同步 docstring 并重跑本脚本。"]
    if mdoc:
        s, secs = parse_docstring(mdoc)
        body = s
        for t, b in secs:
            body += f"\n\n**{t}**：\n{b}" if b else f"\n\n**{t}**："
        blocks += ["", body]
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            blk = render_callable(node, src_rel, 2)
            if blk:
                blocks += ["", "---", "", blk]
            if isinstance(node, ast.ClassDef):
                for sub in node.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        sblk = render_callable(sub, src_rel, 3)
                        if sblk:
                            blocks += ["", sblk]
    return "\n".join(blocks).rstrip() + "\n"


def iter_modules():
    for py in sorted(SRC_DIR.rglob("*.py")):
        if py.name.endswith(".pyc") or py.name == "__init__.py":
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        yield py, tree


def collect_missing() -> list[str]:
    missing: list[str] = []
    for py, tree in iter_modules():
        src_rel = "src/" + str(py.relative_to(SRC_DIR)).replace("\\", "/")
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    missing.append(f"{src_rel}:{node.lineno} {node.name}")
                if isinstance(node, ast.ClassDef):
                    for sub in node.body:
                        if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                                and not ast.get_docstring(sub):
                            missing.append(
                                f"{src_rel}:{sub.lineno} {node.name}.{sub.name}")
    return missing


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate reference docs from docstrings")
    ap.add_argument("--check", action="store_true",
                    help="fail if generated docs are stale vs docstrings")
    ap.add_argument("--dry-run", action="store_true",
                    help="print to stdout, write nothing")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    generated = {py.stem + ".md": render_module(py, tree)
                 for py, tree in iter_modules() if render_module(py, tree).strip()}

    if args.dry_run:
        for name, content in generated.items():
            print(f"===== {name} =====\n{content}")
        return 0

    if args.check:
        tmp = Path(tempfile.mkdtemp())
        stale = False
        for name, content in generated.items():
            (tmp / name).write_text(content, encoding="utf-8")
            cur = OUT_DIR / name
            if not cur.exists() or cur.read_text(encoding="utf-8") != content:
                stale = True
                print(f"[stale] {name} 与代码 docstring 不一致，请重跑 gen-refs.py")
        return 1 if stale else 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = {OUT_DIR / n for n in generated}
    for f in set(OUT_DIR.glob("*.md")) - written:
        f.unlink()
    for name, content in generated.items():
        (OUT_DIR / name).write_text(content, encoding="utf-8")
    n_missing = len(collect_missing())
    print(f"✅ 生成 {len(generated)} 篇 reference（docs/reference/_generated/）；"
          f"{n_missing} 个函数/类仍缺 docstring。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
