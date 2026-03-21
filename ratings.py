"""
Grade ratings module - converts numeric scores to letter grades.
"""


GRADE_SCALE = [
    (95, "A+", "ممتاز+", "#1a7a4a", "#d4edda"),
    (90, "A",  "ممتاز",  "#28a745", "#d4edda"),
    (85, "B+", "جيد جداً+", "#17a2b8", "#d1ecf1"),
    (80, "B",  "جيد جداً", "#20c997", "#d1ecf1"),
    (75, "C+", "جيد+",    "#ffc107", "#fff3cd"),
    (70, "C",  "جيد",     "#fd7e14", "#fff3cd"),
    (60, "D",  "مقبول",   "#e67e22", "#ffeaa7"),
    (50, "D-", "ضعيف",    "#dc3545", "#f8d7da"),
    (0,  "F",  "راسب",    "#721c24", "#f5c6cb"),
]


def get_rating(score, max_score=100):
    """Return grade dict for a given score."""
    if max_score == 0:
        percentage = 0
    else:
        percentage = (score / max_score) * 100

    for min_pct, letter, desc, color, bg in GRADE_SCALE:
        if percentage >= min_pct:
            return {
                "letter": letter,
                "description": desc,
                "color": color,
                "background": bg,
                "percentage": round(percentage, 2),
            }
    return {
        "letter": "F",
        "description": "راسب",
        "color": "#721c24",
        "background": "#f5c6cb",
        "percentage": round(percentage, 2),
    }


def format_grade_display(score, max_score):
    """Return formatted grade display dict."""
    rating = get_rating(score, max_score)
    total = score
    return {
        "score": total,
        "max": max_score,
        "percentage": rating["percentage"],
        "letter": rating["letter"],
        "description": rating["description"],
        "color": rating["color"],
        "background": rating["background"],
        "display": f"{total}/{max_score} ({rating['percentage']}%) - {rating['letter']}",
    }


def get_grades_for_subjects(subjects):
    """Return list of rating dicts for all subjects."""
    results = []
    for s in subjects:
        th = s.get("theoretical_score", 0) or 0
        pr = s.get("practical_score", 0) or 0
        mx_th = s.get("max_theoretical", 50) or 50
        mx_pr = s.get("max_practical", 50) or 50
        total = th + pr
        max_total = mx_th + mx_pr
        rating = get_rating(total, max_total)
        results.append({
            "subject_name": s.get("subject_name", ""),
            **rating,
            "total": total,
            "max_total": max_total,
        })
    return results
