# -*- coding: utf-8 -*-
"""
Vodafone Egypt Balance Bot - بوت فودافون لفحص الرصيد
يخش على ana.vodafone.com.eg ويجيب الرصيد لكل الأرقام اللي عندك

المطور: Arena AI
التاريخ: 2026-09-17
"""

# ===================================================================
# ======================== ⚙️ الإعدادات من فوق ========================
# ===================================================================

# --- ملف الأرقام ---
ACCOUNTS_FILE = "accounts.txt"  # كل سطر فيه رقم:باسورد  مثال: 01012345678:MyPassword123

# --- إعدادات المحاولات (اللي طلبتها) ---
MAX_RETRIES = 3                         # كام مرة يعيد لو الموقع معلق / النت فصل / ايرور عام
RETRY_DELAY_SECONDS = 5                 # يستنى كام ثانية بين كل محاولة والتانية
PAGE_TIMEOUT = 30                       # لو الموقع علق يستنى كام ثانية قبل ما يعتبره فشل
MAX_RETRIES_WRONG_PASSWORD = 1          # كام مرة يعيد لو الباسورد غلط (الديفولت 1 = يجرب مرة واحدة بس ومش هيعيد)
                                        # لو عايزه يحاول مرتين لما الباسورد غلط غيرها لـ 2

# --- إعدادات المتصفح ---
HEADLESS = False                # True = المتصفح مش هيظهر (في الخلفية) / False = هيظهر قدامك
BROWSER_TIMEOUT = 20            # مهلة تحميل الصفحة

# --- إعدادات الحفظ ---
SAVE_TO_CSV = True              # يحفظ النتائج في ملف csv
SAVE_TO_TXT = True              # يحفظ النتائج في ملف txt
RESULTS_CSV = "results.csv"
RESULTS_TXT = "results.txt"

# --- رابط فودافون ---
VODAFONE_URL = "https://ana.vodafone.com.eg/ar/login"

# --- السيليكتورز (لو الموقع اتغير تقدر تعدلهم من هنا بس) ---
# دي أماكن الحقول في موقع أنا فودافون - لو الموقع اتحدث غيرهم بـ Inspect Element
SELECTORS = {
    "phone_input": "input[name='username'], input[type='tel'], input[placeholder*='رقم']",
    "password_input": "input[type='password'], input[name='password']",
    "login_button": "button[type='submit'], button:has-text('تسجيل'), button:has-text('دخول')",
    "balance_element": ".balance, [class*='balance'], [class*='Balance'], div:has-text('رصيد'), div:has-text('جنيه')",
    "error_message": ".error, .alert-danger, [class*='error'], p:has-text('خطأ'), p:has-text('غير صحيح')"
}

# ===================================================================
# ===================== نهاية الإعدادات ==============================
# ===================================================================

import os
import re
import csv
import time
import random
from datetime import datetime
from pathlib import Path

# مكتبات السيلينيوم
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
    from webdriver_manager.chrome import ChromeConfig, ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# ألوان للطباعة في الكونسول
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log(msg, color=Colors.END, prefix="*"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] [{prefix}] {msg}{Colors.END}")

def load_accounts():
    """يقرا الأرقام من الملف"""
    accounts = []
    if not os.path.exists(ACCOUNTS_FILE):
        log(f"ملف {ACCOUNTS_FILE} مش موجود! هعمل واحد جديد كمثال", Colors.YELLOW)
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            f.write("# حط كل رقم في سطر بالشكل ده: رقم:باسورد\n")
            f.write("# مثال:\n")
            f.write("01012345678:Password123\n")
            f.write("01098765432:MyPass456\n")
        log(f"تم إنشاء {ACCOUNTS_FILE} - افتحه وحط أرقامك الحقيقية", Colors.CYAN)
        return []

    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                log(f"سطر {line_num} غلط (لازم رقم:باسورد) -> {line}", Colors.YELLOW)
                continue
            phone, password = line.split(":", 1)
            phone = phone.strip()
            password = password.strip()
            # نظف الرقم
            phone = re.sub(r'\s+', '', phone)
            if not phone.startswith("01"):
                log(f"رقم غريب في سطر {line_num}: {phone}", Colors.YELLOW)
            accounts.append((phone, password))
    
    log(f"تم تحميل {len(accounts)} حساب من {ACCOUNTS_FILE}", Colors.GREEN)
    return accounts

def create_driver():
    """يعمل متصفح كروم بالاعدادات الصح"""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1366,768")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # webdriver-manager هينزل الدرايفر المناسب اوتوماتيك
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(PAGE_TIMEOUT)
        # اخفاء انه بوت
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        log(f"فشل تشغيل كروم: {e}", Colors.RED)
        log("جرب: pip install --upgrade selenium webdriver-manager", Colors.YELLOW)
        return None

