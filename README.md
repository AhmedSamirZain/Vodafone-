# 📱 بوت فودافون - فحص الرصيد | Vodafone Balance Bot

بوت يخش على موقع فودافون الجديد `web.vodafone.com.eg` ويجيب الرصيد لكل أرقامك تلقائي.

## ✨ المميزات

- ✅ يفحص أي عدد أرقام فودافون (حتى 50 رقم - بيتظبط)
- 🔁 محاولات قابلة للتخصيص (موقع معلق / باسورد غلط / حساب معلق) - كلهم 10 افتراضي
- ⏹️ **إيقاف فوري**: زرار بيظهر تحت رسالة بداية الفحص، أو ابعت `/stop` أو `/cancel` في أي وقت
- 🈯 **رسايل أخطاء بالعربي المفهوم**: بدل `RemoteDisconnected` بيقولك بالظبط إيه اللي حصل وهل ده منك ولا من سيرفر فودافون
- 🔕 **وضع هادئ**: ملخص بس من غير تفاصيل كل رقم
- 🔄 **Fallback سيلينيوم**: لو الـ API فشل 3 مرات يحول للمتصفح تلقائياً
- ⏱️ مهلة API قابلة للضبط (10-60 ثانية)
- ⏩ انتقال بين الأرقام (10 ثواني افتراضي)
- ⏰ فحص تلقائي كل ساعة و 20 دقيقة (80 دقيقة) - تقدر تغيره
- 📊 تفاصيل كل محاولة + رسالة الموقع (الباسورد غلط / معلق / نجح والرصيد كذا)
- 💬 يشتغل على تليجرام **و** على Streamlit

## 🚀 التشغيل على Streamlit Cloud (من GitHub)

### 1. ارفع على GitHub
```bash
git init
git add .
git commit -m "Vodafone bot ready"
git branch -M main
git remote add origin https://github.com/USERNAME/vodafone-bot.git
git push -u origin main
```

### 2. شغل على Streamlit
1. ادخل https://share.streamlit.io
2. دوس **New app**
3. اختار الريبو `vodafone-bot` والملف `streamlit_app.py`
4. دوس **Deploy** - هيشتغل في دقيقة!

> ملاحظة: `packages.txt` فيه `chromium` عشان السيلينيوم يشتغل على Streamlit Cloud

### 3. التشغيل المحلي
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
هيفتح على http://localhost:8501

## 🤖 بوت تليجرام

```bash
# 1. كلم @BotFather وخد التوكن
# 2. حطه في vodafone_telegram_bot.py فوق في BOT_TOKEN
# 3. أو حطه في Secrets على السيرفر باسم BOT_TOKEN

pip install -r requirements.txt
python vodafone_telegram_bot.py
```

أوامر تليجرام:
- `/start` - القائمة الرئيسية
- `➕ إضافة رقم` -> `01022683237:Samir@123`
- `💰 فحص الكل` - يفحصهم واحد واحد
- `⚙️ الإعدادات` - تغير كل حاجة

## ⚙️ الإعدادات (مشروحة في أول الملف)

| الإعداد | الديفولت | الشرح |
|---------|----------|-------|
| `MAX_RETRIES` | 3 | محاولات الموقع المعلق |
| `MAX_RETRIES_WRONG_PASSWORD` | 1 | محاولات الباسورد الغلط (مرة واحدة بس) |
| `MAX_RETRIES_ACCOUNT_LOCKED` | 1 | محاولات الحساب المعلق |
| `RETRY_DELAY_SECONDS` | 5 | انتظار بين المحاولات |
| `DELAY_BETWEEN_NUMBERS` | 1 | انتقال بين الأرقام |
| `AUTO_CHECK_INTERVAL_MINUTES` | 80 | ساعة و 20 دقيقة |
| `VODAFONE_URL` | web.vodafone.com.eg | رابط فودافون الحقيقي (Keycloak) |

كلهم فوق في أول الملف مع شرح سطر سطر لو غيرت 2 لـ 3 ده بتاع ايه.

## 📁 الملفات

- `streamlit_app.py` - واجهة Streamlit (للـ Web)
- `vodafone_telegram_bot.py` - بوت تليجرام (1300 سطر مشروح)
- `vodafone_bot.py` - بوت عادي بدون تليجرام
- `requirements.txt` - المكتبات
- `packages.txt` - حزم كروم لـ Streamlit Cloud
- `.streamlit/config.toml` - ألوان وثيم

## 🔗 الروابط

- موقع فودافون: https://web.vodafone.com.eg
- صفحة الدخول: https://web.vodafone.com.eg/auth/realms/vf-realm/...

## ⚠️ تنبيه

- متشاركش باسوردك مع حد
- البوت ليك انت بس (حط ADMIN_IDS لو عايزه خاص)
- فودافون ممكن تطلب كابتشا/OTP ساعات

© 2026 Arena AI
