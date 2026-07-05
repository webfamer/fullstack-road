from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Sizhe_Xiang_English_Resume.pdf"

NAVY = colors.HexColor("#17233C")
BLUE = colors.HexColor("#2563EB")
MUTED = colors.HexColor("#526078")
LINE = colors.HexColor("#D9E1EC")
CONTENT_WIDTH = 176 * mm


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(BLUE)
    canvas.setLineWidth(1.3)
    canvas.line(14 * mm, 11 * mm, width - 14 * mm, 11 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.2)
    canvas.drawString(14 * mm, 7.3 * mm, "Sizhe Xiang | AI Application / Full-Stack Engineer")
    canvas.drawRightString(width - 14 * mm, 7.3 * mm, str(doc.page))
    canvas.restoreState()


def make_styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle("name", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=24, leading=27, textColor=NAVY),
        "target": ParagraphStyle("target", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11.3, leading=15, textColor=BLUE),
        "contact": ParagraphStyle("contact", parent=base["Normal"], fontName="Helvetica", fontSize=9.2, leading=13, textColor=MUTED),
        "section": ParagraphStyle("section", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11.4, leading=15, textColor=BLUE, spaceBefore=7, spaceAfter=3),
        "body": ParagraphStyle("body", parent=base["Normal"], fontName="Helvetica", fontSize=9.1, leading=13.2, textColor=NAVY),
        "bullet": ParagraphStyle("bullet", parent=base["Normal"], fontName="Helvetica", fontSize=8.9, leading=12.6, leftIndent=9, firstLineIndent=-7, spaceAfter=2, textColor=NAVY),
        "title": ParagraphStyle("title", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=NAVY),
        "date": ParagraphStyle("date", parent=base["Normal"], fontName="Helvetica", fontSize=8.4, leading=11.5, alignment=TA_RIGHT, textColor=MUTED),
        "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.4, leading=11.8, spaceAfter=1, textColor=MUTED),
        "stack": ParagraphStyle("stack", parent=base["Normal"], fontName="Helvetica", fontSize=8.2, leading=11.3, spaceAfter=1.5, textColor=MUTED),
    }


def section(title, styles):
    return [
        Spacer(1, 2.2 * mm),
        Paragraph(title.upper(), styles["section"]),
        Table([[""]], colWidths=[CONTENT_WIDTH], rowHeights=[0.3 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), BLUE)])),
        Spacer(1, 1.8 * mm),
    ]


def header(name, role, date, styles):
    table = Table(
        [[Paragraph(f"{name} | {role}", styles["title"]), Paragraph(date, styles["date"])]],
        colWidths=[133 * mm, 43 * mm],
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
    ]))
    return table


def bullet(text, styles):
    return Paragraph(f"- {text}", styles["bullet"])


def project(name, role, date, description, tech, bullets, styles):
    parts = [
        header(name, role, date, styles),
        Paragraph(description, styles["meta"]),
        Paragraph(f"<b>Tech:</b> {tech}", styles["stack"]),
    ]
    parts.extend(bullet(item, styles) for item in bullets)
    parts.append(Spacer(1, 3 * mm))
    return KeepTogether(parts)


def job(company, role, date, description, styles):
    return KeepTogether([
        header(company, role, date, styles),
        bullet(description, styles),
        Spacer(1, 2.4 * mm),
    ])


