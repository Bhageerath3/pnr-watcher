import os
import requests
from pnr_scraper import get_current_status

STATUS_FILE = "last_status.txt"

# Read secrets from environment (GitHub Actions / local env)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram credentials not set")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)


def read_last_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return f.read().strip()
    return None


def write_last_status(status):
    with open(STATUS_FILE, "w") as f:
        f.write(status)


# def main():
#     booking, current = get_current_status()
#     last = read_last_status()

#     if last is None:
#         print(f"Initial status: {current}")
#         write_last_status(current)
#         return

#     if current != last:
#         msg = (
#             "🚨 PNR STATUS CHANGED!\n\n"
#             f"Previous: {last}\n"
#             f"Current : {current}"
#         )
#         print(msg)
#         send_telegram(msg)
#         write_last_status(current)
#     else:
#         print(f"No change — Current Status: {current}")

def main():
    booking, current = get_current_status()
    last = read_last_status()

    msg = (
        "🧪 TEST ALERT (every 5 minute)\n\n"
        f"Current status: {current}"
    )

    print(msg)
    send_telegram(msg)

    write_last_status(current)

if __name__ == "__main__":
    main()
