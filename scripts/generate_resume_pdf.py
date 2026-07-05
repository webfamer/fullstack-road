from pathlib import Path
import html
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "项思哲_AI应用开发_投递优化稿.md"
OUTPUT = ROOT / "output/pdf/项思哲_AI应用开发_AI全栈_简历.pdf"

BLUE = colors.HexColor("#356FE3")
TEXT = colors.HexColor("#20242B")
MUTED = colors.HexColor("#59616D")
LINE = colors.HexColor("#D9E2F2")


def register_fonts():
    pdfmetrics.registerFont(TTFont("ResumeCN", "/System/Library/Fonts/STHeiti Light.ttc", subfontIndex=0))
    pdfmetrics.registerFont(TTFont("ResumeCN-Bold", "/System/Library/Fonts/STHeiti Medium.ttc", subfontIndex=0))


def clean(text: str) -> str:
    text = text.replace("**", "").replace("`", "")
    return html.escape(text.strip())


def footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(BLUE)
    canvas.rect(0, height - 5 * mm, width, 5 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.4)
    canvas.line(18 * mm, 10 * mm, width - 18 * mm, 10 * mm)
    canvas.setFont("ResumeCN", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 6.5 * mm, "项思哲 | AI 应用开发 / AI 全栈")
    canvas.drawRightString(width - 18 * mm, 6.5 * mm, str(doc.page))
    canvas.restoreState()


def styles():
    base = getSampleStyleSheet()
    common = dict(fontName="ResumeCN", textColor=TEXT, wordWrap="CJK", allowWidows=0, allowOrphans=0)
    return {
        "name": ParagraphStyle(
            "Name", parent=base["Normal"], fontName="ResumeCN-Bold", fontSize=20,
            leading=22, textColor=colors.HexColor("#111827"), spaceAfter=2 * mm,
        ),
        "contact": ParagraphStyle(
            "Contact", parent=base["Normal"], fontName="ResumeCN", fontSize=8.8,
            leading=11, textColor=MUTED, spaceAfter=1.1 * mm,
        ),
        "target": ParagraphStyle(
            "Target", parent=base["Normal"], fontName="ResumeCN-Bold", fontSize=9.2,
            leading=12, textColor=TEXT, spaceAfter=4.5 * mm,
        ),
        "section": ParagraphStyle(
            "Section", parent=base["Normal"], fontName="ResumeCN-Bold", fontSize=12,
            leading=14, textColor=BLUE, spaceBefore=2.4 * mm, spaceAfter=1.8 * mm,
        ),
        "heading": ParagraphStyle(
            "Heading", parent=base["Normal"], fontName="ResumeCN-Bold", fontSize=9.5,
            leading=12, textColor=colors.HexColor("#111827"),
        ),
        "date": ParagraphStyle(
            "Date", parent=base["Normal"], fontName="ResumeCN", fontSize=8.2,
            leading=11, textColor=MUTED, alignment=2,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"], fontName="ResumeCN", fontSize=8.35,
            leading=11.7, textColor=TEXT, spaceAfter=1.1 * mm,
        ),
        "summary": ParagraphStyle(
            "Summary", parent=base["Normal"], fontName="ResumeCN", fontSize=8.55,
            leading=12.2, textColor=TEXT, spaceAfter=1.3 * mm,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"], fontName="ResumeCN", fontSize=8.2,
            leading=11.45, textColor=TEXT, leftIndent=3.2 * mm, firstLineIndent=-2.8 * mm,
            bulletIndent=0, spaceAfter=0.75 * mm,
        ),
        "tech": ParagraphStyle(
            "Tech", parent=base["Normal"], fontName="ResumeCN", fontSize=7.95,
            leading=10.8, textColor=MUTED, spaceAfter=1.1 * mm,
        ),
    }


def section_title(text, style):
    title = Paragraph(clean(text), style)
    return Table(
        [[title]], colWidths=[174 * mm],
        style=TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 0.7, BLUE),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2 * mm),
        ]),
    )


def item_heading(title, date, st):
    return Table(
        [[Paragraph(clean(title), st["heading"]), Paragraph(clean(date), st["date"])]],
        colWidths=[125 * mm, 49 * mm],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0.8 * mm),
        ]),
    )


def parse_resume(st):
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    cutoff = lines.index("## 面试准备边界")
    lines = lines[:cutoff]
    story = []
    i = 0
    section = ""
    while i < len(lines):
        raw = lines[i].rstrip()
        text = raw.strip()
        if not text:
            i += 1
            continue
        if text.startswith("# "):
            story.append(Paragraph(clean(text[2:]), st["name"]))
        elif i == 2:
            story.append(Paragraph(clean(text), st["contact"]))
        elif text.startswith("求职方向："):
            story.append(Paragraph(clean(text), st["target"]))
        elif text.startswith("## "):
            section = text[3:]
            story.append(section_title(section, st["section"]))
            story.append(Spacer(1, 1.2 * mm))
        elif text.startswith("### "):
            title = text[4:]
            if title.startswith("BI 报表分析平台"):
                story.append(PageBreak())
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            date = ""
            if j < len(lines) and re.fullmatch(r"\d{4}\.\d{2} - \d{4}\.\d{2}", lines[j].strip()):
                date = lines[j].strip()
                i = j
            story.append(item_heading(title, date, st))
        elif text.startswith("- "):
            story.append(Paragraph("• " + clean(text[2:]), st["bullet"]))
        elif text.startswith("技术栈："):
            story.append(Paragraph("<b>技术栈：</b>" + clean(text[4:]), st["tech"]))
        else:
            style = st["summary"] if section == "个人优势" else st["body"]
            story.append(Paragraph(clean(text), style))
        i += 1
    return story


def main():
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    width, height = A4
    frame = Frame(
        18 * mm, 13 * mm, width - 36 * mm, height - 25 * mm,
        leftPadding=0, rightPadding=0, topPadding=7 * mm, bottomPadding=2 * mm,
    )
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=12 * mm, bottomMargin=13 * mm,
        title="项思哲 - AI 应用开发 / AI 全栈工程师简历",
        author="项思哲",
        subject="AI 应用开发工程师简历",
    )
    doc.addPageTemplates(PageTemplate(id="resume", frames=[frame], onPage=footer))
    st = styles()
    doc.build(parse_resume(st))
    print(OUTPUT)


if __name__ == "__main__":
    main()
