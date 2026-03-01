# 📦 دليل التثبيت والتشغيل
# Installation and Running Guide

## المتطلبات | Requirements

### النظام | System
- **نظام التشغيل**: Windows, macOS, أو Linux
- **Python**: 3.8 أو أعلى
- **RAM**: 4GB على الأقل
- **مساحة التخزين**: 500MB

### البرامج المطلوبة | Required Software
- Python 3.8+
- pip (مدير الحزم)
- Git (اختياري)

---

## 🚀 خطوات التثبيت | Installation Steps

### الخطوة 1: تحميل المشروع | Download Project

#### الطريقة الأولى: استنساخ من GitHub
```bash
git clone https://github.com/your-username/digit_text_app.git
cd digit_text_app
```

#### الطريقة الثانية: تحميل الملفات يدويًا
- قم بتحميل جميع الملفات من المشروع
- ضعها في مجلد واحد (مثل `digit_text_app`)
- افتح Terminal/Command Prompt في هذا المجلد

### الخطوة 2: إنشاء بيئة افتراضية (اختياري لكن موصى به)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### الخطوة 3: تثبيت المكتبات المطلوبة
```bash
pip install -r requirements.txt
```

أو قم بتثبيت المكتبات يدويًا:
```bash
pip install streamlit numpy opencv-python Pillow scikit-learn matplotlib scipy pandas
```

### الخطوة 4: التحقق من التثبيت
```bash
python -c "import streamlit; import sklearn; print('✓ جميع المكتبات مثبتة بنجاح')"
```

---

## ▶️ تشغيل التطبيق | Running the Application

### تشغيل تطبيق Streamlit
```bash
streamlit run streamlit_app.py
```

**النتيجة المتوقعة**:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

سيفتح التطبيق تلقائيًا في متصفحك على `http://localhost:8501`

### تشغيل سكريبت الاختبار
```bash
python test_pipeline.py
```

### تشغيل Jupyter Notebook
```bash
jupyter notebook advanced_notebook.ipynb
```

---

## 🔧 استكشاف الأخطاء | Troubleshooting

### المشكلة: "ModuleNotFoundError: No module named 'streamlit'"

**الحل**:
```bash
pip install --upgrade streamlit
```

### المشكلة: "Permission denied" عند التثبيت

**الحل** (Linux/macOS):
```bash
pip install --user -r requirements.txt
```

أو استخدم `sudo`:
```bash
sudo pip install -r requirements.txt
```

### المشكلة: التطبيق بطيء جدًا

**الحل**:
1. تأكد من أن لديك ذاكرة كافية (RAM)
2. أغلق البرامج الأخرى
3. أعد تشغيل التطبيق

### المشكلة: خطأ في OpenCV

**الحل**:
```bash
pip install --upgrade opencv-python
```

### المشكلة: لا يمكن فتح المتصفح تلقائيًا

**الحل**:
- افتح المتصفح يدويًا
- انسخ الرابط من Terminal (عادة `http://localhost:8501`)
- الصقه في شريط العنوان

---

## 📝 الملفات الرئيسية | Main Files

| الملف | الوصف |
|------|-------|
| `streamlit_app.py` | التطبيق الرئيسي |
| `digit_recognition_notebook.py` | خط أنابيب التصنيف |
| `test_pipeline.py` | سكريبت الاختبار |
| `advanced_notebook.ipynb` | Jupyter Notebook |
| `requirements.txt` | المكتبات المطلوبة |
| `README.md` | دليل المشروع |
| `INSTALLATION.md` | هذا الملف |

---

## 🌐 الوصول إلى التطبيق | Accessing the Application

### محليًا | Locally
- **URL**: `http://localhost:8501`
- **يعمل على**: جهازك فقط

### عبر الشبكة | Over Network
- **URL**: `http://192.168.x.x:8501`
- **ملاحظة**: استبدل `192.168.x.x` بـ IP عنوان جهازك

### الحصول على IP عنوان جهازك

#### Windows
```bash
ipconfig
```

#### macOS/Linux
```bash
ifconfig
```

---

## 📊 اختبار التثبيت | Testing Installation

### اختبار سريع
```bash
python -c "
from digit_recognition_notebook import DigitRecognitionPipeline
pipeline = DigitRecognitionPipeline()
print('✓ تم استيراد المكتبة بنجاح')
"
```

### اختبار شامل
```bash
python test_pipeline.py
```

---

## 🔄 تحديث المكتبات | Updating Libraries

### تحديث جميع المكتبات
```bash
pip install --upgrade -r requirements.txt
```

### تحديث مكتبة محددة
```bash
pip install --upgrade streamlit
```

---

## 🗑️ إلغاء التثبيت | Uninstallation

### حذف البيئة الافتراضية
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### حذف المكتبات
```bash
pip uninstall -r requirements.txt -y
```

---

## 💡 نصائح مفيدة | Useful Tips

### 1. استخدام Virtual Environment
يوصى بشدة باستخدام بيئة افتراضية لتجنب تضارب المكتبات:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 2. حفظ المتطلبات
إذا أضفت مكتبات جديدة، قم بتحديث `requirements.txt`:
```bash
pip freeze > requirements.txt
```

### 3. استخدام Conda (بديل)
إذا كنت تستخدم Anaconda:
```bash
conda create -n digit_app python=3.10
conda activate digit_app
pip install -r requirements.txt
```

### 4. تشغيل في الخلفية
#### Linux/macOS
```bash
nohup streamlit run streamlit_app.py > app.log 2>&1 &
```

#### Windows
```bash
start streamlit run streamlit_app.py
```

---

## 📞 الدعم والمساعدة | Support and Help

### الأسئلة الشائعة | FAQ

**س: هل يمكنني تشغيل التطبيق على هاتفي؟**
ج: نعم، إذا كنت على نفس الشبكة، استخدم IP عنوان جهازك.

**س: كم وقت يستغرق تحميل النموذج؟**
ج: عادة 2-3 ثواني في المرة الأولى.

**س: هل يمكنني استخدام نموذج مخصص؟**
ج: نعم، يمكنك تعديل `digit_recognition_notebook.py`.

### الاتصال | Contact
- **البريد الإلكتروني**: [your-email@example.com]
- **GitHub Issues**: [your-repo-url/issues]

---

## 📚 مراجع إضافية | Additional References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Scikit-learn Guide](https://scikit-learn.org/stable/documentation.html)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

**آخر تحديث**: 2026
**الإصدار**: 1.0.0

**Last Updated**: 2026
**Version**: 1.0.0
