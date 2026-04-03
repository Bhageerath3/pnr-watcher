from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def get_current_status(pnr):

    url = f"https://www.railyatri.in/pnr-status/{pnr}"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 20)
    driver.get(url)

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "pnr-search-result-title")
            )
        )

        status_blocks = driver.find_elements(
            By.CSS_SELECTOR, "#status .statusType"
        )

        booking_status = status_blocks[0].text
        current_status = status_blocks[1].text

        return {
            "pnr": pnr,
            "booking": booking_status,
            "current": current_status
        }

    finally:
        driver.quit()


# Optional standalone testing
if __name__ == "__main__":

    test_pnr = "4430098831"

    result = get_current_status(test_pnr)

    print("PNR:", result["pnr"])
    print("Booking Status:", result["booking"])
    print("Current Status:", result["current"])