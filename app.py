"""
Flask web application - University Academic Results Bot.
Run with: python app.py
"""
import os
import json
from flask import (
    Flask, render_template, request, redirect, url_for,
    jsonify, session, send_file, abort,
)
from io import BytesIO

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from analytics import calculate_statistics, analyze_performance
from ratings import get_grades_for_subjects
from recommendations import generate_recommendations, get_motivation_message
from alerts_system import generate_alerts, format_alerts
from charts import get_grades_chart_data, get_performance_pie_data, get_theoretical_practical_data
from reports import generate_pdf_report

# ---------------------------------------------------------------------------
# Demo data (used when Supabase is not configured)
# ---------------------------------------------------------------------------
DEMO_STUDENTS = [
    {
        "id": "1",
        "university_id": "2021001",
        "name": "أحمد محمد الخالدي",
        "subjects": [
            {"subject_name": "رياضيات متقطعة", "theoretical_score": 42, "practical_score": 18, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "برمجة 1", "theoretical_score": 45, "practical_score": 19, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "دوائر كهربائية", "theoretical_score": 38, "practical_score": 15, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "فيزياء هندسية", "theoretical_score": 44, "practical_score": 17, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "لغة عربية تقنية", "theoretical_score": 47, "practical_score": 20, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "منطق رقمي", "theoretical_score": 40, "practical_score": 16, "max_theoretical": 50, "max_practical": 20},
        ],
    },
    {
        "id": "2",
        "university_id": "2021002",
        "name": "سارة عبدالله النعيمي",
        "subjects": [
            {"subject_name": "رياضيات متقطعة", "theoretical_score": 23, "practical_score": 9, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "برمجة 1", "theoretical_score": 38, "practical_score": 14, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "دوائر كهربائية", "theoretical_score": 19, "practical_score": 7, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "فيزياء هندسية", "theoretical_score": 30, "practical_score": 11, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "لغة عربية تقنية", "theoretical_score": 44, "practical_score": 18, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "منطق رقمي", "theoretical_score": 28, "practical_score": 10, "max_theoretical": 50, "max_practical": 20},
        ],
    },
    {
        "id": "3",
        "university_id": "2021003",
        "name": "خالد عمر البلوشي",
        "subjects": [
            {"subject_name": "رياضيات متقطعة", "theoretical_score": 48, "practical_score": 20, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "برمجة 1", "theoretical_score": 50, "practical_score": 20, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "دوائر كهربائية", "theoretical_score": 46, "practical_score": 19, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "فيزياء هندسية", "theoretical_score": 49, "practical_score": 20, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "لغة عربية تقنية", "theoretical_score": 47, "practical_score": 20, "max_theoretical": 50, "max_practical": 20},
            {"subject_name": "منطق رقمي", "theoretical_score": 48, "practical_score": 19, "max_theoretical": 50, "max_practical": 20},
        ],
    },
]

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = Flask(__name__)
_secret = os.environ.get("SECRET_KEY", "")
if not _secret:
    import warnings
    warnings.warn(
        "SECRET_KEY is not set. Using an insecure default – set SECRET_KEY in production.",
        stacklevel=1,
    )
    _secret = "dev-only-insecure-key-set-SECRET_KEY-env-var"
app.secret_key = _secret

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)

_supabase_client = None


def get_supabase():
    global _supabase_client
    if _supabase_client is None and USE_SUPABASE:
        try:
            from supabase import create_client
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as exc:
            app.logger.error("Supabase init error: %s", exc)
    return _supabase_client


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------
def _parse_subjects(raw):
    """Ensure subjects field is a Python list."""
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (ValueError, TypeError):
            return []
    return []


def fetch_all_students():
    sb = get_supabase()
    if sb:
        try:
            resp = sb.table("students").select("*").execute()
            return resp.data or []
        except Exception as exc:
            app.logger.error("Supabase fetch error: %s", exc)
    return DEMO_STUDENTS


def fetch_student_by_id(student_id):
    sb = get_supabase()
    if sb:
        try:
            resp = sb.table("students").select("*").eq("id", student_id).execute()
            if resp.data:
                return resp.data[0]
        except Exception as exc:
            app.logger.error("Supabase fetch error: %s", exc)
    return next((s for s in DEMO_STUDENTS if str(s["id"]) == str(student_id)), None)


