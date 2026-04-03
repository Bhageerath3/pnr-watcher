import os
import requests
from pnr_scraper import get_current_status

STATUS_FILE = "last_status.txt"

# Your PNR dictionary
PNR_LIST = {
    "4335882785": "Telangana SF Express | HYD Deccan 06:00 (4 May) → New Delhi 08:00 (5 May)",
    "4548059789": "Sampark Kranti  | KCG 08:15 (4 May) → Nizamuddin 08:10 (5 May)",
    "2949425962": "Telangana Express | New Delhi 16:00 (5 May) → HYD Deccan 17:10 (6 May)",
    "4755835470": "Dakshin SF Express | HYD Deccan 23:00 (16 May) → Nizamuddin 03:45 (18 May)",
    "2153367387": "Telangana Express | New Delhi 16:00 (18 May) → HYD Deccan 17:10 (19 May)"
}

# Telegram secrets
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

    data = {}

    if not os.path.exists(STATUS_FILE):
        return data

    with open(STATUS_FILE, "r") as f:
        for line in f:

            line = line.strip()

            if not line:
                continue

            if "|" not in line:
                continue

            pnr, status = line.split("|", 1)

            data[pnr] = status

    return data


def write_last_status(status_dict):

    with open(STATUS_FILE, "w") as f:

        for pnr, status in status_dict.items():
            f.write(f"{pnr}|{status}\n")


def main():

    from datetime import datetime, timezone

    print("⏱ Run time (UTC):", datetime.now(timezone.utc))

    last_status = read_last_status()
    new_status = {}

    changes = []
    no_change = []

    for pnr, description in PNR_LIST.items():

        print("\n----------------------------------")
        print("Checking:", description)
        print("PNR:", pnr)

        try:

            data = get_current_status(pnr)

            booking = data["booking"]
            current = data["current"]

            new_status[pnr] = current

            previous = last_status.get(pnr)

            if previous is None:
                no_change.append(
                    f"{description}\nPNR: {pnr}\nCurrent status: {current}"
                )

            elif previous != current:
                changes.append(
                    f"{description}\nPNR: {pnr}\nPrevious: {previous}\nCurrent : {current}"
                )

            else:
                no_change.append(
                    f"{description}\nPNR: {pnr}\nCurrent status: {current}"
                )

        except Exception as e:

            print("Error checking PNR:", pnr)
            print(e)

    # Send combined Telegram message

    if changes:

        msg = "🚨 PNR STATUS CHANGED!\n\n" + "\n\n".join(changes)

    else:

        msg = "✅ PNR STATUS CHECK\n\nNo change\n\n" + "\n\n".join(no_change)

    print(msg)

    send_telegram(msg)

    write_last_status(new_status)


if __name__ == "__main__":
    main()