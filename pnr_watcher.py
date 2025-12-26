from pnr_scraper import get_current_status
import os

STATUS_FILE = "last_status.txt"

def read_last_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return f.read().strip()
    return None

def write_last_status(status):
    with open(STATUS_FILE, "w") as f:
        f.write(status)

def main():
    booking, current = get_current_status()
    last_status = read_last_status()

    if last_status is None:
        print(f"Initial status: {current}")
    elif current != last_status:
        print("🚨 STATUS CHANGED!")
        print(f"Previous: {last_status}")
        print(f"Current : {current}")
    else:
        print(f"No change — Current Status: {current}")

    write_last_status(current)

if __name__ == "__main__":
    main()
