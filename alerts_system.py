"""
Alerts system - generates contextual academic alerts.
"""

from analytics import get_weak_subjects


def generate_alerts(stats, subjects):
    """Return list of alert dicts based on student statistics."""
    alerts = []
    avg = stats.get("average", 0)
    failed = stats.get("failed", 0)
    pass_rate = stats.get("pass_rate", 0)
    highest = stats.get("highest_score", 0)
    lowest = stats.get("lowest_score", 0)
    weak = get_weak_subjects(subjects)

    # Critical alerts
    if failed > 0:
        subj_word = "مادة" if failed == 1 else "مواد"
        alerts.append({
            "type": "critical",
            "icon": "🔴",
            "title": "تحذير: رسوب في مواد",
            "message": f"لديك {failed} {subj_word} راسبة. يجب معالجة هذا الأمر بشكل عاجل.",
            "priority": 1,
        })

    if avg < 50:
        alerts.append({
            "type": "critical",
            "icon": "🚨",
            "title": "المعدل العام منخفض جداً",
            "message": f"معدلك العام {avg}% وهو دون حد النجاح. تواصل مع الإرشاد الأكاديمي فوراً.",
            "priority": 1,
        })

    # Warning alerts
    if 50 <= avg < 60:
        alerts.append({
            "type": "warning",
            "icon": "⚠️",
            "title": "المعدل يحتاج تحسيناً",
            "message": f"معدلك {avg}% قريب من حد الخطر. ركّز على رفع درجاتك.",
            "priority": 2,
        })

    if len(weak) >= 3:
        alerts.append({
            "type": "warning",
            "icon": "📉",
            "title": "عدة مواد ضعيفة",
            "message": f"لديك {len(weak)} مواد بأداء ضعيف. ضع خطة دراسية لمعالجتها.",
            "priority": 2,
        })

    if (highest - lowest) > 40 and len(subjects) > 2:
        alerts.append({
            "type": "warning",
            "icon": "📊",
            "title": "تفاوت كبير في الدرجات",
            "message": "هناك فجوة كبيرة بين أعلى وأدنى درجاتك. حاول تحقيق توازن في أدائك.",
            "priority": 2,
        })

    # Info alerts
    if pass_rate == 100:
        alerts.append({
            "type": "success",
            "icon": "✅",
            "title": "نجاح في جميع المواد",
            "message": "تهانينا! لقد نجحت في جميع المواد المسجلة.",
            "priority": 3,
        })

    if avg >= 85:
        alerts.append({
            "type": "success",
            "icon": "🏅",
            "title": "مستوى متميز",
            "message": f"معدلك {avg}% يضعك في مصاف المتفوقين. استمر!",
            "priority": 3,
        })

    if not alerts:
        alerts.append({
            "type": "info",
            "icon": "ℹ️",
            "title": "لا توجد تنبيهات",
            "message": "لا توجد تنبيهات مهمة حالياً. استمر في مسيرتك الأكاديمية.",
            "priority": 4,
        })

    alerts.sort(key=lambda a: a["priority"])
    return alerts


def format_alerts(alerts):
    """Map internal type names to Bootstrap alert classes."""
    type_map = {
        "critical": "danger",
        "warning": "warning",
        "info": "info",
        "success": "success",
    }
    return [
        {**a, "bs_class": type_map.get(a["type"], "secondary")}
        for a in alerts
    ]
