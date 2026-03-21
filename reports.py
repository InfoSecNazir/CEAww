"""
PDF report generation module using ReportLab.
Falls back to plain-text if ReportLab is unavailable.
"""
from io import BytesIO


def _try_reportlab():
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        return True
    except ImportError:
        return False


def generate_pdf_report(student, subjects, stats):
    """
    Generate a PDF report for the student.
    Returns bytes of the PDF, or falls back to text bytes.
    """
    if not _try_reportlab():
        return generate_text_report(student, subjects, stats).encode("utf-8")

    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm

    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=18,
        spaceAfter=12,
        alignment=1,
    )
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=13,
        spaceAfter=8,
        spaceBefore=12,
    )
    normal_style = styles["Normal"]

    story = []

    # Title
    story.append(Paragraph("University Academic Results Report", title_style))
    story.append(Spacer(1, 0.4 * cm))

    # Student info
    story.append(Paragraph("Student Information", heading_style))
    info_data = [
        ["Name:", student.get("name", "-")],
        ["University ID:", student.get("university_id", "-")],
        ["Performance Level:", stats.get("performance_level", "-")],
        ["Average:", f"{stats.get('average', 0)}%"],
    ]
    info_table = Table(info_data, colWidths=[5 * cm, 11 * cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#4361ee")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [colors.HexColor("#f8f9fa"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e6")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.4 * cm))

    # Statistics
    story.append(Paragraph("Statistics", heading_style))
    stat_data = [
        ["Total Subjects", "Passed", "Failed", "Pass Rate", "Average"],
        [
            str(stats.get("total_subjects", 0)),
            str(stats.get("passed", 0)),
            str(stats.get("failed", 0)),
            f"{stats.get('pass_rate', 0)}%",
            f"{stats.get('average', 0)}%",
        ],
    ]
    stat_table = Table(stat_data, colWidths=[3.2 * cm] * 5)
    stat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4361ee")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e6")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(stat_table)
    story.append(Spacer(1, 0.4 * cm))

    # Subjects table
    story.append(Paragraph("Subject Results", heading_style))
    subj_header = ["Subject", "Theoretical", "Practical", "Total", "Max", "%"]
    subj_rows = [subj_header]
    for s in subjects:
        th = s.get("theoretical_score", 0) or 0
        pr = s.get("practical_score", 0) or 0
        mx_th = s.get("max_theoretical", 50) or 50
        mx_pr = s.get("max_practical", 50) or 50
        total = th + pr
        mx = mx_th + mx_pr
        pct = round((total / mx) * 100, 1) if mx else 0
        subj_rows.append([
            s.get("subject_name", "-"),
            f"{th}/{mx_th}",
            f"{pr}/{mx_pr}",
            str(total),
            str(mx),
            f"{pct}%",
        ])

    col_w = [6 * cm, 2.5 * cm, 2.5 * cm, 2 * cm, 2 * cm, 2 * cm]
    subj_table = Table(subj_rows, colWidths=col_w)
    subj_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4361ee")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e6")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8f9fa"), colors.white]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(subj_table)

    doc.build(story)
    buf.seek(0)
    return buf.read()


def generate_text_report(student, subjects, stats):
    """Plain-text fallback report."""
    lines = [
        "=" * 60,
        "       تقرير النتائج الأكاديمية الجامعية",
        "=" * 60,
        f"الاسم: {student.get('name', '-')}",
        f"الرقم الجامعي: {student.get('university_id', '-')}",
        f"مستوى الأداء: {stats.get('performance_level', '-')}",
        f"المعدل العام: {stats.get('average', 0)}%",
        "",
        "--- الإحصائيات ---",
        f"إجمالي المواد: {stats.get('total_subjects', 0)}",
        f"المواد الناجحة: {stats.get('passed', 0)}",
        f"المواد الراسبة: {stats.get('failed', 0)}",
        f"نسبة النجاح: {stats.get('pass_rate', 0)}%",
        "",
        "--- نتائج المواد ---",
    ]
    for s in subjects:
        th = s.get("theoretical_score", 0) or 0
        pr = s.get("practical_score", 0) or 0
        mx_th = s.get("max_theoretical", 50) or 50
        mx_pr = s.get("max_practical", 50) or 50
        total = th + pr
        mx = mx_th + mx_pr
        pct = round((total / mx) * 100, 1) if mx else 0
        lines.append(f"  {s.get('subject_name', '-')}: {total}/{mx} ({pct}%)")

    lines += ["", "=" * 60]
    return "\n".join(lines)
