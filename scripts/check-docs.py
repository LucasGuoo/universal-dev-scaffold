#!/usr/bin/env python3
"""Docs health checker (universal-dev-scaffold 可选工具链).

Keeps the Diátaxis docs under ``docs/`` in sync with ``src/``:

1. Internal markdown links resolve to real files.
2. ``docs/README.md`` index is consistent with the actual doc files.
3. ``src/...`` paths cited in docs exist.
4. (opt-in, --require-docstrings) Every top-level function/class in ``src/``
   has a docstring; missing ones are reported (warn by default, error with flag).
   Docstrings are the source of truth — ``scripts/gen-refs.py`` renders them into
   the reference docs, so the old line-number check is no longer needed.

Design note: reference docs are generated from docstrings, so line numbers and
signatures are always correct. The stable anchor is the function/class *name*.

Usage:
    python scripts/check-docs.py [--root ROOT] [--symbols] [--strict] [--require-docstrings]
Exit code: 0 if no errors (warnings never fail unless --strict / --require-docstrings).
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
SRC_DIR = REPO_ROOT / "src"
CATEGORY_DIRS = ["tutorials", "how-to", "reference", "explanation"]

# External modules we should never flag when seen as `aiohttp.web.X`.
EXTERNAL_MODULES = {
    "aiohttp", "httpx", "pydantic", "datetime", "typing", "os", "sys",
    "yaml", "json", "base64", "hmac", "urllib", "time", "logging",
}
# Suffixes that mean a dotted token is a file, not a symbol.
FILE_SUFFIXES = {"yaml", "yml", "md", "json", "py", "pyc", "db", "txt", "sh", "toml"}
# Known non-symbol identifiers (fields / constants / params / values) to ignore.
ALLOW = {
    # fields / attrs
    "event_key", "has_webhook", "event_log", "retry_queue", "retry_log",
    "trigger_log", "shared_secret", "meta", "status", "system", "message",
    "ts", "version", "action", "params", "channel", "next_at", "attempts",
    "max_attempts", "final_status", "created_at", "triggered_at",
    "finished_at", "base_url", "secret", "channel_map", "storage_path",
    "bind_host", "bind_port", "notifier", "config", "storage", "scheduler",
    "engine", "handle_func", "event", "cfg", "row_id", "app", "request",
    "raw", "sig", "fn", "func", "name",
    # constants
    "_BUILTIN_ACTIONS", "_SCHEMA", "retry_registry",
    # values
    "noop", "ack", "pending", "running", "success", "exhausted",
    "processed", "unmatched", "unknown_system", "duplicate", "failed",
    "EventV1",
}

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
SRC_PATH_RE = re.compile(r"`(src/[A-Za-z0-9_./-]+?)(?::\d+)?`")
FILE_CITE_RE = re.compile(r"文件[：:]\s*`(src/[^`]+?):(\d+)`")
HEADING_RE = re.compile(r"^(#{2,4})\s+(.*)$")
IDENT_RE = re.compile(r"[A-Za-z_][\w.]*")


def _doc_target_rel(url: str, base: Path, docs: Path) -> str | None:
    """If ``url`` is a real relative .md link, return its path relative to docs/.

    Returns None for http/anchor/template/non-.md targets.
    """
    u = url.strip()
    if not u or u.startswith(("http", "mailto", "#")) or "{" in u or "}" in u:
        return None
    target = u.split("#", 1)[0]
    if not target.endswith(".md"):
        return None
    resolved = (base / target).resolve()
    if resolved.is_file() and resolved.is_relative_to(docs):
        return str(resolved.relative_to(docs))
    return None


def collect_src_symbols():
    """Return (modules, top_level, class_methods, method_names)."""
    modules: set[str] = set()
    top_level: set[str] = set()
    class_methods: dict[str, set[str]] = {}
    method_names: set[str] = set()
    for py in SRC_DIR.rglob("*.py"):
        if py.name.endswith(".pyc"):
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        modules.add(py.stem)
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                top_level.add(node.name)
                if isinstance(node, ast.ClassDef):
                    methods = {
                        s.name
                        for s in node.body
                        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef))
                    }
                    class_methods[node.name] = methods
                    method_names |= methods
    return modules, top_level, class_methods, method_names


def collect_missing_docstrings():
    """Return ['src/x.py:NN name', ...] for top-level funcs/classes lacking docstrings."""
    missing: list[str] = []
    for py in SRC_DIR.rglob("*.py"):
        if py.name.endswith(".pyc") or py.name == "__init__.py":
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        rel = "src/" + str(py.relative_to(SRC_DIR)).replace("\\", "/")
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if ast.get_docstring(node) is None:
                    missing.append(f"{rel}:{node.lineno} {node.name}")
                if isinstance(node, ast.ClassDef):
                    for sub in node.body:
                        if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                                and ast.get_docstring(sub) is None:
                            missing.append(
                                f"{rel}:{sub.lineno} {node.name}.{sub.name}")
    return missing


def is_symbol_token(tok: str):
    t = tok.strip()
    if not t or " " in t:
        return None
    if t.startswith(("http", "mailto")):
        return None
    if "/" in t:
        return None
    if not IDENT_RE.fullmatch(t):
        return None
    return t


def validate_symbol(t, modules, top_level, class_methods, method_names, issues):
    if "." in t:
        x, y = t.split(".", 1)
        if x in EXTERNAL_MODULES:
            return
        if y.split(".")[-1] in FILE_SUFFIXES:
            return
        if x in modules and y in (top_level | method_names):
            return
        if x in class_methods and y in class_methods[x]:
            return
        if y in (top_level | method_names):
            return
        if x in class_methods:
            issues.append(f"符号 `{t}` 未找到（类 {x} 无方法 {y}）")
            return
        issues.append(f"符号 `{t}` 未找到（{x} 非已知模块/类，或 {y} 未定义）")
        return
    if t in ALLOW:
        return
    if t in (top_level | method_names | set(class_methods)):
        return
    issues.append(f"符号 `{t}` 在文档中引用但 src/ 未定义")


def heading_symbol(text: str) -> str | None:
    t = text.strip()
    t = re.sub(r"^class\s+", "", t, flags=re.I)
    m = re.split(r"[(\s]| -> ", t, maxsplit=1)[0].strip()
    if IDENT_RE.fullmatch(m):
        return m
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Check docs/ <-> src/ consistency")
    ap.add_argument("--root", default=str(REPO_ROOT))
    ap.add_argument("--symbols", action="store_true",
                    help="also audit code symbols referenced in docs (noisy)")
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    ap.add_argument("--require-docstrings", action="store_true",
                    help="missing docstrings in src/ become errors (default: warn)")
    args = ap.parse_args()

    # Ensure UTF-8 output even on Windows (GBK) consoles.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    root = Path(args.root).resolve()
    docs = root / "docs"
    src = root / "src"

    errors: list[str] = []
    warns: list[str] = []

    modules, top_level, class_methods, method_names = collect_src_symbols()

    md_files = sorted(docs.rglob("*.md"))

    # --- 1. internal link integrity (real .md links only) ---
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        for m in MD_LINK_RE.finditer(text):
            url = m.group(1).strip()
            if (url.startswith(("http", "mailto", "#"))
                    or "{" in url or "}" in url):
                continue
            target = url.split("#", 1)[0]
            if not target or not target.endswith(".md"):
                continue
            if not (md.parent / target).resolve().exists():
                errors.append(f"{md.relative_to(root)}: 悬空链接 `{url}`")

    # --- 2. index consistency (docs/README.md) ---
    index = docs / "README.md"
    registered: set[str] = set()
    if index.exists():
        text = index.read_text(encoding="utf-8")
        for m in MD_LINK_RE.finditer(text):
            r = _doc_target_rel(m.group(1), index.parent, docs)
            if r:
                registered.add(r)
        for m in re.finditer(r"`([\w./-]+\.md)`", text):
            r = _doc_target_rel(m.group(1), index.parent, docs)
            if r:
                registered.add(r)
    actual = {
        str(p.relative_to(docs))
        for p in docs.rglob("*.md")
        if str(p.relative_to(docs)) != "README.md"
        and "_generated" not in p.parts
    }
    for f in sorted(actual - registered):
        errors.append(f"docs/README.md 索引缺失：{f}（新增文档未登记）")
    for f in sorted(registered - actual):
        errors.append(f"docs/README.md 索引悬空：{f}（已删除但未注销）")

    # --- 3. src path existence ---
    for md in md_files:
        for m in SRC_PATH_RE.finditer(md.read_text(encoding="utf-8")):
            rel = m.group(1)
            if not (root / rel).exists():
                errors.append(f"{md.relative_to(root)}: 引用的 {rel} 不存在")

    # --- 4. docstring presence (opt-in enforcement) ---
    missing_doc = collect_missing_docstrings()
    if missing_doc:
        msg = (f"{len(missing_doc)} 个 src/ 函数/类缺 docstring"
               f"（生成 reference 时会被跳过）：{'；'.join(missing_doc[:20])}")
        if args.require_docstrings:
            errors.append(msg)
        else:
            warns.append(msg)

    # --- 5. symbol existence (opt-in, warnings only) ---
    if args.symbols:
        for md in md_files:
            for m in CODE_SPAN_RE.finditer(md.read_text(encoding="utf-8")):
                tok = is_symbol_token(m.group(1))
                if not tok:
                    continue
                validate_symbol(tok, modules, top_level, class_methods,
                                method_names, warns)

    # --- report ---
    print(f"文档健康检查：扫描 {len(md_files)} 个 md，"
          f"{len(errors)} 个错误，{len(warns)} 个警告"
          + ("" if args.symbols else "（符号检查未启用，加 --symbols 开启）"))
    if warns:
        print("\n[警告] 漂移 / 可疑符号（不阻断，建议修复）：")
        for w in warns:
            print("  - " + w)
    if errors:
        print("\n[错误] 必须修复：")
        for e in errors:
            print("  - " + e)
        return 1
    if args.strict and warns:
        return 1
    print("\n✅ 文档与代码一致（无错误）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