def build():
    styles = make_styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=17 * mm, rightMargin=17 * mm,
        topMargin=15 * mm, bottomMargin=16 * mm,
        title="Sizhe Xiang - English Resume",
        author="Sizhe Xiang",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="resume", frames=[frame], onPage=footer)])

    story = [
        Paragraph("Sizhe Xiang", styles["name"]),
        Paragraph("AI APPLICATION / FULL-STACK ENGINEER", styles["target"]),
        Paragraph("Hangzhou, China | +86 187 5765 2156 | webfamer@163.com", styles["contact"]),
    ]
    story += section("Professional Summary", styles)
    story.append(Paragraph(
        "Full-stack engineer with 6+ years of experience spanning enterprise frontend development, Node.js backend services, and Python-based AI applications. Hands-on experience building BI platforms, LangGraph/LangChain workflows, RAG-powered metadata retrieval, Text-to-SQL agents, real-time data pipelines, and data visualization systems. Proven ability to own end-to-end delivery, from architecture and implementation to deployment, performance optimization, and production troubleshooting.",
        styles["body"],
    ))

    story += section("Technical Skills", styles)
    skills = [
        ("AI Applications", "LangGraph, LangChain, RAG, Text-to-SQL, SQL Agents, Qdrant, Elasticsearch"),
        ("Backend", "Python, FastAPI, Node.js, NestJS, MySQL, Redis, TCP, JWT, RBAC, SSE"),
        ("Frontend", "React, Vue.js, TypeScript, Umi, Recoil, ECharts, VTable, WebSocket, Unity WebGL"),
        ("Engineering", "Monorepo, Webpack, Storybook, Docker, Nginx, component libraries, production troubleshooting"),
    ]
    rows = [[Paragraph(f"<b>{label}</b>", styles["body"]), Paragraph(value, styles["body"])] for label, value in skills]
    table = Table(rows, colWidths=[29 * mm, 147 * mm])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1),
        ("TOPPADDING", (0, 0), (-1, -1), 0.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
    ]))
    story.append(table)

    story += section("Selected Projects", styles)
    story.append(project(
        "BI Conversational Analytics Agent", "Full-Stack Developer", "Nov 2025 - Apr 2026",
        "Natural-language analytics tool that enables business users to query sales, order, product-category, and regional metrics in Chinese.",
        "Python, FastAPI, LangGraph, LangChain, MySQL, Qdrant, Elasticsearch, React, SSE",
        [
            "Built LangChain nodes for query expansion, field and metric interpretation, and SQL generation.",
            "Orchestrated the end-to-end Text-to-SQL workflow as a LangGraph state graph and used checkpointing to persist and resume execution state.",
            "Developed a metadata knowledge base covering schemas, field aliases, metric definitions, and representative field values, with retrieval across MySQL, Qdrant, and Elasticsearch.",
            "Delivered a FastAPI and SSE query service plus a React chat interface that streams processing status and renders final results as charts.",
        ], styles,
    ))
    story.append(project(
        "BI Reporting and Analytics Platform", "Frontend Developer", "Apr 2025 - Oct 2025",
        "Self-service BI platform for configurable reports, drag-and-drop report generation, dashboards, exports, and sharing.",
        "React, TypeScript, Monorepo, Recoil, Webpack, Storybook, VTable",
        [
            "Developed core workflows for report viewing, dashboard presentation, exports, and sharing, while supporting feature iterations and production issue resolution.",
            "Built a reusable chart component library in Storybook using a pipeline-based architecture and distributed it as an npm package across multiple projects.",
            "Implemented complex table capabilities with VTable and an adapter pattern, including field-specific rendering, adaptive column widths, frozen columns, and drill-down interactions.",
            "Improved page-loading experience through CDN-hosted images, skeleton screens, asynchronous component loading, and multi-region deployment adaptations.",
        ], styles,
    ))
    story.append(PageBreak())
    story.append(project(
        "Power Equipment Monitoring Cloud Platform", "Full-Stack Developer", "Oct 2024 - Apr 2025",
        "Device-access and management platform for cable-well monitoring, covering telemetry ingestion, packet parsing, alerts, authorization, analytics, and operational dashboards.",
        "React, Umi, NestJS, MySQL, Redis, TCP",
        [
            "Independently designed and developed the frontend and backend, delivering device, packet, alert, account, role, and menu-management modules.",
            "Designed a TCP ingestion and parsing pipeline with protocol detection, packet fragmentation and reassembly handling, raw packet storage, and persistence of parsed results.",
            "Implemented JWT authentication and RBAC with menu-level permissions to isolate features and operations by role.",
            "Optimized critical APIs and slow SQL queries, reducing response time from more than 10 seconds to approximately 2 seconds; supported 400+ connected devices and 10,000+ messages per day.",
        ], styles,
    ))
    story.append(project(
        "Smart Training Range Command Dashboard", "Frontend Developer", "Jun 2023 - Jun 2024",
        "Real-time visualization dashboard for training sessions, personnel trajectories, hit events, live video, results, and post-session review.",
        "React, Umi, ECharts, WebSocket, Unity WebGL, Node.js",
        [
            "Developed core dashboard modules for multidimensional visualization of training data, personnel movement, hit feedback, and results.",
            "Built a Node.js transcoding and streaming service that converted RTSP video to MPEG and synchronized live footage with personnel trajectory data.",
            "Processed high-frequency training data over WebSocket and integrated Unity WebGL for 3D rendering of trajectories, gestures, and hit feedback.",
            "Improved long-running stability and responsiveness by resolving video blank screens, UI freezes, and excessive memory consumption.",
        ], styles,
    ))

    story += section("Professional Experience", styles)
    jobs = [
        ("Yida Information Technology Co., Ltd.", "Frontend / Full-Stack Developer", "Apr 2025 - Apr 2026", "Contributed to an enterprise BI analytics platform and a natural-language data-query product, covering reporting workflows, component systems, AI application interactions, and production support."),
        ("Sichuan Weijuzhen Technology Co., Ltd.", "Full-Stack Developer, Remote", "Oct 2024 - Mar 2025", "Delivered the frontend and backend of a power-equipment monitoring platform, including device integration, packet parsing, alert rules, access control, analytics, dashboards, deployment, performance optimization, and production troubleshooting."),
        ("Hangzhou Zhangqi Network Technology Co., Ltd.", "Full-Stack Developer", "Jun 2022 - Sep 2024", "Developed data-visualization dashboards, administration systems, and mobile applications, with ownership of core frontend modules, authorization, application foundations, and on-site issue resolution."),
        ("Hangzhou Pinming Safety Control Information Technology Co., Ltd.", "Frontend Developer / Team Lead", "Apr 2021 - Jun 2022", "Contributed to the Zhuangzhuang SaaS platform and led a frontend team responsible for task allocation, requirement estimation, component-library development, and delivery coordination."),
        ("Zhejiang Panshi Information Technology Co., Ltd.", "Frontend Developer", "Dec 2019 - Mar 2021", "Developed an overseas lending platform, Flutter applications, an SMS platform, and H5 marketing pages."),
    ]
    for item in jobs:
        story.append(job(*item, styles))

    story += section("Education", styles)
    story.append(header("Taiyuan University of Science and Technology", "B.Eng. in Internet of Things Engineering", "Sep 2015 - Jun 2019", styles))

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
