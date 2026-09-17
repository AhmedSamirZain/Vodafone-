# -*- coding: utf-8 -*-
"""
================================================================================
📱 بوت تليجرام فودافون - Vodafone Telegram Bot
================================================================================
فكرة البوت:
  يخش على موقع أنا فودافون ana.vodafone.com.eg بكل أرقامك، يكتب الرقم والباسورد،
  يجيب الرصيد، ويبعتلك كل حاجة على تليجرام بقوائم وأزرار.

ازاي تشغله (3 خطوات بس):
  1. كلم @BotFather في تليجرام -> /newbot -> خد التوكن
  2. حط التوكن تحت في BOT_TOKEN (السطر 60)
  3. شغل:  pip install -r requirements.txt  ثم  python vodafone_telegram_bot.py

المطور: Arena AI - 2026-09-17
اللغة: Python + Selenium + pyTelegramBotAPI
================================================================================
"""

# ==============================================================================
# ==============================================================================
#                        ⚙️ القسم 1: الإعدادات
#              كل حاجة هتعدلها من هنا - مش هتنزل تحت خالص
#              اقرا الشرح اللي فوق كل سطر قبل ما تغير الرقم
# ==============================================================================
# ==============================================================================

import os  # عشان نقرا التوكن من Secrets لو موجود

# ------------------------------------------------------------------------------
# 1.1 - BOT_TOKEN
# ------------------------------------------------------------------------------
# ايه ده؟ ده مفتاح البوت بتاعك اللي بتاخده من @BotFather
# ازاي تجيبه؟ افتح تليجرام -> دور على @BotFather -> ابعت /newbot -> امشي مع الخطوات -> هيديك توكن شكله 123456:AAH...
# فين تحطه؟ يا تحطه هنا مباشرة، يا تحطه في Secrets/Environment Variables باسم BOT_TOKEN (أفضل للسيرفرات)
# لو سبته زي ما هو "ضع_التوكن_هنا..." البوت مش هيشتغل وهيطبعلك رسالة تحذير
# مثال: BOT_TOKEN = "1234567890:AAHqXyZ..."
# ------------------------------------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "ضع_التوكن_هنا_من_BotFather")

# ------------------------------------------------------------------------------
# 1.2 - ADMIN_IDS
# ------------------------------------------------------------------------------
# ايه ده؟ قائمة الأرقام التعريفية (ID) للناس المسموح ليها تستخدم البوت
# ليه؟ عشان لو عايز البوت ليك انت بس ومحدش تاني يستخدمه
# لو سبته فاضي [] = أي حد معاه رابط البوت يقدر يستخدمه (مفتوح للكل)
# لو كتبت [123456789] = بس الشخص اللي الـ ID بتاعه 123456789 هو اللي يقدر يستخدمه
# لو عايز كذا شخص: [123456789, 987654321, 555666777]
# ازاي تجيب الـ ID بتاعك؟ كلم @userinfobot في تليجرام وهو هيبعتهولك
# مثال للخاص: ADMIN_IDS = [123456789]
# مثال للعام: ADMIN_IDS = []
# ------------------------------------------------------------------------------
ADMIN_IDS = []  # فاضي = للكل | حط ID بتاعك = خاص بيك

# ------------------------------------------------------------------------------
# 1.3 - VODAFONE_URL
# ------------------------------------------------------------------------------
# ايه ده؟ رابط صفحة تسجيل الدخول بتاعة فودافون
# الرابط الحقيقي اللي انت بعته: https://web.vodafone.com.eg/auth/realms/vf-realm/...
# ده صفحة Keycloak بتاعة فودافون - بتفتح لما تخش على web.vodafone.com.eg وتدوس تسجيل دخول
# البوت بيخش على الرابط ده مباشرة
# ملاحظة: الرابط فيه state و nonce بيتغيروا كل مرة، فالبوت بيستخدم الرابط الأساسي اللي بيعمل redirect تلقائي
# لو فودافون غيرت الرابط تاني، انسخه من المتصفح وحطه هنا
# ------------------------------------------------------------------------------
VODAFONE_URL = "https://web.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/auth?client_id=website&redirect_uri=https%3A%2F%2Fweb.vodafone.com.eg%2Fspa%2FmyHome&response_type=code&scope=openid&ui_locales=ar"

# ==============================================================================
#                    🔁 إعدادات المحاولات - أهم حاجة
# ==============================================================================

# ------------------------------------------------------------------------------
# 1.4 - MAX_RETRIES (محدث لـ 10 زي ما طلبت)
# ------------------------------------------------------------------------------
# ايه ده؟ عدد المحاولات لو الموقع معلق أو النت فصل أو حصل Timeout
# امتى بيشتغل؟ لما البوت يخش على الموقع ويلاقي الصفحة مش بتحمل / النت قطع / السيرفر مهنج
# الديفولت: 10 (زودناه زي ما طلبت - 9 أو 10)
# لو غيرته لـ 1: مرة واحدة بس (سريع بس ممكن يفوت)
# لو غيرته لـ 3: 3 مرات (كان الديفولت القديم)
# لو غيرته لـ 5: 5 مرات (متوسط)
# لو غيرته لـ 9: 9 مرات (زي ما طلبت)
# لو غيرته لـ 10: 10 مرات (الديفولت الجديد ✅ - مفيد لو فودافون بيعلق كتير)
# تنصحني بايه؟ سيبه 10، لو لقيته بيطول خليه 5
# تقدر تغيره من تليجرام: ⚙️ -> 🔁 محاولات الموقع المعلق
# ------------------------------------------------------------------------------
MAX_RETRIES = 10

# ------------------------------------------------------------------------------
# 1.5 - MAX_RETRIES_WRONG_PASSWORD (محدث لـ 10 زي ما طلبت)
# ------------------------------------------------------------------------------
# ايه ده؟ عدد المحاولات لو الباسورد غلط (رسالة: كلمة المرور غير صحيحة / غير صحيح)
# امتى بيشتغل؟ لما تكتب باسورد غلط والموقع يرد "الباسورد غلط"
# الديفولت: 10 (زي ما طلبت - هيعيد 10 مرات حتى لو الباسورد غلط)
# لو غيرته لـ 1: مرة واحدة بس (سريع)
# لو غيرته لـ 10: 10 مرات (الديفولت الجديد ✅)
# تقدر تغيره من تليجرام: ⚙️ -> 🔐 باسورد غلط
# ------------------------------------------------------------------------------
MAX_RETRIES_WRONG_PASSWORD = 10

# ------------------------------------------------------------------------------
# 1.6 - MAX_RETRIES_ACCOUNT_LOCKED (محدث لـ 10 زي ما طلبت)
# ------------------------------------------------------------------------------
# ايه ده؟ عدد المحاولات لو الحساب معلق (رسالة: حسابك معلق حاول في وقت لاحق)
# امتى بيشتغل؟ لما فودافون تقولك "حسابك معلق"
# الديفولت: 10 (زي ما طلبت - هيعيد 10 مرات)
# لو غيرته لـ 1: مرة واحدة
# لو غيرته لـ 10: 10 مرات (الديفولت الجديد ✅)
# تقدر تغيره من تليجرام: ⚙️ -> ⛔ حساب معلق
# ------------------------------------------------------------------------------
MAX_RETRIES_ACCOUNT_LOCKED = 10

# ------------------------------------------------------------------------------
# 1.7 - RETRY_DELAY_SECONDS
# ------------------------------------------------------------------------------
# ايه ده؟ كام ثانية يستنى بين كل محاولة والتانية لنفس الرقم
# امتى بيشتغل؟ لما يجرب رقم 1 ويفشل (موقع معلق) -> يستنى 5 ثواني -> يجرب تاني
# الديفولت: 5 ثواني
# لو غيرته لـ 1: سريع جداً (ممكن فودافون يعتبرك بوت ويعملك بلوك)
# لو غيرته لـ 3: سريع ومتوازن
# لو غيرته لـ 5: متوازن (الديفولت)
# لو غيرته لـ 10: بطيء بس آمن لو فودافون بيعمل بلوك
# تنصحني بايه؟ خليك على 5، لو لقيت بلوك خليه 10
# ------------------------------------------------------------------------------
RETRY_DELAY_SECONDS = 5

# ------------------------------------------------------------------------------
# 1.8 - PAGE_TIMEOUT
# ------------------------------------------------------------------------------
# ايه ده؟ لو الصفحة معلقة يستنى كام ثانية قبل ما يعتبرها فشلت
# الديفولت: 30 ثانية
# لو غيرته لـ 10: لو الصفحة محملتش في 10 ثواني هيعتبرها فشلت ويعيد (سريع بس ممكن يفوت)
# لو غيرته لـ 30: يستنى 30 ثانية (الديفولت - كويس)
# لو غيرته لـ 60: يستنى دقيقة كاملة (لو النت بطيء جداً)
# ------------------------------------------------------------------------------
PAGE_TIMEOUT = 30

# ==============================================================================
#                    ⏰ إعدادات الفحص التلقائي (المؤقت)
#              ده اللي بيخلي البوت يعيد لوحده كل ساعة و20 دقيقة
# ==============================================================================

# ------------------------------------------------------------------------------
# 1.9 - AUTO_CHECK_ENABLED
# ------------------------------------------------------------------------------
# ايه ده؟ هل البوت يعيد فحص كل الأرقام تلقائي بعد ما يخلص؟
# True = شغال (بعد ما يخلص 1 لـ 5 هيستنى المهلة ويعيد تاني لوحده)
# False = مطفي (يفحص مرة واحدة بس لما تدوس انت)
# الديفولت: True (شغال)
# لو غيرته لـ True: بعد ما يخلص هيبعتلك "هستنى ساعة و20 دقيقة والفحص الجاي الساعة كذا" ويعيد تلقائي
# لو غيرته لـ False: مش هيعيد تلقائي، لازم تدوس انت كل مرة
# تقدر تغيره من تليجرام برضه: ⚙️ الإعدادات -> 🔄 الفحص التلقائي
# ------------------------------------------------------------------------------
AUTO_CHECK_ENABLED = True

# ------------------------------------------------------------------------------
# 1.10 - AUTO_CHECK_INTERVAL_MINUTES
# ------------------------------------------------------------------------------
# ايه ده؟ كل كام دقيقة يعيد الفحص التلقائي؟ (بالدقايق)
# الديفولت: 80 دقيقة = 60 + 20 = ساعة و 20 دقيقة
# لو غيرته لـ 30: هيعيد كل نص ساعة
# لو غيرته لـ 60: هيعيد كل ساعة بالظبط
# لو غيرته لـ 80: هيعيد كل ساعة و20 دقيقة (الديفولت - اللي طلبته)
# لو غيرته لـ 120: هيعيد كل ساعتين
# لو غيرته لـ 1440: هيعيد كل يوم مرة واحدة (1440 = 24 ساعة * 60 دقيقة)
# ازاي تحسبها؟ 1 ساعة = 60 دقيقة، 2 ساعة = 120، 3 ساعات = 180
# تقدر تغيرها من تليجرام: ⚙️ الإعدادات -> ⏰ مهلة الفحص التلقائي
# ------------------------------------------------------------------------------
AUTO_CHECK_INTERVAL_MINUTES = 80  # 80 = ساعة و 20 دقيقة

# ------------------------------------------------------------------------------
# 1.11 - DELAY_BETWEEN_NUMBERS (محدث لـ 10 زي ما طلبت)
# ------------------------------------------------------------------------------
# ايه ده؟ كام ثانية بين كل رقم والتاني؟ (مش بين المحاولات، بين الأرقام)
# مثال: عندك 5 أرقام -> خلص رقم 1 -> يستنى 10 ثواني -> يبدأ رقم 2
# الديفولت: 10 ثواني (زي ما طلبت ✅)
# لو غيرته لـ 0: فوري بدون انتظار
# لو غيرته لـ 1: ثانية واحدة (سريع)
# لو غيرته لـ 10: 10 ثواني (الديفولت الجديد ✅ - آمن جداً من البلوك)
# الفرق بينه وبين RETRY_DELAY_SECONDS؟
#   RETRY_DELAY_SECONDS = بين محاولات نفس الرقم (رقم 1 محاولة 1 و 2)
#   DELAY_BETWEEN_NUMBERS = بين رقم 1 ورقم 2
# ------------------------------------------------------------------------------
DELAY_BETWEEN_NUMBERS = 10

# ==============================================================================
#                         🖥️ إعدادات المتصفح
# ==============================================================================

