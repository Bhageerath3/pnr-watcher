import time
from pnr_scraper import get_current_status

CHECK_INTERVAL = 60 * 60  # 1 hour
last_status = None

print("📡 PNR Status Watcher started (checks every 1 hour)")

while True:
    try:
        booking, current = get_current_status()

        if last_status is None:
            print(f"Initial status: {current}")
            last_status = current

        elif current != last_status:
            print("\n🚨 STATUS CHANGED!")
            print(f"Previous: {last_status}")
            print(f"Current : {current}\n")
            last_status = current

        else:
            print(f"No change — Current Status: {current}")

    except Exception as e:
        print("⚠️ Error while checking PNR:", e)

    time.sleep(CHECK_INTERVAL)
