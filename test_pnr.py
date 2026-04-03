from pnr_scraper import get_current_status

PNR_LIST = [
    "4335882785",
    "4548059789",
    "2949425962",
    "4755835470",
    "2153367387"
]

print("\n===== PNR STATUS TEST =====\n")

for pnr in PNR_LIST:

    print(f"Checking PNR: {pnr}")
    print("-" * 40)

    try:
        data = get_current_status(pnr)

        print("Train Name      :", data["train"])
        print("Booking Status  :", data["booking"])
        print("Current Status  :", data["current"])

    except Exception as e:
        print("Error fetching PNR:", e)

    print("\n")