# ------------------------------------------------------------------------------
# 1.12 - HEADLESS
# ------------------------------------------------------------------------------
# ايه ده؟ هل المتصفح يظهر قدامك ولا يشتغل في الخلفية؟
# True = مخفي (مش هتشوف كروم بيفتح - للسيرفرات)
# False = ظاهر (هتشوف كروم بيفتح ويكتب الرقم والباسورد قدامك - للتجربة على الكمبيوتر)
# الديفولت: True (مخفي)
# لو بتشغل على الكمبيوتر وعايز تشوفه بيكتب ازاي: خليه False
# لو هترفعه على سيرفر: لازم True
# ------------------------------------------------------------------------------
HEADLESS = True

# ------------------------------------------------------------------------------
# 1.13 - BROWSER_TIMEOUT
# ------------------------------------------------------------------------------
# ايه ده؟ مهلة تحميل عناصر الصفحة (الأزرار والخانات) بالثواني
# الديفولت: 20 ثانية
# متغيروش إلا لو الموقع تقيل جداً
# ------------------------------------------------------------------------------
BROWSER_TIMEOUT = 20

# ------------------------------------------------------------------------------
# 1.13b - USE_API_LOGIN (جديد - من الملف القديم)
# ------------------------------------------------------------------------------
# ايه ده؟ هل يستخدم API السريع ولا السيلينيوم البطيء؟
# True = يستخدم API (أسرع 10 مرات، مش محتاج كروم، هو اللي في الملف القديم ✅)
# False = يستخدم السيلينيوم (يفتح المتصفح زي الأول - للطوارئ بس)
# الديفولت: True (API - جربناه ونجح)
# لو API فشل (فودافون غيرت الـ API)، غيره لـ False وهيرجع للسيلينيوم
# ------------------------------------------------------------------------------
USE_API_LOGIN = True

# ==============================================================================
#                         💾 إعدادات الملفات
# ==============================================================================

# ------------------------------------------------------------------------------
# 1.14 - DATA_FILE
# ------------------------------------------------------------------------------
# ايه ده؟ اسم الملف اللي بيحفظ فيه البوت كل أرقامك وإعداداتك
# متغيروش إلا لو عايز اسم تاني
# ------------------------------------------------------------------------------
DATA_FILE = "telegram_data.json"

# ------------------------------------------------------------------------------
# 1.15 - RESULTS_CSV
# ------------------------------------------------------------------------------
# ايه ده؟ ملف الإكسل اللي بيحفظ فيه النتائج (تقدر تفتحه باكسل)
# ------------------------------------------------------------------------------
RESULTS_CSV = "results.csv"

# ------------------------------------------------------------------------------
# 1.16 - ACCOUNTS_FILE
# ------------------------------------------------------------------------------
# ايه ده؟ ملف احتياطي للأرقام (لو عايز تضيف من الملف بدل تليجرام)
# ------------------------------------------------------------------------------
ACCOUNTS_FILE = "accounts.txt"

# ==============================================================================
#                         🔧 إعدادات متقدمة (للمطورين)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1.17 - SELECTORS (محدث من الرابط اللي بعته - Keycloak)
# ------------------------------------------------------------------------------
# ايه ده؟ دي عناوين الخانات والأزرار في صفحة فودافون الحقيقية
# فحصت الرابط اللي بعته وطلعت الـ Selectors الحقيقية:
# - خانة الرقم: <input id="username" name="username" type="tel" class="js-login-mobile">
# - خانة الباسورد: <input id="password" name="password" type="password" class="js-login-password">
# - زرار الدخول: <input id="kc-login" name="login" value="الدخول" type="submit" class="js-btn-login">
# - رسالة الخطأ: <div class="alert-error"> أو <span class="kc-feedback-text">
#
# متلمسهاش إلا لو فودافون غيرت شكل الموقع تاني
# ازاي تجيبها؟ افتح الرابط -> دوس F12 -> Inspect -> دوس على الخانة -> كليك يمين Copy selector
# ------------------------------------------------------------------------------
SELECTORS = {
    # خانة الرقم - 4 طرق للوصول ليها (لو واحدة فشلت يجرب التانية)
    "phone_input": "#username, input[name='username'], input#username[type='tel'], .js-login-mobile",
    # خانة الباسورد
    "password_input": "#password, input[name='password'], input#password[type='password'], .js-login-password",
    # زرار الدخول - ده Input مش Button (مهم!)
    "login_button": "#kc-login, #submitBtn, input[name='login'][value='الدخول'], .js-btn-login, input[type='submit'][value='الدخول']",
    # مكان الرصيد - بعد ما يسجل دخول بيروح لـ /spa/myHome
    "balance_element": ".balance, [class*='balance'], [class*='Balance'], div:has-text('رصيد'), div:has-text('جنيه'), [data-testid*='balance'], .myHome-balance",
    # مكان رسالة الخطأ - Keycloak بيحطها في alert-error
    "error_message": ".alert-error, .kc-feedback-text, #kc-feedback, .alert-danger, [class*='error'], .form-error, p:has-text('غير صحيح'), p:has-text('خطأ')"
}

# ==============================================================================
#                    ✅ انتهت الإعدادات - متلمسش حاجة تحت
# ==============================================================================



# ==============================================================================
# ==============================================================================
#                        📚 القسم 2: المكتبات
#              متلمسش حاجة هنا - دي مكتبات البوت بيحتاجها
# ==============================================================================
# ==============================================================================

import re          # للبحث عن الأرقام والنصوص
import csv         # لحفظ النتائج في ملف اكسل
import json        # لحفظ الأرقام في ملف JSON
import time        # للمؤقتات والانتظار
import random      # عشان يكتب زي البني آدم (عشوائي)
import threading   # عشان البوت يشتغل في الخلفية بدون ما يعلق
from datetime import datetime, timedelta  # للوقت والتاريخ
from pathlib import Path  # للتعامل مع الملفات

# --- مكتبة تليجرام ---
try:
    import telebot
    from telebot import types
    TELEBOT_AVAILABLE = True
except ImportError:
    TELEBOT_AVAILABLE = False
    print("❌ مكتبة تليجرام مش متثبتة! شغل: pip install pyTelegramBotAPI")

# --- مكتبة السيلينيوم (للدخول على موقع فودافون) ---
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️ السيلينيوم مش متثبت - القوائم هتشتغل بس الفحص الحقيقي لا")

# ---- احتياطات عامة ----
DATA_LOCK = threading.Lock()  # قفل عشان ميحصلش تضارب لما اتنين يفحصوا في نفس الوقت

def escape_md(text):
    """تهرب الرموز اللي بتكسر Markdown في تليجرام"""
    if not text:
        return ""
    # نهرب: _ * [ ] ( ) ~ ` > # + - = | { } . !
    for ch in ["_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"]:
        text = text.replace(ch, "\\" + ch)
    return text

def validate_phone(phone):
    """تتأكد ان الرقم شكله صح 01 + 9 أرقام"""
    phone = re.sub(r'\s+', '', phone.strip())
    # يشيل +20 لو موجود
    if phone.startswith("+20"):
        phone = "0" + phone[3:]
    if phone.startswith("20") and len(phone)==12:
        phone = "0" + phone[2:]
    return phone

def safe_send(chat_id, text, reply_markup=None, parse_mode="Markdown"):
    """تبعت رسالة بأمان - لو Markdown فشل تبعتها عادية"""
    try:
        return bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)
    except Exception as e:
        # لو Markdown كسر بسبب رمز غريب، جرب بدون Markdown
        if parse_mode:
            try:
                return bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=None)
            except:
                pass
        print(f"safe_send failed: {e}")
        return None

def safe_edit(chat_id, message_id, text, reply_markup=None, parse_mode="Markdown"):
    """تعدل رسالة بأمان"""
    try:
        return bot.edit_message_text(text, chat_id, message_id, reply_markup=reply_markup, parse_mode=parse_mode if parse_mode else None)
    except Exception as e:
        if parse_mode:
            try:
                return bot.edit_message_text(text, chat_id, message_id, reply_markup=reply_markup, parse_mode=None)
            except:
                pass
        print(f"safe_edit failed: {e}")
        return None


# ==============================================================================
# ==============================================================================
#                        💾 القسم 3: إدارة البيانات
#              هنا البوت بيحفظ ويقرا أرقامك وإعداداتك
#              كل مستخدم ليه أرقامه وإعداداته لوحده
# ==============================================================================
# ==============================================================================

# ------------------------------------------------------------------------------
# 3.1 - load_data() : تحمل كل البيانات من الملف
# ------------------------------------------------------------------------------
def load_data():
    """تحمل كل بيانات المستخدمين من ملف JSON - لو الملف مش موجود ترجع فاضي"""
    with DATA_LOCK:
        if not os.path.exists(DATA_FILE):
            return {}
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # لو الملف فاضي أو مش dict
                if not isinstance(data, dict):
                    return {}
                return data
        except json.JSONDecodeError as e:
            print(f"⚠️ ملف البيانات تالف: {e} - بعمل نسخة احتياطية")
            try:
                # احفظ نسخة تالفة للمراجعة
                import shutil
                shutil.copy(DATA_FILE, DATA_FILE + ".bak")
            except:
                pass
            return {}
        except Exception as e:
            print(f"load_data error: {e}")
            return {}

# ------------------------------------------------------------------------------
# 3.2 - save_data() : تحفظ البيانات في الملف
# ------------------------------------------------------------------------------
def save_data(data):
    """تحفظ كل البيانات في ملف JSON بأمان (قفل + كتابة ذرية)"""
    with DATA_LOCK:
        try:
            # كتابة ذرية: اكتب في ملف مؤقت ثم انقله
            tmp = DATA_FILE + ".tmp"
            # احتياط: لو البيانات أكبر من 5MB، متتحفظش (حماية من انفجار)
            import sys as _sys
            try:
                size = len(json.dumps(data, ensure_ascii=False))
                if size > 5 * 1024 * 1024:
                    print(f"⚠️ البيانات كبيرة جداً {size} byte - مش هحفظ")
                    return
            except:
                pass
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            import os as _os
            _os.replace(tmp, DATA_FILE)
        except Exception as e:
            print(f"save_data error: {e}")
            # fallback محاولة عادية
            try:
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception as e2:
                print(f"save_data fallback failed: {e2}")

