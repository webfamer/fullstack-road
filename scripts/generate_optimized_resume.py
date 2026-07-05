from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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
OUTPUT = ROOT / "output" / "pdf" / "项思哲_AI应用开发工程师_优化版.pdf"
ANNOTATED_OUTPUT = ROOT / "output" / "pdf" / "项思哲_AI应用开发工程师_修改标注版.pdf"

BLUE = colors.HexColor("#2563EB")
INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#526078")
LIGHT = colors.HexColor("#E7ECF3")


def register_fonts():
    pdfmetrics.registerFont(TTFont("CN", "/System/Library/Fonts/STHeiti Light.ttc"))
    pdfmetrics.registerFont(TTFont("CN-Bold", "/System/Library/Fonts/STHeiti Medium.ttc"))


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(BLUE)
    canvas.rect(0, h - 4 * mm, w, 4 * mm, fill=1, stroke=0)
    canvas.setFont("CN", 7.5)
    canvas.setFillColor(colors.HexColor("#7B879A"))
    canvas.drawRightString(w - 15 * mm, 9 * mm, f"项思哲 · AI 应用开发工程师   {doc.page}")
    canvas.restoreState()


def styles(annotated=False):
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle("name", parent=base["Normal"], fontName="CN-Bold", fontSize=22, leading=25, textColor=INK),
        "target": ParagraphStyle("target", parent=base["Normal"], fontName="CN-Bold", fontSize=11.5, leading=15, textColor=colors.HexColor("#169B62") if annotated else BLUE),
        "contact": ParagraphStyle("contact", parent=base["Normal"], fontName="CN", fontSize=8.8, leading=12, textColor=MUTED),
        "section": ParagraphStyle("section", parent=base["Heading2"], fontName="CN-Bold", fontSize=11.5, leading=15, textColor=BLUE, spaceBefore=5, spaceAfter=4, borderColor=BLUE, borderWidth=0, borderPadding=0),
        "summary": ParagraphStyle("summary", parent=base["Normal"], fontName="CN", fontSize=8.9, leading=13.2, textColor=colors.HexColor("#169B62") if annotated else INK),
        "item": ParagraphStyle("item", parent=base["Normal"], fontName="CN", fontSize=8.6, leading=12.4, textColor=colors.HexColor("#D66A00") if annotated else INK, leftIndent=9, firstLineIndent=-7, bulletIndent=0, spaceAfter=2),
        "meta": ParagraphStyle("meta", parent=base["Normal"], fontName="CN", fontSize=8.2, leading=11.5, textColor=MUTED),
        "title": ParagraphStyle("title", parent=base["Normal"], fontName="CN-Bold", fontSize=9.7, leading=12.5, textColor=INK),
        "date": ParagraphStyle("date", parent=base["Normal"], fontName="CN", fontSize=8.3, leading=11.5, alignment=TA_RIGHT, textColor=MUTED),
        "small": ParagraphStyle("small", parent=base["Normal"], fontName="CN", fontSize=8.1, leading=11.2, textColor=INK),
        "changed": ParagraphStyle("changed", parent=base["Normal"], fontName="CN", fontSize=8.1, leading=11.2, textColor=colors.HexColor("#D66A00") if annotated else INK),
        "legend": ParagraphStyle("legend", parent=base["Normal"], fontName="CN", fontSize=7.6, leading=10, textColor=MUTED),
    }


def section(title, s):
    return [Spacer(1, 1.5 * mm), Paragraph(title, s["section"]), Table([[""]], colWidths=[180 * mm], rowHeights=[0.35 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), BLUE)]))]


def role_header(name, role, date, s):
    t = Table(
        [[Paragraph(name, s["title"]), Paragraph(date, s["date"])], [Paragraph(role, s["meta"]), ""]],
        colWidths=[130 * mm, 50 * mm],
    )
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    return t


def bullet(text, s):
    return Paragraph(f"• {text}", s["item"])


def project(name, role, date, intro, stack, bullets, s):
    parts = [role_header(name, role, date, s), Paragraph(intro, s["changed"]), Paragraph(f"<font color='#526078'>技术栈：</font>{stack}", s["meta"])]
    parts.extend(bullet(x, s) for x in bullets)
    parts.append(Spacer(1, 1.8 * mm))
    return KeepTogether(parts)


