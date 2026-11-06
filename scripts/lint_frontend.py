"""Frontend hygiene & CSS guidelines linter for NOPE (zero-dependency).

Enforces:
  * Zero `!important` declarations in modular component stylesheets.
  * Zero hardcoded hex or rgb/rgba color values outside `:root` (enforces CSS variables).
  * Zero duplicate selector blocks within the same scope.
  * Balanced braces across all CSS stylesheets.
  * Dead CSS classes / ids and unused JS functions.

Exit code:
  1 if violations are found, 0 if clean.
  Supports `--ratchet` to enforce the ratchet against baseline during incremental migration,
  and `--update-baseline` to lock in improvements.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"
STATIC_DIR = APP / "static"
JS_PATH = STATIC_DIR / "app.js"
HTML_PATH = APP / "web" / "index.html"
BASELINE_PATH = Path(__file__).with_name("frontend_lint_baseline.json")

CLASS_ALLOWLIST = {"w3", "woff2", "is-current"}
RATCHETED = ("important_count", "duplicate_selectors", "hex_colors", "raw_colors_outside_root")


def _strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group()), css, flags=re.S)


def _brace_errors(css: str, filename: str) -> list[str]:
    errors, depth = [], 0
    for index, char in enumerate(css):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                line = css.count("\n", 0, index) + 1
                errors.append(f"{filename}:{line}: stray closing brace '}}'")
                depth = 0
    if depth > 0:
        errors.append(f"{filename}: {depth} unclosed '{{' at end of file")
    return errors


def _get_duplicate_selectors(raw_css: str, css_clean: str) -> dict[str, list[int]]:
    css_no_urls = re.sub(r"url\([^)]*\)", "", css_clean)
    scopes: dict[str, list[tuple[str, int]]] = {"root": []}

    pos = 0
    while pos < len(css_no_urls):
        brace_pos = css_no_urls.find("{", pos)
        if brace_pos == -1:
            break
        header = css_no_urls[pos:brace_pos].strip()
        start_line = raw_css[:brace_pos].count("\n") + 1

        depth = 1
        cur = brace_pos + 1
        while cur < len(css_no_urls) and depth > 0:
            if css_no_urls[cur] == "{":
                depth += 1
            elif css_no_urls[cur] == "}":
                depth -= 1
            cur += 1
        body = css_no_urls[brace_pos + 1 : cur - 1]

        if header.startswith("@media") or header.startswith("@supports"):
            for m in re.finditer(r"([^{};]+)\{[^{}]*\}", body):
                s = m.group(1).strip()
                if s and not s.startswith("@") and not re.fullmatch(r"[\d.%\s,fromto]+", s):
                    rel_line = start_line + body[: m.start()].count("\n")
                    scopes.setdefault(header, []).append((s, rel_line))
        elif header and not header.startswith("@") and not re.fullmatch(r"[\d.%\s,fromto]+", header):
            scopes["root"].append((header, start_line))

        pos = cur

    dups: dict[str, list[int]] = {}
    for scope, sel_list in scopes.items():
        counts = Counter(s[0] for s in sel_list)
        for s, line in sel_list:
            if counts[s] > 1:
                key = f"{s} ({scope})" if scope != "root" else s
                dups.setdefault(key, []).append(line)
    return dups


def lint_frontend(strict: bool = True) -> tuple[dict[str, int], list[str]]:
    css_files = sorted(STATIC_DIR.rglob("*.css"))
    # Exclude backup files
    css_files = [p for p in css_files if not p.name.endswith(".bak")]

    js = JS_PATH.read_text(encoding="utf-8") if JS_PATH.exists() else ""
    html = HTML_PATH.read_text(encoding="utf-8") if HTML_PATH.exists() else ""
    python_sources = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in APP.rglob("*")
        if path.suffix in {".py", ".md", ".txt"} and "__pycache__" not in path.parts
    )
    haystack = js + html + python_sources
    violations: list[str] = []

    total_important = 0
    total_raw_colors = 0
    total_duplicate_instances = 0
    distinct_hex_set: set[str] = set()
    total_css_lines = 0
    all_selectors: set[str] = set()

    for css_file in css_files:
        raw_css = css_file.read_text(encoding="utf-8")
        clean_css = _strip_comments(raw_css)
        css_no_urls = re.sub(r"url\([^)]*\)", "", clean_css)
        total_css_lines += raw_css.count("\n")

        # 1. Structural brace errors
        brace_errs = _brace_errors(clean_css, css_file.name)
        violations.extend(brace_errs)

        # 2. Find :root blocks
        root_spans = [m.span() for m in re.finditer(r":root\s*\{([^}]*)\}", clean_css)]

        def is_inside_root(pos: int, spans: list[tuple[int, int]] = root_spans) -> bool:
            return any(start <= pos <= end for start, end in spans)

        # 3. !important declarations
        file_important = []
        for m in re.finditer(r"!important\b", clean_css):
            line = raw_css.count("\n", 0, m.start()) + 1
            file_important.append(line)
        total_important += len(file_important)

        # 4. Raw colors outside :root
        file_raw_colors = []
        for m in re.finditer(r"#[0-9a-fA-F]{3,8}\b", css_no_urls):
            distinct_hex_set.add(m.group().lower())
            if not is_inside_root(m.start()):
                line = raw_css.count("\n", 0, m.start()) + 1
                file_raw_colors.append((line, m.group()))

        for m in re.finditer(r"\brgba?\([^)]+\)", css_no_urls):
            if not is_inside_root(m.start()):
                line = raw_css.count("\n", 0, m.start()) + 1
                file_raw_colors.append((line, m.group()))
        total_raw_colors += len(file_raw_colors)

        # 5. Duplicate selectors (scope-aware)
        dup_map = _get_duplicate_selectors(raw_css, clean_css)
        file_dup_count = sum(len(lines) - 1 for lines in dup_map.values())
        total_duplicate_instances += file_dup_count

        # Collect selectors for dead class check
        for m in re.finditer(r"([^{};]+)\{[^{}]*\}", css_no_urls):
            s = m.group(1).strip()
            if s and not s.startswith("@"):
                all_selectors.add(s)

        # For modular files (anything other than legacy styles.css): ZERO TOLERANCE
        if css_file.name != "styles.css":
            if file_important:
                violations.append(f"{css_file.name}: {len(file_important)} '!important' found (must be 0)")
            if file_raw_colors:
                violations.append(
                    f"{css_file.name}: {len(file_raw_colors)} raw colors outside :root found (must use tokens): "
                    + ", ".join(f"{c} at L{l}" for l, c in file_raw_colors[:3])
                )
            if dup_map:
                violations.append(f"{css_file.name}: {len(dup_map)} duplicate selector(s) found (must be 0)")

    # 6. Dead classes and IDs
    classes = {c for c in re.findall(r"\.(-?[a-zA-Z_][\w-]*)", " ".join(all_selectors))}
    for name in sorted(classes - CLASS_ALLOWLIST):
        if name not in haystack:
            violations.append(f"CSS class '.{name}' is never referenced in JS/HTML/Python")

    ids = {i for i in re.findall(r"#([a-zA-Z_][\w-]*)", " ".join(all_selectors)) if not re.fullmatch(r"[0-9a-fA-F]{3,8}", i)}
    for name in sorted(ids):
        if name not in haystack:
            violations.append(f"CSS id '#{name}' is never referenced in JS/HTML/Python")

    # 7. Unused JS functions
    js_functions = re.findall(r"^(?:async\s+)?function\s+([A-Za-z_$][\w$]*)", js, flags=re.M)
    for name in sorted(set(js_functions)):
        if len(re.findall(r"(?<![\w$])" + re.escape(name) + r"(?![\w$])", js + html)) <= 1:
            violations.append(f"app.js: function '{name}' is defined but never used")

    metrics = {
        "important_count": total_important,
        "raw_colors_outside_root": total_raw_colors,
        "duplicate_selectors": total_duplicate_instances,
        "hex_colors": len(distinct_hex_set),
        "css_lines": total_css_lines,
        "js_lines": js.count("\n"),
    }

    if strict:
        if total_important:
            violations.append(f"styles.css: {total_important} '!important' declarations remain to be migrated")
        if total_raw_colors:
            violations.append(f"styles.css: {total_raw_colors} hardcoded colors remain to be tokenized")
        if total_duplicate_instances:
            violations.append(f"styles.css: {total_duplicate_instances} duplicate selector instances remain to be consolidated")

    return metrics, violations


def main() -> int:
    is_update_baseline = "--update-baseline" in sys.argv
    is_ratchet_mode = "--ratchet" in sys.argv

    # Standard check applies strict mode unless in ratchet mode
    strict = not (is_ratchet_mode or is_update_baseline)
    metrics, violations = lint_frontend(strict=strict)

    baseline = json.loads(BASELINE_PATH.read_text()) if BASELINE_PATH.exists() else {}

    if is_update_baseline:
        BASELINE_PATH.write_text(json.dumps(metrics, indent=2) + "\n")
        print(f"Baseline updated: {metrics}")
        return 0

    print("Frontend Metrics & Guidelines Check:")
    print("-------------------------------------")
    for key, value in metrics.items():
        limit = baseline.get(key)
        marker = ""
        if key in RATCHETED and limit is not None:
            if value > limit:
                marker = f"  <-- REGRESSION (baseline: {limit})"
            elif value < limit:
                marker = f"  (improved from {limit})"
        print(f"  {key:25} {value}{marker}")
    print("-------------------------------------")

    if is_ratchet_mode:
        ratchet_errors = []
        for key in RATCHETED:
            limit = baseline.get(key)
            val = metrics.get(key, 0)
            if limit is not None and val > limit:
                ratchet_errors.append(f"{key} rose from {limit} to {val} (ratchet: may only go down)")
        if ratchet_errors or violations:
            all_errs = violations + ratchet_errors
            print(f"\n[LINT FAIL] {len(all_errs)} issue(s) found:")
            for err in all_errs:
                print(f"  - {err}")
            return 1
        print("\n[LINT PASS] All checks passed within ratchet limits.")
        return 0

    if violations:
        print(f"\n[LINT FAIL] {len(violations)} violation(s) found:")
        for err in violations:
            print(f"  - {err}")
        return 1

    print("\n[LINT PASS] Clean! 0 violations found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
