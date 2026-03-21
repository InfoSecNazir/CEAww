"""
Analytics module - calculates student performance statistics.
"""


def _subject_total(subj):
    th = subj.get("theoretical_score", 0) or 0
    pr = subj.get("practical_score", 0) or 0
    return th + pr


def _subject_max(subj):
    mx_th = subj.get("max_theoretical", 50) or 50
    mx_pr = subj.get("max_practical", 50) or 50
    return mx_th + mx_pr


def _subject_percentage(subj):
    total = _subject_total(subj)
    max_total = _subject_max(subj)
    if max_total == 0:
        return 0
    return round((total / max_total) * 100, 2)


def calculate_statistics(subjects):
    """Return aggregated statistics dict for a list of subjects."""
    if not subjects:
        return {
            "total_subjects": 0,
            "passed": 0,
            "failed": 0,
            "pass_rate": 0,
            "fail_rate": 0,
            "average": 0,
            "highest_score": 0,
            "lowest_score": 0,
            "performance_level": "غير متاح",
            "total_score": 0,
            "max_total_score": 0,
        }

    percentages = [_subject_percentage(s) for s in subjects]
    passed = sum(1 for p in percentages if p >= 50)
    failed = len(percentages) - passed
    total = len(percentages)

    avg = round(sum(percentages) / total, 2) if total else 0
    highest = round(max(percentages), 2) if percentages else 0
    lowest = round(min(percentages), 2) if percentages else 0
    pass_rate = round((passed / total) * 100, 2) if total else 0
    fail_rate = round((failed / total) * 100, 2) if total else 0

    total_score = sum(_subject_total(s) for s in subjects)
    max_total_score = sum(_subject_max(s) for s in subjects)

    if avg >= 90:
        level = "ممتاز"
    elif avg >= 80:
        level = "جيد جداً"
    elif avg >= 70:
        level = "جيد"
    elif avg >= 60:
        level = "مقبول"
    elif avg >= 50:
        level = "ضعيف"
    else:
        level = "راسب"

    return {
        "total_subjects": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "fail_rate": fail_rate,
        "average": avg,
        "highest_score": highest,
        "lowest_score": lowest,
        "performance_level": level,
        "total_score": total_score,
        "max_total_score": max_total_score,
    }


def analyze_performance(subjects):
    """Full performance analysis including subject-level data."""
    stats = calculate_statistics(subjects)
    enriched = []
    for s in subjects:
        pct = _subject_percentage(s)
        enriched.append({
            **s,
            "percentage": pct,
            "total": _subject_total(s),
            "max_total": _subject_max(s),
            "passed": pct >= 50,
        })
    return {
        "stats": stats,
        "subjects": enriched,
        "weak": get_weak_subjects(subjects),
        "strong": get_strong_subjects(subjects),
    }


def get_weak_subjects(subjects, threshold=50):
    """Return subjects with percentage below threshold."""
    return [
        {**s, "percentage": _subject_percentage(s)}
        for s in subjects
        if _subject_percentage(s) < threshold
    ]


def get_strong_subjects(subjects, threshold=75):
    """Return subjects with percentage at or above threshold."""
    return [
        {**s, "percentage": _subject_percentage(s)}
        for s in subjects
        if _subject_percentage(s) >= threshold
    ]
