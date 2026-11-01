# CEAww

[English](README.md) · [العربية](README_AR.md) · [فهرس الملفات](docs/INDEX_AR.md)

لوحة نتائج أكاديمية بـ Flask مع رسوم بيانية وتوصيات واتصال Supabase.

## المحتوى

- [app.py](app.py)
- [requirements.txt](requirements.txt)
- [templates](templates)
- [static](static)
- [.env.example](.env.example)

## الإعداد والاستخدام

أنشئ بيئة Python افتراضية وثبّت المتطلبات. انسخ `.env.example` إلى `.env` واضبط `SUPABASE_URL` و`SUPABASE_KEY` و`SECRET_KEY`.

```sh
python -m venv .venv
# فعّل البيئة الافتراضية حسب الصدفة المستخدمة.
python -m pip install -r requirements.txt
python app.py
```

منفذ التطوير الافتراضي 5000 ويمكن تغييره عبر `PORT`.

## الترخيص

لا يتضمن المستودع ملف ترخيص في الجذر حالياً. هذا التوثيق لا يضيف ترخيصاً جديداً.

## المساهمة والتنقل

[CONTRIBUTING.md](CONTRIBUTING.md) · [فهرس التوثيق](docs/INDEX_AR.md) · [فهرس المشاريع العامة](https://github.com/InfoSecNazir/InfoSecNazir/blob/main/PROJECTS_AR.md)

## نطاق التحقق

تمت مراجعة أسماء الملفات ومسارات التوثيق وملفات الحزم لتنظيم المستودع. لم يتم تشغيل التطبيق أو نشره ضمن هذا التحديث.
