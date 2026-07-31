import os
import re
import subprocess
import sys
import tempfile
import yaml

CONTENT_DIR = "content"
OUTPUT_DIR = "report/generated"
LUA_FILTER = os.path.join("scripts", "hugo-notice.lua")

SECTION_TITLES_VI = {
    "1-Worklog": "Nhật ký công việc",
    "2-Proposal": "Đề xuất",
    "3-BlogsPosted": "Các bài blogs đã đăng",
    "4-EventParticipated": "Các sự kiện đã tham gia",
    "5-Workshop": "Workshop",
    "6-Self-evaluation": "Tự đánh giá",
    "7-Feedback": "Chia sẻ, đóng góp ý kiến",
}

SECTION_TITLES_EN = {
    "1-Worklog": "Worklog",
    "2-Proposal": "Proposal",
    "3-BlogsPosted": "Blogs Posted",
    "4-EventParticipated": "Events Participated",
    "5-Workshop": "Workshop",
    "6-Self-evaluation": "Self-Evaluation",
    "7-Feedback": "Sharing and Feedback",
}

TOP_BODY_VI = "Báo cáo thực tập"
TOP_BODY_EN = "Internship Report"

LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def check_dependencies():
    if not os.path.isdir(CONTENT_DIR):
        raise RuntimeError(f"Content directory not found: {CONTENT_DIR}")

    if not os.path.exists(LUA_FILTER):
        raise RuntimeError(f"Lua filter not found: {LUA_FILTER}")

    try:
        subprocess.run(
            ["pandoc", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        raise RuntimeError("pandoc is not installed or not in PATH")


def sort_key(dirpath):
    parts = []

    for seg in dirpath.split(os.sep):
        m = re.match(r"(\d+(?:\.\d+)*)", seg)
        if m:
            parts.append(tuple(int(x) for x in m.group(1).split(".")))
        else:
            parts.append((9999,))

    return tuple(parts)


def tex_safe(name):
    return re.sub(r"[^a-zA-Z0-9]", "_", name).strip("_")


def strip_emojis(text):
    if not text:
        return ""
    emoji_pattern = re.compile(
        "["
        "\U0001F000-\U0001FAFF"
        "\U00002600-\U000027BF"
        "\u200d"
        "\ufe0f"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub("", text)


def sanitize_latex_text(text):
    if text is None:
        return ""

    text = strip_emojis(str(text))
    return re.sub(
        r"[\\&%$#_{}~^]",
        lambda m: LATEX_SPECIALS[m.group(0)],
        text,
    )


def extract_frontmatter(content):
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", content, re.DOTALL)
    if not match:
        return {}

    try:
        fm = yaml.safe_load(match.group(1))
        return fm if isinstance(fm, dict) else {}
    except yaml.YAMLError:
        return {}


def read_frontmatter(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return extract_frontmatter(fh.read())
    except Exception as e:
        print(f"Warning: cannot read frontmatter from {path}: {e}", file=sys.stderr)
        return {}


def strip_frontmatter(content):
    content = content.strip()
    match = re.match(r"^---\s*\n.*?\n---\s*(?:\n|$)", content, re.DOTALL)
    if match:
        return content[match.end():].strip()
    return content


def get_bool_meta(meta, keys, default):
    for key in keys:
        if key in meta:
            return bool(meta[key])
    return default


def get_list_meta(meta, keys):
    for key in keys:
        value = meta.get(key)
        if value is None:
            continue

        if isinstance(value, list):
            return [str(x) for x in value]

        if isinstance(value, str):
            return [x.strip() for x in value.split(",") if x.strip()]

    return []


def check_duplicate_outputs(pages):
    seen = {}

    for rel_dir, out_name, _title, _meta in pages:
        if out_name in seen:
            raise ValueError(
                f"Duplicate generated filename: {out_name}.tex\n"
                f"  - {seen[out_name]}\n"
                f"  - {rel_dir}"
            )

        seen[out_name] = rel_dir


# ---------------------------------------------------------------------------
# Markdown filters before Pandoc
# ---------------------------------------------------------------------------

def split_markdown_table_row(line):
    stripped = line.strip()

    if not stripped.startswith("|"):
        return None

    if stripped.endswith("|"):
        stripped = stripped[1:-1]
    else:
        stripped = stripped[1:]

    return [cell.strip() for cell in stripped.split("|")]


def is_markdown_table_separator(line):
    cells = split_markdown_table_row(line)
    if not cells:
        return False

    return all(re.match(r"^:?-{3,}:?$", cell.strip()) for cell in cells)


def make_markdown_table_row(cells):
    return "| " + " | ".join(cells) + " |"


def filter_markdown_tables(content, keep_columns):
    """Whitelist columns in Markdown pipe tables."""
    if not keep_columns:
        return content

    keep_norm = {c.strip().lower() for c in keep_columns}

    lines = content.splitlines()
    out = []
    i = 0

    while i < len(lines):
        is_table_start = (
            i + 1 < len(lines)
            and split_markdown_table_row(lines[i]) is not None
            and is_markdown_table_separator(lines[i + 1])
        )

        if not is_table_start:
            out.append(lines[i])
            i += 1
            continue

        header_cells = split_markdown_table_row(lines[i])
        sep_cells = split_markdown_table_row(lines[i + 1])

        keep_idx = [
            idx for idx, name in enumerate(header_cells)
            if name.strip().lower() in keep_norm
        ]

        if not keep_idx:
            out.append(lines[i])
            i += 1
            continue

        out.append(make_markdown_table_row([header_cells[idx] for idx in keep_idx]))
        out.append(make_markdown_table_row([sep_cells[idx] for idx in keep_idx]))

        i += 2

        while i < len(lines) and split_markdown_table_row(lines[i]) is not None:
            row_cells = split_markdown_table_row(lines[i])

            if len(row_cells) < len(header_cells):
                row_cells += [""] * (len(header_cells) - len(row_cells))

            out.append(make_markdown_table_row([row_cells[idx] for idx in keep_idx]))
            i += 1

    return "\n".join(out)

def normalize_col_name(name):
    return re.sub(r"\s+", " ", str(name).strip()).lower()


def latex_escape_cell(text):
    """Escape normal text for LaTeX table cells, but keep simple formatting."""
    if text is None:
        return ""

    text = str(text).strip()

    # Remove markdown links <https://...> -> https://...
    text = re.sub(r"<(https?://[^>]+)>", r"\1", text)

    # Markdown bold
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)

    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }

    # Escape only outside simple LaTeX commands introduced above.
    # Simpler and okay for report use:
    for k, v in replacements.items():
        if k == "\\":
            continue
        text = text.replace(k, v)

    # Restore \textbf after escaping braces.
    text = text.replace(r"\textbf\{", r"\textbf{").replace(r"\}", "}")

    return text


def task_cell_to_latex(text):
    """Convert a worklog Task cell with <br>, '-' and '+' markers to multiline LaTeX."""
    if not text:
        return ""

    text = str(text)

    # Normalize line breaks from Hugo/Markdown table cell.
    text = text.replace("<br>", "\n")
    text = text.replace("<br/>", "\n")
    text = text.replace("<br />", "\n")
    text = text.replace("&emsp;", " ")

    raw_lines = [x.strip() for x in text.splitlines()]
    raw_lines = [x for x in raw_lines if x]

    if not raw_lines:
        return ""

    out = []
    in_itemize = False

    def open_itemize():
        nonlocal in_itemize
        if not in_itemize:
            out.append(r"\begin{itemize}")
            out.append(r"\setlength\itemsep{0.15em}")
            out.append(r"\setlength\parskip{0pt}")
            in_itemize = True

    def close_itemize():
        nonlocal in_itemize
        if in_itemize:
            out.append(r"\end{itemize}")
            in_itemize = False

    for line in raw_lines:
        line = line.strip()

        # "- Task"
        if line.startswith("-"):
            open_itemize()
            item = line[1:].strip()
            out.append(r"\item " + latex_escape_cell(item))

        # "+ sub task"
        elif line.startswith("+"):
            open_itemize()
            item = line[1:].strip()
            out.append(r"\item[] \hspace{1em}+ " + latex_escape_cell(item))

        # fallback normal line
        else:
            if in_itemize:
                out.append(r"\item " + latex_escape_cell(line))
            else:
                out.append(latex_escape_cell(line) + r"\\")

    close_itemize()

    return "\n".join(out)


def simple_cell_to_latex(text):
    """Convert normal table cell to LaTeX."""
    if text is None:
        return ""

    text = str(text).strip()
    text = text.replace("<br>", r"\\ ")
    text = text.replace("<br/>", r"\\ ")
    text = text.replace("<br />", r"\\ ")
    text = text.replace("&emsp;", " ")

    return latex_escape_cell(text)


def extract_first_markdown_table(content):
    """Extract first pipe markdown table.

    Returns: before, header_cells, rows, after
    """
    lines = content.splitlines()

    for i in range(len(lines) - 1):
        if (
            split_markdown_table_row(lines[i]) is not None
            and is_markdown_table_separator(lines[i + 1])
        ):
            header = split_markdown_table_row(lines[i])
            rows = []

            j = i + 2
            while j < len(lines) and split_markdown_table_row(lines[j]) is not None:
                row = split_markdown_table_row(lines[j])

                if len(row) < len(header):
                    row += [""] * (len(header) - len(row))

                rows.append(row[:len(header)])
                j += 1

            before = "\n".join(lines[:i]).strip()
            after = "\n".join(lines[j:]).strip()

            return before, header, rows, after

    return content, None, None, ""


def render_worklog_table_latex(header, rows, keep_columns):
    """Render worklog markdown table as custom LaTeX longtable."""
    header_norm = [normalize_col_name(h) for h in header]
    keep_norm = [normalize_col_name(c) for c in keep_columns]

    keep_idx = []
    keep_names = []

    for col in keep_norm:
        if col in header_norm:
            idx = header_norm.index(col)
            keep_idx.append(idx)
            keep_names.append(header[idx])

    if not keep_idx:
        keep_idx = list(range(len(header)))
        keep_names = header

    # Detect columns
    day_names = {"day", "thứ", "thu"}
    task_names = {"task", "công việc", "cong viec"}
    complete_names = {"completion date", "complete date", "ngày hoàn thành", "ngay hoan thanh"}

    latex = []
    latex.append(r"\begingroup")
    latex.append(r"\small")
    latex.append(r"\setlength{\tabcolsep}{5pt}")
    latex.append(r"\renewcommand{\arraystretch}{1.2}")
    latex.append(r"\begin{longtable}{|p{0.07\linewidth}|p{0.72\linewidth}|p{0.17\linewidth}|}")
    latex.append(r"\hline")

    # Force nicer names based on selected columns count.
    display_headers = []
    for name in keep_names:
        n = normalize_col_name(name)
        if n in day_names:
            display_headers.append("Day" if name.lower() == "day" else "Thứ")
        elif n in task_names:
            display_headers.append("Task" if name.lower() == "task" else "Công việc")
        elif n in complete_names:
            display_headers.append("Completion Date" if "date" in name.lower() else "Ngày hoàn thành")
        else:
            display_headers.append(name)

    # If user selects exactly Day/Task/Completion, use 3-column layout.
    latex.append(" & ".join(r"\textbf{" + latex_escape_cell(h) + "}" for h in display_headers) + r" \\ \hline")
    latex.append(r"\endhead")

    for row in rows:
        selected = [row[idx] if idx < len(row) else "" for idx in keep_idx]
        rendered = []

        for name, cell in zip(keep_names, selected):
            n = normalize_col_name(name)

            if n in task_names:
                rendered.append(task_cell_to_latex(cell))
            else:
                rendered.append(simple_cell_to_latex(cell))

        latex.append(" & ".join(rendered) + r" \\ \hline")

    latex.append(r"\end{longtable}")
    latex.append(r"\endgroup")

    return "\n".join(latex)


def preprocess_worklog_markdown(content, meta):
    """Convert worklog markdown table into raw LaTeX before Pandoc."""
    content = strip_frontmatter(content)

    keep_columns = get_list_meta(
        meta,
        ["reportTableColumns", "report_table_columns", "latexTableColumns", "latex_table_columns"],
    )

    before, header, rows, after = extract_first_markdown_table(content)

    if header is None:
        return content

    table_latex = render_worklog_table_latex(header, rows, keep_columns)

    pieces = []
    if before:
        pieces.append(before)

    pieces.append(table_latex)

    if after:
        pieces.append(after)

    return "\n\n".join(pieces)

def filter_markdown_sections(content, keep_headings):
    """Whitelist markdown sections by heading text.

    Keeps content before the first heading.
    If a heading is kept, its subsection content is kept until another
    same-level or higher-level heading appears.
    """
    if not keep_headings:
        return content

    keep_norm = {h.strip().lower() for h in keep_headings}

    lines = content.splitlines()
    out = []

    keep_stack_level = None
    before_first_heading = True
    keeping = True

    for line in lines:
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)

        if m:
            before_first_heading = False
            level = len(m.group(1))
            title = re.sub(r"\s+#*$", "", m.group(2)).strip()
            title_norm = title.lower()

            if title_norm in keep_norm:
                keeping = True
                keep_stack_level = level
                out.append(line)
                continue

            if keep_stack_level is not None and level > keep_stack_level and keeping:
                out.append(line)
                continue

            keeping = False
            keep_stack_level = None
            continue

        if before_first_heading or keeping:
            out.append(line)

    return "\n".join(out)


def preprocess_markdown(content, meta=None):
    meta = meta or {}

    report_type = str(meta.get("reportType") or meta.get("report_type") or "").lower()

    if report_type == "worklog":
        content = preprocess_worklog_markdown(content, meta)
    else:
        content = strip_frontmatter(content)

        keep_headings = get_list_meta(
            meta,
            ["reportHeadings", "report_headings", "latexHeadings", "latex_headings"],
        )

        keep_columns = get_list_meta(
            meta,
            ["reportTableColumns", "report_table_columns", "latexTableColumns", "latex_table_columns"],
        )

        if keep_headings:
            content = filter_markdown_sections(content, keep_headings)

        if keep_columns:
            content = filter_markdown_tables(content, keep_columns)

    content = re.sub(r"!\[([^\]]*)\]\(/fcaj-workshop/images/", r"![\1](", content)
    content = re.sub(r"!\[([^\]]*)\]\(/static/images/", r"![\1](", content)
    content = re.sub(r"!\[([^\]]*)\]\(/images/",      r"![\1](", content)

    content = re.sub(
        r"\{\{%\s*notice\s+(\w+)\s*%\}\}\s*",
        r"\n::: {\1}\n",
        content,
    )
    content = re.sub(r"\s*\{\{%\s*/notice\s*%\}\}", r"\n:::\n", content)

    content = content.replace("&emsp;", r"\qquad ")
    content = content.replace("\u2705", r"\checkmark")
    content = content.replace("\u2610", r"$\square$")
    content = re.sub(r"⚠\ufe0f?", "!", content)
    content = content.replace("\u26a0", "!")
    content = content.replace("\u2192", r"$\rightarrow$")
    content = strip_emojis(content)

    return content
# ---------------------------------------------------------------------------
# Pandoc LaTeX conversion
# ---------------------------------------------------------------------------
def neutralize_body_headings(latex):
    """Convert Pandoc headings to visual bold headings."""

    heading_cmds = ["section", "subsection", "subsubsection", "paragraph", "subparagraph"]

    # 1. Bỏ toàn bộ \hypertarget wrapper nhưng giữ nội dung bên trong.
    # Pandoc thường sinh:
    # \hypertarget{id}{%
    # \section{Title}\label{id}}
    latex = re.sub(
        r"\\hypertarget\{[^{}]*\}\{\s*%?\s*",
        "",
        latex,
        flags=re.DOTALL,
    )

    # Sau khi bỏ phần mở \hypertarget, thường sẽ dư "}" sau \label hoặc sau heading.
    latex = re.sub(
        r"(\\label\{[^{}]*\})\s*\}",
        r"\1",
        latex,
        flags=re.DOTALL,
    )

    # 2. Remove labels.
    latex = re.sub(r"\\label\{[^{}]*\}", "", latex)

    # 3. Convert standalone headings thành text đậm.
    for cmd in heading_cmds:
        latex = re.sub(
            rf"\\{cmd}\{{([^{{}}]*)\}}",
            r"\\vspace{0.5em}\\noindent\\textbf{\1}\\par",
            latex,
            flags=re.DOTALL,
        )

    # 4. Safety net: nếu vẫn còn dạng hỏng:
    # \hypertarget{id}{\vspace{0.5em}\noindent\textbf{Title}\par}
    latex = re.sub(
        r"\\hypertarget\{[^{}]*\}\{\s*(\\vspace\{0\.5em\}\\noindent\\textbf\{[^{}]*\}\\par)\s*\}",
        r"\1",
        latex,
        flags=re.DOTALL,
    )
    latex = re.sub(
        r"(\\vspace\{0\.5em\}\\noindent\\textbf\{[^{}]*\}\\par)\}",
        r"\1",
        latex,
        flags=re.DOTALL,
    )

    return latex

def compact_longtables(latex):
    """Make Pandoc longtables more compact without modifying column specs."""
    if r"\begin{longtable}" not in latex:
        return latex

    latex = latex.replace(
        r"\begin{longtable}",
        r"""\begingroup
\small
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.15}
\begin{longtable}"""
    )

    latex = latex.replace(
        r"\end{longtable}",
        r"""\end{longtable}
\endgroup"""
    )

    return latex


def format_tables_with_grid(latex):
    """Add grid lines (horizontal \\hline and vertical | column borders) to longtable environments."""
    if r"\begin{longtable}" not in latex:
        return latex

    def transform_table(match):
        table_text = match.group(0)

        # 1. Replace booktabs rules (\toprule, \midrule, \bottomrule) with \hline
        table_text = re.sub(r"\\toprule(\s*\\noalign\{\})?", r"\\hline", table_text)
        table_text = re.sub(r"\\midrule(\s*\\noalign\{\})?", r"\\hline", table_text)
        table_text = re.sub(r"\\bottomrule(\s*\\noalign\{\})?", r"\\hline", table_text)

        # 2. Modify column specifier in \begin{longtable}[...]{spec} or \begin{longtable}{spec}
        def fix_spec(m):
            head = m.group(1)  # \begin{longtable} or \begin{longtable}[...]
            spec = m.group(2)  # inner column specification string

            # Remove @{} and @{\noalign{...}} and existing |
            spec_clean = re.sub(r"@\{[^}]*\}", "", spec)
            spec_clean = spec_clean.replace("|", " ")

            lines = [line.strip() for line in spec_clean.splitlines() if line.strip()]
            cols = []
            for l in lines:
                # Split multiple column specs on the same line if present
                sub_cols = re.split(r"\s+(?=>|p\{|m\{|b\{|(?<!\\)\b[clr]\b)", l)
                for sc in sub_cols:
                    if sc.strip():
                        cols.append(sc.strip())

            if not cols:
                return m.group(0)

            fixed_cols = ["|" + c for c in cols]
            new_spec = " ".join(fixed_cols) + "|"
            new_spec = re.sub(r"\|+", "|", new_spec)

            return f"{head}{{{new_spec}}}"

        table_text = re.sub(
            r"(\\begin\{longtable\}(?:\[[^\]]*\])?)\{(.*?)\}\s*(?=\\toprule|\\hline|\\midrule|\\endhead)",
            fix_spec,
            table_text,
            count=1,
            flags=re.DOTALL
        )

        # 3. Add \hline after each body row
        if r"\endhead" in table_text:
            parts = table_text.split(r"\endhead", 1)
            head_part = parts[0] + r"\endhead"
            body_part = parts[1]

            foot_str = ""
            if r"\endlastfoot" in body_part:
                foot_split = body_part.split(r"\endlastfoot", 1)
                foot_str = foot_split[0] + r"\endlastfoot"
                body_part = foot_split[1]
            elif r"\endfoot" in body_part:
                foot_split = body_part.split(r"\endfoot", 1)
                foot_str = foot_split[0] + r"\endfoot"
                body_part = foot_split[1]

            body_lines = body_part.splitlines(True)
            new_body = []
            for line in body_lines:
                stripped = line.rstrip()
                if r"\end{longtable}" in line:
                    new_body.append(line)
                elif stripped.endswith(r"\\"):
                    new_body.append(stripped + r" \hline" + ("\n" if line.endswith("\n") else ""))
                elif stripped.endswith(r"\\ \hline"):
                    new_body.append(line)
                else:
                    new_body.append(line)

            table_text = head_part + foot_str + "".join(new_body)

        return table_text

    return re.sub(r"\\begin\{longtable\}.*?\\end\{longtable\}", transform_table, latex, flags=re.DOTALL)


def postprocess_latex(latex):
    latex = re.sub(r"\\label\{[^}]+\}", "", latex)
    latex = neutralize_body_headings(latex)
    latex = format_tables_with_grid(latex)
    latex = compact_longtables(latex)
    return latex


def convert_to_latex(md_text, source_path=None):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_in = os.path.join(tmpdir, "input.md")
        tmp_out = os.path.join(tmpdir, "output.tex")

        with open(tmp_in, "w", encoding="utf-8") as f:
            f.write(md_text)

        try:
            subprocess.run(
                [
                    "pandoc",
                    tmp_in,
                    "-f", "markdown+raw_tex+fenced_divs+bracketed_spans",
                    "-t", "latex",
                    "--top-level-division=section",
                    "--lua-filter", LUA_FILTER,
                    "-o", tmp_out,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            if source_path:
                print(f"\nPandoc failed for: {source_path}", file=sys.stderr)
            print(e.stderr, file=sys.stderr)
            raise

        with open(tmp_out, encoding="utf-8") as f:
            latex = f.read()

    return postprocess_latex(latex)


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_pages(lang):
    suffix = ".vi" if lang == "vi" else ""
    filename = f"_index{suffix}.md"

    all_dirs = set()
    pages = []
    skip_dirs = set()

    for root, _dirs, files in os.walk(CONTENT_DIR):
        rel = os.path.relpath(root, CONTENT_DIR)

        if rel == ".":
            continue

        # If any ancestor directory is skipped, skip this directory too.
        if any(rel == d or rel.startswith(d + os.sep) for d in skip_dirs):
            continue

        if filename not in files:
            continue

        md_path = os.path.join(root, filename)
        meta = read_frontmatter(md_path)

        include = get_bool_meta(
            meta,
            ["includeInReport", "include_in_report", "isincludeinlatex", "includeInLatex"],
            True,
        )

        if not include:
            print(f"  SKIP: {rel}")
            skip_dirs.add(rel)
            continue

        all_dirs.add(rel)

        title = meta.get("title")
        title = str(title) if title is not None else None

        pages.append((rel, tex_safe(rel), title, meta))

    container_dirs = {
        d for d in all_dirs
        if any(p.startswith(d + os.sep) for p in all_dirs)
    }

    pages.sort(key=lambda p: sort_key(p[0]))
    check_duplicate_outputs(pages)

    return pages, container_dirs
# ---------------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------------

def process_language(lang):
    suffix = ".vi" if lang == "vi" else ""
    lang_dir = os.path.join(OUTPUT_DIR, lang)
    os.makedirs(lang_dir, exist_ok=True)

    pages, containers = discover_pages(lang)

    for rel_dir, out_name, _title, meta in pages:
        md_path = os.path.join(CONTENT_DIR, rel_dir, f"_index{suffix}.md")

        with open(md_path, encoding="utf-8") as f:
            md_content = f.read()

        processed = preprocess_markdown(md_content, meta=meta)
        latex = convert_to_latex(processed, source_path=md_path)

        out_path = os.path.join(lang_dir, f"{out_name}.tex")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(latex)

        marker = "C" if rel_dir in containers else "L"
        print(f"  {lang.upper()}: [{marker}] {out_name}.tex")

    return pages, containers


def build_include_file(lang, pages, containers):
    titles = SECTION_TITLES_VI if lang == "vi" else SECTION_TITLES_EN
    top_body = TOP_BODY_VI if lang == "vi" else TOP_BODY_EN

    sections = {}

    for rel_dir, out_name, title, meta in pages:
        sec = rel_dir.split(os.sep)[0]
        sections.setdefault(sec, []).append((rel_dir, out_name, title, meta))

    lines = []

    lines.append(r"\providecommand{\tightlist}{%")
    lines.append(r"  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}%")
    lines.append(r"}")
    lines.append(r"\providecommand{\pandocbounded}[1]{#1}")
    lines.append("")

    lines.append(f"\\section{{{sanitize_latex_text(top_body)}}}")
    lines.append("")

    for sec_dir in sorted(sections, key=lambda s: sort_key(s)):
        if sec_dir == "7-Feedback":
            continue
        sec_pages = sections[sec_dir]
        sec_title = titles.get(sec_dir, sec_dir.replace("-", " "))

        lines.append(f"\\subsection{{{sanitize_latex_text(sec_title)}}}")
        lines.append("")

        for rel_dir, out_name, title, meta in sec_pages:
            depth = rel_dir.count(os.sep) + 1

            if depth == 1 and rel_dir in containers:
                continue

            if rel_dir in containers:
                lines.append(f"\\input{{generated/{lang}/{out_name}}}")
                lines.append("")

            elif depth == 1:
                lines.append(f"\\input{{generated/{lang}/{out_name}}}")
                lines.append("")

            else:
                label = (
                    sanitize_latex_text(title)
                    if title
                    else sanitize_latex_text(rel_dir.split(os.sep)[-1].replace("-", " "))
                )

                lines.append(f"\\subsubsection{{{label}}}")
                lines.append(f"\\input{{generated/{lang}/{out_name}}}")
                lines.append("")

        lines.append(r"\newpage")
        lines.append("")

    out_path = os.path.join(OUTPUT_DIR, f"content_body_{lang}.tex")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"  -> {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        check_dependencies()

        print("=== Converting Hugo content to LaTeX ===\n")

        for lang in ("en", "vi"):
            print(f"-- {lang.upper()} --")
            pages, containers = process_language(lang)
            build_include_file(lang, pages, containers)
            print()

        print("Done.")

    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)