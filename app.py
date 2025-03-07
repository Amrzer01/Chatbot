from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import difflib  # للبحث الذكي في البيانات

# ✅ إعداد مفتاح API
GENAI_API_KEY = "AIzaSyC8BMJTqamEK9cHB-rvtxwJ-wfbvA5eeGs"  # ضع مفتاح API هنا
genai.configure(api_key=GENAI_API_KEY)

# ✅ تحديد نموذج Gemini المناسب
MODEL_NAME = "gemini-1.5-flash-latest"
model = genai.GenerativeModel(MODEL_NAME)

# ✅ تحديد مسار ملف البيانات
file_path = "extracted_text.txt"

# ✅ التأكد من أن الملف موجود
if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ خطأ: لم يتم العثور على الملف '{file_path}'. تأكد من وضع البيانات في المسار الصحيح.")

# ✅ تحميل البيانات من الملف النصي
with open(file_path, "r", encoding="utf-8") as f:
    university_data = f.read().split("\n")  # تقسيم البيانات إلى أسطر لسهولة البحث

# ✅ تشغيل Flask
app = Flask(__name__, template_folder="templates")

# ✅ ردود جاهزة للأسئلة الشائعة والتحيات
custom_responses = {
    "من صنعك": "👨‍💻 لقد تم إنشائي بواسطة البشمهندس عمرو خالد!",
    "من هو مبرمجك": "💡 تم تطويري بواسطة البشمهندس عمرو خالد!",
    "شكرا": "💖 العفو! أنا هنا دائمًا للمساعدة 😊",
}

friendly_responses = {
    "هلا": "هلا فيك! 😍 كيف أقدر أساعدك اليوم؟",
    "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته! 🌸 كيف حالك؟",
    "مرحبا": "أهلًا وسهلًا! 🤗 كيف يمكنني مساعدتك؟",
}

# ✅ البحث الذكي في بيانات الجامعة باستخدام `difflib`
def search_university_data(query):
    best_match = difflib.get_close_matches(query, university_data, n=1, cutoff=0.4)  # تحسين البحث
    return best_match[0] if best_match else None

# ✅ عرض الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("index.html")

# ✅ نقطة API لمعالجة استفسارات الشات بوت
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip().lower()

    if not user_message:
        return jsonify({"response": "❌ من فضلك أدخل سؤالًا واضحًا 😊."})

    # ✅ التحقق من الردود الجاهزة
    if user_message in custom_responses:
        return jsonify({"response": custom_responses[user_message]})

    # ✅ التحقق من التحيات
    if user_message in friendly_responses:
        return jsonify({"response": friendly_responses[user_message]})

    # ✅ البحث الذكي في بيانات الجامعة
    answer_from_data = search_university_data(user_message)
    if answer_from_data:
        return jsonify({"response": f"📌 {answer_from_data}"})

    # ✅ طلب Gemini API إذا لم يتم العثور على إجابة في البيانات
    prompt = f"""
    لديك هذه المعلومات فقط عن الجامعة:
    {' '.join(university_data[:50])}  # إرسال أول 50 سطر فقط لتوفير الموارد

    أجب عن السؤال التالي بناءً على هذه المعلومات فقط:
    {user_message}

    إذا لم تجد إجابة واضحة، أخبر المستخدم بلطف أنه يستطيع البحث في موقع الجامعة الرسمي.
    """

    response = model.generate_content(prompt)
    answer = response.text.strip() if response.text else "🤔 لم أجد معلومات دقيقة، يمكنك التحقق من موقع الجامعة الرسمي."

    return jsonify({"response": answer})

# ✅ تشغيل التطبيق
if __name__ == "__main__":
    app.run(debug=True)
