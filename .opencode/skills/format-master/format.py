#!/usr/bin/env python3
"""
format.py — تنسيق احترافي للكود والواجهات
=========================================
ترتيب، محاذاة، أناقة، تناسق، جماليات
"""
import os, sys, re, json, subprocess
from pathlib import Path
from typing import Optional, List, Union

# ═══════════════════════════════════════════════════════════
# 1. تنسيق الكود التلقائي
# ═══════════════════════════════════════════════════════════

def format_project(path: str = ".", check_only: bool = False) -> List[str]:
    """تنسيق كل ملفات المشروع — يكتشف الأنواع تلقائياً"""
    path = Path(path)
    if not path.exists():
        return [f"❌ المسار غير موجود: {path}"]
    results = []
    write_flag = "--check" if check_only else "--write"

    # Python
    py_files = list(path.rglob("*.py"))
    if py_files:
        try:
            r = subprocess.run(["black", str(path), "--line-length", "100", "--quiet"],
                               capture_output=True, text=True, timeout=60)
            if r.returncode == 0:
                results.append(f"✅ Python (Black): {len(py_files)} ملف")
            else:
                # محاولة بدون quiet
                subprocess.run(["black", str(path), "--line-length", "100"],
                               capture_output=True, timeout=60)
                results.append(f"✅ Python (Black): {len(py_files)} ملف")
        except FileNotFoundError:
            results.append("⚠️  Black غير مثبت. شغل: pip install black")
        except Exception as e:
            results.append(f"⚠️  خطأ Black: {e}")

        try:
            r = subprocess.run(["ruff", "check", str(path), "--fix", "--quiet"],
                               capture_output=True, text=True, timeout=30)
            results.append(f"✅ Python (Ruff): فحص وإصلاح")
        except FileNotFoundError:
            pass
        except Exception as e:
            results.append(f"⚠️  خطأ Ruff: {e}")

    # HTML
    html_files = list(path.rglob("*.html"))
    if html_files:
        try:
            subprocess.run(["prettier", write_flag, "--parser", "html"] +
                           [str(f) for f in html_files], capture_output=True, timeout=30)
            results.append(f"✅ HTML: {len(html_files)} ملف")
        except FileNotFoundError:
            results.append("⚠️  Prettier غير مثبت. شغل: npm install -g prettier")
        except Exception as e:
            # HTML fallback: تنسيق يدوي
            n = _format_html_fallback(html_files)
            results.append(f"✅ HTML (يدوي): {n} ملف")

    # CSS
    css_files = list(path.rglob("*.css"))
    if css_files:
        try:
            subprocess.run(["prettier", write_flag] + [str(f) for f in css_files],
                           capture_output=True, timeout=30)
            results.append(f"✅ CSS: {len(css_files)} ملف")
        except:
            n = _format_css_fallback(css_files)
            results.append(f"✅ CSS (يدوي): {n} ملف")

    # JS/TS
    for ext in ["*.js", "*.ts", "*.jsx", "*.tsx"]:
        files = list(path.rglob(ext))
        if files:
            try:
                subprocess.run(["prettier", write_flag] + [str(f) for f in files],
                               capture_output=True, timeout=30)
                results.append(f"✅ JS/TS ({ext}): {len(files)} ملف")
            except:
                pass

    # JSON
    json_files = list(path.rglob("*.json"))
    if json_files:
        try:
            subprocess.run(["prettier", write_flag] + [str(f) for f in json_files],
                           capture_output=True, timeout=30)
            results.append(f"✅ JSON: {len(json_files)} ملف")
        except:
            n = 0
            for f in json_files:
                try:
                    data = json.loads(f.read_text(encoding='utf-8'))
                    f.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                                  encoding='utf-8')
                    n += 1
                except: pass
            results.append(f"✅ JSON (يدوي): {n} ملف")

    # Markdown
    md_files = list(path.rglob("*.md"))
    if md_files:
        try:
            subprocess.run(["prettier", write_flag, "--parser", "markdown"] +
                           [str(f) for f in md_files], capture_output=True, timeout=30)
            results.append(f"✅ Markdown: {len(md_files)} ملف")
        except:
            pass

    if not results:
        results.append("ℹ️  ما لقيت ملفات للتنسيق")

    return results


def _format_html_fallback(files: List[Path]) -> int:
    """تنسيق HTML يدوي (بدون Prettier)"""
    n = 0
    for f in files:
        try:
            content = f.read_text(encoding='utf-8')
            # تباعد بسيط
            content = re.sub(r'>\s+<', '>\n<', content)
            content = re.sub(r'\s{2,}', ' ', content)
            content = content.replace('> ', '>\n  ')
            # إضافة مسافة بادئة
            lines = content.split('\n')
            result = []
            indent = 0
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped.startswith('</'):
                    indent = max(0, indent - 1)
                result.append('  ' * indent + stripped)
                if stripped.startswith('<') and not stripped.startswith('</') and not stripped.endswith('/>'):
                    if not stripped.startswith('<!') and not stripped.startswith('<!--'):
                        indent += 1
            f.write_text('\n'.join(result), encoding='utf-8')
            n += 1
        except:
            pass
    return n


