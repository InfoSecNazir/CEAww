"""
Smart recommendations module - generates personalised academic advice.
"""

from analytics import get_weak_subjects, get_strong_subjects


def generate_recommendations(stats, subjects):
    """Return a list of recommendation dicts based on student performance."""
    recs = []
    avg = stats.get("average", 0)
    pass_rate = stats.get("pass_rate", 0)
    weak = get_weak_subjects(subjects)
    strong = get_strong_subjects(subjects)

    # Overall performance recommendations
    if avg >= 90:
        recs.append({
            "type": "success",
            "icon": "🏆",
            "title": "أداء استثنائي",
            "body": "تحافظ على مستوى أكاديمي متميز جداً. فكر في المشاركة في المسابقات العلمية أو الأبحاث.",
        })
    elif avg >= 75:
        recs.append({
            "type": "info",
            "icon": "⭐",
            "title": "أداء جيد",
            "body": "مستواك جيد. ارفع سقف تطلعاتك واستهدف التميز في المواد التي تحبها.",
        })
    elif avg >= 60:
        recs.append({
            "type": "warning",
            "icon": "📚",
            "title": "يحتاج تحسين",
            "body": "مستواك مقبول لكن يمكنك تحقيق أكثر. خصص وقتاً إضافياً للمراجعة اليومية.",
        })
    else:
        recs.append({
            "type": "danger",
            "icon": "🚨",
            "title": "يحتاج جهداً مكثفاً",
            "body": "مستواك يحتاج تحسيناً عاجلاً. تواصل مع أساتذتك واطلب الدعم الأكاديمي فوراً.",
        })

    # Weak subjects
    if weak:
        names = "، ".join(s["subject_name"] for s in weak[:3])
        recs.append({
            "type": "warning",
            "icon": "⚠️",
            "title": "مواد تحتاج اهتماماً",
            "body": f"ركّز على تحسين أدائك في: {names}. خصص ساعات مراجعة منتظمة لهذه المواد.",
        })

    # Strong subjects
    if strong:
        names = "، ".join(s["subject_name"] for s in strong[:3])
        recs.append({
            "type": "success",
            "icon": "💪",
            "title": "مواد متميزة",
            "body": f"تتألق في: {names}. استثمر هذا التميز لمساعدة زملائك وتعزيز ثقتك بنفسك.",
        })

    # Pass rate recommendations
    if pass_rate < 50:
        recs.append({
            "type": "danger",
            "icon": "📋",
            "title": "خطة دراسية عاجلة",
            "body": "نسبة النجاح منخفضة. ضع جدولاً دراسياً منظماً وتواصل مع مرشدك الأكاديمي.",
        })
    elif pass_rate < 75:
        recs.append({
            "type": "warning",
            "icon": "📅",
            "title": "تنظيم الوقت",
            "body": "حسّن توزيع وقتك بين المواد المختلفة لرفع معدل نجاحك الكلي.",
        })

    # Study habits
    recs.append({
        "type": "info",
        "icon": "💡",
        "title": "نصيحة دراسية",
        "body": "المراجعة المنتظمة (30 دقيقة يومياً لكل مادة) أفضل من الدراسة المكثفة قبل الامتحانات.",
    })

    return recs


def get_motivation_message(pass_rate):
    """Return a motivational message based on pass rate."""
    if pass_rate >= 90:
        return "رائع! أنت من أفضل الطلاب. استمر في هذا التميز! 🌟"
    elif pass_rate >= 75:
        return "أداء جيد! بقليل من الجهد الإضافي ستصل إلى القمة. 💪"
    elif pass_rate >= 50:
        return "أنت على الطريق الصحيح. لا تستسلم واستمر في المحاولة! 📚"
    else:
        return "لا تيأس! كل خبير كان مبتدئاً. ابدأ بخطوة صغيرة كل يوم. 🌱"