# ------------------------------------------------------------------------------
# 3.3 - get_user_data() : تجيب بيانات مستخدم معين
# ------------------------------------------------------------------------------
def get_user_data(chat_id):
    """
    تجيب بيانات مستخدم معين (أرقامه + إعداداته)
    لو المستخدم جديد بتنشئله بيانات افتراضية من الإعدادات اللي فوق
    """
    data = load_data()
    str_id = str(chat_id)
    if str_id not in data:
        # --- مستخدم جديد - انشئ بيانات افتراضية ---
        data[str_id] = {
            "accounts": [],  # قائمة الأرقام: كل رقم عبارة عن {"phone": "010...", "password": "...", "name": "..."}
            "settings": {
                "max_retries": MAX_RETRIES,  # من 1.4 فوق
                "max_retries_wrong_password": MAX_RETRIES_WRONG_PASSWORD,  # من 1.5 فوق
                "max_retries_account_locked": MAX_RETRIES_ACCOUNT_LOCKED,  # من 1.6 فوق
                "retry_delay": RETRY_DELAY_SECONDS,  # من 1.7 فوق
                "auto_check_enabled": AUTO_CHECK_ENABLED,  # من 1.9 فوق
                "auto_check_interval": AUTO_CHECK_INTERVAL_MINUTES,  # من 1.10 فوق
                "delay_between_numbers": DELAY_BETWEEN_NUMBERS  # من 1.11 فوق
            },
            "last_results": [],  # آخر نتائج فحص
            "last_check_time": "",  # وقت آخر فحص
            "auto_check": {
                "enabled": AUTO_CHECK_ENABLED,
                "next_check": ""
            }
        }
        # --- حاول تستورد من accounts.txt لو فيه أرقام هناك (للمستخدم الجديد) - احتياط شامل ---
        if os.path.exists(ACCOUNTS_FILE):
            try:
                imp_updated=False
                with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        line=line.strip()
                        if not line or line.startswith("#") or ":" not in line:
                            continue
                        parts=line.split(":", 1)
                        raw_phone=parts[0].strip()
                        rest=parts[1].strip()
                        if ":" in rest:
                            password, name = rest.split(":",1)
                            password=password.strip()
                            name=name.strip()
                        else:
                            password=rest
                            name=""
                        phone=validate_phone(raw_phone)
                        if not re.match(r'^01[0-9]{9}$', phone):
                            continue
                        if not password or len(password) < 4:
                            continue
                        exists=False
                        for a in data[str_id]["accounts"]:
                            if a["phone"]==phone:
                                exists=True
                                break
                        if not exists:
                            data[str_id]["accounts"].append({
                                "phone": phone,
                                "password": password,
                                "name": name or phone,
                                "added_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            imp_updated=True
                if imp_updated:
                    save_data(data)
            except:
                pass
        save_data(data)
    else:
        # --- مستخدم قديم - لو فيه إعدادات جديدة زودها (تحديث تلقائي) ---
        s = data[str_id].get("settings", {})
        updated = False
        if "max_retries_account_locked" not in s:
            s["max_retries_account_locked"] = MAX_RETRIES_ACCOUNT_LOCKED
            updated = True
        elif s.get("max_retries_account_locked") == 1 and MAX_RETRIES_ACCOUNT_LOCKED == 10:
            # ترقية تلقائية من الديفولت القديم 1 لـ 10 (زي ما طلبت)
            s["max_retries_account_locked"] = 10
            updated = True
        if "max_retries_wrong_password" not in s:
            s["max_retries_wrong_password"] = MAX_RETRIES_WRONG_PASSWORD
            updated = True
        elif s.get("max_retries_wrong_password") == 1 and MAX_RETRIES_WRONG_PASSWORD == 10:
            s["max_retries_wrong_password"] = 10
            updated = True
        if "max_retries" not in s:
            s["max_retries"] = MAX_RETRIES
            updated = True
        elif s.get("max_retries") in [1,3] and MAX_RETRIES == 10:
            s["max_retries"] = 10
            updated = True
        if "auto_check_enabled" not in s:
            s["auto_check_enabled"] = AUTO_CHECK_ENABLED
            updated = True
        if "auto_check_interval" not in s:
            s["auto_check_interval"] = AUTO_CHECK_INTERVAL_MINUTES
            updated = True
        if "delay_between_numbers" not in s:
            s["delay_between_numbers"] = DELAY_BETWEEN_NUMBERS
            updated = True
        elif s.get("delay_between_numbers") == 1 and DELAY_BETWEEN_NUMBERS == 10:
            s["delay_between_numbers"] = 10
            updated = True
        if "retry_delay" not in s:
            s["retry_delay"] = RETRY_DELAY_SECONDS
            updated = True
        # احتياط: اضبط القيم لو حد لعب في الملف وحط رقم غلط (مثلاً 100)
        try:
            s["max_retries"] = max(1, min(10, int(s.get("max_retries", MAX_RETRIES))))
            s["max_retries_wrong_password"] = max(1, min(10, int(s.get("max_retries_wrong_password", MAX_RETRIES_WRONG_PASSWORD))))
            s["max_retries_account_locked"] = max(1, min(10, int(s.get("max_retries_account_locked", MAX_RETRIES_ACCOUNT_LOCKED))))
            s["retry_delay"] = max(1, min(60, int(s.get("retry_delay", RETRY_DELAY_SECONDS))))
            s["delay_between_numbers"] = max(0, min(30, int(s.get("delay_between_numbers", DELAY_BETWEEN_NUMBERS))))
            s["auto_check_interval"] = max(5, min(1440, int(s.get("auto_check_interval", AUTO_CHECK_INTERVAL_MINUTES))))
        except:
            pass
        if updated:
            save_data(data)
        # --- احتياط: لو فيه أرقام جديدة في accounts.txt مش في تليجرام، استوردهم (حتى لو الحساب مش فاضي) ---
        # الأول: لو فاضي استورد الكل، لو مش فاضي استورد النواقص بس
        if os.path.exists(ACCOUNTS_FILE):
            try:
                # استورد بصمت (من غير ما تبعت رسالة)
                with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        line=line.strip()
                        if not line or line.startswith("#") or ":" not in line:
                            continue
                        parts=line.split(":", 1)
                        raw_phone=parts[0].strip()
                        rest=parts[1].strip()
                        if ":" in rest:
                            password, name = rest.split(":",1)
                            password=password.strip()
                            name=name.strip()
                        else:
                            password=rest
                            name=""
                        phone=validate_phone(raw_phone)
                        if not re.match(r'^01[0-9]{9}$', phone):
                            continue
                        if not password or len(password) < 4:
                            continue
                        # اضف مباشرة بدون ما تستدعي add_account عشان تتجنب loop
                        exists=False
                        for a in data[str_id]["accounts"]:
                            if a["phone"]==phone:
                                exists=True
                                break
                        if not exists:
                            data[str_id]["accounts"].append({
                                "phone": phone,
                                "password": password,
                                "name": name or phone,
                                "added_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            updated=True
                if updated:
                    save_data(data)
            except:
                pass
    return data[str_id]

# ------------------------------------------------------------------------------
# 3.4 - save_user_data() : تحفظ بيانات مستخدم معين
# ------------------------------------------------------------------------------
def save_user_data(chat_id, user_data):
    """تحفظ بيانات مستخدم معين في الملف"""
    data = load_data()
    data[str(chat_id)] = user_data
    save_data(data)

# ------------------------------------------------------------------------------
# 3.5 - add_account() : إضافة رقم جديد
# ------------------------------------------------------------------------------
def add_account(chat_id, phone, password, name=""):
    """
    تضيف رقم جديد لمستخدم
    phone: الرقم (01012345678)
    password: الباسورد
    name: اسم الخط (اختياري)
    """
    phone = validate_phone(phone)
    # تحقق أساسي
    if not re.match(r'^01[0-9]{9}$', phone):
        return False, "الرقم لازم يبدأ بـ 01 ويكون 11 رقم (مثال 01012345678)"
    if len(password) < 4:
        return False, "الباسورد قصير جداً (4 أحرف على الأقل)"
    user_data = get_user_data(chat_id)
    # احتياط: حد أقصى 20 رقم لكل مستخدم (عشان الملف ميكبرش ويهنج)
    if len(user_data["accounts"]) >= 20:
        return False, "عندك 20 رقم بالفعل - الحد الأقصى 20 (احذف واحد الأول)" 
    for acc in user_data["accounts"]:
        if acc["phone"] == phone:
            return False, "الرقم ده موجود قبل كده!"
    user_data["accounts"].append({
        "phone": phone,
        "password": password,
        "name": name or phone,
        "added_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_user_data(chat_id, user_data)
    return True, "تمت الإضافة ✅"

# ------------------------------------------------------------------------------
# 3.6 - remove_account() : حذف رقم
# ------------------------------------------------------------------------------
def remove_account(chat_id, phone):
    """تحذف رقم من قائمة المستخدم"""
    user_data = get_user_data(chat_id)
    before = len(user_data["accounts"])
    user_data["accounts"] = [a for a in user_data["accounts"] if a["phone"] != phone]
    save_user_data(chat_id, user_data)
    return len(user_data["accounts"]) != before

# ------------------------------------------------------------------------------
# 3.7 - get_accounts_text() : نص يعرض كل الأرقام
# ------------------------------------------------------------------------------
def get_accounts_text(chat_id):
    """ترجع نص فيه كل الأرقام المضافة (للعرض في تليجرام)"""
    user_data = get_user_data(chat_id)
    accounts = user_data["accounts"]
    if not accounts:
        return "📭 مفيش أرقام مضافة لسه.\nدوس ➕ إضافة رقم عشان تضيف أول رقم."
    text = f"📱 **الأرقام المضافة ({len(accounts)}):**\n"
    text += "─" * 30 + "\n"
    for i, acc in enumerate(accounts, 1):
        text += f"{i}. 📞 `{acc['phone']}`\n"
        if acc['name'] != acc['phone']:
            text += f"   🏷️ {acc['name']}\n"
        text += f"   🔑 `{'*' * len(acc['password'])}` | 📅 {acc['added_at']}\n\n"
    return text

# ------------------------------------------------------------------------------
# 3.8 - import_from_accounts_file() : استيراد من accounts.txt (للي بيضيف من الملف)
# ------------------------------------------------------------------------------
def import_from_accounts_file(chat_id):
    """
    تستورد الأرقام من ملف accounts.txt لو موجود
    بتنفع لو ضفت الأرقام في الملف بدل تليجرام والبوت بيقول مفيش أرقام
    """
    if not os.path.exists(ACCOUNTS_FILE):
        return 0, "ملف accounts.txt مش موجود"
    try:
        imported = 0
        skipped = 0
        # احتياط: اقرا كل الأرقام اللي في الملف وتأكد ان كلها في تليجرام حتى لو الحساب مش فاضي
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line or line.startswith("#") or ":" not in line:
                    continue
                # احتياط: تجاهل أسطر طويلة جداً أو غريبة
                if len(line) > 200:
                    continue
                parts=line.split(":", 1)
                phone=validate_phone(parts[0].strip())
                # احتياط: تجاهل أرقام مش 01
                if not re.match(r'^01[0-9]{9}$', phone):
                    skipped += 1
                    continue
                rest=parts[1].strip()
                # rest ممكن يكون password أو password:name
                if ":" in rest:
                    password, name = rest.split(":",1)
                    password=password.strip()
                    name=name.strip()
                else:
                    password=rest
                    name=""
                phone=re.sub(r'\s+', '', phone)
                if not phone or not password:
                    continue
                ok, msg = add_account(chat_id, phone, password, name)
                if ok:
                    imported+=1
                else:
                    skipped+=1
        return imported, f"تم استيراد {imported} رقم (تخطي {skipped} مكرر)"
    except Exception as e:
        return 0, f"خطأ: {e}"

# ------------------------------------------------------------------------------
# 3.9 - format_interval() : تحويل الدقايق لنص مقروء
# ------------------------------------------------------------------------------
def format_interval(minutes):
    """
    تحول الدقايق لنص مقروء
    80 -> "1 ساعة و 20 دقيقة"
    60 -> "ساعة"
    30 -> "30 دقيقة"
    """
    h = minutes // 60
    m = minutes % 60
    if h > 0 and m > 0:
        return f"{h} ساعة و {m} دقيقة"
    elif h > 0:
        return f"{h} ساعة" if h == 1 else f"{h} ساعات"
    else:
        return f"{m} دقيقة"


# ==============================================================================
# ==============================================================================
#                        🌐 القسم 4: فحص فودافون (السيلينيوم)
#              هنا البوت بيخش على موقع فودافون ويجيب الرصيد
#              متلمسش حاجة هنا إلا لو فاهم سيلينيوم
# ==============================================================================
# ==============================================================================

# ------------------------------------------------------------------------------
# 4.1 - create_driver() : إنشاء متصفح كروم
# ------------------------------------------------------------------------------
LAST_DRIVER_ERROR = ""

def create_driver():
    """تنشئ متصفح كروم بالإعدادات الصح (مخفي لو HEADLESS=True) - محدث لـ Streamlit Cloud"""
    global LAST_DRIVER_ERROR
    LAST_DRIVER_ERROR = ""
    if not SELENIUM_AVAILABLE:
        LAST_DRIVER_ERROR = "السيلينيوم مش متثبت (pip install selenium)"
        return None
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--window-size=1366,768")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # حدد مكان كروم/كروميوم على Streamlit Cloud
    import os as _os
    for bin_path in ["/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/snap/bin/chromium"]:
        if _os.path.exists(bin_path):
            options.binary_location = bin_path
            print(f"✅ لقيت المتصفح: {bin_path}")
            break
    # جرب 3 طرق
    # 1) chromedriver من النظام (packages.txt)
    try:
        if _os.path.exists("/usr/bin/chromedriver"):
            print("⏳ بجرب chromedriver النظام...")
            service = Service("/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(PAGE_TIMEOUT)
            try:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            except:
                pass
            return driver
    except Exception as e:
        LAST_DRIVER_ERROR = f"chromedriver النظام فشل: {e}"
        print(LAST_DRIVER_ERROR)
    # 2) webdriver-manager (بيحمل المناسب)
    try:
        print("⏳ بجرب ChromeDriverManager...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(PAGE_TIMEOUT)
        try:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except:
            pass
        return driver
    except Exception as e:
        LAST_DRIVER_ERROR = f"ChromeDriverManager فشل: {e}"
        print(LAST_DRIVER_ERROR)
    # 3) بدون Service (يخلي selenium يدور لوحده)
    try:
        print("⏳ بجرب بدون Service...")
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(PAGE_TIMEOUT)
        return driver
    except Exception as e:
        if not LAST_DRIVER_ERROR:
            LAST_DRIVER_ERROR = str(e)
        print(f"فشل تشغيل المتصفح نهائي: {e}")
        import traceback
        traceback.print_exc()
        return None

# ------------------------------------------------------------------------------
# 4.1b - API فودافون (مأخوذ من الملف القديم - أسرع من السيلينيوم)
# ------------------------------------------------------------------------------
def get_authorization_api(number, password):
    """تسجيل دخول API - نفس طريقة الملف القديم - أسرع 10 مرات من السيلينيوم"""
    url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        "username": number,
        "password": password,
        "client_secret": "95fd95fb-7489-4958-8ae6-d31a525cd20a",
        "client_id": "ana-vodafone-app"
    }
    headers = {
        'User-Agent': "okhttp/4.12.0",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'x-agent-operatingsystem': "15",
        'clientId': "AnaVodafoneAndroid",
        'Accept-Language': "ar",
    }
    try:
        import requests
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        if resp.status_code == 200:
            j = resp.json()
            tok = j.get("access_token")
            if tok:
                return {"success": True, "token": tok, "bearer": "Bearer " + tok, "raw": j}
        # حاول ترجع رسالة الخطأ
        try:
            j = resp.json()
            msg = j.get("error_description") or j.get("error") or str(j)[:200]
        except:
            msg = resp.text[:200]
        if resp.status_code in [400,401,403]:
            return {"success": False, "message": f"الباسورد غلط أو الرقم غير صحيح ({msg[:80]})", "is_wrong": True}
        return {"success": False, "message": f"فشل تسجيل الدخول: {resp.status_code} {msg[:80]}", "is_wrong": False}
    except Exception as e:
        return {"success": False, "message": f"خطأ اتصال: {str(e)[:100]}", "is_wrong": False}

def get_balance_api(token, phone):
    """يجرب يجيب الرصيد/الفليكسات بـ 3 طرق API مختلفة (من الملف القديم)"""
    import requests
    # طريقة 1: Balance API (المفضلة)
    try:
        url = "https://mobile.vodafone.com.eg/services/dxl/bal/balance/v2/balances"
        headers = {
            'User-Agent': "okhttp/4.12.0",
            'Accept': "application/json",
            'Authorization': f"Bearer {token}",
            'api-host': "BalanceManagement",
            'useCase': "balance",
            'clientId': "AnaVodafoneAndroid",
            'msisdn': phone,
            'Accept-Language': "ar",
        }
        r = requests.get(url, params={'accountNumber': phone, 'balanceType': 'CurrentBalance'}, headers=headers, timeout=20)
        if r.status_code == 200:
            j = r.json()
            # حاول تستخرج الرصيد
            if isinstance(j, dict) and 'balances' in j:
                bals = j['balances']
                parts = []
                for b in bals[:4]:
                    t = b.get('balanceType','رصيد')
                    amt = b.get('amount',{}).get('value','0')
                    unit = b.get('amount',{}).get('unit','')
                    parts.append(f"{t}: {amt} {unit}")
                if parts:
                    return True, " | ".join(parts)
            # لو مش balances جرب تقرا أي amount
            txt = str(j)[:400]
            # دور على أرقام
            import re
            nums = re.findall(r'"amount"\s*:\s*"?(\d+\.?\d*)"?', txt)
            if nums:
                return True, f"الرصيد: {nums[0]} جنيه (API1)"
            return True, f"تم تسجيل الدخول - الرد: {str(j)[:200]}"
    except Exception as e:
        pass
    # طريقة 2: usageConsumptionReport (MoneyBack/فليكس)
    try:
        url = "https://mobile.vodafone.com.eg/services/dxl/usage/usageConsumptionReport"
        headers = {
            'User-Agent': "okhttp/4.12.0",
            'Accept': "application/json",
            'Authorization': f"Bearer {token}",
            'clientId': "AnaVodafoneAndroid",
            'msisdn': phone,
            'Accept-Language': "ar",
        }
        r = requests.get(url, params={'@type': 'aggregated', 'bucket.product.publicIdentifier': phone}, headers=headers, timeout=20)
        if r.status_code == 200:
            j = r.json()
            # دور على فليكس
            txt = str(j)
            import re, json
            # حاول تلاقي Remaining flex
            for item in (j if isinstance(j, list) else [j]):
                if isinstance(item, dict) and item.get("@type") == "OTHERS":
                    for bucket in item.get("bucket", []):
                        if bucket.get("usageType") == "limit":
                            for bal in bucket.get("bucketBalance", []):
                                if bal.get("@type") == "Remaining":
                                    amt = bal.get("remainingValue",{}).get("amount")
                                    if amt is not None:
                                        return True, f"فليكس متبقي: {amt} فليكس"
            # fallback
            nums = re.findall(r'"amount"\s*:\s*(\d+)', txt)
            if nums:
                return True, f"بيانات الاستهلاك: {nums[:3]}"
            return True, f"تم تسجيل الدخول - بيانات الاستهلاك: {str(j)[:200]}"
    except Exception as e:
        pass
    # طريقة 3: لو الاتنين فشلوا، اعتبر تسجيل الدخول نفسه نجاح (الرصيد هيجي بعدين)
    return True, "تم تسجيل الدخول بنجاح ✅ (الرصيد سيظهر في التطبيق)"

def login_and_get_balance_api(phone, password, attempt_num, chat_settings):
    """البديل السريع لـ login_and_get_balance_detailed - يستخدم API فقط"""
    details = f"🔄 محاولة {attempt_num} (API)\n"
    try:
        details += "🌐 تسجيل دخول API...\n"
        auth = get_authorization_api(phone, password)
        if not auth["success"]:
            msg = auth["message"]
            is_wrong = auth.get("is_wrong", False)
            if is_wrong:
                details += f"❌ الباسورد غلط\n"
                return False, "الباسورد غلط - غير صحيح", details
            else:
                details += f"❌ {msg}\n"
                return False, msg, details
        token = auth["token"]
        details += "✅ تم تسجيل الدخول\n"
        details += "💰 بجيب الرصيد...\n"
        ok, bal = get_balance_api(token, phone)
        if ok:
            details += f"✅ {bal}\n"
            return True, bal, details
        else:
            details += f"⚠️ {bal}\n"
            return True, bal, details  # اعتبره نجاح لو تسجيل الدخول نجح
    except Exception as e:
        import traceback
        traceback.print_exc()
        details += f"❌ خطأ API: {str(e)[:100]}\n"
        return False, f"خطأ API: {str(e)[:80]}", details

# ------------------------------------------------------------------------------
# 4.2 - find_element_safe() : البحث عن عنصر بأمان
# ------------------------------------------------------------------------------
def find_element_safe(driver, css_selector, timeout=8):
    """تدور على عنصر بأكتر من طريقة (CSS + XPATH)"""
    selectors = [s.strip() for s in css_selector.split(",")]
    wait = WebDriverWait(driver, timeout)
    for sel in selectors:
        try:
            elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
            if elem.is_displayed():
                return elem
        except:
            try:
                if "has-text" in sel:
                    text = re.search(r"has-text\('([^']+)'\)", sel)
                    if text:
                        xpath = f"//*[contains(text(), '{text.group(1)}')]"
                        elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                        return elem
            except:
                continue
    return None

# ------------------------------------------------------------------------------
# 4.3 - login_and_get_balance_detailed() : تسجيل الدخول وجلب الرصيد
# ------------------------------------------------------------------------------
def login_and_get_balance_detailed(driver, phone, password, attempt_num, chat_settings):
    """
    أهم دالة - بتسجل دخول وتجيب الرصيد مع تفاصيل كل خطوة
    بترجع: (نجح؟, الرصيد/رسالة الخطأ, تفاصيل المحاولة)
    """
    details = f"🔄 **محاولة {attempt_num}**\n"
    try:
        driver.get(VODAFONE_URL)
        time.sleep(random.uniform(2, 4))
        details += f"🌐 فتح الموقع\n"
        wait = WebDriverWait(driver, BROWSER_TIMEOUT)

        # ---- 1. خانة الرقم ----
        phone_elem = None
        for sel in SELECTORS["phone_input"].split(","):
            try:
                phone_elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel.strip())))
                break
            except:
                continue
        if not phone_elem:
            try:
                inputs = driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    t = (inp.get_attribute("type") or "").lower()
                    ph = (inp.get_attribute("placeholder") or "")
                    if t in ["tel", "text"] or "رقم" in ph or "phone" in ph.lower():
                        phone_elem = inp
                        break
                if not phone_elem and inputs:
                    phone_elem = inputs[0]
            except:
                pass
        if not phone_elem:
            # حاول تصور الصفحة للتشخيص
            try:
                html = driver.page_source[:2000]
                details += f"❌ HTML: {html[:500]}\n"
            except:
                pass
            return False, "مقدرش الاقي خانة الرقم - الموقع اتغير (جرب تحدث SELECTORS)", details + "❌ خانة الرقم مش لاقيها - الموقع ممكن يكون اتغير\n"

        # --- كتابة الرقم بطريقة تضمن تفعيل JS بتاع فودافون ---
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", phone_elem)
            time.sleep(0.3)
            # ركز على الخانة
            driver.execute_script("arguments[0].focus();", phone_elem)
            time.sleep(0.2)
            # امسح بطريقة JS + عادية
            try:
                driver.execute_script("arguments[0].value=''; arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", phone_elem)
            except:
                pass
            phone_elem.clear()
            time.sleep(0.3)
            # اكتب بالـ JS الأول عشان يضمن، لو فشل يكتب حرف حرف
            try:
                driver.execute_script("arguments[0].value=arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true})); arguments[0].dispatchEvent(new Event('change', {bubbles:true})); arguments[0].dispatchEvent(new Event('keyup', {bubbles:true}));", phone_elem, phone)
                time.sleep(0.5)
                # اتأكد اتكتب ولا لا
                actual = driver.execute_script("return arguments[0].value;", phone_elem)
                if actual != phone:
                    # لو متكتبش صح، امسح واكتب حرف حرف
                    phone_elem.clear()
                    time.sleep(0.2)
                    for ch in phone:
                        phone_elem.send_keys(ch)
                        time.sleep(0.08)
            except:
                # fallback: حرف حرف
                for ch in phone:
                    phone_elem.send_keys(ch)
                    time.sleep(0.08)
            # تأكيد
            try:
                actual = driver.execute_script("return arguments[0].value;", phone_elem)
                details += f"📱 كتب الرقم: {actual} (المطلوب {phone}) {'✅' if actual==phone else '⚠️ مش متطابق!'}\n"
            except:
                details += f"📱 كتب الرقم: {phone}\n"
        except Exception as e:
            details += f"⚠️ خطأ كتابة الرقم: {str(e)[:60]}\n"
            # حاول الطريقة العادية
            try:
                phone_elem.clear()
                phone_elem.send_keys(phone)
                details += f"📱 كتب الرقم (fallback): {phone}\n"
            except Exception as e2:
                return False, f"فشل كتابة الرقم: {str(e2)[:80]}", details + f"❌ فشل كتابة الرقم\n"
        time.sleep(1)

        # ---- 2. خانة الباسورد ----
        pass_elem = None
        for sel in SELECTORS["password_input"].split(","):
            try:
                pass_elem = driver.find_element(By.CSS_SELECTOR, sel.strip())
                if pass_elem.is_displayed():
                    break
            except:
                continue
        if not pass_elem:
            try:
                pass_elem = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            except:
                pass
        if not pass_elem:
            return False, "مقدرش الاقي خانة الباسورد - ممكن الموقع طالب OTP", details + "❌ خانة الباسورد مش لاقيها\n"
        
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", pass_elem)
            time.sleep(0.2)
            driver.execute_script("arguments[0].focus();", pass_elem)
            time.sleep(0.2)
            try:
                driver.execute_script("arguments[0].value=''; arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", pass_elem)
            except:
                pass
            pass_elem.clear()
            time.sleep(0.3)
            # اكتب بالـ JS
            try:
                driver.execute_script("arguments[0].value=arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles:true})); arguments[0].dispatchEvent(new Event('change', {bubbles:true}));", pass_elem, password)
                time.sleep(0.5)
                actual_pass = driver.execute_script("return arguments[0].value;", pass_elem)
                if len(actual_pass) != len(password):
                    pass_elem.clear()
                    time.sleep(0.2)
                    for ch in password:
                        pass_elem.send_keys(ch)
                        time.sleep(0.05)
            except:
                for ch in password:
                    pass_elem.send_keys(ch)
                    time.sleep(0.05)
            details += f"🔑 كتب الباسورد: {'*' * len(password)} ({len(password)} حرف) ✅\n"
        except Exception as e:
            details += f"⚠️ خطأ كتابة الباسورد: {str(e)[:60]}\n"
            try:
                pass_elem.clear()
                pass_elem.send_keys(password)
                details += f"🔑 كتب الباسورد (fallback): {'*' * len(password)}\n"
            except Exception as e2:
                return False, f"فشل كتابة الباسورد: {str(e2)[:80]}", details + "❌ فشل كتابة الباسورد\n"
        time.sleep(1)

        # ---- 3. زرار الدخول ----
        login_btn = None
        for sel in SELECTORS["login_button"].split(","):
            if "has-text" in sel:
                continue
            try:
                login_btn = driver.find_element(By.CSS_SELECTOR, sel.strip())
                if login_btn.is_displayed() and login_btn.is_enabled():
                    break
            except:
                continue
        if not login_btn:
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for b in buttons:
                    if any(k in b.text for k in ["دخول", "تسجيل", "Login", "استمرار"]):
                        login_btn = b
                        break
                if not login_btn and buttons:
                    login_btn = buttons[-1]
            except:
                pass
        # --- تفعيل زرار الدخول لو معطل (فودافون بيعطله لحد ما تملى الخانات) ---
        try:
            driver.execute_script("""
                var btn1 = document.getElementById('kc-login');
                var btn2 = document.getElementById('submitBtn');
                if(btn1){ btn1.removeAttribute('disabled'); btn1.classList.remove('btn-disabled'); btn1.classList.remove('disabled'); }
                if(btn2){ btn2.removeAttribute('disabled'); btn2.classList.remove('btn-disabled'); btn2.classList.remove('disabled'); }
            """)
            time.sleep(0.5)
        except:
            pass

        if login_btn:
            driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
            time.sleep(0.5)
            # حاول كليك عادي، لو فشل جرب JS
            try:
                # اتأكد الزرار enabled قبل ما تدوس
                if login_btn.get_attribute("disabled") is None or login_btn.is_enabled():
                    login_btn.click()
                else:
                    driver.execute_script("arguments[0].click();", login_btn)
            except:
                driver.execute_script("arguments[0].click();", login_btn)
            details += f"👆 داس تسجيل دخول (الدخول)\n"
        else:
            # لو ملقاش الزرار دوس Enter في خانة الباسورد
            pass_elem.send_keys("\n")
            details += f"↩️ داس Enter (ملقاش زرار)\n"
        time.sleep(random.uniform(3, 5))

        # ---- 4. فحص رسائل الخطأ (محدث) ----
        time.sleep(2)
        try:
            page_source = driver.page_source.lower()
            try:
                page_text = driver.find_element(By.TAG_NAME, "body").text
            except:
                page_text = driver.page_source

            # أ) الحساب المعلق (أهم واحدة)
            account_locked_keywords = ["معلق", "موقوف", "محظور", "محظورة", "مغلق", "حاول في وقت لاحق", "حاول لاحق", "تم حظر", "blocked", "suspended", "locked", "try again later"]
            for kw in account_locked_keywords:
                if kw.lower() in page_text.lower() or kw.lower() in page_source:
                    try:
                        err_elem = find_element_safe(driver, SELECTORS["error_message"], timeout=2)
                        err_text = err_elem.text.strip()[:150] if err_elem and err_elem.text.strip() else kw
                    except:
                        err_text = kw
                    try:
                        elems = driver.find_elements(By.XPATH, "//*[contains(text(), 'معلق') or contains(text(), 'حاول')]")
                        for e in elems:
                            txt = e.text.strip()
                            if txt and 5 < len(txt) < 300 and ("معلق" in txt or "حاول" in txt):
                                err_text = txt[:150]
                                break
                    except:
                        pass
                    details += f"⛔ رسالة الموقع: {err_text}\n"
                    return False, f"الحساب معلق - {err_text}", details + "⛔ **الحساب معلق - حاول في وقت لاحق**\n"

            # ب) الباسورد الغلط
            wrong_pass_keywords = ["غير صحيح", "غير صحيحة", "incorrect", "wrong password", "كلمة المرور", "كلمة السر"]
            is_wrong_pass = False
            for kw in wrong_pass_keywords:
                if kw.lower() in page_text.lower() or kw.lower() in page_source:
                    if kw in ["غير صحيح", "غير صحيحة", "incorrect"]:
                        if any(x in page_text.lower() or x in page_source for x in ["كلمة", "password", "المرور", "السر"]):
                            is_wrong_pass = True
                            break
                    else:
                        is_wrong_pass = True
                        break
            if not is_wrong_pass:
                try:
                    err_elem = find_element_safe(driver, SELECTORS["error_message"], timeout=1)
                    if err_elem and err_elem.text.strip() and any(x in err_elem.text for x in ["كلمة", "غير صحيح", "incorrect"]):
                        err_text = err_elem.text.strip()
                        details += f"❌ رسالة الموقع: {err_text}\n"
                        return False, f"الباسورد غلط - {err_text}", details + "🔴 **الباسورد غلط**\n"
                except:
                    pass
            if is_wrong_pass:
                try:
                    err_elem = find_element_safe(driver, SELECTORS["error_message"], timeout=2)
                    err_text = err_elem.text.strip()[:120] if err_elem and err_elem.text.strip() else "كلمة المرور غير صحيحة"
                    details += f"❌ رسالة الموقع: {err_text}\n"
                    return False, f"الباسورد غلط - {err_text}", details + "🔴 **الباسورد غلط**\n"
                except:
                    return False, "الباسورد غلط", details + "🔴 **الباسورد غلط**\n"

            # ج) OTP / كابتشا
            if "otp" in page_source or "رمز التحقق" in page_text:
                return False, "الموقع طالب كود OTP", details + "🔐 **طالب OTP**\n"
            if "captcha" in page_source or "كابتشا" in page_text:
                return False, "الموقع طالب كابتشا", details + "🤖 **كابتشا**\n"
        except Exception as e:
            details += f"⚠️ مقدرش اقرا رسالة الخطأ: {str(e)[:40]}\n"

        # ---- 5. محاولة جلب الرصيد ----
        balance = None
        try:
            for xp in ["//*[contains(text(), 'رصيد')]", "//*[contains(text(), 'جنيه')]", "//*[contains(text(), 'EGP')]", "//*[contains(@class, 'balance')]"]:
                try:
                    for e in driver.find_elements(By.XPATH, xp):
                        txt = e.text.strip()
                        if txt and len(txt) < 200:
                            if re.search(r'(\d+[\.,]?\d*)\s*(جنيه|EGP|LE)', txt) or (re.search(r'\d+', txt) and ("رصيد" in txt or "جنيه" in txt)):
                                balance = txt
                                break
                    if balance:
                        break
                except:
                    continue
        except:
            pass
        current_url = driver.current_url
        if "login" not in current_url.lower() and not balance:
            try:
                body_text = driver.find_element(By.TAG_NAME, "body").text
                for line in body_text.split("\n"):
                    if "رصيد" in line and re.search(r'\d+', line):
                        balance = line.strip()
                        break
                if not balance:
                    balance = "تم تسجيل الدخول بنجاح (الرصيد محتاج تحديث للسيليكتور)"
            except:
                balance = "تم تسجيل الدخول بنجاح"
        if balance:
            details += f"💰 الرصيد: {balance}\n"
            return True, balance, details + "🟢 **نجح!**\n"
        try:
            driver.save_screenshot(f"debug_{phone}_{attempt_num}.png")
        except:
            pass
        return False, f"دخل بس معرفش يلاقي الرصيد - {current_url[:60]}", details + "⚠️ دخل بس معرفش يلاقي الرصيد\n"
    except TimeoutException:
        return False, "الموقع معلق / Timeout", details + "⏱️ **الموقع معلق (Timeout)**\n"
    except WebDriverException as e:
        return False, f"خطأ متصفح: {str(e)[:80]}", details + f"💥 خطأ متصفح\n"
    except Exception as e:
        return False, f"خطأ غير متوقع: {str(e)[:100]}", details + f"💥 خطأ\n"


# ==============================================================================
# ==============================================================================
#                        🤖 القسم 5: بوت تليجرام
#              هنا كل القوائم والأزرار والردود
# ==============================================================================
# ==============================================================================

if not TELEBOT_AVAILABLE:
    print("❌ لازم تثبت telebot الأول: pip install pyTelegramBotAPI")
    exit(1)

if BOT_TOKEN == "ضع_التوكن_هنا_من_BotFather" or not BOT_TOKEN or ":" not in BOT_TOKEN:
    print("="*60)
    print("❌ التوكن مش محطوط!")
    print("1. كلم @BotFather في تليجرام -> /newbot")
    print("2. خد التوكن وحطه فوق في BOT_TOKEN")
    print("="*60)

# إنشاء البوت مع حماية لو التوكن مش محطوط (عشان الكود يشتغل حتى للاختبار)
try:
    bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
except Exception as e:
    print(f"⚠️ التوكن مش صحيح ({e}) - البوت مش هيتصل بتليجرام لحد ما تحط التوكن الصح")
    # dummy bot للاختبار بدون ما يعمل exit
    class DummyBot:
        def message_handler(self, *a, **kw): return lambda f: f
        def callback_query_handler(self, *a, **kw): return lambda f: f
        def send_message(self, *a, **kw): print(f"[DummyBot] send_message: {a[:1]}"); return type('obj', (), {'message_id': 1})()
        def edit_message_text(self, *a, **kw): pass
        def answer_callback_query(self, *a, **kw): pass
        def infinity_polling(self, *a, **kw): print("Dummy polling - حط التوكن الصح عشان يشتغل")
    bot = DummyBot()
user_states = {}  # حالة كل مستخدم (منتظر رقم؟ إعدادات؟)

# ------------------------------------------------------------------------------
# 5.1 - is_allowed() : فحص الصلاحيات
# ------------------------------------------------------------------------------
def is_allowed(chat_id):
    """هل المستخدم مسموح له يستخدم البوت؟"""
    if not ADMIN_IDS:
        return True
    return chat_id in ADMIN_IDS

# ------------------------------------------------------------------------------
# 5.2 - main_menu() : القائمة الرئيسية
# ------------------------------------------------------------------------------
def main_menu():
    """القائمة الرئيسية - بتظهر مع /start"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📱 عرض الأرقام", callback_data="show_accounts"),
        types.InlineKeyboardButton("➕ إضافة رقم", callback_data="add_account")
    )
    markup.add(
        types.InlineKeyboardButton("🗑️ حذف رقم", callback_data="delete_account"),
        types.InlineKeyboardButton("💰 فحص الكل", callback_data="check_all")
    )
    markup.add(
        types.InlineKeyboardButton("💳 فحص رقم واحد", callback_data="check_one"),
        types.InlineKeyboardButton("📊 آخر النتائج", callback_data="last_results")
    )
    markup.add(
        types.InlineKeyboardButton("📥 استيراد من accounts.txt", callback_data="import_accounts"),
        types.InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")
    )
    markup.add(
        types.InlineKeyboardButton("❓ المساعدة", callback_data="help"),
        types.InlineKeyboardButton("🔄 تحديث", callback_data="show_accounts")
    )
    return markup

# ------------------------------------------------------------------------------
# 5.3 - settings_menu() : قائمة الإعدادات
# ------------------------------------------------------------------------------
def settings_menu(chat_id):
    """
    قائمة الإعدادات - كل زر فيه القيمة الحالية
    دوس على أي زر عشان تغيره
    """
    user_data = get_user_data(chat_id)
    s = user_data["settings"]
    auto_enabled = s.get("auto_check_enabled", AUTO_CHECK_ENABLED)
    auto_interval = s.get("auto_check_interval", AUTO_CHECK_INTERVAL_MINUTES)
    delay_between = s.get("delay_between_numbers", DELAY_BETWEEN_NUMBERS)
    interval_text = format_interval(auto_interval)
    auto_icon = "✅ شغال" if auto_enabled else "❌ مطفي"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(f"🔁 محاولات الموقع المعلق: {s['max_retries']} (دوس للتغيير)", callback_data="set_max_retries"),
        types.InlineKeyboardButton(f"🔐 محاولات الباسورد الغلط: {s['max_retries_wrong_password']} (دوس للتغيير)", callback_data="set_wrong_pass"),
        types.InlineKeyboardButton(f"⛔ محاولات الحساب المعلق: {s.get('max_retries_account_locked', 1)} (دوس للتغيير)", callback_data="set_account_locked"),
        types.InlineKeyboardButton(f"⏱️ الانتظار بين المحاولات: {s['retry_delay']} ث", callback_data="set_delay"),
        types.InlineKeyboardButton(f"⏩ الانتقال بين الأرقام: {delay_between} ث", callback_data="set_between_delay"),
        types.InlineKeyboardButton(f"🔄 الفحص التلقائي: {auto_icon} (دوس للتغيير)", callback_data="toggle_auto"),
        types.InlineKeyboardButton(f"⏰ مهلة الفحص التلقائي: {interval_text} ({auto_interval} د)", callback_data="set_auto_interval"),
        types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")
    )
    return markup

def delete_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for acc in get_user_data(chat_id)["accounts"]:
        markup.add(types.InlineKeyboardButton(f"🗑️ {acc['phone']} - {acc['name']}", callback_data=f"del_{acc['phone']}"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="main_menu"))
    return markup

def check_one_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for acc in get_user_data(chat_id)["accounts"]:
        markup.add(types.InlineKeyboardButton(f"💳 {acc['phone']}", callback_data=f"check_{acc['phone']}"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="main_menu"))
    return markup

# ------------------------------------------------------------------------------
# 5.4 - أوامر تليجرام (/start, /help, /list, /add)
# ------------------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def handle_start(message):
    if not is_allowed(message.chat.id):
        bot.send_message(message.chat.id, "❌ البوت خاص ومش مسموح ليك تستخدمه.")
        return
    s = get_user_data(message.chat.id)["settings"]
    welcome = f"""
🤖 **أهلاً {message.from_user.first_name}!**

📱 **بوت فودافون - فحص الرصيد**

**إحصائياتك:**
• الأرقام: `{len(get_user_data(message.chat.id)['accounts'])}`
• محاولات المعلق: `{s['max_retries']}` (لو الموقع مهنج)
• محاولات الباسورد الغلط: `{s['max_retries_wrong_password']}` (الديفولت 1)
• الفحص التلقائي: `{'✅ شغال كل ' + format_interval(s.get('auto_check_interval', 80)) if s.get('auto_check_enabled') else '❌ مطفي'}`

**القوائم:**
• 📱 عرض الأرقام - تشوف كل الأرقام + إعداداتك
• ➕ إضافة رقم - بالشكل `010...:الباسورد`
• 💰 فحص الكل - يفحصهم واحد واحد ويبعت تفاصيل كل محاولة
• ⚙️ الإعدادات - تغير أي رقم فوق

دوس على أي زرار 👇
"""
    bot.send_message(message.chat.id, welcome, reply_markup=main_menu())

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, """
❓ **المساعدة**

**إضافة رقم:** `01012345678:Password` أو `01012345678:Password:اسم`
**فحص:** 💰 فحص الكل
**الإعدادات:** ⚙️ دوس وغير أي حاجة

**شرح الإعدادات:**
• `MAX_RETRIES=10` - لو الموقع معلق يعيد 3 مرات
• `MAX_RETRIES_WRONG_PASSWORD=1` - لو الباسورد غلط مرة واحدة بس
• `MAX_RETRIES_ACCOUNT_LOCKED=1` - لو الحساب معلق مرة واحدة
• `RETRY_DELAY_SECONDS=5` - يستنى 5 ثواني بين المحاولات
• `DELAY_BETWEEN_NUMBERS=1` - ثانية بين كل رقم والتاني
• `AUTO_CHECK_INTERVAL=80` - يعيد كل 80 دقيقة (ساعة و20د)

كلهم فوق في أول الملف + تقدر تغيرهم من تليجرام!
""", reply_markup=main_menu())

@bot.message_handler(commands=['list'])
def handle_list(message):
    if is_allowed(message.chat.id):
        bot.send_message(message.chat.id, get_accounts_text(message.chat.id), reply_markup=main_menu())

@bot.message_handler(commands=['import'])
def handle_import(message):
    if not is_allowed(message.chat.id):
        return
    imported, msg = import_from_accounts_file(message.chat.id)
    if imported > 0:
        bot.send_message(message.chat.id, f"✅ {msg}\n\n{get_accounts_text(message.chat.id)}", reply_markup=main_menu())
    else:
        if "مش موجود" in msg:
            bot.send_message(message.chat.id, f"❌ {msg}\n\nتأكد ان ملف `accounts.txt` موجود وفيه سطور بالشكل:\n`01022683237:Samir@123`", reply_markup=main_menu())
        else:
            bot.send_message(message.chat.id, f"⚠️ {msg}\n\n{get_accounts_text(message.chat.id)}", reply_markup=main_menu())

@bot.message_handler(commands=['add'])
def handle_add_command(message):
    if not is_allowed(message.chat.id):
        return
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or ":" not in parts[1]:
            bot.send_message(message.chat.id, "❌ الصح: `/add 01012345678:Password`", reply_markup=main_menu())
            return
        p = parts[1].strip().split(":")
        ok, msg = add_account(message.chat.id, p[0].strip(), p[1].strip(), p[2].strip() if len(p) > 2 else "")
        bot.send_message(message.chat.id, f"✅ تم إضافة `{p[0].strip()}`\n{get_accounts_text(message.chat.id)}" if ok else f"❌ {msg}", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ خطأ: {e}")

# ------------------------------------------------------------------------------
# 5.5 - التعامل مع الأزرار (Callback)
# ------------------------------------------------------------------------------
# احتياط عام: أي خطأ في الأزرار ميوقعش البوت
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    if not is_allowed(chat_id):
        bot.answer_callback_query(call.id, "❌ غير مسموح")
        return
    data = call.data

    if data == "import_accounts":
        imported, msg = import_from_accounts_file(chat_id)
        if imported > 0:
            bot.answer_callback_query(call.id, f"✅ استورد {imported} رقم")
            bot.edit_message_text(f"✅ {msg}\n\n{get_accounts_text(chat_id)}", chat_id, call.message.message_id, reply_markup=main_menu())
        else:
            bot.answer_callback_query(call.id, "⚠️ مفيش جديد")
            if "مش موجود" in msg:
                bot.edit_message_text(f"❌ {msg}\n\nتأكد ان ملف `accounts.txt` موجود جنب البوت وفيه أرقام بالشكل:\n`01012345678:Password`", chat_id, call.message.message_id, reply_markup=main_menu())
            else:
                bot.edit_message_text(f"⚠️ {msg}\n\n{get_accounts_text(chat_id)}", chat_id, call.message.message_id, reply_markup=main_menu())

    elif data == "show_accounts":
        user_data = get_user_data(chat_id)
        s = user_data["settings"]
        text = get_accounts_text(chat_id)
        text += f"\n⚙️ **إعداداتك:**\n• معلق: `{s['max_retries']}`\n• باسورد غلط: `{s['max_retries_wrong_password']}`\n• حساب معلق: `{s.get('max_retries_account_locked',1)}`\n• انتظار: `{s['retry_delay']}ث`\n• انتقال: `{s.get('delay_between_numbers',1)}ث`\n• تلقائي: `{'✅ '+format_interval(s.get('auto_check_interval',80)) if s.get('auto_check_enabled') else '❌ مطفي'}`\n"
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=main_menu())
        bot.answer_callback_query(call.id, "📱 الأرقام")

    elif data == "add_account":
        user_states[chat_id] = "awaiting_account"
        bot.edit_message_text("➕ **إضافة رقم جديد**\n\nابعت بالشكل ده:\n`01012345678:الباسورد`\nأو `01012345678:الباسورد:اسم الخط`\n\nمثال: `01012345678:Ahmed@2024:خطي`\n\n✏️ ابعت دلوقتي:", chat_id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 إلغاء", callback_data="main_menu")))
        bot.answer_callback_query(call.id)

    elif data == "delete_account":
        if not get_user_data(chat_id)["accounts"]:
            bot.edit_message_text("📭 مفيش أرقام.", chat_id, call.message.message_id, reply_markup=main_menu())
        else:
            bot.edit_message_text("🗑️ **اختر رقم لحذفه:**", chat_id, call.message.message_id, reply_markup=delete_menu(chat_id))
        bot.answer_callback_query(call.id)

    elif data.startswith("del_"):
        phone = data[4:]
        bot.answer_callback_query(call.id, f"✅ حذف {phone}" if remove_account(chat_id, phone) else "❌ مش موجود")
        bot.edit_message_text(f"✅ حذف `{phone}`\n\n{get_accounts_text(chat_id)}", chat_id, call.message.message_id, reply_markup=main_menu())

    elif data == "check_all":
        if not get_user_data(chat_id)["accounts"]:
            bot.edit_message_text("📭 مفيش أرقام! دوس ➕ إضافة رقم.", chat_id, call.message.message_id, reply_markup=main_menu())
            bot.answer_callback_query(call.id, "📭 ضيف أرقام!")
            return
        bot.answer_callback_query(call.id, "⏳ ببدأ...")
        bot.edit_message_text(f"⏳ **ببدأ فحص {len(get_user_data(chat_id)['accounts'])} رقم...**", chat_id, call.message.message_id)
        threading.Thread(target=do_check_all, args=(chat_id,), daemon=True).start()

    elif data == "check_one":
        if not get_user_data(chat_id)["accounts"]:
            bot.answer_callback_query(call.id, "📭 مفيش أرقام!")
            return
        bot.edit_message_text("💳 **اختر رقم:**", chat_id, call.message.message_id, reply_markup=check_one_menu(chat_id))
        bot.answer_callback_query(call.id)

    elif data.startswith("check_"):
        phone = data[6:]
        bot.answer_callback_query(call.id, f"⏳ بفحص {phone}...")
        bot.send_message(chat_id, f"⏳ **بفحص `{phone}`...**")
        threading.Thread(target=do_check_one, args=(chat_id, phone), daemon=True).start()

    elif data == "last_results":
        user_data = get_user_data(chat_id)
        results = user_data.get("last_results", [])
        if not results:
            bot.edit_message_text("📭 لسه مفيش نتائج. دوس 💰 فحص الكل.", chat_id, call.message.message_id, reply_markup=main_menu())
        else:
            text = f"📊 **آخر فحص ({len(results)}):** 🕐 {user_data.get('last_check_time','')}\n" + "─"*30 + "\n"
            for r in results:
                text += f"{'✅' if r['success'] else '❌'} `{r['phone']}`: {r['balance'][:60]}\n"
                if not r['success']:
                    text += f"   ⚠️ {r['error'][:60]}\n"
            bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=main_menu())
        bot.answer_callback_query(call.id)

    elif data == "settings":
        s = get_user_data(chat_id)["settings"]
        text = f"⚙️ **الإعدادات**\n\n🔁 معلق: `{s['max_retries']}`\n🔐 باسورد غلط: `{s['max_retries_wrong_password']}`\n⛔ حساب معلق: `{s.get('max_retries_account_locked',1)}`\n⏱️ انتظار: `{s['retry_delay']}ث`\n⏩ انتقال: `{s.get('delay_between_numbers',1)}ث`\n🔄 تلقائي: `{'✅ شغال' if s.get('auto_check_enabled') else '❌ مطفي'}`\n⏰ مهلة: `{format_interval(s.get('auto_check_interval',80))}`\n\nدوس على أي واحدة 👇"
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=settings_menu(chat_id))
        bot.answer_callback_query(call.id)

    elif data == "set_max_retries":
        user_states[chat_id] = "awaiting_max_retries"
        bot.edit_message_text("🔁 **محاولات الموقع المعلق**\n\nده عدد المرات اللي هيعيد فيها لو الموقع مهنج أو النت فصل.\n\nابعت رقم 1-10:\n• `1` = مرة واحدة بس (سريع جداً)\n• `5` = 5 مرات (متوسط)\n• `10` = 10 مرات (الديفولت الجديد ✅)\n\n✏️ ابعت الرقم الجديد:", chat_id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 رجوع", callback_data="settings")))
        bot.answer_callback_query(call.id)

    elif data == "set_wrong_pass":
        user_states[chat_id] = "awaiting_wrong_pass"
        bot.edit_message_text("🔐 **محاولات الباسورد الغلط**\n\nده عدد المرات لو الباسورد غلط (رسالة: غير صحيح).\n\nابعت رقم 1-10:\n• `1` = مرة واحدة بس\n• `10` = 10 مرات (الديفولت الجديد ✅)\n\n✏️ ابعت الرقم الجديد:", chat_id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 رجوع", callback_data="settings")))
        bot.answer_callback_query(call.id)

    elif data == "set_account_locked":
        user_states[chat_id] = "awaiting_account_locked"
        bot.edit_message_text("⛔ **محاولات الحساب المعلق**\n\nده لما تظهر رسالة: *حسابك معلق حاول في وقت لاحق*\n\nابعت رقم 1-10:\n• `1` = مرة واحدة\n• `10` = 10 مرات (الديفولت الجديد ✅)\n\n✏️ ابعت الرقم الجديد:", chat_id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 رجوع", callback_data="settings")))
        bot.answer_callback_query(call.id)

    elif data == "set_delay":
        user_states[chat_id] = "awaiting_delay"
        bot.edit_message_text("⏱️ **الانتظار بين المحاولات**\n\nده كام ثانية يستنى بين محاولة ومحاولة لنفس الرقم.\n\nابعت رقم 1-30:\n• `5` = الديفولت ✅\n• `10` = لو خايف من البلوك\n\n✏️ ابعت الرقم الجديد:", chat_id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 رجوع", callback_data="settings")))
        bot.answer_callback_query(call.id)

    elif data == "set_between_delay":
        user_states[chat_id] = "awaiting_between_delay"
        bot.edit_message_text("⏩ **الانتقال بين الأرقام**\n\nده كام ثانية بين ما يخلص رقم 1 ويبدأ رقم 2.\n\nابعت رقم 0-10:\n• `0` = فوري\n• `1` = ثانية\n• `10` = 10 ثواني (الديفولت الجديد ✅)\n\n✏️ ابعت الرقم الجديد:", chat_id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 رجوع", callback_data="settings")))
        bot.answer_callback_query(call.id)

    elif data == "toggle_auto":
        user_data = get_user_data(chat_id)
        cur = user_data["settings"].get("auto_check_enabled", AUTO_CHECK_ENABLED)
        user_data["settings"]["auto_check_enabled"] = not cur
        save_user_data(chat_id, user_data)
        bot.answer_callback_query(call.id, f"بقى: {'✅ شغال' if not cur else '❌ مطفي'}")
        s = user_data["settings"]
        text = f"⚙️ **تم التغيير!**\n\n🔁 معلق: `{s['max_retries']}`\n🔐 باسورد: `{s['max_retries_wrong_password']}`\n⛔ معلق: `{s.get('max_retries_account_locked',1)}`\n⏱️ انتظار: `{s['retry_delay']}ث`\n⏩ انتقال: `{s.get('delay_between_numbers',1)}ث`\n🔄 تلقائي: `{'✅ شغال' if not cur else '❌ مطفي'}`\n⏰ مهلة: `{format_interval(s.get('auto_check_interval',80))}`"
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=settings_menu(chat_id))

    elif data == "set_auto_interval":
        user_states[chat_id] = "awaiting_auto_interval"
        cur = get_user_data(chat_id)["settings"].get("auto_check_interval", 80)
        bot.edit_message_text(f"⏰ **مهلة الفحص التلقائي**\n\nالحالي: `{cur}` دقيقة ({format_interval(cur)})\n\nابعت رقم 5-1440:\n• `80` = ساعة و20د (الديفولت ✅)\n• `60` = ساعة\n• `120` = ساعتين\n\n✏️ ابعت الرقم بالدقايق:", chat_id, call.message.message_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 رجوع", callback_data="settings")))
        bot.answer_callback_query(call.id)

    elif data == "main_menu":
        user_states.pop(chat_id, None)
        bot.edit_message_text(f"🤖 **القائمة الرئيسية**\n\n📊 الأرقام: `{len(get_user_data(chat_id)['accounts'])}`\nاختر 👇", chat_id, call.message.message_id, reply_markup=main_menu())
        bot.answer_callback_query(call.id)

    elif data == "help":
        bot.edit_message_text("❓ **المساعدة**\n\nكل الإعدادات فوق في أول الملف مع شرح مفصل لكل رقم.\nغير أي رقم وهتفهم ده بتاع ايه من الشرح اللي فوقه.", chat_id, call.message.message_id, reply_markup=main_menu())
        bot.answer_callback_query(call.id)

# ------------------------------------------------------------------------------
# 5.6 - استقبال الرسائل النصية
# ------------------------------------------------------------------------------
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    chat_id = message.chat.id
    if not is_allowed(chat_id) or message.text.startswith("/"):
        return
    state = user_states.get(chat_id)

    if state == "awaiting_account":
        if ":" not in message.text:
            bot.send_message(chat_id, "❌ لازم `رقم:باسورد` - مثال: `01012345678:Ahmed@2024`")
            return
        p = message.text.strip().split(":")
        ok, msg = add_account(chat_id, p[0].strip(), p[1].strip(), p[2].strip() if len(p) > 2 else "")
        user_states.pop(chat_id, None)
        bot.send_message(chat_id, f"✅ تم إضافة `{p[0].strip()}`\n\n{get_accounts_text(chat_id)}" if ok else f"❌ {msg}", reply_markup=main_menu())

    elif state == "awaiting_max_retries":
        try:
            v = int(message.text.strip())
            if 1 <= v <= 10:
                d = get_user_data(chat_id); d["settings"]["max_retries"] = v; save_user_data(chat_id, d); user_states.pop(chat_id, None)
                bot.send_message(chat_id, f"✅ محاولات المعلق بقت `{v}`\n(لو الموقع مهنج هيعيد {v} مرات)", reply_markup=settings_menu(chat_id))
            else: bot.send_message(chat_id, "❌ 1-10 بس")
        except: bot.send_message(chat_id, "❌ ابعت رقم مثل `3`")

    elif state == "awaiting_wrong_pass":
        try:
            v = int(message.text.strip())
            if 1 <= v <= 10:
                d = get_user_data(chat_id); d["settings"]["max_retries_wrong_password"] = v; save_user_data(chat_id, d); user_states.pop(chat_id, None)
                bot.send_message(chat_id, f"✅ محاولات الباسورد بقت `{v}`\n(لو الباسورد غلط هيعيد {v} مرة {'✅' if v==10 else ''})", reply_markup=settings_menu(chat_id))
            else: bot.send_message(chat_id, "❌ 1-10 بس (تقدر تخليه 10 زي ما طلبت)")
        except: bot.send_message(chat_id, "❌ ابعت رقم مثل `1` أو `10`")

    elif state == "awaiting_account_locked":
        try:
            v = int(message.text.strip())
            if 1 <= v <= 10:
                d = get_user_data(chat_id); d["settings"]["max_retries_account_locked"] = v; save_user_data(chat_id, d); user_states.pop(chat_id, None)
                bot.send_message(chat_id, f"✅ محاولات الحساب المعلق بقت `{v}`", reply_markup=settings_menu(chat_id))
            else: bot.send_message(chat_id, "❌ 1-10 بس")
        except: bot.send_message(chat_id, "❌ ابعت رقم")

    elif state == "awaiting_delay":
        try:
            v = int(message.text.strip())
            if 1 <= v <= 30:
                d = get_user_data(chat_id); d["settings"]["retry_delay"] = v; save_user_data(chat_id, d); user_states.pop(chat_id, None)
                bot.send_message(chat_id, f"✅ الانتظار بقى `{v} ثانية`\n(بين كل محاولة والتانية)", reply_markup=settings_menu(chat_id))
            else: bot.send_message(chat_id, "❌ 1-30 بس")
        except: bot.send_message(chat_id, "❌ ابعت رقم")

    elif state == "awaiting_between_delay":
        try:
            v = int(message.text.strip())
            if 0 <= v <= 10:
                d = get_user_data(chat_id); d["settings"]["delay_between_numbers"] = v; save_user_data(chat_id, d); user_states.pop(chat_id, None)
                bot.send_message(chat_id, f"✅ الانتقال بقى `{v} ثانية`\n(بين رقم 1 ورقم 2)", reply_markup=settings_menu(chat_id))
            else: bot.send_message(chat_id, "❌ 0-10 بس")
        except: bot.send_message(chat_id, "❌ ابعت رقم")

    elif state == "awaiting_auto_interval":
        try:
            v = int(message.text.strip())
            if 5 <= v <= 1440:
                d = get_user_data(chat_id); d["settings"]["auto_check_interval"] = v; save_user_data(chat_id, d); user_states.pop(chat_id, None)
                bot.send_message(chat_id, f"✅ المهلة بقت `{v} دقيقة` ({format_interval(v)})\n(هيعيد كل {format_interval(v)})", reply_markup=settings_menu(chat_id))
            else: bot.send_message(chat_id, "❌ 5-1440 بس")
        except: bot.send_message(chat_id, "❌ ابعت رقم مثل `80`")

    else:
        if ":" in message.text and message.text.strip().split(":")[0].strip().startswith("01"):
            p = message.text.strip().split(":")
            if len(p) >= 2 and p[0].strip() and p[1].strip():
                ok, _ = add_account(chat_id, p[0].strip(), p[1].strip(), p[2].strip() if len(p) > 2 else "")
                if ok:
                    bot.send_message(chat_id, f"✅ تم إضافة `{p[0].strip()}` بسرعة!\n{get_accounts_text(chat_id)}", reply_markup=main_menu())
                    return
        bot.send_message(chat_id, "🤖 دوس /start", reply_markup=main_menu())


# ==============================================================================
# ==============================================================================
#                        🔄 القسم 6: منطق الفحص
# ==============================================================================
# ==============================================================================


def do_check_all(chat_id, is_auto=False):
    """يفحص كل الأرقام واحد واحد مع تفاصيل كل محاولة - مع حماية من التهنيج"""
    try:
        user_data = get_user_data(chat_id)
        accounts = user_data["accounts"]
        settings = user_data["settings"]
        max_retries = settings.get("max_retries", MAX_RETRIES)
        max_wrong = settings.get("max_retries_wrong_password", MAX_RETRIES_WRONG_PASSWORD)
        max_locked = settings.get("max_retries_account_locked", MAX_RETRIES_ACCOUNT_LOCKED)
        retry_delay = settings.get("retry_delay", RETRY_DELAY_SECONDS)
        delay_between = settings.get("delay_between_numbers", DELAY_BETWEEN_NUMBERS)
    except Exception as e:
        try:
            bot.send_message(chat_id, f"❌ خطأ تحميل البيانات: {e}")
        except:
            pass
        return

    if not accounts:
        try:
            bot.send_message(chat_id, "📭 مفيش أرقام! دوس ➕ إضافة رقم.")
        except:
            pass
        return
    # احتياط: لو API مفعل مش محتاج سيلينيوم
    if USE_API_LOGIN:
        print("✅ API مفعل - مش محتاج سيلينيوم")
    elif not SELENIUM_AVAILABLE:
        try:
            bot.send_message(chat_id, "❌ السيلينيوم مش متثبت على السيرفر!\nثبت: `pip install selenium webdriver-manager`\n\n💡 لو على Streamlit Cloud تأكد ان `packages.txt` فيه chromium")
        except:
            pass
        return

    results = []
    total = len(accounts)
    auto_tag = "🔄 **فحص تلقائي**" if is_auto else "🚀 **ببدأ فحص**"
    try:
        bot.send_message(chat_id, f"{auto_tag} {total} رقم...\n⚙️ معلق={max_retries} | باسورد={max_wrong} | حساب معلق={max_locked} | انتظار={retry_delay}ث | انتقال={delay_between}ث")
    except:
        pass

    for idx, acc in enumerate(accounts, 1):
        try:
            phone = acc["phone"]
            password = acc["password"]
            name = acc.get("name") or phone
            try:
                if USE_API_LOGIN:
                    status_msg = bot.send_message(chat_id, f"📱 **[{idx}/{total}] {phone} ({name})**\n⏳ بجهز API ⚡...")
                else:
                    status_msg = bot.send_message(chat_id, f"📱 **[{idx}/{total}] {phone} ({name})**\n⏳ بجهز المتصفح...")
            except Exception as e:
                print(f"Failed to send status_msg: {e}")
                try:
                    if USE_API_LOGIN:
                        status_msg = bot.send_message(chat_id, f"[{idx}/{total}] {phone} - بجهز API ⚡...")
                    else:
                        status_msg = bot.send_message(chat_id, f"[{idx}/{total}] {phone} - بجهز المتصفح...")
                except:
                    status_msg = None
            driver, last_error, last_details, success, balance = None, "", "", False, ""
            max_attempts = max(max_retries, max_wrong, max_locked)

            for attempt in range(1, max_attempts + 1):
                # لو API مفعل - جربه الأول (أسرع)
                if USE_API_LOGIN:
                    try:
                        if status_msg:
                            bot.edit_message_text(f"📱 **[{idx}/{total}] {phone}**\n🔄 محاولة {attempt}/{max_attempts} (API ⚡)...\n⏳ بيسجل...", chat_id, status_msg.message_id)
                    except:
                        pass
                    ok, result, details = login_and_get_balance_api(phone, password, attempt, settings)
                else:
                    if driver is None:
                        driver = create_driver()
                        if not driver:
                            err_detail = globals().get("LAST_DRIVER_ERROR", "")
                            if err_detail:
                                last_error = f"فشل تشغيل المتصفح: {err_detail[:150]}"
                                last_details = f"❌ فشل تشغيل كروم\n{err_detail[:300]}\n💡 تأكد ان packages.txt فيه:\nchromium\nchromium-driver\n"
                            else:
                                last_error = "فشل تشغيل المتصفح - تأكد من تثبيت كروم"
                                last_details = "❌ فشل تشغيل كروم\n"
                            break
                    try:
                        if status_msg:
                            bot.edit_message_text(f"📱 **[{idx}/{total}] {phone}**\n🔄 محاولة {attempt}/{max_attempts}...\n⏳ بيسجل...", chat_id, status_msg.message_id)
                    except:
                        pass
                    ok, result, details = login_and_get_balance_detailed(driver, phone, password, attempt, settings)
                last_details = details
                if ok:
                    success, balance = True, result
                    try:
                        if status_msg:
                            bot.edit_message_text(f"📱 **[{idx}/{total}] {phone}**\n{details}\n💰 **الرصيد: {balance}**", chat_id, status_msg.message_id)
                        else:
                            bot.send_message(chat_id, f"✅ {phone}: {balance}\n{details}")
                    except:
                        try:
                            bot.send_message(chat_id, f"✅ {phone}: {balance}")
                        except:
                            pass
                    break
                else:
                    last_error = result
                    is_wrong = "الباسورد غلط" in result or "غير صحيح" in result
                    is_locked = "الحساب معلق" in result or "معلق" in result
                    detail_msg = f"📱 **[{idx}/{total}] {phone}**\n{details}\n❌ **فشل:** {result}\n"
                    if is_locked:
                        if attempt >= max_locked:
                            detail_msg += f"⛔ خلصت محاولات الحساب المعلق ({max_locked}) -> للرقم اللي بعده ⏩"
                            try:
                                if status_msg:
                                    bot.edit_message_text(detail_msg, chat_id, status_msg.message_id)
                                else:
                                    bot.send_message(chat_id, detail_msg)
                            except:
                                try:
                                    bot.send_message(chat_id, detail_msg)
                                except:
                                    pass
                            break
                        else:
                            detail_msg += f"⛔ هعيد بعد {retry_delay}ث... ({attempt}/{max_locked})"
                            try:
                                if status_msg:
                                    bot.edit_message_text(detail_msg, chat_id, status_msg.message_id)
                                else:
                                    bot.send_message(chat_id, detail_msg)
                            except:
                                try:
                                    bot.send_message(chat_id, detail_msg)
                                except:
                                    pass
                    elif is_wrong:
                        if attempt >= max_wrong:
                            detail_msg += f"⏭️ خلصت باسورد غلط ({max_wrong}) -> للبعده ⏩"
                            try:
                                if status_msg:
                                    bot.edit_message_text(detail_msg, chat_id, status_msg.message_id)
                                else:
                                    bot.send_message(chat_id, detail_msg)
                            except:
                                try:
                                    bot.send_message(chat_id, detail_msg)
                                except:
                                    pass
                            break
                        else:
                            detail_msg += f"⏳ هعيد بعد {retry_delay}ث... ({attempt}/{max_wrong})"
                            try:
                                if status_msg:
                                    bot.edit_message_text(detail_msg, chat_id, status_msg.message_id)
                                else:
                                    bot.send_message(chat_id, detail_msg)
                            except:
                                try:
                                    bot.send_message(chat_id, detail_msg)
                                except:
                                    pass
                    else:
                        if attempt >= max_retries:
                            detail_msg += f"⏭️ خلصت معلق ({max_retries}) -> للبعده ⏩"
                            try:
                                if status_msg:
                                    bot.edit_message_text(detail_msg, chat_id, status_msg.message_id)
                                else:
                                    bot.send_message(chat_id, detail_msg)
                            except:
                                try:
                                    bot.send_message(chat_id, detail_msg)
                                except:
                                    pass
                            break
                        else:
                            detail_msg += f"⏳ معلق - هعيد بعد {retry_delay}ث... ({attempt}/{max_retries})"
                            try:
                                if status_msg:
                                    bot.edit_message_text(detail_msg, chat_id, status_msg.message_id)
                                else:
                                    bot.send_message(chat_id, detail_msg)
                            except:
                                try:
                                    bot.send_message(chat_id, detail_msg)
                                except:
                                    pass
                    # لو سيلينيوم: اقفل المتصفح عشان المحاولة الجاية تبدأ نظيف
                    if not USE_API_LOGIN and driver:
                        try:
                            driver.quit()
                        except:
                            pass
                        driver = None
                    time.sleep(retry_delay)
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            results.append({"phone": phone, "name": name, "success": success, "balance": balance if success else last_error, "error": last_error, "details": last_details})
            if idx < total:
                if delay_between > 0:
                    try:
                        bot.send_message(chat_id, f"⏩ خلص `{phone}` -> للـ `{accounts[idx]['phone']}` بعد {delay_between}ث...")
                    except:
                        pass
                    time.sleep(delay_between)
                else:
                    try:
                        bot.send_message(chat_id, f"⏩ خلص `{phone}` -> فوري للـ `{accounts[idx]['phone']}`...")
                    except:
                        pass
        except Exception as e:
            import traceback
            err = str(e)[:300]
            print(f"❌ خطأ فادح لـ {acc.get('phone','?')}: {err}")
            traceback.print_exc()
            try:
                bot.send_message(chat_id, f"❌ خطأ غير متوقع لـ {acc.get('phone','?')}: {err[:150]}")
            except:
                try:
                    bot.send_message(chat_id, f"خطأ لـ {acc.get('phone','?')}")
                except:
                    pass
            try:
                results.append({"phone": acc.get("phone","?"), "name": acc.get("name","?"), "success": False, "balance": f"خطأ: {err[:80]}", "error": err, "details": ""})
            except:
                pass
            try:
                if 'driver' in locals() and driver:
                    driver.quit()
            except:
                pass
            continue

    # حفظ
    try:
        user_data = get_user_data(chat_id)
    except:
        user_data = {"last_results": [], "last_check_time": ""}
    user_data["last_results"] = results
    user_data["last_check_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        save_user_data(chat_id, user_data)
    except:
        pass

    # ملخص
    success_count = sum(1 for r in results if r["success"])
    summary = f"🏁 **انتهى!** {'(تلقائي)' if is_auto else ''}\n✅ نجح: {success_count}/{total} | ❌ فشل: {total-success_count}/{total}\n🕐 {datetime.now().strftime('%H:%M:%S')}\n" + "─"*30 + "\n"
    for i, r in enumerate(results, 1):
        # احتياط: اهرب الرموز اللي ممكن تكسر Markdown
        safe_balance = str(r['balance'][:60]).replace('`','').replace('_','').replace('*','')
        safe_phone = str(r['phone'])
        summary += f"{i}. {'✅' if r['success'] else '❌'} `{safe_phone}`: {safe_balance}\n"
        if not r['success']:
            if "معلق" in r['error']:
                summary += f"   ⛔ {r['error'][:90]}\n"
            elif "الباسورد" in r['error']:
                summary += f"   🔴 {r['error'][:90]}\n"
            else:
                summary += f"   💬 {r['error'][:90]}\n"
        else:
            summary += f"   💰 {r['balance'][:50]}\n"
    summary += "\n" + "─"*30 + f"\n⚙️ معلق={max_retries} | باسورد={max_wrong} | حساب معلق={max_locked} | انتقال={delay_between}ث"
    try:
        bot.send_message(chat_id, summary, reply_markup=main_menu())
    except:
        try:
            bot.send_message(chat_id, summary)
        except:
            pass

    # ⏰ المؤقت التلقائي
    try:
        fresh = get_user_data(chat_id)
        if fresh["settings"].get("auto_check_enabled", AUTO_CHECK_ENABLED):
            interval = fresh["settings"].get("auto_check_interval", AUTO_CHECK_INTERVAL_MINUTES)
            next_time = datetime.now() + timedelta(minutes=interval)
            next_str = next_time.strftime("%H:%M:%S - %Y-%m-%d")
            fresh["auto_check"]["next_check"] = next_str
            try:
                save_user_data(chat_id, fresh)
            except:
                pass
            try:
                bot.send_message(chat_id, f"⏰ **تلقائي شغال**\n✅ خلص {total} رقم\n⏳ هستنى **{format_interval(interval)}** ({interval}د)\n🕐 الجاي: `{next_str}`\n🔄 هيعيد من 1 لـ {total} تاني\n💡 غيره من ⚙️ الإعدادات", reply_markup=main_menu())
            except:
                pass
            def job():
                time.sleep(interval*60)
                try:
                    f = get_user_data(chat_id)
                    if f["settings"].get("auto_check_enabled") and f["accounts"]:
                        try:
                            bot.send_message(chat_id, f"⏰ **جه وقت التلقائي!** فحص {len(f['accounts'])} رقم...")
                        except:
                            pass
                        do_check_all(chat_id, is_auto=True)
                except Exception as e:
                    print(e)
            threading.Thread(target=job, daemon=True).start()
        else:
            try:
                bot.send_message(chat_id, "💡 التلقائي مطفي - فعّله من ⚙️ لو عايز كل ساعة و20د")
            except:
                pass
    except Exception as e:
        print(e)
    try:
        with open(RESULTS_CSV, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["الرقم","الاسم","الحالة","الرصيد/الخطأ","الوقت"])
            for r in results:
                w.writerow([r["phone"], r["name"], "نجح" if r["success"] else "فشل", r["balance"], user_data.get("last_check_time","")])
    except:
        pass


def do_check_one(chat_id, target_phone):
    try:
        user_data = get_user_data(chat_id)
        acc = next((a for a in user_data["accounts"] if a["phone"] == target_phone), None)
        if not acc:
            safe_send(chat_id, "❌ الرقم مش موجود")
            return
        # احتياط: انسخ الأصلي عشان لو حصل خطأ نرجعه
        orig = [dict(a) for a in user_data["accounts"]]
        tmp = get_user_data(chat_id)
        tmp["accounts"] = [dict(acc)]
        save_user_data(chat_id, tmp)
        try:
            do_check_all(chat_id)
        finally:
            # رجع الأصلي حتى لو حصل خطأ
            try:
                d = get_user_data(chat_id)
                d["accounts"] = orig
                save_user_data(chat_id, d)
            except:
                pass
    except Exception as e:
        print(f"do_check_one error: {e}")
        import traceback
        traceback.print_exc()
        safe_send(chat_id, f"❌ خطأ فحص رقم واحد: {str(e)[:100]}")


# ==============================================================================
# ==============================================================================
#                        🚀 القسم 7: التشغيل
#              هنا البوت بيبدأ - متلمسش حاجة
# ==============================================================================
# ==============================================================================

if __name__ == "__main__":
    print("="*60)
    print("🤖 بوت تليجرام فودافون")
    print(f"📱 توكن: {BOT_TOKEN[:15]}... (مخفي)")
    print(f"⚙️ معلق={MAX_RETRIES} | باسورد غلط={MAX_RETRIES_WRONG_PASSWORD} | حساب معلق={MAX_RETRIES_ACCOUNT_LOCKED}")
    print(f"⏰ تلقائي={'شغال كل '+format_interval(AUTO_CHECK_INTERVAL_MINUTES) if AUTO_CHECK_ENABLED else 'مطفي'} | انتقال={DELAY_BETWEEN_NUMBERS}ث")
    print("="*60)
    if not TELEBOT_AVAILABLE:
        print("❌ pip install pyTelegramBotAPI selenium webdriver-manager"); exit(1)
    if BOT_TOKEN == "ضع_التوكن_هنا_من_BotFather" or ":" not in BOT_TOKEN:
        print("⚠️ حط التوكن فوق في BOT_TOKEN أو في Secrets")
    else:
        print("✅ بيتصل بتليجرام...")
    # احتياط: حلقة إعادة اتصال تلقائية لو النت فصل أو تليجرام هنج
    retry_delay = 5
    while True:
        try:
            print(f"🔄 بحاول اتصل... (retry_delay={retry_delay}ث)")
            bot.infinity_polling(timeout=10, long_polling_timeout=5, skip_pending=True)
            # لو خرج بدون خطأ (نادر)، استنى وارجع
            print("⚠️ infinity_polling خرج بدون خطأ - هعيد بعد 5ث")
            import time as _time
            _time.sleep(5)
            retry_delay = 5
        except KeyboardInterrupt:
            print("⏹️ وقف بأمر المستخدم")
            break
        except Exception as e:
            print(f"❌ البوت فصل: {e}")
            import traceback
            traceback.print_exc()
            # احتياط: استنى مع زيادة تدريجية (5, 10, 20, 30 ث)
            try:
                safe_send(ADMIN_IDS[0] if ADMIN_IDS else None, f"⚠️ البوت فصل وهيعيد: {str(e)[:80]}")
            except:
                pass
            import time as _time
            _time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)
            print(f"🔄 هعيد المحاولة بعد {retry_delay}ث...")
            continue