def _format_css_fallback(files: List[Path]) -> int:
    """تنسيق CSS يدوي (بدون Prettier)"""
    n = 0
    for f in files:
        try:
            content = f.read_text(encoding='utf-8')
            content = re.sub(r'\s+', ' ', content)
            content = content.replace('{', ' {\n  ')
            content = content.replace(';', ';\n  ')
            content = content.replace('}', '\n}\n\n')
            content = re.sub(r'\n\s+\n', '\n\n', content)
            f.write_text(content.strip(), encoding='utf-8')
            n += 1
        except:
            pass
    return n


# ═══════════════════════════════════════════════════════════
# 2. تنسيق النصوص
# ═══════════════════════════════════════════════════════════

def format_arabic_text(text: str) -> str:
    """تنسيق النص العربي — محاذاة، ترقيم، مسافات"""
    if not text:
        return text
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.replace('?', '؟').replace(',', '،').replace(';', '؛')
    text = re.sub(r'([،؛؟!])([^\s])', r'\1 \2', text)
    text = re.sub(r'\s+([،؛؟!])', r'\1', text)
    text = f"\u202B{text}\u202C" if any('\u0600' <= c <= '\u06FF' for c in text) else text
    return text.strip()


def justify_text(text: str, width: int = 60) -> str:
    """محاذاة النص — توزيع المسافات بين الكلمات"""
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph.strip():
            lines.append('')
            continue
        words = paragraph.split()
        line = []
        line_len = 0
        for word in words:
            if line_len + len(word) + len(line) > width:
                if len(line) == 1:
                    lines.append(' '.join(line))
                else:
                    spaces_needed = width - line_len
                    gaps = len(line) - 1
                    if gaps > 0:
                        extra = spaces_needed // gaps
                        remainder = spaces_needed % gaps
                        justified = ''
                        for i, w in enumerate(line[:-1]):
                            justified += w + ' ' * (1 + extra + (1 if i < remainder else 0))
                        justified += line[-1]
                        lines.append(justified)
                    else:
                        lines.append(line[0])
                line = [word]
                line_len = len(word)
            else:
                line.append(word)
                line_len += len(word)
        if line:
            lines.append(' '.join(line))
    return '\n'.join(lines)


def align_table(data: List[list], headers: List[str] = None) -> str:
    """جدول منسق"""
    if not data:
        return ""
    if headers:
        all_rows = [headers] + data
    else:
        all_rows = data
        headers = data[0]

    col_widths = [len(str(h)) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    lines = [sep]
    if headers:
        hdr = "| " + " | ".join(str(h).ljust(w) for h, w in zip(headers, col_widths)) + " |"
        lines.append(hdr)
        lines.append(sep)
    for row in data:
        r = "| " + " | ".join(str(c).ljust(w) for c, w in zip(row, col_widths)) + " |"
        lines.append(r)
    lines.append(sep)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# 3. تنسيق JSON
# ═══════════════════════════════════════════════════════════

def format_json(data: Union[dict, list, str], indent: int = 2) -> str:
    """تنسيق JSON مقروء مع دعم العربي"""
    if isinstance(data, str):
        data = json.loads(data)
    return json.dumps(data, ensure_ascii=False, indent=indent, sort_keys=True) + "\n"


def format_json_file(path: str) -> str:
    """تنسيق ملف JSON"""
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    formatted = format_json(data)
    Path(path).write_text(formatted, encoding='utf-8')
    return f"✅ {path}"


# ═══════════════════════════════════════════════════════════
# 4. تنسيق CSS
# ═══════════════════════════════════════════════════════════

def beautify_css(css: str) -> str:
    """تجميل وجعل CSS مقروءاً"""
    css = re.sub(r'/\*[\s\S]*?\*/', lambda m: '\n' + m.group(0) + '\n', css)
    css = re.sub(r'\s+', ' ', css)
    css = css.replace('{', ' {\n    ')
    css = css.replace(';', ';\n    ')
    css = css.replace('}', '\n}\n\n')
    css = re.sub(r',\s*', ',\n    ', css)
    css = re.sub(r'\n\s+\n', '\n\n', css)
    return css.strip()


def minify_css(css: str) -> str:
    """تصغير CSS للإنتاج"""
    css = re.sub(r'/\*[\s\S]*?\*/', '', css)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};:,])\s*', r'\1', css)
    css = re.sub(r';}', r'}', css)
    return css.strip()


