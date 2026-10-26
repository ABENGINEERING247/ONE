from io import BytesIO
import re, zipfile, json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from xml.sax.saxutils import escape

def _clean_title(title):
    return re.sub(r"[^\w\-]+", "_", title.strip())[:70] or "ONE_research"

def docx_bytes(title, markdown):
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Inches(0.8); sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.9); sec.right_margin = Inches(0.9)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"; normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)
    p = doc.add_paragraph()
    p.alignment = 1
    r = p.add_run(title); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(18); r.font.color.rgb = RGBColor(19, 100, 83)
    for line in markdown.splitlines():
        s = line.strip()
        if not s: continue
        if s.startswith("# "):
            continue
        if s.startswith("### "): doc.add_heading(s[4:], level=3)
        elif s.startswith("## "): doc.add_heading(s[3:], level=1)
        elif s.startswith("# "): doc.add_heading(s[2:], level=1)
        elif s.startswith("> "):
            p = doc.add_paragraph(s[2:])
            p.paragraph_format.left_indent = Inches(0.25)
        elif re.match(r"^\d+\.\s", s):
            doc.add_paragraph(re.sub(r"^\d+\.\s", "", s), style="List Number")
        elif s.startswith("- "):
            doc.add_paragraph(s[2:], style="List Bullet")
        else:
            doc.add_paragraph(s.replace("**", "").replace("`", ""))
    footer = sec.footer.paragraphs[0]
    footer.text = "ONE — AI Research Agent | Review all claims and references before submission"
    out = BytesIO(); doc.save(out); return out.getvalue()

def pdf_bytes(title, markdown):
    out = BytesIO()
    doc = SimpleDocTemplate(out, pagesize=A4, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ONEtitle", parent=styles["Title"], textColor=colors.HexColor("#138A72"), alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=18, leading=22, spaceAfter=18))
    styles.add(ParagraphStyle(name="H1custom", parent=styles["Heading1"], textColor=colors.HexColor("#176B5B"), spaceBefore=12, spaceAfter=6))
    story = [Paragraph(escape(title), styles["ONEtitle"])]
    for line in markdown.splitlines():
        s = line.strip()
        if not s: story.append(Spacer(1, 5)); continue
        if s.startswith("> "):
            story.append(Paragraph(f"<i>{escape(s[2:])}</i>", styles["BodyText"]))
        elif s.startswith("### "):
            story.append(Paragraph(escape(s[4:]), styles["Heading2"]))
        elif s.startswith("## "):
            story.append(Paragraph(escape(s[3:]), styles["H1custom"]))
        elif s.startswith("# "):
            continue
        elif s.startswith("- "):
            story.append(Paragraph("• " + escape(s[2:]), styles["BodyText"]))
        elif re.match(r"^\d+\.\s", s):
            story.append(Paragraph(escape(s), styles["BodyText"]))
        else:
            story.append(Paragraph(escape(s.replace("**", "").replace("`", "")), styles["BodyText"]))
        story.append(Spacer(1, 4))
    doc.build(story)
    return out.getvalue()

def latex_source(title, markdown):
    body = []
    for line in markdown.splitlines():
        s = line.strip()
        if not s: continue
        if s.startswith("# "): continue
        if s.startswith("### "): body.append(r"\subsection{" + _latex_escape(s[4:]) + "}")
        elif s.startswith("## "): body.append(r"\section{" + _latex_escape(s[3:]) + "}")
        elif s.startswith("> "): body.append(r"\begin{quote}" + _latex_escape(s[2:]) + r"\end{quote}")
        elif s.startswith("- "): body.append(r"\begin{itemize}\item " + _latex_escape(s[2:]) + r"\end{itemize}")
        else: body.append(_latex_escape(s.replace("**", "").replace("`", "")))
        body.append("")
    return (r"""\documentclass[12pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{setspace}
\onehalfspacing
\title{""" + _latex_escape(title) + r"""}
\author{Prepared with ONE -- AI Research Agent}
\date{\today}
\begin{document}
\maketitle
""" + "\n".join(body) + r"""
\end{document}
""").encode("utf-8")

def _latex_escape(s):
    replacements = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(replacements.get(c, c) for c in s)

def project_zip(title, markdown, sources):
    out = BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{_clean_title(title)}/manuscript.md", markdown)
        z.writestr(f"{_clean_title(title)}/manuscript.tex", latex_source(title, markdown))
        z.writestr(f"{_clean_title(title)}/sources.json", json.dumps(sources, indent=2, ensure_ascii=False))
        z.writestr(f"{_clean_title(title)}/README.txt", "ONE research project export. Review claims, sources, methodology, and any required declarations before submission.")
    return out.getvalue()