def build(output=OUTPUT, annotated=False):
    register_fonts()
    s = styles(annotated)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(str(output), pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=14 * mm, bottomMargin=14 * mm, title="项思哲 - AI应用开发工程师")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="resume", frames=[frame], onPage=header_footer)])

    story = [
        Paragraph("项思哲", s["name"]),
        Paragraph("AI 应用开发工程师｜RAG · Agent · Text-to-SQL", s["target"]),
        Paragraph("18757652156　｜　webfamer@163.com　｜　杭州　｜　7 年软件开发经验", s["contact"]),
    ]
    if annotated:
        story.append(Paragraph("标注说明：<font color='#169B62'>绿色 = 新增定位/概述</font>　　<font color='#D66A00'>橙色 = 重写、压缩或成果化表达</font>　　黑色 = 基本保留信息", s["legend"]))
    story += section("个人概述", s)
    story.append(Paragraph("近 7 年软件开发经验，具备从前端核心开发、Node.js 全栈到 Python AI 应用开发的完整经历。聚焦企业知识库、RAG 与 Text-to-SQL 场景，能够独立完成 Agent 工作流、混合检索、权限体系、流式交互及可视化结果展示。具备企业级 BI 和设备平台交付经验，曾支撑 400+ 设备接入，并将关键接口响应时间由十几秒降低至约 2 秒。", s["summary"]))

    story += section("核心能力", s)
    skills = [
        [Paragraph("<b>AI 应用</b>", s["small"]), Paragraph("企业知识库、RAG、Text-to-SQL、LangChain、LangGraph、混合检索、RRF、Rerank、工具调用", s["changed"])],
        [Paragraph("<b>后端开发</b>", s["small"]), Paragraph("Python、FastAPI、Node.js、NestJS、PostgreSQL、pgvector、Elasticsearch、Redis、MySQL、Qdrant", s["changed"])],
        [Paragraph("<b>前端开发</b>", s["small"]), Paragraph("React、Vue、TypeScript、Taro、BI 报表、复杂表格、数据可视化、AI 对话交互", s["changed"])],
        [Paragraph("<b>工程交付</b>", s["small"]), Paragraph("Docker、Nginx、Monorepo、Vite、Webpack、Storybook、JWT/RBAC、SSE、线上排障", s["changed"])],
    ]
    st = Table(skills, colWidths=[24 * mm, 156 * mm])
    st.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    story.append(st)

    story += section("重点项目", s)
    story.append(project(
        "企业知识库管理平台", "全栈开发", "2025.12 - 2026.04",
        "面向企业内部资料分散与检索效率低的问题，建设支持文档入库、权限检索、答案溯源和多轮问答的知识库平台。",
        "Python / FastAPI / PostgreSQL / pgvector / Elasticsearch / Redis / MinIO / LangChain / SSE",
        [
            "设计并落地文档入库流水线，串联文件存储、异步解析、文本清洗、分块、Embedding 生成及向量索引入库，形成可复用的知识入库流程。",
            "基于 pgvector 与 Elasticsearch 构建向量、关键词混合召回，引入 RRF 融合、Rerank 和标签过滤，改善单一检索方式在专业术语与语义问题上的召回偏差。",
            "交付带引用溯源的 RAG 问答能力，支持按知识库、用户权限和文档状态过滤，并返回来源文档、页码及原始 chunk，增强答案可核验性。",
            "基于 Redis 管理短期上下文与问答状态，持久化历史消息以支持多轮对话；通过 SSE 实时返回处理状态和生成内容。",
            "落地 RBAC 与 RAG 链路日志，记录召回、重排、生成和异常信息，为效果分析及线上排障提供依据。",
        ], s))
    story.append(project(
        "BI 智能问数 Agent", "全栈开发", "2025.09 - 2025.12",
        "面向 BI 自助分析场景，建设将中文问题转换为安全 SQL，并以表格、图表返回经营指标的智能问数工具。",
        "NestJS / LangChain / LangGraph / MySQL / Qdrant / Elasticsearch / React / SSE",
        [
            "建设 BI 元数据知识库，向量化存储表结构、字段别名与指标口径，并维护字段取值、枚举值和业务术语关键词索引。",
            "基于 LangChain 与 LangGraph 编排问题理解、元数据召回、SQL 生成、校验、错误修正及结果解释流程，形成可追踪的 Text-to-SQL 工作流。",
            "设计 SQL 安全机制，落实只读限制、表字段白名单、语法校验与错误修正，降低错误查询和高风险查询进入执行阶段的概率。",
            "交付 SSE 流式问数接口与 React 对话界面，实时展示处理阶段，并将查询结果以表格和图表形式呈现。",
        ], s))
    story.append(PageBreak())
    story.append(project(
        "BI 报表分析平台", "前端开发", "2025.04 - 2025.09",
        "面向业务数据分析与可视化场景的 BI 自定义报表平台，支持字段配置、拖拽报表、仪表盘、导出与分享。",
        "React / TypeScript / Monorepo / Recoil / Webpack / Storybook / VTable",
        [
            "参与报表查看、仪表盘、导出分享等核心链路开发，承担需求交付、接口联调和线上问题处理。",
            "基于 Storybook 和管道模式建设图表组件库，以 npm 包支持多个项目复用；基于 VTable 和适配器模式交付字段渲染、冻结列、列宽自适应及表格下钻。",
            "完成图片 CDN、骨架屏、组件异步加载和多区域部署改造，改善报表页面加载与跨区域访问体验。",
        ], s))
    story.append(project(
        "电力设备监测云平台", "全栈开发", "2024.10 - 2025.03",
        "面向电缆井设备监测场景的设备接入与管理平台，覆盖设备管理、报文解析、告警、权限、统计分析和驾驶舱展示。",
        "React / Umi / NestJS / MySQL / Redis / TCP",
        [
            "独立完成平台前后端设计与开发，交付设备、报文、告警、账号、角色与菜单等核心模块。",
            "设计 TCP 报文接入与解析链路，处理协议识别、拆包/粘包、原始报文落库和解析结果持久化。",
            "落地 JWT 认证和 RBAC 权限体系，实现不同角色的功能访问与操作隔离。",
            "优化核心接口与慢 SQL，将关键接口响应时间由十几秒降低至约 2 秒；平台支撑 400+ 设备接入，日均处理 1 万+ 条报文。",
        ], s))

    story += section("工作经历", s)
    jobs = [
        ("亿达信息技术有限公司", "前端 / 全栈开发", "2025.04 - 2026.04", "参与企业级 BI、企业知识库及智能问数场景建设，负责报表核心链路、RAG 检索问答、AI 对话交互、接口联调与线上问题处理。"),
        ("四川微矩阵科技有限公司", "全栈开发（远程）", "2024.10 - 2025.03", "负责电力设备监测云平台前后端交付，覆盖设备接入、TCP 报文解析、告警、权限、统计分析、部署及性能优化。"),
        ("杭州掌奇网络科技有限公司", "前端开发", "2022.06 - 2024.09", "参与可视化大屏、后台管理和移动端项目，负责核心模块、权限体系、业务框架及现场问题保障。"),
        ("杭州品茗安控信息技术股份有限公司", "前端开发 / 前端小组长", "2021.04 - 2022.06", "参与“桩桩”SaaS 系统开发，承担任务分配、需求评估、组件库建设及交付协调。"),
        ("浙江盘石信息技术股份有限公司", "前端开发", "2019.12 - 2021.03", "参与海外信贷业务平台、Flutter 应用、短信平台及 H5 活动页开发。"),
    ]
    for company, role, date, desc in jobs:
        story.append(KeepTogether([role_header(company, role, date, s), Paragraph(desc, s["changed"]), Spacer(1, 1.8 * mm)]))

    story += section("教育经历", s)
    story.append(role_header("太原科技大学", "物联网工程 · 本科 · 全日制", "2015.09 - 2019.06", s))
    doc.build(story)
    print(output)


if __name__ == "__main__":
    build(OUTPUT, annotated=False)
    build(ANNOTATED_OUTPUT, annotated=True)