def sort_css_properties(css: str) -> str:
    """ترتيب خصائص CSS أبجدياً"""
    def sort_block(m):
        block = m.group(0)
        selector = block.split('{')[0].strip()
        props = block.split('{')[1].split('}')[0].strip()
        prop_list = [p.strip() for p in props.split(';') if p.strip()]
        prop_list.sort(key=lambda x: x.split(':')[0].strip().lower())
        sorted_props = ';\n    '.join(prop_list)
        return f"{selector} {{\n    {sorted_props}\n}}"
    css = re.sub(r'[^{]+\{[^}]+\}', sort_block, css)
    return css


# ═══════════════════════════════════════════════════════════
# 5. إنشاء إعدادات التنسيق
# ═══════════════════════════════════════════════════════════

def create_format_configs(path: str = ".") -> List[str]:
    """إنشاء ملفات إعدادات التنسيق للمشروع"""
    path = Path(path)
    results = []

    # .prettierrc
    prettier = {
        "semi": True,
        "singleQuote": True,
        "tabWidth": 2,
        "trailingComma": "all",
        "printWidth": 100,
        "arrowParens": "always",
        "endOfLine": "lf"
    }
    (path / ".prettierrc").write_text(
        json.dumps(prettier, indent=2) + "\n", encoding='utf-8')
    results.append("✅ .prettierrc")

    # .editorconfig
    editorconfig = """root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[*.md]
trim_trailing_whitespace = false
"""
    (path / ".editorconfig").write_text(editorconfig, encoding='utf-8')
    results.append("✅ .editorconfig")

    # .gitattributes
    gitattr = """*.py text diff=python
*.js text
*.ts text
*.html text
*.css text
*.json text
*.md text
*.sh text eol=lf
*.bat text eol=crlf
"""
    (path / ".gitattributes").write_text(gitattr, encoding='utf-8')
    results.append("✅ .gitattributes")

    return results


# ═══════════════════════════════════════════════════════════
# 6. تنسيق النواتج الصوتية / التقارير
# ═══════════════════════════════════════════════════════════

def format_report(title: str, sections: dict, style: str = "markdown") -> str:
    """تنسيق تقرير احترافي"""
    lines = []
    if style == "markdown":
        lines.append(f"# {title}")
        lines.append(f"**التاريخ:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("---")
        for section, content in sections.items():
            lines.append(f"\n## {section}\n")
            if isinstance(content, list):
                for item in content:
                    lines.append(f"- {item}")
            elif isinstance(content, dict):
                for k, v in content.items():
                    lines.append(f"- **{k}:** {v}")
            else:
                lines.append(str(content))
        lines.append("\n---")
        lines.append("*التقرير منسق بواسطة DevCenter Format Master*")
    else:
        lines.append(f"=== {title} ===")
        lines.append(f"التاريخ: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("=" * 50)
        for section, content in sections.items():
            lines.append(f"\n-- {section} --\n")
            if isinstance(content, list):
                for item in content:
                    lines.append(f"  - {item}")
            elif isinstance(content, dict):
                for k, v in content.items():
                    lines.append(f"  {k}: {v}")
            else:
                lines.append(f"  {content}")
        lines.append("=" * 50)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# 7. CLI
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Format Master — تنسيق احترافي")
    parser.add_argument("path", nargs="?", default=".", help="المسار للتنسيق")
    parser.add_argument("--check", action="store_true", help="فحص فقط بدون كتابة")
    parser.add_argument("--config", action="store_true", help="إنشاء ملفات الإعدادات")
    parser.add_argument("--json", type=str, help="تنسيق ملف JSON")
    parser.add_argument("--css", type=str, help="تجميل ملف CSS")
    parser.add_argument("--minify-css", type=str, help="تصغير ملف CSS")
    parser.add_argument("--table", action="store_true", help="تنسيق كجدول من stdin")

    args = parser.parse_args()

    if args.config:
        results = create_format_configs(args.path)
        for r in results:
            print(r)

    elif args.json:
        print(format_json_file(args.json))

    elif args.css:
        css = Path(args.css).read_text(encoding='utf-8')
        Path(args.css).write_text(beautify_css(css), encoding='utf-8')
        print(f"✅ {args.css} — تم التجميل")

    elif args.minify_css:
        css = Path(args.minify_css).read_text(encoding='utf-8')
        Path(args.minify_css).write_text(minify_css(css), encoding='utf-8')
        print(f"✅ {args.minify_css} — تم التصغير")

    elif args.table:
        import sys as _sys
        lines = [l.strip() for l in _sys.stdin.read().split('\n') if l.strip()]
        if lines:
            data = [l.split('\t') for l in lines]
            print(align_table(data[1:], data[0] if len(data) > 1 else None))

    else:
        results = format_project(args.path, check_only=args.check)
        for r in results:
            print(r)
