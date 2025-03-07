import os
import sys

# ✅ تأكد من دعم الترميز العربي
sys.stdout.reconfigure(encoding='utf-8')

# ✅ تحميل البيانات من `extracted_text.txt`
file_path = "extracted_text.txt"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ خطأ: لم يتم العثور على الملف '{file_path}'.")

with open(file_path, "r", encoding="utf-8") as f:
    data = f.read()

# ✅ تقسيم النصوص إلى أجزاء صغيرة لتحسين التدريب
chunks = data.split("\n\n")

# ✅ حفظ البيانات المعالجة في ملف جديد
with open("processed_data.txt", "w", encoding="utf-8") as f:
    f.write("\n---\n".join(chunks))

print("✅ تم تجهيز البيانات بنجاح!")
