import requests
import time
import sys

# عرض رسالة ثابتة أعلى الكود في المنتصف
def print_header():
    header_text = "█ ✪ █▓▓▓▓▓ [🐉 ʙʏ: ᴀʙᴅᴀʟʟᴀʜ  ᴢᴀʜʀᴀɴ 🐉] ▓▓▓▓█ ✪ █\n *******************************************************\n🔴 The script has been active successfully ✅✅"  # التعديل هنا
    width = 80  # عرض الشاشة (يمكنك تغييره حسب الحاجة)
    space = (width - len(header_text)) // 2  # حساب المسافة لتوسيط النص
    sys.stdout.write(f"{' ' * space}{header_text}")
    sys.stdout.flush()

# إعداد الهيدر للطلب مع التوكن الذي سيدخله المستخدم
def get_headers(token):
    return {
        "Host": "api.wepartytt.com",
        "cache-control": "max-age=0",
        "language": "ar",
        "authorization": token,
        "content-type": "application/json",
        "apikey": "3d124ec3",
        "memberid": "cc26e96ae995211e74174966c9425ebf",
        "version": "6.3.100",
    }

# روابط الـ API
url_login = "https://api.wepartytt.com/auth/v6/login"
url_harvest = "https://api.wepartytt.com/member-asset/v6/game/mining/harvest"
url_get_money = "https://api.wepartytt.com/cash_requests/v6/red_packets_info?country=EG"
url_up_level = "https://api.wepartytt.com/member-asset/v6/game/mining/up_level"

# دالة تسجيل الدخول للحصول على التوكن
def login():
    headers = {
        "apikey": "3d124ec3",
        "content-type": "application/json",
    }
    data = {
        "code": "88bf90387b5769ee12074fd3cf742d100bffafe44f77fb7362dba365f42cd5db",
        "id": "cc26e96ae995211e74174966c9425ebf",
    }
    try:
        sys.stdout.write("\rLogging in... ⏳")
        sys.stdout.flush()
        response = requests.post(url_login, headers=headers, json=data)
        if response.status_code == 200:
            token = response.json().get('data', {}).get('token')
            if token:
                sys.stdout.write("\r✅ Login Successful!             \n")
                sys.stdout.flush()
            else:
                sys.stdout.write("\r❌ Login Failed: Token Missing. \n")
                sys.stdout.flush()
            return token
        sys.stdout.write("\r❌ Login Failed: Invalid Response.\n")
        sys.stdout.flush()
        return None
    except requests.exceptions.RequestException:
        sys.stdout.write("\r❌ Login Failed: Connection Error.\n")
        sys.stdout.flush()
        return None

# وظيفة لجلب المال الحالي
def fetch_current_money(previous_money, headers):
    try:
        sys.stdout.write("\rFetching Money... ⏳")
        sys.stdout.flush()
        response = requests.get(url_get_money, headers=headers)
        if response.status_code == 200:
            total_money = response.json().get("data", {}).get("total_money", 0)
            if total_money != previous_money:
                sys.stdout.write(f"\r💰 Total Money: {total_money}      \n")
                sys.stdout.flush()
                return total_money
        return previous_money
    except Exception:
        sys.stdout.write("\r❌ Error fetching money!          \n")
        sys.stdout.flush()
        return previous_money

# وظيفة لإرسال طلب الحصاد
def harvest(headers):
    try:
        sys.stdout.write("\rHarvesting... ⏳")  # رسالة واحدة عند بدء الحصاد
        sys.stdout.flush()
        response = requests.post(url_harvest, headers=headers)
        if response.status_code == 200:
            sys.stdout.write("\r✅ Harvest Successful!  ")  # طباعة النتيجة في نفس السطر
            sys.stdout.flush()
            return True
        else:
            sys.stdout.write("\r❌ Harvest Failed!               \n")
            sys.stdout.flush()
            return False
    except Exception:
        sys.stdout.write("\r❌ Error during harvesting!       \n")
        sys.stdout.flush()
        return False

# وظيفة لرفع المستوى
def up_level(headers):
    sys.stdout.flush()
    try:
        response = requests.post(url_up_level, headers=headers)
        if response.status_code == 200:
            sys.stdout.flush()
            return True
        else:
            sys.stdout.write("\r❌ Upgrade Failed!               \n")
            sys.stdout.flush()
            return False
    except Exception:
        sys.stdout.write("\r❌ Error during upgrade!          \n")
        sys.stdout.flush()
        return False

# دالة لتحديث التوكن
def refresh_token(current_token, last_token_update):
    if time.time() - last_token_update > 120:
        new_token = login()
        if new_token:
            return new_token, time.time()
    return current_token, last_token_update

# حلقة التنفيذ الرئيسية
def main_loop():
    print_header()
    print("\n")

    token = login()
    if not token:
        sys.stdout.write("\r❌ Failed to login. Exiting...\n")
        sys.stdout.flush()
        return

    headers = get_headers(token)
    sys.stdout.flush()

    previous_money = 0
    last_harvest_time = time.time()
    last_up_level_time = time.time()
    last_token_update = time.time()

    while True:
        token, last_token_update = refresh_token(token, last_token_update)
        headers = get_headers(token)

        previous_money = fetch_current_money(previous_money, headers)

        # فقط إذا مر وقت معين يتم الحصاد مرة واحدة.
        if time.time() - last_harvest_time >= 3:
            harvest(headers)
            last_harvest_time = time.time()

        if time.time() - last_up_level_time >= 60:
            up_level(headers)
            last_up_level_time = time.time()

        time.sleep(10)

# تشغيل البرنامج
main_loop()