def search_students(query):
    sb = get_supabase()
    if sb:
        try:
            resp = (
                sb.table("students")
                .select("*")
                .or_(f"university_id.ilike.%{query}%,name.ilike.%{query}%")
                .execute()
            )
            return resp.data or []
        except Exception as exc:
            app.logger.error("Supabase search error: %s", exc)
    q = query.lower()
    return [
        s for s in DEMO_STUDENTS
        if q in s["name"].lower() or q in s["university_id"].lower()
    ]


def _build_student_context(student):
    """Build full context dict for a student."""
    subjects = _parse_subjects(student.get("subjects", []))
    stats = calculate_statistics(subjects)
    grades = get_grades_for_subjects(subjects)
    # Merge percentage/total into subject dicts for template use
    enriched = []
    for s, g in zip(subjects, grades):
        enriched.append({**s, **g})
    return {
        "student": student,
        "subjects": enriched,
        "stats": stats,
        "motivation": get_motivation_message(stats.get("pass_rate", 0)),
        "demo_mode": not USE_SUPABASE,
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", demo_mode=not USE_SUPABASE)


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").strip()
    if not query:
        return redirect(url_for("index"))

    # Track searches in session
    searches = session.get("recent_searches", [])
    if query not in searches:
        searches.insert(0, query)
        session["recent_searches"] = searches[:10]

    results = search_students(query)
    if len(results) == 1:
        return redirect(url_for("student_results", student_id=results[0]["id"]))

    return render_template(
        "index.html",
        search_results=results,
        query=query,
        demo_mode=not USE_SUPABASE,
    )


@app.route("/student/<student_id>")
def student_results(student_id):
    student = fetch_student_by_id(student_id)
    if not student:
        abort(404)
    ctx = _build_student_context(student)
    recs = generate_recommendations(ctx["stats"], _parse_subjects(student.get("subjects", [])))
    alerts = format_alerts(generate_alerts(ctx["stats"], _parse_subjects(student.get("subjects", []))))
    ctx.update({"recommendations": recs, "alerts": alerts})
    return render_template("results.html", **ctx)


@app.route("/api/statistics/<student_id>")
def api_statistics(student_id):
    student = fetch_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    subjects = _parse_subjects(student.get("subjects", []))
    stats = calculate_statistics(subjects)
    return jsonify(stats)


@app.route("/api/charts/<student_id>")
def api_charts(student_id):
    student = fetch_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    subjects = _parse_subjects(student.get("subjects", []))
    stats = calculate_statistics(subjects)
    return jsonify({
        "grades": get_grades_chart_data(subjects),
        "pie": get_performance_pie_data(stats),
        "comparison": get_theoretical_practical_data(subjects),
    })


@app.route("/api/ratings/<student_id>")
def api_ratings(student_id):
    student = fetch_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    subjects = _parse_subjects(student.get("subjects", []))
    return jsonify(get_grades_for_subjects(subjects))


@app.route("/api/recommendations/<student_id>")
def api_recommendations(student_id):
    student = fetch_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    subjects = _parse_subjects(student.get("subjects", []))
    stats = calculate_statistics(subjects)
    return jsonify({
        "recommendations": generate_recommendations(stats, subjects),
        "motivation": get_motivation_message(stats.get("pass_rate", 0)),
    })


@app.route("/api/alerts/<student_id>")
def api_alerts(student_id):
    student = fetch_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    subjects = _parse_subjects(student.get("subjects", []))
    stats = calculate_statistics(subjects)
    alerts = format_alerts(generate_alerts(stats, subjects))
    return jsonify(alerts)


@app.route("/export/pdf/<student_id>")
def export_pdf(student_id):
    student = fetch_student_by_id(student_id)
    if not student:
        abort(404)
    subjects = _parse_subjects(student.get("subjects", []))
    stats = calculate_statistics(subjects)
    pdf_bytes = generate_pdf_report(student, subjects, stats)
    filename = f"results_{student.get('university_id', student_id)}.pdf"
    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


@app.route("/admin")
def admin():
    import flask as _flask
    students = fetch_all_students()
    recent = session.get("recent_searches", [])
    total_subjects = sum(
        len(_parse_subjects(s.get("subjects", []))) for s in students
    )
    return render_template(
        "admin.html",
        students=students,
        recent_searches=recent,
        total_students=len(students),
        total_subjects=total_subjects,
        demo_mode=not USE_SUPABASE,
        supabase_url=SUPABASE_URL or "غير مُهيأ",
        flask_version=_flask.__version__,
    )


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html", error="الصفحة أو الطالب غير موجود.", demo_mode=not USE_SUPABASE), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, host="0.0.0.0", port=port)
