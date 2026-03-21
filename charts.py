"""
Charts data module - prepares Chart.js-compatible datasets.
"""

from analytics import _subject_percentage, _subject_total, _subject_max


_GRADE_COLORS = {
    "A+": "#1a7a4a",
    "A":  "#28a745",
    "B+": "#17a2b8",
    "B":  "#20c997",
    "C+": "#ffc107",
    "C":  "#fd7e14",
    "D":  "#e67e22",
    "D-": "#dc3545",
    "F":  "#721c24",
}


def _letter_from_pct(pct):
    if pct >= 95: return "A+"
    if pct >= 90: return "A"
    if pct >= 85: return "B+"
    if pct >= 80: return "B"
    if pct >= 75: return "C+"
    if pct >= 70: return "C"
    if pct >= 60: return "D"
    if pct >= 50: return "D-"
    return "F"


def get_grades_chart_data(subjects):
    """Bar chart data: percentage per subject."""
    if not subjects:
        return {}
    labels = [s.get("subject_name", f"مادة {i+1}") for i, s in enumerate(subjects)]
    percentages = [_subject_percentage(s) for s in subjects]
    colors = [_GRADE_COLORS.get(_letter_from_pct(p), "#6c757d") for p in percentages]

    return {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "النسبة المئوية",
                "data": percentages,
                "backgroundColor": [c + "cc" for c in colors],
                "borderColor": colors,
                "borderWidth": 2,
                "borderRadius": 6,
            }],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "legend": {"display": False},
                "tooltip": {
                    "callbacks": {}
                },
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "max": 100,
                    "ticks": {"callback": "percent"},
                }
            },
        },
    }


def get_performance_pie_data(stats):
    """Pie/doughnut chart data: pass vs fail."""
    passed = stats.get("passed", 0)
    failed = stats.get("failed", 0)
    return {
        "type": "doughnut",
        "data": {
            "labels": ["ناجح", "راسب"],
            "datasets": [{
                "data": [passed, failed],
                "backgroundColor": ["#28a74580", "#dc354580"],
                "borderColor": ["#28a745", "#dc3545"],
                "borderWidth": 2,
            }],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "legend": {"position": "bottom"},
            },
        },
    }


def get_theoretical_practical_data(subjects):
    """Grouped bar chart: theoretical vs practical per subject."""
    if not subjects:
        return {}
    labels = [s.get("subject_name", f"مادة {i+1}") for i, s in enumerate(subjects)]

    th_pcts = []
    pr_pcts = []
    for s in subjects:
        th = s.get("theoretical_score", 0) or 0
        pr = s.get("practical_score", 0) or 0
        mx_th = s.get("max_theoretical", 50) or 50
        mx_pr = s.get("max_practical", 50) or 50
        th_pcts.append(round((th / mx_th) * 100, 2) if mx_th else 0)
        pr_pcts.append(round((pr / mx_pr) * 100, 2) if mx_pr else 0)

    return {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "النظري",
                    "data": th_pcts,
                    "backgroundColor": "#4361ee80",
                    "borderColor": "#4361ee",
                    "borderWidth": 2,
                    "borderRadius": 4,
                },
                {
                    "label": "العملي",
                    "data": pr_pcts,
                    "backgroundColor": "#f72585aa",
                    "borderColor": "#f72585",
                    "borderWidth": 2,
                    "borderRadius": 4,
                },
            ],
        },
        "options": {
            "responsive": True,
            "plugins": {
                "legend": {"position": "top"},
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "max": 100,
                },
            },
        },
    }