def find_element_safe(driver, css_selector, timeout=10):
    """يدور على عنصر بأكتر من طريقة"""
    selectors = [s.strip() for s in css_selector.split(",")]
    wait = WebDriverWait(driver, timeout)
    for sel in selectors:
        try:
            # جرب CSS
            elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
            if elem.is_displayed():
                return elem
        except:
            try:
                # جرب XPATH لو فيه نص
                if "has-text" in sel:
                    text = re.search(r"has-text\('([^']+)'\)", sel)
                    if text:
                        xpath = f"//*[contains(text(), '{text.group(1)}')]"
                        elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                        return elem
            except:
                continue
    return None

def login_and_get_balance(driver, phone, password, attempt_num=1):
    """
    يسجل دخول برقم واحد ويجيب الرصيد
    بيرجع (نجح؟, الرصيد/رسالة الخطأ)
    """
    log(f"[{phone}] محاولة {attempt_num} - بيسجل دخول...", Colors.BLUE)
    
    try:
        driver.get(VODAFONE_URL)
        time.sleep(random.uniform(2, 4)) # يستنى الصفحة تحمل زي البني آدم

        # 1. يدور على خانة الرقم
        wait = WebDriverWait(driver, BROWSER_TIMEOUT)
        
        # جرب كل السيليكتورز المحتملة لخانة الرقم
        phone_elem = None
        for sel in SELECTORS["phone_input"].split(","):
            sel = sel.strip()
            try:
                phone_elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
                break
            except:
                continue
        
        # لو ملقاش بـ CSS جرب يدور على أي input
        if not phone_elem:
            try:
                inputs = driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    t = (inp.get_attribute("type") or "").lower()
                    ph = (inp.get_attribute("placeholder") or "")
                    if t in ["tel", "text"] or "رقم" in ph or "phone" in ph.lower() or "mobile" in ph.lower():
                        phone_elem = inp
                        break
                if not phone_elem and inputs:
                    phone_elem = inputs[0] # اول واحد وخلاص
            except:
                pass

        if not phone_elem:
            return False, "مقدرش الاقي خانة الرقم - الموقع اتغير؟ حدث SELECTORS فوق"

        # اكتب الرقم
        phone_elem.clear()
        time.sleep(0.5)
        # اكتب حرف حرف عشان يبان طبيعي
        for ch in phone:
            phone_elem.send_keys(ch)
            time.sleep(random.uniform(0.05, 0.15))
        time.sleep(1)

        # 2. خانة الباسورد
        pass_elem = None
        for sel in SELECTORS["password_input"].split(","):
            sel = sel.strip()
            try:
                pass_elem = driver.find_element(By.CSS_SELECTOR, sel)
                if pass_elem.is_displayed():
                    break
            except:
                continue
        
        if not pass_elem:
            # جرب اي input باسورد
            try:
                pass_elem = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            except:
                pass

        if not pass_elem:
            return False, "مقدرش الاقي خانة الباسورد - ممكن الموقع طالب OTP بدل الباسورد"

        pass_elem.clear()
        time.sleep(0.3)
        for ch in password:
            pass_elem.send_keys(ch)
            time.sleep(random.uniform(0.05, 0.15))
        time.sleep(1)

        # 3. دوس تسجيل دخول
        login_btn = None
        for sel in SELECTORS["login_button"].split(","):
            sel = sel.strip()
            try:
                # تجاهل has-text
                if "has-text" in sel:
                    continue
                login_btn = driver.find_element(By.CSS_SELECTOR, sel)
                if login_btn.is_displayed() and login_btn.is_enabled():
                    break
            except:
                continue
        
        if not login_btn:
            # دور على اي زرار
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for b in buttons:
                    txt = b.text.strip()
                    if any(k in txt for k in ["دخول", "تسجيل", "Login", "استمرار", "متابعة"]):
                        login_btn = b
                        break
                if not login_btn and buttons:
                    login_btn = buttons[-1]
            except:
                pass

        if login_btn:
            driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
            time.sleep(0.5)
            try:
                login_btn.click()
            except:
                driver.execute_script("arguments[0].click();", login_btn)
        else:
            # جرب Enter
            pass_elem.send_keys("\n")

        time.sleep(random.uniform(3, 5))

        # 4. استنى النتيجة
        # هل فيه رسالة خطأ؟
        time.sleep(2)
        page_source = driver.page_source.lower()
        page_text = driver.find_element(By.TAG_NAME, "body").text

        # كلمات تدل على خطأ الباسورد
        wrong_pass_keywords = ["غير صحيح", "خطأ", "incorrect", "wrong password", "كلمة المرور", "حاول مرة أخرى"]
        for kw in wrong_pass_keywords:
            if kw.lower() in page_source or kw in page_text:
                # اتأكد انه مش مجرد كلام عادي
                try:
                    err_elem = find_element_safe(driver, SELECTORS["error_message"], timeout=3)
                    if err_elem:
                        return False, f"الباسورد غلط - {err_elem.text.strip()[:100]}"
                except:
                    pass
                # لو لقى الكلمة وملقاش عنصر ايرور واضح، اعتبره باسورد غلط
                if "غير صحيح" in page_text or "incorrect" in page_source:
                    return False, "الباسورد غلط"

        # 5. دور على الرصيد
        # استنى لحد ما يظهر الرصيد او الصفحة الرئيسية
        balance = None
        try:
            # استنى اي حاجة فيها رصيد او جنيه
            wait_balance = WebDriverWait(driver, 10)
            # جرب XPATH مرن
            xpaths = [
                "//*[contains(text(), 'رصيد')]",
                "//*[contains(text(), 'جنيه')]",
                "//*[contains(text(), 'EGP')]",
                "//*[contains(text(), 'Balance')]",
                "//*[contains(@class, 'balance')]",
                "//*[contains(@class, 'Balance')]"
            ]
            for xp in xpaths:
                try:
                    elems = driver.find_elements(By.XPATH, xp)
                    for e in elems:
                        txt = e.text.strip()
                        if txt and len(txt) < 200: # مش نص طويل
                            # دور على رقم جوه النص
                            match = re.search(r'(\d+[\.,]?\d*)\s*(جنيه|EGP|LE|ج\.م)', txt)
                            if match:
                                balance = txt
                                break
                            # لو النص نفسه فيه رقم
                            if re.search(r'\d+', txt) and ("رصيد" in txt or "جنيه" in txt):
                                balance = txt
                                break
                    if balance:
                        break
                except:
                    continue
        except:
            pass

        # لو ملقاش رصيد بس الصفحة اتنقلت (url اتغير) يبقى دخل بنجاح
        current_url = driver.current_url
        if "login" not in current_url.lower() and not balance:
            # خد كل نص الصفحة ودور على رصيد
            try:
                body_text = driver.find_element(By.TAG_NAME, "body").text
                # دور على سطر فيه رصيد
                for line in body_text.split("\n"):
                    if "رصيد" in line and re.search(r'\d+', line):
                        balance = line.strip()
                        break
                if not balance:
                    # لو مفيش كلمة رصيد خالص، يبقى دخل بس لسه محملش
                    # هات اول رقم شبه رصيد
                    balance = "تم تسجيل الدخول بنجاح (الرصيد محتاج تحديث للسيليكتور)"
            except:
                balance = "تم تسجيل الدخول بنجاح"

        if balance:
            return True, balance
        
        # لو وصل هنا ومعرفش يحدد
        # خد سكرين شوت للمساعدة
        try:
            driver.save_screenshot(f"debug_{phone}_{attempt_num}.png")
            log(f"[{phone}] حفظت سكرين شوت debug_{phone}_{attempt_num}.png عشان تراجع", Colors.YELLOW)
        except:
            pass

        return False, f"دخل بس معرفش يلاقي الرصيد - الصفحة: {current_url[:80]} - جرب تغير SELECTORS"

    except TimeoutException:
        return False, "الموقع معلق / Timeout - هيعيد المحاولة"
    except WebDriverException as e:
        msg = str(e)[:150]
        if "net::ERR" in msg or "timeout" in msg.lower():
            return False, f"مشكلة في النت/الموقع معلق - {msg[:80]}"
        return False, f"خطأ متصفح: {msg[:100]}"
    except Exception as e:
        return False, f"خطأ غير متوقع: {str(e)[:120]}"

