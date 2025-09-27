import requests
import time
from datetime import datetime
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import phonenumbers

# === Data kamu (langsung dipakai) ===
TOKEN = "8151370724:AAElSpMXFmfVrC6rQNmFzakTDnnN1diwenw"
CHAT_ID = "-1003162457112"

USERNAME = "yanduoxi3@gmail.com"
PASSWORD = "bld12345@"
LOGIN_URL = "https://www.ivasms.com/portal/live/my_sms"

MAIN_CHANNEL_LINK = "https://t.me/your_main_channel"
NUMBER_GROUP_LINK = "https://t.me/your_number_group"
BOT_OWNER_LINK = "https://t.me/your_owner"
# ====================================

bot = Bot(TOKEN)

def get_country_info(number):
    try:
        parsed_number = phonenumbers.parse(number)
        country_code = phonenumbers.region_code_for_number(parsed_number)
        if not country_code:
            return "🌍 Unknown"
        flag = "".join(chr(127397 + ord(c)) for c in country_code)
        return f"{flag} {country_code}"
    except:
        return "🌍 Unknown"

def login_and_fetch():
    session = requests.Session()
    login_data = {
        "email": USERNAME,
        "password": PASSWORD
    }
    session.post(LOGIN_URL, data=login_data)

    response = session.get("https://www.ivasms.com/portal/live/my_sms")
    return response.text

def parse_messages(html):
    """
    ⚠️ Ini masih dummy contoh.
    Harus disesuaikan dengan struktur HTML asli di IVASMS.
    """
    return [
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "number": "+22999123456",
            "service": "WhatsApp",
            "otp": "391-766",
            "msg": "391-766 هو رمز التحقق الخاص بك"
        }
    ]

def send_to_telegram(message):
    keyboard = [
        [
            InlineKeyboardButton("📢 Main Channel", url=MAIN_CHANNEL_LINK),
            InlineKeyboardButton("📋 Number Group", url=NUMBER_GROUP_LINK)
        ],
        [InlineKeyboardButton("👨‍💻 BOT OWNER", url=BOT_OWNER_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(
        chat_id=CHAT_ID,
        text=message,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

def format_message(msg):
    country_info = get_country_info(msg["number"])
    return f"""
✨<b>OTP Received</b>✨

🕒 <b>Time:</b> {msg['time']}
📞 <b>Number:</b> {msg['number']}
🌍 <b>Country:</b> {country_info}
🛠️ <b>Service:</b> {msg['service']}
🔐 <b>OTP Code:</b> {msg['otp']}
📝 <b>Msg:</b> {msg['msg']}
""".strip()

def main():
    sent_otps = set()
    while True:
        html = login_and_fetch()
        messages = parse_messages(html)

        for msg in messages:
            if msg['otp'] not in sent_otps:
                text = format_message(msg)
                send_to_telegram(text)
                sent_otps.add(msg['otp'])

        time.sleep(10)

if __name__ == "__main__":
    main()