def process_account(phone, password):
    """يعالج حساب واحد مع كل المحاولات"""
    driver = None
    last_error = ""
    
    # هنلف على أكبر عدد محاولات فيهم عشان نغطي الحالتين
    max_attempts = max(MAX_RETRIES, MAX_RETRIES_WRONG_PASSWORD)

    for attempt in range(1, max_attempts + 1):
        if driver is None:
            driver = create_driver()
            if not driver:
                return phone, "فشل تشغيل المتصفح", False

        success, result = login_and_get_balance(driver, phone, password, attempt)
        
        if success:
            log(f"[{phone}] ✅ نجح! الرصيد: {result}", Colors.GREEN, "✔")
            try:
                driver.quit()
            except:
                pass
            return phone, result, True
        
        # فشل
        last_error = result
        is_wrong_password = "الباسورد غلط" in result or "غير صحيح" in result or "incorrect" in result.lower()

        if is_wrong_password:
            log(f"[{phone}] ❌ محاولة {attempt}/{MAX_RETRIES_WRONG_PASSWORD} فشلت (باسورد غلط): {result}", Colors.RED)
            # شيك هل لسه ليه محاولات للباسورد الغلط؟
            if attempt >= MAX_RETRIES_WRONG_PASSWORD:
                log(f"[{phone}] ⏭️ الباسورد غلط وخلصت محاولاته ({MAX_RETRIES_WRONG_PASSWORD}) فمش هعيد تاني", Colors.YELLOW)
                break
            else:
                log(f"[{phone}] ⏳ الباسورد غلط بس لسه فاضل محاولة - هستنى {RETRY_DELAY_SECONDS} ثانية...", Colors.YELLOW)
        else:
            # ده ايرور عادي (الموقع معلق/نت/...)
            log(f"[{phone}] ❌ محاولة {attempt}/{MAX_RETRIES} فشلت (موقع معلق): {result}", Colors.RED)
            if attempt >= MAX_RETRIES:
                log(f"[{phone}] ⏭️ خلصت محاولات الموقع المعلق ({MAX_RETRIES})", Colors.YELLOW)
                break
            else:
                log(f"[{phone}] ⏳ هستنى {RETRY_DELAY_SECONDS} ثانية قبل المحاولة الجاية...", Colors.YELLOW)
        
        # لو لسه فيه محاولات، اقفل المتصفح وافتح واحد جديد
        try:
            driver.quit()
        except:
            pass
        driver = None
        time.sleep(RETRY_DELAY_SECONDS)
        time.sleep(1)
    
    # كل المحاولات فشلت
    if driver:
        try:
            driver.quit()
        except:
            pass
    return phone, last_error, False

def save_results(results):
    """يحفظ النتائج"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if SAVE_TO_TXT:
        with open(RESULTS_TXT, "w", encoding="utf-8") as f:
            f.write(f"نتائج فحص فودافون - {timestamp}\n")
            f.write("="*50 + "\n")
            for phone, balance, success in results:
                status = "✅ نجح" if success else "❌ فشل"
                f.write(f"{phone} | {status} | {balance}\n")
        log(f"تم الحفظ في {RESULTS_TXT}", Colors.CYAN)

    if SAVE_TO_CSV:
        with open(RESULTS_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["الرقم", "الحالة", "الرصيد/الخطأ", "الوقت"])
            for phone, balance, success in results:
                status = "نجح" if success else "فشل"
                writer.writerow([phone, status, balance, timestamp])
        log(f"تم الحفظ في {RESULTS_CSV}", Colors.CYAN)

def main():
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("="*60)
    print("  📱 بوت فودافون - فحص الرصيد لأرقام متعددة")
    print("  Vodafone Egypt Balance Bot")
    print("="*60)
    print(f"{Colors.END}")

    if not SELENIUM_AVAILABLE:
        log("المكتبات مش متثبتة! شغل:", Colors.RED)
        print("  pip install selenium webdriver-manager")
        return

    accounts = load_accounts()
    if not accounts:
        log("مفيش أرقام! افتح accounts.txt وحط أرقامك", Colors.RED)
        log(f"الصيغة: رقم:باسورد  (كل واحد في سطر)", Colors.YELLOW)
        input("دوس Enter بعد ما تحط الأرقام...")
        accounts = load_accounts()
        if not accounts:
            return

    log(f"هبدأ فحص {len(accounts)} رقم - لو الموقع علق هيحاول {MAX_RETRIES} مرات | لو الباسورد غلط هيحاول {MAX_RETRIES_WRONG_PASSWORD} مرة (الديفولت 1)", Colors.BOLD)
    print("-"*60)

    results = []
    for idx, (phone, password) in enumerate(accounts, 1):
        log(f"--- [{idx}/{len(accounts)}] بيعالج {phone} ---", Colors.BOLD)
        phone_res, balance, success = process_account(phone, password)
        results.append((phone_res, balance, success))
        
        # راحة صغيرة بين الأرقام عشان فودافون متعملش بلوك
        if idx < len(accounts):
            wait = random.uniform(3, 6)
            log(f"راحة {wait:.1f} ثانية قبل الرقم الجاي...", Colors.YELLOW)
            time.sleep(wait)
        print("-"*60)

    # ملخص
    print(f"\n{Colors.BOLD}{Colors.GREEN}========== الملخص =========={Colors.END}")
    success_count = sum(1 for _, _, s in results if s)
    for phone, balance, success in results:
        icon = "✅" if success else "❌"
        color = Colors.GREEN if success else Colors.RED
        print(f"{color}{icon} {phone} : {balance}{Colors.END}")
    
    print(f"\n{Colors.BOLD}النجاح: {success_count}/{len(results)}{Colors.END}")
    
    save_results(results)
    log("خلصنا! ✅", Colors.GREEN)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\nتم الإيقاف بواسطة المستخدم", Colors.YELLOW)
    except Exception as e:
        log(f"خطأ عام: {e}", Colors.RED)
        import traceback
        traceback.print_exc()
    finally:
        input("\nدوس Enter عشان تقفل...")
